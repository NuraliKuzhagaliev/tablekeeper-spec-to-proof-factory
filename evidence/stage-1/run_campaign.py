#!/usr/bin/env python3
"""Linux-native exact-revision orchestration. Requires explicit Conductor release.

python run_campaign.py --revision FULL_SHA --released --repo /mnt/d/dark/band-work/result
Diagnostics and raw official output go OUTSIDE result. No raw exports are persisted.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

LABEL = "tablekeeper.verifier=adversarial-verifier"
OFFICIAL = Path("/mnt/d/dark/dark-factory-wearedevs")


def command(args, log=None, timeout=120, cwd=None):
    if log:
        with Path(log).open("w") as stream:
            result = subprocess.run(args, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
    else:
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError("command failed: " + " ".join(str(x) for x in args[:4])
                           + ("; inspect " + str(log) if log else "; " + result.stderr.strip()[:250]))
    return "" if log else result.stdout.strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--revision", required=True)
    p.add_argument("--released", action="store_true")
    p.add_argument("--repo", default="/mnt/d/dark/band-work/result")
    p.add_argument("--diagnostics", default="/mnt/d/dark/band-work/checks")
    p.add_argument("--boundary-only", action="store_true", help="released targeted regression gate; skip official/full campaign")
    p.add_argument("--materialized", help="existing clean native pinned clone; never shared mutable checkout")
    args = p.parse_args()
    if not args.released or not re.fullmatch("[0-9a-f]{40}", args.revision):
        p.error("Conductor release and full 40-character SHA are mandatory")
    if not sys.platform.startswith("linux"):
        p.error("verification must run in Linux; no Windows/WSL linked worktrees")
    run_id = "av-stage1-" + args.revision[:12] + "-" + uuid.uuid4().hex[:8]
    out = Path(args.diagnostics).resolve() / run_id
    out.mkdir(parents=True)
    native = Path(args.materialized).resolve().parent if args.materialized else Path(tempfile.mkdtemp(prefix=run_id + "-"))
    repo = Path(args.materialized).resolve() if args.materialized else native / "production"
    if args.materialized and str(repo).startswith("/mnt/"):
        p.error("materialized clone must be on Linux-native filesystem")
    network = run_id + "-net"
    image = run_id + ":service"
    names = [run_id + "-source", run_id + "-destination"]
    if not args.boundary_only:
        names.append(run_id + "-third")
    metadata = {"production_revision": args.revision, "run_id": run_id,
                "classification": "INCONCLUSIVE", "diagnostics": str(out),
                "immutable_materialization": str(repo), "resource_limits": {"cpu": 2, "memory": "2g"},
                "budgets": {"readiness_seconds": 60, "request_seconds": 5, "control_seconds": 10}}
    started = []
    created_network = built = False
    try:
        metadata["docker_version"] = command(["docker", "version", "--format", "{{.Server.Version}}"])
        check_sha = command(["git", "-C", args.repo, "rev-parse", args.revision + "^{commit}"])
        if check_sha != args.revision:
            raise RuntimeError("assigned production revision unavailable")
        if shutil.disk_usage(native).free < 512 * 1024 * 1024:
            raise RuntimeError("preflight: insufficient native disk")
        if not args.materialized:
            command(["git", "clone", "--no-hardlinks", "--no-checkout", args.repo, str(repo)], out / "clone.log")
            command(["git", "-C", str(repo), "checkout", "--detach", args.revision], out / "checkout.log")
        if command(["git", "-C", str(repo), "rev-parse", "HEAD"]) != args.revision:
            raise RuntimeError("pinned clone HEAD mismatch")
        if command(["git", "-C", str(repo), "status", "--porcelain"]):
            raise RuntimeError("pinned clone is not clean")
        # Freeze tracked content; .git is retained for official revision provenance.
        for file in repo.rglob("*"):
            if file.is_file() and ".git" not in file.relative_to(repo).parts:
                file.chmod(file.stat().st_mode & ~0o222)
        metadata["official_revision"] = command(["git", "-C", str(OFFICIAL), "rev-parse", "HEAD"])
        diff = subprocess.run(["git", "-C", str(OFFICIAL), "diff", "--ignore-space-at-eol", "--quiet"])
        if diff.returncode:
            raise RuntimeError("preflight: official checkout has substantive tracked modifications")
        metadata["official_only_eol_differences"] = bool(command(["git", "-C", str(OFFICIAL), "status", "--porcelain"]))
        campaign = Path(__file__).with_name("campaign.py")
        metadata["campaign_sha256"] = hashlib.sha256(campaign.read_bytes()).hexdigest()
        metadata["orchestrator_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        command([sys.executable, str(campaign), "calibrate"], out / "calibration.log")
        # Official isolated harness builds the exact clean revision independently.
        if args.boundary_only:
            command(["docker", "image", "inspect", "df-harness-runner", "--format", "{{.Id}}"])
            metadata["official_checks"] = "NOT RUN: Conductor targeted-rejection gate; full check deferred to replacement SHA"
        else:
            harness = [sys.executable, "-m", "harness", "run", "--track", "tablekeeper", "--mode", "isolated",
                       "--repo", str(repo), "--stage", "1", "--out", str(out / "official")]
            with (out / "official-console.log").open("w") as stream:
                official = subprocess.run(harness, cwd=OFFICIAL, stdout=stream, stderr=subprocess.STDOUT, timeout=1800)
            metadata["official_exit_code"] = official.returncode
        command(["docker", "build", "-t", image, str(repo / "stage-1")], out / "independent-build.log", timeout=1800)
        built = True
        command(["docker", "network", "create", "--internal", "--label", LABEL, network])
        created_network = True
        boot_times = {}
        ports = [8765, 8766] + ([] if args.boundary_only else [8080])
        for i, name in enumerate(names):
            port = ports[i]
            boot_times[name] = time.monotonic()
            port_args = ["-e", "PORT=" + str(port)] if i < 2 else []
            command(["docker", "run", "-d", "--name", name, "--label", LABEL, "--network", network,
                     "--cpus", "2", "--memory", "2g", *port_args, image])
            started.append(name)
        metadata["container_ports"] = ports
        metadata["third_container_port_env_omitted"] = not args.boundary_only
        metadata["network_internal"] = command(["docker", "network", "inspect", "-f", "{{.Internal}}", network]) == "true"
        readiness = {}
        for i, name in enumerate(names):
            url = "http://" + name + ":" + str(ports[i])
            probe_code = ("import urllib.request,json; r=urllib.request.urlopen('" + url
                          + "/health',timeout=2); assert r.status==200 and json.load(r)=={'status':'ok'}")
            deadline = boot_times[name] + 60
            healthy = False
            while time.monotonic() < deadline:
                alive = command(["docker", "inspect", "-f", "{{.State.Running}}", name])
                if alive != "true":
                    break
                result = subprocess.run(["docker", "run", "--rm", "--network", network, "df-harness-runner",
                                         "python", "-c", probe_code], capture_output=True, timeout=8)
                if result.returncode == 0:
                    healthy = True
                    readiness[name] = round(time.monotonic() - boot_times[name], 3)
                    break
                time.sleep(.25)
            if not healthy:
                raise RuntimeError("readiness failed; classify using container state/logs before verdict")
        metadata["readiness_seconds"] = readiness
        runner = ["docker", "run", "--rm", "--name", run_id + "-runner", "--label", LABEL, "--network", network,
                  "-v", str(campaign) + ":/campaign.py:ro", "-v", str(out) + ":/out", "df-harness-runner",
                  "python", "/campaign.py", "http", "--source", "http://" + names[0] + ":8765",
                  "--destination", "http://" + names[1] + ":8766",
                  "--control", "/out", "--out", "/out/independent-summary.json"]
        if args.boundary_only:
            runner += ["--cases", "ignored_numeric_receipt_boundaries", "calendar_extremes"]
        else:
            runner += ["--third", "http://" + names[2] + ":8080"]
        with (out / "independent-console.log").open("w") as stream:
            independent = subprocess.Popen(runner, stdout=stream, stderr=subprocess.STDOUT)
            deadline = time.monotonic() + 900
            source_paused = False
            while independent.poll() is None:
                if (out / "pause-source").exists() and not source_paused:
                    command(["docker", "pause", names[0]])
                    source_paused = command(["docker", "inspect", "-f", "{{.State.Paused}}", names[0]]) == "true"
                    if not source_paused:
                        raise RuntimeError("source-unavailable compatibility gate failed")
                    metadata["source_unavailable_during_transfer"] = True
                    (out / "source-unavailable").write_text("paused\n")
                if time.monotonic() >= deadline:
                    subprocess.run(["docker", "rm", "-f", run_id + "-runner"], capture_output=True)
                    independent.wait(timeout=15)
                    raise RuntimeError("independent runner exceeded campaign budget")
                time.sleep(.1)
        metadata["independent_exit_code"] = independent.returncode
        metadata["post_campaign_pinned_sha"] = command(["git", "-C", str(repo), "rev-parse", "HEAD"])
        metadata["production_files_clean_after_execution"] = not bool(command(["git", "-C", str(repo), "status", "--porcelain"]))
        metadata["classification"] = "CAMPAIGN COMPLETED; independent review required for verdict"
    except Exception as error:
        metadata["orchestration_error"] = str(error)
        metadata["classification"] = "INFRASTRUCTURE DEFECT / INCONCLUSIVE; inspect diagnostics"
    finally:
        subprocess.run(["docker", "rm", "-f", run_id + "-runner"], capture_output=True)
        for name in started:
            subprocess.run(["docker", "inspect", name], stdout=(out / (name + "-inspect.json")).open("w"), stderr=subprocess.DEVNULL)
            subprocess.run(["docker", "logs", name], stdout=(out / (name + "-runtime.log")).open("w"), stderr=subprocess.STDOUT)
            subprocess.run(["docker", "rm", "-f", name], capture_output=True)
        if created_network:
            subprocess.run(["docker", "network", "rm", network], capture_output=True)
        if built:
            subprocess.run(["docker", "rmi", image], capture_output=True)
        (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        print(json.dumps(metadata, indent=2))
        # Pinned native materialization retained for review/recovery. Never delete other verifier resources.
    return 0 if metadata.get("independent_exit_code") == 0 and metadata.get("official_exit_code") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

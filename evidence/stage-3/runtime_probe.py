#!/usr/bin/env python3
"""Pinned standalone Docker publication check; no credentials or state exports."""
import argparse
import datetime as dt
import json
import re
import subprocess
import time
import uuid
from pathlib import Path


def run(args, timeout=120):
    value = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if value.returncode:
        raise RuntimeError("command failed: " + " ".join(args[:3]) + "; " + value.stderr[:150])
    return value.stdout.strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--revision", required=True)
    p.add_argument("--released", action="store_true")
    p.add_argument("--materialized", required=True)
    p.add_argument("--diagnostics", default="/mnt/d/dark/band-work/checks")
    args = p.parse_args()
    if not args.released or not re.fullmatch('[0-9a-f]{40}', args.revision):
        p.error('Conductor exact integrated FULL SHA release required')
    repo = Path(args.materialized).resolve()
    if str(repo).startswith("/mnt/") or run(["git", "-C", str(repo), "rev-parse", "HEAD"]) != args.revision:
        p.error("exact clean Linux-native materialization required")
    if run(["git", "-C", str(repo), "status", "--porcelain"]):
        p.error("materialization is dirty")
    name = "av-published-" + args.revision[:12] + "-" + uuid.uuid4().hex[:8]
    out = Path(args.diagnostics) / name
    out.mkdir(parents=True)
    image = name + ":service"
    result = {"revision": args.revision, "scope": "standalone published-port check; offline runtime proven in main isolated campaign",
              "classification": "INCONCLUSIVE", "checks": []}
    built = started = False
    try:
        with (out / "build.log").open("w") as log:
            build = subprocess.run(["docker", "build", "-t", image, str(repo / "stage-3")], stdout=log, stderr=subprocess.STDOUT, timeout=600)
        if build.returncode:
            raise RuntimeError("Docker build infrastructure failed; inspect external build.log")
        built = True
        run(["docker", "run", "-d", "--name", name, "--label", "tablekeeper.verifier=adversarial-verifier",
             "--cpus", "2", "--memory", "2g", "-e", "PORT=8987", "-p", "127.0.0.1::8987", image])
        started = True
        start_text = run(['docker', 'inspect', '-f', '{{.State.StartedAt}}', name])
        start_epoch = dt.datetime.fromisoformat(start_text.replace('Z', '+00:00')).timestamp()
        boot = time.monotonic() - (time.time() - start_epoch)
        mapping = run(["docker", "port", name, "8987/tcp"])
        host_port = int(mapping.rsplit(":", 1)[1])
        result["actual_mapping"] = mapping
        # Native Windows client reaches Docker Desktop's actual host publication.
        powershell = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
        base = "http://127.0.0.1:" + str(host_port)
        health = "$ErrorActionPreference='Stop'; $r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 5 -Uri '" + base + "/health'; if ($r.StatusCode -ne 200 -or ($r.Content | ConvertFrom-Json).status -ne 'ok') { exit 1 }; 'healthy'"
        deadline = boot + 60
        while time.monotonic() < deadline:
            probe = subprocess.run([powershell, "-NoProfile", "-Command", health], capture_output=True, text=True, timeout=8)
            if probe.returncode == 0:
                result["readiness_seconds"] = round(time.monotonic() - boot, 3)
                break
            if run(["docker", "inspect", "-f", "{{.State.Running}}", name]) != "true":
                raise RuntimeError("container exited before readiness")
            time.sleep(.2)
        else:
            raise RuntimeError("published mapping not reachable within readiness budget; inspect infrastructure before product verdict")
        script = ("$ErrorActionPreference='Stop'; $sw=[Diagnostics.Stopwatch]::StartNew(); "
                  "$r=Invoke-WebRequest -UseBasicParsing -Method POST -TimeoutSec 10 -ContentType 'application/json; charset=utf-8' "
                  "-Body '{\"users\":[],\"restaurants\":[],\"reservations\":[]}' -Uri '" + base + "/_test/reset'; "
                  "if ($r.StatusCode -ne 204) { exit 1 }; $reset=$sw.Elapsed.TotalSeconds; $sw.Restart(); "
                  "$r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 5 -Uri '" + base + "/restaurants'; "
                  "if ($r.StatusCode -ne 200 -or ($r.Content | ConvertFrom-Json).restaurants.Count -ne 0) { exit 1 }; "
                  "@{reset_status=204; reset_seconds=$reset; read_status=200; read_seconds=$sw.Elapsed.TotalSeconds} | ConvertTo-Json -Compress")
        result["checks"] = json.loads(run([powershell, "-NoProfile", "-Command", script], timeout=20))
        result["resource_configuration"] = run(["docker", "inspect", "-f", "{{.HostConfig.NanoCpus}} {{.HostConfig.Memory}}", name])
        result["classification"] = "PASS"
    except Exception as error:
        result["classification"] = "INFRASTRUCTURE DEFECT / INCONCLUSIVE"
        result["detail"] = str(error)
    finally:
        if started:
            with (out / "runtime.log").open("w") as log:
                subprocess.run(["docker", "logs", name], stdout=log, stderr=subprocess.STDOUT)
            subprocess.run(["docker", "rm", "-f", name], capture_output=True)
        if built:
            subprocess.run(["docker", "rmi", image], capture_output=True)
        (out / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"diagnostics": str(out), **result}, indent=2))
    return 0 if result["classification"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

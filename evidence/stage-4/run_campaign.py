#!/usr/bin/env python3
"""Exact-release Stage 4 runtime scaffold; results still require independent review."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

ACCEPTED = {1: 'd41a7627711951a07ce7a1718fac47c6ea5b6dd4',
            2: '2c431f7e6c0c5ed3bdae232bde255ec24c1bbab3',
            3: '0ca5880272740494e541a903a49ea423c6e8ce2b'}
TREES = {1: '7d35fe7568addec4437c2eb8705ed788ed46f0f2',
         2: '5e0f3ee38f68f7cb846b28c5dbd1850e7b768f91',
         3: '6db40e3e5b32431d5cb976f67b8be33c633da6ae'}
OFFICIAL = Path('/mnt/d/dark/dark-factory-wearedevs')
LABEL = 'tablekeeper.verifier=adversarial-verifier'


def command(argv, log=None, cwd=None, timeout=180):
    if log:
        with Path(log).open('w') as stream:
            result = subprocess.run(argv, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
    else:
        result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError('command failed; inspect ' + str(log or argv[:3]))
    return '' if log else result.stdout.strip()


def immutable(path, revision):
    if command(['git', '-C', str(path), 'rev-parse', 'HEAD']) != revision:
        raise RuntimeError('pinned revision differs')
    if command(['git', '-C', str(path), 'status', '--porcelain']):
        raise RuntimeError('pinned materialization changed')


def pin(repo, revision, target):
    command(['git', 'clone', '--no-hardlinks', '--no-checkout', str(repo), str(target)])
    command(['git', '-C', str(target), 'checkout', '--detach', revision])
    immutable(target, revision)
    for path in target.rglob('*'):
        if path.is_file() and '.git' not in path.relative_to(target).parts:
            path.chmod(path.stat().st_mode & ~0o222)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--revision', required=True); p.add_argument('--released', action='store_true')
    p.add_argument('--repo', default='/mnt/d/dark/band-work/result')
    p.add_argument('--diagnostics', default='/mnt/d/dark/band-work/checks')
    p.add_argument('--materialized'); p.add_argument('--resume-official')
    p.add_argument('--phase', choices=['full', 'browser4', 'extra4', 'core4', 'core', 'inherited', 'pairs', 'browser1', 'browser2', 'browser3', 'extensions', 'addons', 'disclosure'], default='full')
    p.add_argument('--phases', nargs='+', choices=['browser4', 'extra4', 'core4', 'core', 'inherited', 'pairs', 'browser1', 'browser2', 'browser3', 'extensions', 'addons', 'disclosure'])
    p.add_argument('--cases', nargs='+')
    args = p.parse_args()
    if not sys.platform.startswith('linux') or not args.released or not re.fullmatch('[0-9a-f]{40}', args.revision):
        p.error('Linux and Conductor explicit FULL Stage 4 production release required')
    scripts = Path(__file__).resolve().parent
    run = 'av-stage4-' + args.revision[:12] + '-' + uuid.uuid4().hex[:8]
    out = Path(args.diagnostics).resolve() / run
    if out.is_relative_to(Path(args.repo).resolve()):
        p.error('diagnostics must be outside result')
    out.mkdir(parents=True)
    native = Path(tempfile.mkdtemp(prefix=run + '-'))
    if str(native).startswith('/mnt/'):
        p.error('materialization must be Linux-native')
    candidate = Path(args.materialized).resolve() if args.materialized else native / 'candidate'
    if str(candidate).startswith('/mnt/'):
        p.error('candidate must remain Linux-native')
    old = {i: native / ('accepted-stage' + str(i)) for i in ACCEPTED}
    names = {role: run + '-' + role for role in ['source', 'destination', 'third', 'stage1', 'stage2', 'stage3']}
    ports = {'source': 8865, 'destination': 8866, 'third': 8080, 'stage1': 8871, 'stage2': 8872, 'stage3': 8873}
    urls = {role: 'http://' + name + ':' + str(ports[role]) for role, name in names.items()}
    images = {i: run + ':stage' + str(i) for i in [1, 2, 3, 4]}
    network = run + '-net'; started = []; runners = []; network_created = False
    meta = {'production_revision': args.revision, 'accepted_sources': ACCEPTED,
            'state': 'INCONCLUSIVE', 'limits': {'cpu': 2, 'memory': 2147483648},
            'budgets': {'readiness': 60, 'normal': 5, 'controls': 10}, 'phases': {}}
    try:
        meta['docker_version'] = command(['docker', 'version', '--format', '{{.Server.Version}}'])
        info = json.loads(command(['docker', 'info', '--format', '{{json .}}']))
        meta['host_resources'] = {k: info[k] for k in ['NCPU', 'MemTotal']}
        if info['NCPU'] < 2 or info['MemTotal'] < 2147483648 or shutil.disk_usage(native).free < 512 * 1024 * 1024:
            raise RuntimeError('INFRASTRUCTURE DEFECT: insufficient host resources')
        if args.materialized:
            immutable(candidate, args.revision)
        else:
            pin(args.repo, args.revision, candidate)
        for version in ACCEPTED:
            pin(args.repo, ACCEPTED[version], old[version])
            if command(['git', '-C', str(candidate), 'rev-parse', 'HEAD:stage-' + str(version)]) != TREES[version]:
                raise RuntimeError('frozen accepted lower-stage tree changed')
        meta['immutable_candidate'] = str(candidate)
        meta['official_revision'] = command(['git', '-C', str(OFFICIAL), 'rev-parse', 'HEAD'])
        command(['git', '-C', str(OFFICIAL), 'diff', '--ignore-space-at-eol', '--quiet'])
        meta['executable_sha256'] = {str(x.relative_to(scripts)): hashlib.sha256(x.read_bytes()).hexdigest() for x in scripts.rglob('*.py')}
        command([sys.executable, str(scripts / 'stage4_campaign.py'), 'calibrate'], out / 'calibration.log')
        if args.resume_official:
            official_path = Path(args.resume_official)
            report = json.loads((official_path / 'report.json').read_text())
            digest = command([sys.executable, '-c', "from harness.provenance import suite_digest; print(suite_digest('tablekeeper', ['1','2','3','4']))"], cwd=OFFICIAL)
            if report.get('revision') != args.revision or report.get('mode') != 'isolated' or report.get('state') != 'completed' or report.get('suite_digest') != digest:
                raise RuntimeError('official checkpoint provenance mismatch')
            for stage in ['1', '2', '3', '4']:
                counts = report.get('checks', {}).get(stage, {})
                if report.get('stages', {}).get(stage) != 'pass' or not counts.get('collected') or counts.get('passed') != counts['collected'] or any(counts.get(k) for k in ['failed', 'errors', 'skipped', 'deselected', 'xfailed']):
                    raise RuntimeError('incomplete passing official checkpoint')
            meta['official_checkpoint'] = str(official_path)
        else:
            command([sys.executable, '-m', 'harness', 'run', '--track', 'tablekeeper', '--repo', str(candidate),
                     '--stage', '4', '--mode', 'isolated', '--out', str(out / 'official')],
                    out / 'official-console.log', OFFICIAL, 1200)
            meta['official_checkpoint'] = str(out / 'official')
        command(['docker', 'network', 'create', '--internal', '--label', LABEL, network]); network_created = True
        meta['network_internal'] = command(['docker', 'network', 'inspect', '-f', '{{.Internal}}', network]) == 'true'
        for version in [1, 2, 3, 4]:
            folder = (old[version] if version < 4 else candidate) / ('stage-' + str(version))
            command(['docker', 'build', '-t', images[version], str(folder)], out / ('build-stage' + str(version) + '.log'), timeout=600)
        meta['readiness_seconds'] = {}
        for role, name in names.items():
            argv = ['docker', 'run', '-d', '--name', name, '--label', LABEL, '--network', network, '--cpus', '2', '--memory', '2g']
            if role != 'third':
                argv += ['-e', 'PORT=' + str(ports[role])]
            command(argv + [images[int(role[-1])] if role.startswith('stage') else images[4]])
            started.append(name)
            epoch = dt.datetime.fromisoformat(command(['docker', 'inspect', '-f', '{{.State.StartedAt}}', name]).replace('Z', '+00:00')).timestamp()
            probe = ('import json,time,urllib.request\ndeadline=time.monotonic()+max(0,60-(time.time()-' + repr(epoch) + '))\n'
                     'while time.monotonic()<deadline:\n try:\n  with urllib.request.urlopen(' + repr(urls[role] + '/health') + ',timeout=min(5,deadline-time.monotonic())) as r:\n'
                     "   if r.status==200 and json.load(r)=={'status':'ok'}:break\n except Exception:pass\n time.sleep(.1)\nelse:raise SystemExit(1)\n")
            command(['docker', 'run', '--rm', '--network', network, 'df-harness-runner', 'python', '-c', probe], timeout=65)
            meta['readiness_seconds'][role] = round(time.time() - epoch, 3)
        phases = args.phases or (['inherited', 'pairs', 'core', 'addons', 'core4', 'browser1', 'browser2', 'browser3', 'extensions', 'disclosure'] if args.phase == 'full' else [args.phase])
        for phase in phases:
            for name in started:
                if command(['docker', 'inspect', '-f', '{{.State.Paused}}', name]) == 'true':
                    command(['docker', 'unpause', name])
            control = out / (phase + '-control'); control.mkdir()
            runner = run + '-' + phase + '-runner'; runners.append(runner)
            if phase == 'browser4':
                module='/checks/browser_stage4.py'
            elif phase in ['core4','extra4']:
                module = '/checks/stage4_campaign.py' if phase=='core4' else '/checks/stage4_extensions.py'
            else:
                top = phase in ['core', 'addons', 'disclosure']
                filename = 'stage3_campaign.py' if phase == 'core' else 'stage3_extensions.py' if phase == 'addons' else 'browser_disclosure.py' if phase == 'disclosure' else 'extensions.py' if phase == 'extensions' else 'browser_campaign.py' if phase.startswith('browser') else 'campaign.py'
                module = '/checks/cumulative_stage3/' + ('' if top else 'cumulative/') + filename
            mode = 'inherited' if phase == 'inherited' else 'http'
            argv = ['docker', 'run', '--rm', '--name', runner, '--label', LABEL, '--network', network,
                    '-e', 'PYTHONDONTWRITEBYTECODE=1', '-v', str(scripts) + ':/checks:ro', '-v', str(out) + ':/out',
                    '-w', str(Path(module).parent), 'df-harness-runner', 'python', module]
            if phase not in ['addons', 'disclosure','extra4','browser4']:
                argv += [mode]
            argv += ['--released', '--revision', args.revision, '--source', urls['source'], '--destination', urls['destination']]
            if phase == 'core4':
                argv += ['--out', '/out/core4-summary.json']
            elif phase == 'browser4':
                argv += ['--out','/out/browser4']
            elif phase == 'extra4':
                argv += ['--control', '/out/' + control.name, '--third', urls['third'],
                         '--stage1',urls['stage1'],'--stage2',urls['stage2'],'--stage3',urls['stage3'],
                         '--out','/out/extra4-summary.json']
            else:
                argv += ['--control', '/out/' + control.name]
                if phase in ['core', 'addons']:
                    argv += ['--third', urls['third'], '--stage1', urls['stage1'], '--stage2', urls['stage2'], '--out', '/out/' + phase + '-summary.json']
                elif phase in ['inherited', 'pairs']:
                    argv += ['--third', urls['third'], '--out', '/out/' + phase + '-summary.json']
                    if phase == 'pairs' and not args.cases:
                        argv += ['--cases', 'pair_model_and_seeds', 'pair_create_validation', 'pair_options_oracle',
                                 'pair_receipt_array_identity', 'pair_patch_replacement_rollback', 'pair_batch_final_state',
                                 'pair_dst', 'pair_concurrency_50', 'pair_numeric_capacity', 'pair_reads_and_atomic_snapshots',
                                 'pair_patch_create_serial_oracle', 'pair_snapshot_receipts']
                else:
                    legacy_role = 'stage3' if phase == 'browser3' else 'stage2' if phase == 'browser2' else 'stage1'
                    argv += ['--legacy', urls[legacy_role], '--out', '/out/' + phase]
                    if phase == 'extensions': argv += ['--third', urls['third']]
            if args.cases:
                argv += ['--cases', *args.cases]
            mappings = {role: role for role in names}
            mappings['legacy'] = 'stage3' if phase == 'browser3' else 'stage2' if phase == 'browser2' else 'stage1'
            with (out / (phase + '-console.log')).open('w') as stream:
                process = subprocess.Popen(argv, stdout=stream, stderr=subprocess.STDOUT)
                deadline = time.monotonic() + 1200; handled = set()
                while process.poll() is None:
                    for role, target in mappings.items():
                        for prefix in ['', 'browser-']:
                            marker = prefix + 'pause-' + role
                            if (control / marker).exists() and marker not in handled:
                                command(['docker', 'pause', names[target]])
                                if command(['docker', 'inspect', '-f', '{{.State.Paused}}', names[target]]) != 'true':
                                    raise RuntimeError('INFRASTRUCTURE DEFECT: source unavailable control')
                                (control / (prefix + role + '-unavailable')).write_text('Docker pause confirmed\n')
                                handled.add(marker)
                    if time.monotonic() > deadline:
                        command(['docker', 'rm', '-f', runner]); process.wait(timeout=20)
                        raise RuntimeError('INCONCLUSIVE: campaign process limit exceeded')
                    time.sleep(.1)
                meta['phases'][phase] = {'exit_code': process.returncode, 'unavailable_controls': sorted(handled)}
            if process.returncode:
                break
        immutable(candidate, args.revision)
        for i in old:
            immutable(old[i], ACCEPTED[i])
        meta['state'] = 'EXECUTION CHECKPOINT; expansions/coverage/visual review and formal verdict required'
    finally:
        for name in runners + started:
            if name in started:
                with (out / (name + '.log')).open('w') as stream:
                    subprocess.run(['docker', 'logs', name], stdout=stream, stderr=subprocess.STDOUT)
            subprocess.run(['docker', 'rm', '-f', name], capture_output=True)
        if network_created:
            subprocess.run(['docker', 'network', 'rm', network], capture_output=True)
        for image in images.values():
            subprocess.run(['docker', 'rmi', image], capture_output=True)
        (out / 'metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
        print(json.dumps({'diagnostics': str(out), 'production_revision': args.revision, 'state': meta['state']}))


if __name__ == '__main__':
    main()

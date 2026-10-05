#!/usr/bin/env python3
"""Exact integrated Stage 2 orchestration; no product execution without release."""
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

ACCEPTED = 'd41a7627711951a07ce7a1718fac47c6ea5b6dd4'
OFFICIAL = Path('/mnt/d/dark/dark-factory-wearedevs')
LABEL = 'tablekeeper.verifier=adversarial-verifier'


def command(args, log=None, timeout=180, cwd=None):
    if log:
        with Path(log).open('w') as stream:
            result = subprocess.run(args, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
    else:
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError('command failed; inspect ' + str(log or args[:3]))
    return '' if log else result.stdout.strip()


def pin(shared, revision, target):
    command(['git', 'clone', '--no-hardlinks', '--no-checkout', str(shared), str(target)])
    command(['git', '-C', str(target), 'checkout', '--detach', revision])
    check_pin(target, revision)
    for file in target.rglob('*'):
        if file.is_file() and '.git' not in file.relative_to(target).parts:
            file.chmod(file.stat().st_mode & ~0o222)


def check_pin(path, revision):
    if command(['git', '-C', str(path), 'rev-parse', 'HEAD']) != revision:
        raise RuntimeError('immutable revision mismatch')
    if command(['git', '-C', str(path), 'status', '--porcelain']):
        raise RuntimeError('immutable clone modified')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision', required=True)
    parser.add_argument('--released', action='store_true')
    parser.add_argument('--repo', default='/mnt/d/dark/band-work/result')
    parser.add_argument('--diagnostics', default='/mnt/d/dark/band-work/checks')
    parser.add_argument('--materialized')
    parser.add_argument('--resume-official')
    parser.add_argument('--phase', choices=['full', 'inherited', 'pairs', 'browser', 'extensions'], default='full')
    parser.add_argument('--cases', nargs='+')
    args = parser.parse_args()
    if not sys.platform.startswith('linux') or not args.released or not re.fullmatch('[0-9a-f]{40}', args.revision):
        parser.error('Linux and Conductor exact integrated FULL SHA release required')
    run_id = 'av-stage2-' + args.revision[:12] + '-' + uuid.uuid4().hex[:8]
    out = Path(args.diagnostics).resolve() / run_id
    if out.is_relative_to(Path(args.repo).resolve()):
        parser.error('diagnostics must be outside result repository')
    out.mkdir(parents=True)
    native = Path(tempfile.mkdtemp(prefix=run_id + '-'))
    candidate = Path(args.materialized).resolve() if args.materialized else native / 'candidate'
    if str(candidate).startswith('/mnt/'):
        parser.error('materialization must be Linux-native; no cross-platform linked worktrees')
    old = native / 'accepted-stage1'
    network = run_id + '-net'
    names = [run_id + '-source', run_id + '-destination', run_id + '-third', run_id + '-stage1']
    ports = [8865, 8866, 8080, 8871]
    image, old_image = run_id + ':stage2', run_id + ':stage1'
    scripts = Path(__file__).resolve().parent
    metadata = {'production_revision': args.revision, 'accepted_source_revision': ACCEPTED,
                'diagnostics': str(out), 'classification': 'INCONCLUSIVE', 'limits': {'cpu': 2, 'memory': 2147483648},
                'budgets': {'readiness': 60, 'ordinary_request': 5, 'test_control': 10}, 'phases': {}}
    started = []; network_created = False
    try:
        metadata['docker_version'] = command(['docker', 'version', '--format', '{{.Server.Version}}'])
        metadata['host_resources'] = json.loads(command(['docker', 'info', '--format', '{{json .}}']))
        # Persist only relevant resource measurements, never raw runtime environment.
        metadata['host_resources'] = {k: metadata['host_resources'].get(k) for k in ['NCPU', 'MemTotal']}
        if metadata['host_resources']['NCPU'] < 2 or metadata['host_resources']['MemTotal'] < 2147483648:
            raise RuntimeError('INFRASTRUCTURE DEFECT: host below specified service limits')
        if shutil.disk_usage(native).free < 512 * 1024 * 1024:
            raise RuntimeError('INFRASTRUCTURE DEFECT: inadequate native disk')
        if not args.materialized:
            pin(args.repo, args.revision, candidate)
        else:
            check_pin(candidate, args.revision)
            for file in candidate.rglob('*'):
                if file.is_file() and '.git' not in file.relative_to(candidate).parts:
                    file.chmod(file.stat().st_mode & ~0o222)
        pin(args.repo, ACCEPTED, old)
        if command(['git', '-C', str(candidate), 'rev-parse', 'HEAD:stage-1']) != command(['git', '-C', str(old), 'rev-parse', 'HEAD:stage-1']):
            raise RuntimeError('frozen accepted Stage 1 production tree changed')
        metadata['immutable_candidate'] = str(candidate)
        metadata['immutable_stage1'] = str(old)
        metadata['official_revision'] = command(['git', '-C', str(OFFICIAL), 'rev-parse', 'HEAD'])
        command(['git', '-C', str(OFFICIAL), 'diff', '--ignore-space-at-eol', '--quiet'])
        metadata['executable_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in scripts.glob('*.py')}
        command([sys.executable, str(scripts / 'campaign.py'), 'calibrate'], out / 'calibration.log')
        if args.resume_official:
            checkpoint = Path(args.resume_official).resolve()
            report = json.loads((checkpoint / 'report.json').read_text())
            digest = command([sys.executable, '-c', "from harness.provenance import suite_digest; print(suite_digest('tablekeeper', ['1','2']))"], cwd=OFFICIAL)
            if (report.get('revision') != args.revision or report.get('mode') != 'isolated' or report.get('state') != 'completed'
                    or report.get('suite_digest') != digest or any(report.get('stages', {}).get(s) != 'pass' for s in ['1', '2'])):
                raise RuntimeError('invalid/stale/incomplete official checkpoint')
            for stage in ['1', '2']:
                counts = report.get('checks', {}).get(stage, {})
                if (not counts.get('collected') or counts.get('passed') != counts.get('collected')
                        or any(counts.get(k) for k in ['failed', 'errors', 'skipped', 'deselected', 'xfailed'])):
                    raise RuntimeError('official checkpoint does not contain complete passing stage counts')
            metadata['official_checkpoint'] = str(checkpoint)
        else:
            command([sys.executable, '-m', 'harness', 'run', '--track', 'tablekeeper', '--mode', 'isolated',
                     '--repo', str(candidate), '--stage', '2', '--out', str(out / 'official')], out / 'official-console.log', 900, OFFICIAL)
            metadata['official_checkpoint'] = str(out / 'official')
        command(['docker', 'network', 'create', '--internal', '--label', LABEL, network])
        network_created = True
        metadata['network_internal'] = command(['docker', 'network', 'inspect', '-f', '{{.Internal}}', network]) == 'true'
        for tag, folder, log in [(image, candidate / 'stage-2', 'build-stage2.log'), (old_image, old / 'stage-1', 'build-stage1.log')]:
            command(['docker', 'build', '-t', tag, str(folder)], out / log, 600)
        readiness = '''import json,time,urllib.request
deadline=time.monotonic()+max(0,60-(time.time()-START))
while time.monotonic()<deadline:
 try:
  with urllib.request.urlopen(URL,timeout=1) as r:
   if r.status==200 and json.load(r)=={'status':'ok'}:break
 except Exception:pass
 time.sleep(.1)
else:raise SystemExit(1)
'''
        metadata['readiness_seconds'] = {}
        for i, (name, port) in enumerate(zip(names, ports)):
            argv = ['docker', 'run', '-d', '--name', name, '--label', LABEL, '--network', network, '--cpus', '2', '--memory', '2g']
            if i != 2:
                argv += ['-e', 'PORT=' + str(port)]
            command(argv + [old_image if i == 3 else image]); started.append(name)
            start_text = command(['docker', 'inspect', '-f', '{{.State.StartedAt}}', name])
            start_epoch = dt.datetime.fromisoformat(start_text.replace('Z', '+00:00')).timestamp()
            code = ('URL=' + repr('http://' + name + ':' + str(port) + '/health')
                    + '\nSTART=' + repr(start_epoch) + '\n' + readiness)
            command(['docker', 'run', '--rm', '--network', network, 'df-harness-runner', 'python', '-c', code], timeout=65)
            metadata['readiness_seconds'][name] = round(time.time() - start_epoch, 3)
        phases = ['inherited', 'pairs', 'browser', 'extensions'] if args.phase == 'full' else [args.phase]
        for phase in phases:
            # Each phase has distinct control markers; restore source availability
            # only after the preceding valid checkpoint has completed.
            for name in names:
                if command(['docker', 'inspect', '-f', '{{.State.Paused}}', name]) == 'true':
                    command(['docker', 'unpause', name])
            control = out / (phase + '-control'); control.mkdir()
            runner_name = run_id + '-' + phase + '-runner'
            argv = ['docker', 'run', '--rm', '--name', runner_name, '--label', LABEL, '--network', network,
                    '-e', 'PYTHONDONTWRITEBYTECODE=1', '-v', str(scripts) + ':/checks:ro', '-v', str(out) + ':/out',
                    '-w', '/checks', 'df-harness-runner', 'python', '/checks/' + ('extensions.py' if phase == 'extensions' else 'browser_campaign.py' if phase == 'browser' else 'campaign.py'),
                    'http' if phase != 'inherited' else 'inherited', '--released', '--revision', args.revision,
                    '--source', 'http://' + names[0] + ':8865', '--destination', 'http://' + names[1] + ':8866',
                    '--control', '/out/' + control.name]
            if phase in ('browser', 'extensions'):
                argv += ['--legacy', 'http://' + names[3] + ':8871', '--out', '/out/' + phase]
                if phase == 'extensions':
                    argv += ['--third', 'http://' + names[2] + ':8080']
            else:
                argv += ['--third', 'http://' + names[2] + ':8080', '--out', '/out/' + phase + '-summary.json']
                if phase == 'pairs':
                    argv += ['--legacy', 'http://' + names[3] + ':8871']
            if args.cases:
                argv += ['--cases', *args.cases]
            with (out / (phase + '-console.log')).open('w') as stream:
                process = subprocess.Popen(argv, stdout=stream, stderr=subprocess.STDOUT)
                deadline = time.monotonic() + 900
                handled = set()
                while process.poll() is None:
                    for marker, target, response in [('pause-source', names[0], 'source-unavailable'),
                                                     ('pause-legacy', names[3], 'legacy-unavailable'),
                                                     ('browser-pause-legacy', names[3], 'browser-legacy-unavailable'),
                                                     ('browser-pause-source', names[0], 'browser-source-unavailable')]:
                        if (control / marker).exists() and marker not in handled:
                            command(['docker', 'pause', target])
                            if command(['docker', 'inspect', '-f', '{{.State.Paused}}', target]) != 'true':
                                raise RuntimeError('source unavailable control failed')
                            (control / response).write_text('Docker pause confirmed\n'); handled.add(marker)
                    if time.monotonic() >= deadline:
                        command(['docker', 'rm', '-f', runner_name]); process.wait(timeout=20)
                        raise RuntimeError('INCONCLUSIVE: bounded campaign execution expired')
                    time.sleep(.1)
                metadata['phases'][phase] = {'exit_code': process.returncode, 'source_controls': sorted(handled)}
            if process.returncode:
                break
        check_pin(candidate, args.revision); check_pin(old, ACCEPTED)
        metadata['production_clean_after'] = True
        metadata['classification'] = 'CAMPAIGN COMPLETE; independent verdict/visual review required'
    except Exception as exc:
        metadata['error_class'] = type(exc).__name__
        metadata['error'] = str(exc)
        raise
    finally:
        for phase in ['inherited', 'pairs', 'browser', 'extensions']:
            subprocess.run(['docker', 'rm', '-f', run_id + '-' + phase + '-runner'], capture_output=True)
        for name in started:
            subprocess.run(['docker', 'logs', name], stdout=(out / (name + '.log')).open('w'), stderr=subprocess.STDOUT)
            subprocess.run(['docker', 'rm', '-f', name], capture_output=True)
        if network_created:
            subprocess.run(['docker', 'network', 'rm', network], capture_output=True)
        for tag in [image, old_image]:
            subprocess.run(['docker', 'rmi', tag], capture_output=True)
        (out / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
        print(json.dumps({'diagnostics': str(out), 'production_revision': args.revision, 'classification': metadata['classification']}))


if __name__ == '__main__':
    main()

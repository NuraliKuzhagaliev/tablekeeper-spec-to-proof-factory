#!/usr/bin/env python3
"""Offline preparation/calibration only. Does not build or contact production."""
import ast
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT.parent / 'stage-2'
COPIES = ['campaign.py', 'oracle.py', 'stage1_campaign.py', 'browser_campaign.py',
          'extensions.py', 'runtime_probe.py']


def main():
    target = ROOT / 'cumulative'; target.mkdir(exist_ok=True)
    hashes = {}
    for name in COPIES:
        original = FROZEN / name; copy = target / name
        expected = original.read_bytes()
        if name == 'browser_campaign.py':
            expected = original.read_text().replace(
                "        check('table_ids' not in old and old['table_id'] == 'z', 'upgrade source must supply genuine Stage 1 receipt')",
                "        check(old['table_id'] == 'z' and old.get('table_ids', ['z']) == ['z']\n"
                "              and 'revision' not in old and 'accepted_terms' not in old,\n"
                "              'upgrade source must supply genuine accepted Stage 1 or Stage 2 original receipt')").encode()
        if copy.exists() and copy.read_bytes() != expected:
            raise RuntimeError('owned cumulative copy differs from frozen source: ' + name)
        if not copy.exists():
            copy.write_bytes(expected)
        hashes[name] = hashlib.sha256(copy.read_bytes()).hexdigest()
    ledger = (ROOT / 'requirements.md').read_text(encoding='utf-8')
    rows = []
    for line in ledger.splitlines():
        if not re.match(r'^\| TK[123]-', line):
            continue
        cells = [x.strip() for x in line.strip('|').split('|')]
        if len(cells) not in (7, 8):
            continue
        rows.append({'id': cells[0], 'risk': cells[3].split()[0],
                     'procedures': re.findall(r'[VWZ]\d{2}', cells[-2]), 'status': 'OPEN'})
    assert len(rows) == 557 and len({x['id'] for x in rows}) == 557
    counts = Counter(x['risk'] for x in rows)
    assert counts == {'C': 249, 'H': 285, 'M': 23}, counts
    profiles = sorted({p for r in rows for p in r['procedures']})
    assert len(profiles) == 64 and all(x['procedures'] for x in rows)
    for path in ROOT.rglob('*.py'):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    sys.path.insert(0, str(ROOT))
    model = importlib.import_module('policy_oracle')
    calibration = model.calibrate()
    assert calibration['status'] == 'PASS'
    # Frozen prior oracle calibration is still a verifier check, never product proof.
    prior_calibration = model.pairs.calibrate()
    campaign = importlib.import_module('stage3_campaign')
    gates = []
    for entry, argv in [('stage3_campaign.py', ['http', '--source', 'http://127.0.0.1:1']),
                        ('run_campaign.py', ['--revision', '0' * 40])]:
        result = subprocess.run([sys.executable, str(ROOT / entry), *argv],
                                capture_output=True, text=True, timeout=10)
        assert result.returncode == 2 and 'release required' in result.stderr.lower(), entry
        gates.append({'executable': entry, 'missing_release_refused_before_execution': True})
    manifest = {'state': 'PREPARATION; NO CANDIDATE REVISION RELEASED OR TESTED',
                'ledger_revision': '429c365ae5e36a02883d10d36efed26dcc32a6fa',
                'ledger_sha256': hashlib.sha256((ROOT / 'requirements.md').read_bytes()).hexdigest(),
                'coverage_counts': dict(counts), 'procedures': profiles,
                'obligations': rows, 'new_executable_cases': campaign.CASES,
                'copied_frozen_verifier_sha256': hashes,
                'new_oracle_calibration': calibration, 'prior_oracle_calibration': prior_calibration,
                'release_gate_checks': gates,
                'candidate_http_requests': 0,
                'executable_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in ROOT.rglob('*.py')}}
    (ROOT / 'preparation.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: manifest[k] for k in ['state', 'coverage_counts', 'candidate_http_requests',
                                             'new_oracle_calibration', 'new_executable_cases']}))


if __name__ == '__main__':
    main()

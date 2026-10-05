"""Offline Stage 4 preparation. No candidate, HTTP, build or acceptance execution."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

import seating_oracle as model

ROOT=Path(__file__).resolve().parent
LEDGER='dc5d81ba1fb49732681f4346f5d74efc219e67a9'
FROZEN={1:'d41a7627711951a07ce7a1718fac47c6ea5b6dd4',
        2:'2c431f7e6c0c5ed3bdae232bde255ec24c1bbab3',
        3:'0ca5880272740494e541a903a49ea423c6e8ce2b'}
PROFILES={
 'P01':'restaurant_counter_transitions', 'P02':'preview_permissions_interval_and_receipt_identity',
 'P03':'preview_limits_neutrality_and_failure', 'P04':'own_terms_full_interval_feasibility',
 'P05':'changes_then_waste_objective', 'P06':'reference_rank_vector_and_order_metamorphisms',
 'P07':'pair_members_orientation_and_accepted_capacity', 'P08':'bounded_exhaustive_optimizer_and_calibration',
 'P09':'immutable_preview_receipts_and_reusable_failures', 'P10':'apply_permissions_replay_applied_stale_priority',
 'P11':'restaurant_local_staleness_and_noop_isolation', 'P12':'atomic_reassigned_history_and_retained_values',
 'P13':'repaired_series_flags_schedules_and_once_counters', 'P14':'closure_occupancy_explanations_and_diner_rollback',
 'P15':'series_amend_controls_auth_receipts_and_cas', 'P16':'series_original_dates_current_tables_eligibility',
 'P17':'series_real_noop_empty_cutoff_terms_and_counters', 'P18':'index_ordered_policy_dst_errors_and_final_occupancy',
 'P19':'coordinated_50_transaction_and_snapshot_serialization', 'P20':'mandatory_maximum_planning_and_actual_budgets',
 'P21':'native_three_process_all_seven_receipt_transfer', 'P22':'populated_stage1_stage2_stage3_direct_upgrades',
 'P23':'retained_browser_and_current_repaired_seating', 'P24':'exact_release_clean_runtime_evidence_safety'}


def build_runtime():
    """Owned adaptations of frozen verifier scaffolding, never prior source edits."""
    retained=ROOT.parent/'stage-3'
    for source in retained.rglob('*.py'):
        relative=source.relative_to(retained)
        if len(relative.parts)==1 and source.name in ('prepare.py','run_campaign.py','runtime_probe.py'): continue
        target=ROOT/'cumulative_stage3'/relative
        content=source.read_text()
        if str(relative).replace('\\','/')=='cumulative/browser_campaign.py':
            old="        check(old['table_id'] == 'z' and old.get('table_ids', ['z']) == ['z']\n              and 'revision' not in old and 'accepted_terms' not in old,\n              'upgrade source must supply genuine accepted Stage 1 or Stage 2 original receipt')"
            new="        check(old['table_id'] == 'z' and old.get('table_ids', ['z']) == ['z'],\n              'immutable accepted Stage1/2/3 source must supply its genuine original single receipt')"
            assert old in content
            content=content.replace(old,new)
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists(): assert target.read_text()==content,'unexpected owned cumulative verifier change'
        else: target.write_text(content)
    runner=(retained/'run_campaign.py').read_text()
    runner=runner.replace('Stage 3','Stage 4').replace('av-stage3-','av-stage4-')
    runner=runner.replace("2: '2c431f7e6c0c5ed3bdae232bde255ec24c1bbab3'}","2: '2c431f7e6c0c5ed3bdae232bde255ec24c1bbab3',\n            3: '0ca5880272740494e541a903a49ea423c6e8ce2b'}")
    runner=runner.replace("2: '5e0f3ee38f68f7cb846b28c5dbd1850e7b768f91'}","2: '5e0f3ee38f68f7cb846b28c5dbd1850e7b768f91',\n         3: '6db40e3e5b32431d5cb976f67b8be33c633da6ae'}")
    runner=runner.replace("'core', 'inherited'","'core4', 'core', 'inherited'")
    runner=runner.replace("'browser1', 'browser2'","'browser1', 'browser2', 'browser3'")
    runner=runner.replace("'third', 'stage1', 'stage2']","'third', 'stage1', 'stage2', 'stage3']")
    runner=runner.replace("'stage2': 8872}","'stage2': 8872, 'stage3': 8873}")
    runner=runner.replace('for i in [1, 2, 3]','for i in [1, 2, 3, 4]')
    runner=runner.replace("str(scripts / 'stage3_campaign.py')","str(scripts / 'stage4_campaign.py')")
    runner=runner.replace("['1','2','3']","['1','2','3','4']").replace("['1', '2', '3']","['1', '2', '3', '4']")
    runner=runner.replace("'--stage', '3'","'--stage', '4'")
    runner=runner.replace('for version in [1, 2, 3]:','for version in [1, 2, 3, 4]:').replace('version < 3','version < 4')
    runner=runner.replace('else images[3]','else images[4]')
    runner=runner.replace("['inherited', 'pairs', 'core', 'addons',", "['inherited', 'pairs', 'core', 'addons', 'core4',")
    start=runner.index("            top = phase in")
    finish=runner.index("            if args.cases:", start)
    # The first if args.cases is inside the pairs branch in the retained scaffold;
    # locate the phase-wide argument override after the legacy branch instead.
    finish=runner.index("            if args.cases:\n                argv",start)
    runner=runner[:start]+'''            if phase == 'core4':
                module = '/checks/stage4_campaign.py'
            else:
                top = phase in ['core', 'addons', 'disclosure']
                filename = 'stage3_campaign.py' if phase == 'core' else 'stage3_extensions.py' if phase == 'addons' else 'browser_disclosure.py' if phase == 'disclosure' else 'extensions.py' if phase == 'extensions' else 'browser_campaign.py' if phase.startswith('browser') else 'campaign.py'
                module = '/checks/cumulative_stage3/' + ('' if top else 'cumulative/') + filename
            mode = 'inherited' if phase == 'inherited' else 'http'
            argv = ['docker', 'run', '--rm', '--name', runner, '--label', LABEL, '--network', network,
                    '-e', 'PYTHONDONTWRITEBYTECODE=1', '-v', str(scripts) + ':/checks:ro', '-v', str(out) + ':/out',
                    '-w', str(Path(module).parent), 'df-harness-runner', 'python', module]
            if phase not in ['addons', 'disclosure']:
                argv += [mode]
            argv += ['--released', '--revision', args.revision, '--source', urls['source'], '--destination', urls['destination']]
            if phase == 'core4':
                argv += ['--out', '/out/core4-summary.json']
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
'''+runner[finish:]
    old="            elif args.resume_official and phase == 'browser2':"
    begin=runner.index(old)
    end=runner.index('            mappings =',begin)
    runner=runner[:begin]+runner[end:]
    runner=runner.replace("mappings['legacy'] = 'stage2' if phase == 'browser2' else 'stage1'","mappings['legacy'] = 'stage3' if phase == 'browser3' else 'stage2' if phase == 'browser2' else 'stage1'")
    (ROOT/'run_campaign.py').write_text(runner)
    runtime=(retained/'runtime_probe.py').read_text().replace('"stage-3"','"stage-4"').replace("'stage-3'","'stage-4'")
    (ROOT/'runtime_probe.py').write_text(runtime)


def calibrate_extensions():
    cases=model.witnesses()
    metamorphic=0
    for case in cases:
        args=model.as_args(case); expected=model.solve(**args)
        shifted={**args,'bookings':[model.replace(b,starts=b.starts+10080,ends=b.ends+10080) for b in args['bookings']],
                 'prior_closures':[model.replace(c,starts=c.starts+10080,ends=c.ends+10080) for c in args['prior_closures']],
                 'proposed':model.replace(args['proposed'],starts=args['proposed'].starts+10080,ends=args['proposed'].ends+10080)}
        assert model.solve(**shifted)==expected; metamorphic+=1
        cancelled=model.model_booking('CANCEL','a' if 'a' in args['tables'] else args['tables'][0],1,
                         {x:100 for x in args['tables']},-100,200,status='cancelled')
        assert model.solve(**{**args,'bookings':[*args['bookings'],cancelled]})==expected; metamorphic+=1
        names={x:'opaque-'+str(i) for i,x in enumerate(args['tables'])}
        renamed={**args,'tables':tuple(names[x] for x in args['tables']),
          'pairs':tuple(tuple(names[x] for x in p) for p in args['pairs']),
          'bookings':[model.replace(b,members=tuple(names[x] for x in b.members),capacities={names[x]:v for x,v in b.capacities.items()}) for b in args['bookings']],
          'prior_closures':[model.replace(c,table=names[c.table]) for c in args['prior_closures']],
          'proposed':model.replace(args['proposed'],table=names[args['proposed'].table])}
        result=model.solve(**renamed)
        if expected is None: assert result is None
        else:
            assert result['ranks']==expected['ranks'] and result['moved_count']==expected['moved_count'] and result['unused_seats']==expected['unused_seats']
            assert [a['table_ids'] for a in result['assignments']]==[[names[x] for x in a['table_ids']] for a in expected['assignments']]
        metamorphic+=1
        reordered=model.solve(**{**args,'tables':tuple(reversed(args['tables'])),'pairs':tuple(reversed(args['pairs']))})
        if expected is None: assert reordered is None
        else: assert (reordered['moved_count'],reordered['unused_seats'])==(expected['moved_count'],expected['unused_seats'])
        metamorphic+=1
        remapped=model.solve(**{**args,'bookings':[model.replace(b,reference='REN'+str(i)) for i,b in enumerate(reversed(args['bookings']))]})
        if expected is None: assert remapped is None
        else: assert (remapped['moved_count'],remapped['unused_seats'])==(expected['moved_count'],expected['unused_seats'])
        metamorphic+=1
    adjacent=dict(tables=('a','b','c'),pairs=(),bookings=[model.model_booking('ADJ000','a',2,{'a':2,'b':2,'c':2})],
                  prior_closures=(model.Closure('a',90,100),),proposed=model.Closure('b',0,90))
    assert model.solve(**adjacent)['moved_count']==0
    assert model.solve(**adjacent,variant='closed-intervals')['moved_count']==1
    series={'revision':3,'occurrences':[]}
    dates=['2080-06-01','2080-06-08','2080-06-15','2080-06-22']
    for i,day in enumerate(dates):
        series['occurrences'].append({'index':i,'reference':'REF00'+str(i),'exception':i in (0,3),
            'reservation':{'status':'cancelled' if i==2 else 'confirmed','starts_at_local':('2090-01-01' if i==0 else day)+'T19:00',
                           'table_ids':['c','a'],'party_size':5}})
    error, targets=model.series_targets(series,dates,3,0,'20:00')
    assert error is None and len(targets)==1 and targets[0]['index']==1
    assert targets[0]['starts_at_local']=='2080-06-08T20:00' and targets[0]['table_ids']==['c','a']
    assert model.amend_deltas(targets)=={'restaurant':1,'series':1,'reservations':{'REF001':1}}
    assert model.series_targets(series,dates,2,0,'20:00')[0]=='stale_revision'
    assert model.series_targets(series,dates,3,0,'19:00')[1][0]['changed'] is False
    assert model.amend_deltas(model.series_targets(series,dates,3,0,'19:00')[1])=={'restaurant':0,'series':0,'reservations':{}}
    assert model.series_targets(series,dates,3,2,'20:00')==(None,[])
    assert model.series_targets(series,dates,2,2,'20:00')[0]=='stale_revision'
    assert model.application_deltas([{'reference':'a','changed':True},{'reference':'b','changed':True},{'reference':'c','changed':False}],
                                    {'a':'series1','b':'series1','c':'series2'})=={'restaurant':1,'reservations':{'a':1,'b':1},'series':{'series1':1}}
    invalid=0
    for field,values in [('expected_revision',[None,0,-1,True,'3',3.5]),('from_index',[None,-1,4,True,'0',0.5]),
                         ('local_time',[None,True,3,'24:00','20:60','2:00','20:00:00','20:00Z','20:00+00:00'])]:
        for value in values:
            body={'expected_revision':3,'from_index':0,'local_time':'20:00',field:value}
            assert model.series_targets(series,dates,**body)[0]=='validation_failed'; invalid+=1
    # Complete policy/DST transition is derived from the retained independent oracle.
    sys.path.insert(0,str(ROOT/'cumulative_stage3'))
    import policy_oracle as policies
    def native_series(zone,dates,clock):
        restaurant=policies.fixture(zone=zone,opens='00:00',closes='05:00')['restaurants'][0]
        terms=policies.baseline(restaurant); rows=[]
        for i,day in enumerate(dates):
            start=policies.prior.resolve(day+'T'+clock,zone)
            end=(start.astimezone(policies.dt.timezone.utc)+policies.dt.timedelta(minutes=90)).astimezone(policies.ZoneInfo(zone))
            record={'reference':'DST00'+str(i),'reservation_id':'id'+str(i),'restaurant_id':'r','table_id':'z','table_ids':['z'],
                    'party_size':2,'status':'confirmed','starts_at_local':day+'T'+clock,'starts_at':start.isoformat(),
                    'ends_at':end.isoformat(),'revision':1,'accepted_terms':terms,'created_at':'2020-01-01T00:00:00Z'}
            rows.append({'index':i,'reference':record['reference'],'exception':False,'reservation':record})
        return restaurant,{'series_id':'series','revision':1,'interval_weeks':1,'occurrences':rows}
    berlin_dates=['2026-03-22','2026-03-29','2026-04-05']
    restaurant,agreement=native_series('Europe/Berlin',berlin_dates,'01:30')
    now=model.instant('2020-01-01T00:00:00Z')
    blocker={**agreement['occurrences'][0]['reservation'],'reference':'BLOCK0','reservation_id':'block',
             'starts_at':'2026-03-22T03:30:00+01:00','ends_at':'2026-03-22T05:00:00+01:00'}
    error,after,deltas=model.series_transition(restaurant,[],agreement,berlin_dates,1,0,'02:30',now,[blocker])
    assert error=='invalid_local_time' and after==agreement and deltas=={},'index nonoccupancy must precede final overlap'
    error,after,deltas=model.series_transition(restaurant,[],agreement,berlin_dates,1,0,'01:30',model.instant('2027-01-01T00:00:00Z'))
    assert error is None and after==agreement and deltas=={},'expired semantic series no-op must not check cutoff'
    assert model.series_transition(restaurant,[],agreement,berlin_dates,2,0,'02:30',model.instant('2027-01-01T00:00:00Z'))[0]=='stale_revision'
    assert model.series_transition(restaurant,[],agreement,berlin_dates,1,0,'03:00',model.instant('2027-01-01T00:00:00Z'))[0]=='cutoff_passed'
    ny_dates=['2026-10-25','2026-11-01','2026-11-08']
    restaurant,agreement=native_series('America/New_York',ny_dates,'00:30')
    error,after,deltas=model.series_transition(restaurant,[],agreement,ny_dates,1,0,'01:30',now)
    assert error is None and after['revision']==2 and len(deltas)==3
    assert after['occurrences'][1]['reservation']['starts_at']=='2026-11-01T01:30:00-04:00'
    assert after['occurrences'][1]['reservation']['ends_at']=='2026-11-01T02:00:00-05:00'
    assert all(not x['exception'] for x in after['occurrences'])
    policy={**policies.policy(restaurant,'2026-11-01',reservation_duration_minutes=120),'policy_version':1}
    error,after,deltas=model.series_transition(restaurant,[policy],agreement,ny_dates,1,0,'01:30',now)
    assert error is None and [x['reservation']['accepted_terms']['policy_version'] for x in after['occurrences']]==[0,1,1]
    closure=model.Closure('z',model.instant(after['occurrences'][2]['reservation']['starts_at']),model.instant(after['occurrences'][2]['reservation']['ends_at']))
    error,rolled,deltas=model.series_transition(restaurant,[policy],agreement,ny_dates,1,0,'01:30',now,closures=[closure])
    assert error=='table_unavailable' and rolled==agreement and deltas=={}
    # Complete mandatory-size enumeration streams feasible vectors instead of retaining them.
    caps={x:4 for x in 'abcdef'}
    maximum=dict(tables=tuple(caps),pairs=(('a','c'),('c','d'),('b','e'),('b','f')),
                 bookings=[model.model_booking('MAX00'+str(i),x,2,caps,i*90,i*90+60) for i,x in enumerate(caps)],
                 prior_closures=(),proposed=model.Closure('b',0,600))
    began=time.monotonic(); result=model.solve(**maximum); seconds=time.monotonic()-began
    assert result['considered_count']==6 and result['moved_count']==1 and result['unused_seats']==12
    assert result['ranks']==(0,0,2,3,4,5)
    return {'status':'PASS','metamorphic_comparisons':metamorphic,'series_invalid_control_vectors':invalid,
      'additional_closed_interval_fault_detected':True,'series_original_date_current_tables_cas_noop_empty_deltas':'PASS',
      'series_complete_policy_dst_index_precedence_closure_rollback':'PASS',
      'maximum_model':{'tables':6,'pairs':4,'considered':6,'unfiltered_vectors_bound':10**6,'seconds':round(seconds,3)},
      'candidate_requests':0}


def main():
    if (ROOT/'coverage.json').exists():
        raise SystemExit('Preparation generator is closed once final coverage exists; acceptance evidence remains frozen.')
    build_runtime()
    rows=[]
    for line in (ROOT/'requirements.md').read_text().splitlines():
        if not re.match(r'^\| TK[1234]-',line): continue
        cells=[x.strip() for x in line.strip('|').split('|')]
        if len(cells) not in (7,8): continue
        rows.append({'id':cells[0],'risk':cells[3].split()[0],
                     'procedures':re.findall(r'[VWZP]\d{2}',cells[-2]),'status':'OPEN / NOT EXECUTED'})
    assert len(rows)==730 and len({r['id'] for r in rows})==730
    assert Counter(r['risk'] for r in rows)=={'C':382,'H':325,'M':23}
    profiles=sorted({p for r in rows for p in r['procedures']})
    assert len(profiles)==88 and all(r['procedures'] for r in rows)
    for path in ROOT.rglob('*.py'): ast.parse(path.read_text(),filename=str(path))
    calibration=model.calibrate(); extensions=calibrate_extensions()
    # Earlier independent campaigns are reused read-only, not production modules.
    retained=ROOT.parent/'stage-3'
    hashes={str(p.relative_to(retained)):hashlib.sha256(p.read_bytes()).hexdigest() for p in retained.rglob('*.py')}
    for path in retained.rglob('*.py'):
        blob=subprocess.check_output(['git','show','4ad81381f4e7ef5a6241da7e4d12370e91a900d6:evidence/stage-3/'+str(path.relative_to(retained)).replace('\\','/')],cwd=ROOT.parents[1])
        assert blob.replace(b'\r\n',b'\n')==path.read_bytes().replace(b'\r\n',b'\n')
    gate=subprocess.run([sys.executable,str(ROOT/'stage4_campaign.py'),'http','--source','http://127.0.0.1:1'],capture_output=True,text=True,timeout=10)
    assert gate.returncode==2 and 'release required' in gate.stderr.lower()
    gate_runtime=subprocess.run([sys.executable,str(ROOT/'run_campaign.py'),'--revision','0'*40],capture_output=True,text=True,timeout=10)
    assert gate_runtime.returncode==2 and 'release required' in gate_runtime.stderr.lower()
    output={'state':'PREPARATION ONLY; NO STAGE4 CANDIDATE RELEASED OR TESTED','ledger_revision':LEDGER,
      'ledger_sha256':hashlib.sha256((ROOT/'requirements.md').read_bytes()).hexdigest(),
      'counts':dict(Counter(r['risk'] for r in rows)),'profiles':profiles,'obligations':rows,
      'stage4_case_profiles':PROFILES,'inherited_profile_cases':json.loads((retained/'coverage.json').read_text())['profiles'],
      'frozen_accepted_sources':FROZEN,
      'retained_verifier_sha256':hashes,'optimizer_calibration':calibration,'boundary_model_calibration':extensions,
      'release_gate_refused_before_http':True,'runtime_release_gate_refused':True,'candidate_requests':0,
      'executable_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*.py')}}
    (ROOT/'preparation.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('state','counts','optimizer_calibration','boundary_model_calibration','candidate_requests')}))


if __name__=='__main__': main()

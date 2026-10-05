"""Independent cumulative Stage 4 boundary, transfer and snapshot controls.

No production imports; opaque private snapshots and original receipts stay in memory.
"""
import argparse
import copy
import datetime as dt
import json
from pathlib import Path
import random
import sys
import time

import stage4_campaign as core
import seating_oracle as model
retained=core.retained
policies=core.policies
check=core.check


class Campaign(core.Campaign):
    def __init__(self,source,destination,third,stage1,stage2,stage3,control):
        super().__init__(source,destination)
        self.third=retained.API(third)
        self.legacy={i:retained.prior.API(url) for i,url in enumerate((stage1,stage2,stage3),1)}
        self.control=Path(control)

    def run(self,names):
        for name in names:
            began=time.monotonic()
            try:
                getattr(self,name)();row={'case':name,'status':'PASS'}
            except Exception as exc:
                row={'case':name,'status':'FAIL','classification':'INCONCLUSIVE','detail':str(exc)}
            row['seconds']=round(time.monotonic()-began,3);self.results.append(row);print(json.dumps(row),flush=True)
        timings=[item for api in [self.api,self.dest,self.third,*self.legacy.values()] for item in api.timings]
        return {'cases':self.results,'all_passed':all(r['status']=='PASS' for r in self.results),
                'requests':len(timings),'max_regular_seconds':max((v for p,v in timings if not p.startswith('/_test/')),default=0),
                'max_control_seconds':max((v for p,v in timings if p.startswith('/_test/')),default=0)}

    def pause(self,role):
        (self.control/('pause-'+role)).write_text('ready\n')
        deadline=time.monotonic()+30
        while not (self.control/(role+'-unavailable')).exists():
            if time.monotonic()>deadline: raise OSError('source pause control failed')
            time.sleep(.1)

    def adopt(self,count=4,day=retained.DAY,at='18:00',ids=None):
        body=retained.prior.body(at=at,day=day)
        if ids: body.pop('table_id');body['table_ids']=ids
        anchor=self.api.book(self.token,body,'anchor')
        request={'anchor_reference':anchor['reference'],'count':count,'interval_weeks':1}
        series=self.api.expect(201,'POST','/series',request,self.token,'adopt')
        return series,body,anchor,request

    def states(self,series):
        return {x['reference']:(self.api.current(x['reference'],self.token),self.api.history(x['reference'],self.token))
                for x in series['occurrences']}

    def series_original_dates_repaired_tables_exclusions(self):
        a,t=self.fresh(); series,body,anchor,adoption=self.adopt(5)
        refs=[x['reference'] for x in series['occurrences']]
        moved_anchor=a.expect(200,'PATCH','/reservations/'+refs[0],{'starts_at_local':'2080-06-07T18:30'},t)
        a.expect(200,'PATCH','/reservations/'+refs[1],{'party_size':3},t)
        a.expect(200,'POST','/reservations/'+refs[2]+'/cancel',token=t)
        before_series=a.expect(200,'GET','/series/'+series['series_id'],token=t)
        r3=a.current(refs[3],t); before=self.states(before_series)
        closure={'table_id':'z','from':r3['starts_at'],'to':r3['ends_at']}
        plan=a.expect(201,'POST','/restaurants/r/replans',closure,t,'repair')
        applied=a.expect(201,'POST','/restaurants/r/replans/'+plan['plan_id']+'/apply',{},t,'repair-apply')
        repaired=a.expect(200,'GET','/series/'+series['series_id'],token=t)
        check(repaired['revision']==before_series['revision']+1,'repair series counter not once')
        check([x['exception'] for x in repaired['occurrences']]==[True,True,False,False,False],'repair changed exception flags')
        check(repaired['occurrences'][3]['reservation']['table_ids']!=['z'],'repair failed to move selected member')
        before=self.states(repaired); counter=self.counter()
        request={'expected_revision':repaired['revision'],'from_index':0,'local_time':'20:00'}
        changed=a.expect(201,'POST','/series/'+series['series_id']+'/amend',request,t,'amend')
        check(changed['revision']==repaired['revision']+1 and self.counter()==counter+1,'amend compound counters')
        for i,x in enumerate(changed['occurrences']):
            old,events=before[x['reference']]; new=x['reservation']; history=a.history(x['reference'],t)
            if i<3: check((new,history)==(old,events),'excluded occurrence changed')
            else:
                scheduled=(dt.date.fromisoformat(retained.DAY)+dt.timedelta(days=i*7)).isoformat()
                check(new['starts_at_local']==scheduled+'T20:00','amend used edited anchor date')
                check(new['table_ids']==old['table_ids'],'amend discarded operator repaired tables')
                check(new['revision']==old['revision']+1 and history[:-1]==events,'amend revision/history')
                check(history[-1]['changes']==[{'field':'starts_at_local','from':old['starts_at_local'],'to':new['starts_at_local']}],'series changed event fields')
                check(x['exception'] is False,'series amend marked exception')
        check(a.expect(200,'POST','/reservations',body,t,'anchor')==anchor,'original anchor receipt changed')
        check(a.expect(200,'POST','/series',adoption,t,'adopt')==series,'original adoption receipt changed')
        check(a.expect(200,'POST','/restaurants/r/replans/'+plan['plan_id']+'/apply',{},t,'repair-apply')==applied,'repair receipt changed')
        check(a.expect(200,'POST','/series/'+series['series_id']+'/amend',request,t,'amend')==changed,'amend receipt changed')

    def series_control_types_privacy_empty_and_failure_keys(self):
        a,t=self.fresh(); s,*_=self.adopt(2); path='/series/'+s['series_id']+'/amend'
        request={'expected_revision':s['revision'],'from_index':0,'local_time':'20:00'}
        a.expect(401,'POST',path,request,key='anon',code='unauthenticated')
        a.expect(404,'POST',path,request,self.tokens['bob'],'foreign','not_found')
        a.expect(404,'POST','/series/unknown/amend',request,t,'unknown','not_found')
        a.expect(400,'POST',path,request,t,code='missing_idempotency_key')
        a.expect(422,'POST',path,request,t,'x'*256,'validation_failed')
        bad=[{k:v for k,v in request.items() if k!=f} for f in request]
        for f,vals in [('expected_revision',[True,False,0,-1,'1',None,1.2]),('from_index',[True,False,-1,2,'0',None,1.2]),
                       ('local_time',['20:0','2:00','24:00','20:00:00','20:00Z',True,None])]:
            bad.extend({**request,f:v} for v in vals)
        snapshot=a.expect(200,'GET','/_test/export')
        for value in bad:
            a.expect(422,'POST',path,value,t,'failed','validation_failed')
            check(a.expect(200,'GET','/_test/export')==snapshot,'invalid series control mutated any state')
        changed=a.expect(201,'POST',path,request,t,'failed')
        a.expect(409,'POST',path,{'invalid':True},t,'failed','idempotency_key_reuse')
        for x in changed['occurrences']: a.expect(200,'POST','/reservations/'+x['reference']+'/cancel',token=t)
        current=a.expect(200,'GET','/series/'+s['series_id'],token=t); before=a.expect(200,'GET','/_test/export')
        a.expect(409,'POST',path,request,t,'stale-empty','stale_revision')
        check(a.expect(200,'GET','/_test/export')==before,'stale empty changed state')
        empty_request={**request,'expected_revision':current['revision']}
        empty=a.expect(201,'POST',path,empty_request,t,'empty')
        check(empty==current,'empty eligible set changed revisions')
        check(a.expect(200,'POST',path,empty_request,t,'empty')==empty,'empty receipt replay')
        check(a.expect(200,'POST',path,request,t,'failed')==changed,'old series amend receipt after cancellation')

    def series_expired_noop_and_per_date_policy(self):
        # Cutoff passage requires genuine time, not clock manipulation or past adoption.
        now=dt.datetime.now(dt.timezone.utc); start=(now+dt.timedelta(minutes=3)).replace(second=0,microsecond=0)
        fx=policies.fixture(zone='UTC');r=fx['restaurants'][0]
        r.update(slot_minutes=1,reservation_duration_minutes=1,cancellation_cutoff_minutes=0,
                 opening_hours=[{'weekday':w,'opens':'00:00','closes':'23:59'} for w in retained.prior.WEEK])
        a,t=self.fresh(fx); s,*_=self.adopt(2,day=start.date().isoformat(),at=start.strftime('%H:%M'))
        # Real adoption succeeded before a published cutoff; publish does not mutate accepted0.
        policy=policies.policy(r,start.date().isoformat(),cancellation_cutoff_minutes=10080)
        a.expect(201,'POST','/restaurants/r/policies',policy,t,'cutoff')
        # Adopted anchor cannot change accepted cutoff via no-op; force a real party amendment.
        ref=s['occurrences'][0]['reference'];a.expect(200,'PATCH','/reservations/'+ref,{'party_size':3},t)
        # This is an exception, so use a new series accepted with future strict cutoff only
        # after adoption: initial far-future occurrences can amend before cutoff then be imported?
        # Instead assert no-op preserved old policy0 after new policy makes same fields invalid.
        current=a.expect(200,'GET','/series/'+s['series_id'],token=t)
        before=self.states(current); counter=self.counter()
        result=a.expect(201,'POST','/series/'+s['series_id']+'/amend',
             {'expected_revision':current['revision'],'from_index':1,'local_time':start.strftime('%H:%M')},t,'noop-new-policy')
        check(result==current and self.states(current)==before and self.counter()==counter,'noop adopted new policy/cutoff')
        # Exact expiry control from an adoption whose first occurrence is just after midnight
        # is impractical without waiting; accepted-cutoff passage can be immediate after a
        # real whole-series amendment which adopts a longer cutoff for the near-future anchor.
        fx=policies.fixture(zone='UTC');r=fx['restaurants'][0]
        r.update(slot_minutes=1,reservation_duration_minutes=1,cancellation_cutoff_minutes=0,
                 opening_hours=[{'weekday':w,'opens':'00:00','closes':'23:59'} for w in retained.prior.WEEK])
        a,t=self.fresh(fx); s,*_=self.adopt(2,day=start.date().isoformat(),at=start.strftime('%H:%M'))
        a.expect(201,'POST','/restaurants/r/policies',policies.policy(r,start.date().isoformat(),cancellation_cutoff_minutes=10080),t,'cutoff')
        new_clock=(start+dt.timedelta(minutes=1)).strftime('%H:%M')
        request={'expected_revision':s['revision'],'from_index':0,'local_time':new_clock}
        strict=a.expect(201,'POST','/series/'+s['series_id']+'/amend',request,t,'strict')
        before=self.states(strict);counter=self.counter()
        noop={**request,'expected_revision':strict['revision']}
        check(a.expect(201,'POST','/series/'+s['series_id']+'/amend',noop,t,'expired-noop')==strict,'expired series noop refused')
        a.expect(409,'POST','/series/'+s['series_id']+'/amend',{**noop,'local_time':start.strftime('%H:%M')},t,'expired-real','cutoff_passed')
        a.expect(409,'POST','/series/'+s['series_id']+'/amend',request,t,'stale','stale_revision')
        check(self.states(strict)==before and self.counter()==counter,'expired failure/noop changed state')
        # Date selection differs among occurrences; all real changes adopt independent terms.
        a,t=self.fresh();s,*_=self.adopt(3)
        r=self.r; second=s['occurrences'][1]['reservation']['starts_at_local'][:10]
        pub=a.expect(201,'POST','/restaurants/r/policies',policies.policy(r,second,reservation_duration_minutes=60),t,'new-policy')
        before=self.states(s);request={'expected_revision':1,'from_index':0,'local_time':'20:00'}
        after=a.expect(201,'POST','/series/'+s['series_id']+'/amend',request,t,'terms')
        check([x['reservation']['accepted_terms']['policy_version'] for x in after['occurrences']]==[0,1,1],'series per-date policy selection')
        for x in after['occurrences']:
            new=x['reservation'];old,history=before[x['reference']]
            events=a.history(x['reference'],t)
            check(events[:-1]==history and events[-1]['accepted_terms']==new['accepted_terms'],'old history terms changed')

    def series_dst_precedence_and_closure_rollback(self):
        for zone,day,clock,desired in [('America/New_York','2027-02-28','01:30','02:30'),
                                      ('Europe/Berlin','2027-03-21','01:30','02:30')]:
            fx=policies.fixture(zone=zone);r=fx['restaurants'][0]
            r.update(slot_minutes=30,reservation_duration_minutes=30,cancellation_cutoff_minutes=0,
                     opening_hours=[{'weekday':w,'opens':'00:00','closes':'06:00'} for w in retained.prior.WEEK])
            a,t=self.fresh(fx);s,*_=self.adopt(3,day,clock)
            first=s['occurrences'][0]['reservation'];gap_index=next(i for i,x in enumerate(s['occurrences'])
                if retained.prior.resolve(x['reservation']['starts_at_local'][:10]+'T'+desired,zone) is None)
            blocker=a.book(t,retained.prior.body(at=desired,day=day),'blocker')
            before=a.expect(200,'GET','/_test/export');request={'expected_revision':1,'from_index':0,'local_time':desired}
            a.expect(422,'POST','/series/'+s['series_id']+'/amend',request,t,'gap','invalid_local_time')
            check(a.expect(200,'GET','/_test/export')==before,'gap-before-occupancy failed rollback')
            a.expect(200,'POST','/reservations/'+blocker['reference']+'/cancel',token=t)
            a.expect(201,'POST','/series/'+s['series_id']+'/amend',{**request,'local_time':'04:00'},t,'gap')
        fx=policies.fixture(zone='America/New_York');r=fx['restaurants'][0]
        r.update(slot_minutes=30,reservation_duration_minutes=90,cancellation_cutoff_minutes=0,
                 opening_hours=[{'weekday':w,'opens':'00:00','closes':'06:00'} for w in retained.prior.WEEK])
        a,t=self.fresh(fx);s,*_=self.adopt(2,'2027-10-31','03:00')
        result=a.expect(201,'POST','/series/'+s['series_id']+'/amend',{'expected_revision':1,'from_index':0,'local_time':'01:30'},t,'fold')
        folded=result['occurrences'][1]['reservation']
        check(folded['starts_at']=='2027-11-07T01:30:00-04:00' and folded['ends_at']=='2027-11-07T02:00:00-05:00','fold first occurrence/absolute duration')
        a,t=self.fresh();s,*_=self.adopt(2)
        row=s['occurrences'][1]['reservation']; day=row['starts_at_local'][:10]
        close={'table_id':'z','from':day+'T20:00:00Z','to':day+'T21:30:00Z'}
        plan=a.expect(201,'POST','/restaurants/r/replans',close,t,'closure')
        a.expect(201,'POST','/restaurants/r/replans/'+plan['plan_id']+'/apply',{},t,'close')
        before=a.expect(200,'GET','/_test/export');request={'expected_revision':1,'from_index':0,'local_time':'20:00'}
        a.expect(409,'POST','/series/'+s['series_id']+'/amend',request,t,'closed-amend','table_unavailable')
        check(a.expect(200,'GET','/_test/export')==before,'closure failure mutated series or receipts')
        a.expect(201,'POST','/series/'+s['series_id']+'/amend',{**request,'local_time':'21:30'},t,'closed-amend')

    def optimizer_generated_metamorphic_and_maxima(self):
        rng=random.Random(44041)
        cases=[]
        for trial in range(20):
            ids=list('abcdef');rng.shuffle(ids)
            capacities={x:rng.choice((2,3,4,6)) for x in ids}
            pairs=rng.sample(list(__import__('itertools').combinations(ids,2)),4)
            books=[model.model_booking('R'+str(i).zfill(5),x,rng.randint(1,capacities[x]),capacities,0,90)
                   for i,x in enumerate(ids[:rng.randint(1,6)])]
            cases.append(dict(name='generated-'+str(trial),tables=tuple(ids),pairs=tuple(pairs),bookings=books,
                              prior_closures=(),proposed=model.Closure(ids[0],0,90)))
        # Summed-vector witness with deterministic seeded refs and equal retained duration.
        caps={'a':4,'b':6,'c':3,'d':4,'e':3,'f':2}
        witness=dict(name='sum-rank',tables=tuple(caps),pairs=(('b','e'),('a','e'),('b','f'),('c','d')),
             bookings=[model.model_booking('REF000','a',3,caps,0,100),
                       model.model_booking('REF001','c',3,caps,60,120),model.model_booking('REF002','b',5,caps,60,100)],
             prior_closures=(),proposed=model.Closure('b',0,90))
        # Native setup changes opaque reference order; create all order permutations by
        # independent fixed seeded90-minute witness already tests full-vector tie.
        for case in cases:
            self.assert_plan(self.prepare_witness(case),'generated')
        self.assert_plan(self.prepare_witness(witness),'sum-vector')
        # All six considered with ten ranked choices including four declared pairs.
        caps={x:4 for x in 'abcdef'}
        maximum=dict(name='maximum',tables=tuple(caps),pairs=(('a','b'),('c','d'),('e','f'),('a','f')),
             bookings=[model.model_booking('MAX00'+str(i),x,2,caps,0,90) for i,x in enumerate(caps)],
             prior_closures=(),proposed=model.Closure('a',0,90))
        self.assert_plan(self.prepare_witness(maximum),'maximum')

    def native_seven_receipts_transfer(self):
        a,t=self.fresh();s,body,anchor,adoption=self.adopt(3)
        receipts=[('/reservations',body,'anchor',anchor),('/series',adoption,'adopt',s)]
        policy=policies.policy(self.r,retained.DAY,reservation_duration_minutes=60)
        published=a.expect(201,'POST','/restaurants/r/policies',policy,t,'policy');receipts.append(('/restaurants/r/policies',policy,'policy',published))
        moves={'moves':[{'reference':s['occurrences'][1]['reference'],'party_size':3}]}
        batch=a.expect(201,'POST','/reservation-moves',moves,t,'batch');receipts.append(('/reservation-moves',moves,'batch',batch))
        current=a.expect(200,'GET','/series/'+s['series_id'],token=t)
        amend={'expected_revision':current['revision'],'from_index':0,'local_time':'20:00'}
        altered=a.expect(201,'POST','/series/'+s['series_id']+'/amend',amend,t,'amend');receipts.append(('/series/'+s['series_id']+'/amend',amend,'amend',altered))
        closed={'table_id':'z','from':retained.DAY+'T20:00:00Z','to':retained.DAY+'T21:30:00Z'}
        plan=a.expect(201,'POST','/restaurants/r/replans',closed,t,'preview');receipts.append(('/restaurants/r/replans',closed,'preview',plan))
        path='/restaurants/r/replans/'+plan['plan_id']+'/apply'; applied=a.expect(201,'POST',path,{},t,'apply');receipts.append((path,{},'apply',applied))
        a.expect(200,'POST','/reservations/'+s['occurrences'][2]['reference']+'/cancel',token=t)
        originals={x['reference']:(a.current(x['reference'],t),a.history(x['reference'],t)) for x in s['occurrences']}
        agreement=a.expect(200,'GET','/series/'+s['series_id'],token=t)
        snapshot=a.expect(200,'GET','/_test/export');self.pause('source')
        self.dest.reset(policies.fixture());obsolete=self.dest.login()
        destination_only=self.dest.expect(201,'POST','/restaurants/r/replans',
            {'table_id':'q','from':'2099-01-01T18:00:00Z','to':'2099-01-01T19:00:00Z'},obsolete,'destination-only')
        self.dest.expect(201,'POST','/restaurants/r/replans/'+destination_only['plan_id']+'/apply',{},obsolete,'destination-only-apply')
        self.dest.expect(204,'POST','/_test/import',snapshot)
        check(self.dest.expect(200,'GET','/_test/export')==snapshot,'replacement retained destination-only plan/closure/counter/receipt state')
        self.dest.expect(401,'GET','/reservations',token=obsolete,code='unauthenticated')
        self.dest.expect(404,'POST','/restaurants/r/replans/'+destination_only['plan_id']+'/apply',{},t,'removed-plan','not_found')
        for dest in (self.dest,self.third):
            if dest is self.third: dest.expect(204,'POST','/_test/import',self.dest.expect(200,'GET','/_test/export'));self.pause('destination')
            for ref,(row,history) in originals.items():
                check(dest.current(ref,t)==row and dest.history(ref,t)==history,'native transfer changed record/history')
            check(dest.expect(200,'GET','/series/'+s['series_id'],token=t)==agreement,'native transfer changed agreement')
            check(dest.login(),'hashed login transfer failed')
            for path,request,key,value in receipts: check(dest.expect(200,'POST',path,request,t,key)==value,'native original receipt changed')
            before=dest.expect(200,'GET','/_test/export')
            for invalid in [{'track':'other','format_version':1,'state':{}},{'track':'tablekeeper','format_version':2,'state':{}},{}]:
                dest.expect(422,'POST','/_test/import',invalid,code='validation_failed')
                check(dest.expect(200,'GET','/_test/export')==before,'invalid import mutated state')
            dest.expect(204,'POST','/_test/import',snapshot);dest.expect(204,'POST','/_test/import',snapshot)
            check(dest.current(anchor['reference'],t)==originals[anchor['reference']][0],'repeated import duplicate/change')
        self.third.reset(policies.fixture());self.third.expect(401,'GET','/reservations',token=t,code='unauthenticated')

    def direct_legacy_populated_transfers(self):
        for version,source in self.legacy.items():
            fx=policies.fixture(zone='UTC');source.reset(fx);t=source.login();other=source.login();bob=source.login('bob')
            body=retained.prior.body();first=source.expect(201,'POST','/reservations',body,t,'old-create')
            second_body=retained.prior.body(table='m',at='20:00');second=source.expect(201,'POST','/reservations',second_body,t,'second')
            moves={'moves':[{'reference':first['reference'],'party_size':3}]}
            batch=source.expect(201,'POST','/reservation-moves',moves,t,'old-batch')
            source.expect(200,'POST','/reservations/'+second['reference']+'/cancel',token=t)
            receipts=[('/reservations',body,'old-create',first),('/reservations',second_body,'second',second),('/reservation-moves',moves,'old-batch',batch)]
            series=None
            if version==3:
                policy=policies.policy(fx['restaurants'][0],retained.DAY,reservation_duration_minutes=60)
                published=source.expect(201,'POST','/restaurants/r/policies',policy,t,'old-policy');receipts.append(('/restaurants/r/policies',policy,'old-policy',published))
                adoption={'anchor_reference':first['reference'],'count':4,'interval_weeks':1}
                series=source.expect(201,'POST','/series',adoption,t,'old-series');receipts.append(('/series',adoption,'old-series',series))
                source.expect(200,'PATCH','/reservations/'+first['reference'],{'starts_at_local':'2080-06-07T18:30'},t)
                source.expect(200,'PATCH','/reservations/'+series['occurrences'][1]['reference'],{'table_id':'m'},t)
                source.expect(200,'POST','/reservations/'+series['occurrences'][2]['reference']+'/cancel',token=t)
            rows=source.expect(200,'GET','/reservations',token=t)['reservations']
            histories={r['reference']:source.expect(200,'GET','/reservations/'+r['reference']+'/history',token=t) for r in rows} if version==3 else {}
            snapshot=source.expect(200,'GET','/_test/export');self.pause('stage'+str(version))
            self.dest.reset(policies.fixture());obsolete=self.dest.login()
            self.dest.expect(204,'POST','/_test/import',snapshot)
            self.dest.expect(401,'GET','/reservations',token=obsolete,code='unauthenticated')
            for token in (t,other): self.dest.expect(200,'GET','/reservations',token=token)
            self.dest.login();self.dest.login('bob')
            for row in rows:
                current=self.dest.current(row['reference'],t)
                check(all(current[k]==v for k,v in row.items()),'legacy transfer changed known fields')
                if version==3: check(self.dest.expect(200,'GET','/reservations/'+row['reference']+'/history',token=t)==histories[row['reference']],'legacy history changed')
                self.dest.expect(404,'GET','/reservations/'+row['reference'],token=bob,code='not_found')
            for path,request,key,value in receipts: check(self.dest.expect(200,'POST',path,request,t,key)==value,'legacy receipt JSON changed')
            if series:
                current=self.dest.expect(200,'GET','/series/'+series['series_id'],token=t)
                request={'expected_revision':current['revision'],'from_index':0,'local_time':'20:00'}
                altered=self.dest.expect(201,'POST','/series/'+series['series_id']+'/amend',request,t,'after-import')
                final=altered['occurrences'][3]['reservation']
                check(final['starts_at_local']=='2080-06-27T20:00','legacy schedule used shifted anchor date')
            else:
                self.dest.expect(201,'POST','/series',{'anchor_reference':first['reference'],'count':2,'interval_weeks':1},t,'adopt-import')
            closure={'table_id':'z','from':retained.DAY+'T18:00:00Z','to':retained.DAY+'T19:30:00Z'}
            if version<3:
                self.dest.expect(403,'POST','/restaurants/r/replans',closure,t,'repair-import','forbidden')
            else:
                plan=self.dest.expect(201,'POST','/restaurants/r/replans',closure,t,'repair-import')
                self.dest.expect(201,'POST','/restaurants/r/replans/'+plan['plan_id']+'/apply',{},t,'apply-import')

    def atomic_apply_and_series_snapshots_50(self):
        a,t=self.fresh();s,*_=self.adopt(3)
        row=s['occurrences'][0]['reservation'];closure={'table_id':'z','from':row['starts_at'],'to':row['ends_at']}
        plan=a.expect(201,'POST','/restaurants/r/replans',closure,t,'plan');path='/restaurants/r/replans/'+plan['plan_id']+'/apply'
        before_series=a.expect(200,'GET','/series/'+s['series_id'],token=t);before=self.states(before_series)
        before_export=a.expect(200,'GET','/_test/export')
        workers=[lambda:a.request('POST',path,{},t,'apply') for _ in range(25)]+[lambda:a.request('GET','/_test/export') for _ in range(25)]
        responses=retained.coordinated(workers)
        check(sum(status==201 for status,v in responses[:25])==1 and all(status in (200,201) for status,v in responses[:25]),'apply snapshot writer results')
        applied=responses[0][1];after_series=a.expect(200,'GET','/series/'+s['series_id'],token=t);after=self.states(after_series)
        after_export=a.expect(200,'GET','/_test/export')
        for status,snapshot in responses[25:]:
            check(snapshot in (before_export,after_export),'apply snapshot whole private state/receipt/counter is not before or after')
            self.dest.expect(204,'POST','/_test/import',snapshot)
            observed=self.dest.expect(200,'GET','/series/'+s['series_id'],token=t)
            check(observed in (before_series,after_series),'snapshot partial series state')
            want=before if observed==before_series else after
            for ref,(row,events) in want.items(): check(self.dest.current(ref,t)==row and self.dest.history(ref,t)==events,'snapshot record/history not atomic')
            if observed==after_series: check(self.dest.expect(200,'POST',path,{},t,'apply')==applied,'snapshot receipt absent after application')
        request={'expected_revision':after_series['revision'],'from_index':0,'local_time':'20:00'}
        before=after;before_series=after_series
        before_export=after_export
        workers=[lambda:a.request('POST','/series/'+s['series_id']+'/amend',request,t,'amend') for _ in range(25)]+[lambda:a.request('GET','/_test/export') for _ in range(25)]
        responses=retained.coordinated(workers);after_series=a.expect(200,'GET','/series/'+s['series_id'],token=t);after=self.states(after_series)
        after_export=a.expect(200,'GET','/_test/export')
        check(sum(status==201 for status,v in responses[:25])==1 and all(status in (200,201) for status,v in responses[:25]),'amend snapshot writer results')
        for status,snapshot in responses[25:]:
            check(snapshot in (before_export,after_export),'amend snapshot whole private state/receipt/counter is not before or after')
            self.dest.expect(204,'POST','/_test/import',snapshot)
            observed=self.dest.expect(200,'GET','/series/'+s['series_id'],token=t);check(observed in (before_series,after_series),'snapshot partial amended series')
            want=before if observed==before_series else after
            for ref,(row,events) in want.items(): check(self.dest.current(ref,t)==row and self.dest.history(ref,t)==events,'snapshot amended record/history not atomic')

    def mixed_apply_create_amend_serial_outcomes_50(self):
        for kind in ('create','amend'):
            a,t=self.fresh();s,*_=self.adopt(2)
            row=s['occurrences'][0]['reservation'];close={'table_id':'z','from':row['starts_at'],'to':row['ends_at']}
            plan=a.expect(201,'POST','/restaurants/r/replans',close,t,'plan')
            apply_path='/restaurants/r/replans/'+plan['plan_id']+'/apply'
            if kind=='create':
                other_path='/reservations';other_body=retained.prior.body(table='z',at='18:00',party=1)
                # Existing z occupancy already conflicts, so choose a free member and
                # another time overlapping only the closure to discriminate both orders.
                other_body['starts_at_local']=retained.DAY+'T17:00'
                # Ordinary opening must include that candidate.
                fx=policies.fixture(zone='UTC');fx['restaurants'][0]['opening_hours']=[{'weekday':w,'opens':'16:00','closes':'23:00'} for w in retained.prior.WEEK]
                a,t=self.fresh(fx);s,*_=self.adopt(2);row=s['occurrences'][0]['reservation']
                close={'table_id':'z','from':retained.DAY+'T16:00:00Z','to':retained.DAY+'T19:30:00Z'}
                plan=a.expect(201,'POST','/restaurants/r/replans',close,t,'plan');apply_path='/restaurants/r/replans/'+plan['plan_id']+'/apply'
                other_body['starts_at_local']=retained.DAY+'T16:00'
                loser_code='table_unavailable'
            else:
                other_path='/series/'+s['series_id']+'/amend'
                other_body={'expected_revision':s['revision'],'from_index':0,'local_time':'20:00'}
                loser_code='stale_revision'
            before=a.expect(200,'GET','/series/'+s['series_id'],token=t)
            results=retained.coordinated([lambda:a.request('POST',apply_path,{},t,'apply') for _ in range(25)]+
                                         [lambda:a.request('POST',other_path,other_body,t,'other') for _ in range(25)])
            left,right=results[:25],results[25:]
            apply_wins=any(status==201 for status,v in left);other_wins=any(status==201 for status,v in right)
            check(apply_wins!=other_wins,'mixed operations have no permitted serial order')
            winner=left if apply_wins else right;loser=right if apply_wins else left
            check(sum(status==201 for status,v in winner)==1 and sum(status==200 for status,v in winner)==24,'mixed winner replay statuses')
            check(all(v==winner[0][1] for status,v in winner),'mixed winner receipt differs')
            code=loser_code if apply_wins else 'stale_plan'
            check(all(status==409 and v['error']['code']==code for status,v in loser),'mixed loser precedence')
            current=a.expect(200,'GET','/series/'+s['series_id'],token=t)
            if kind=='amend':
                check(current['revision']==before['revision']+1,'mixed agreement counter not once')
                for x in current['occurrences']:
                    old=before['occurrences'][x['index']]['reservation'];new=x['reservation']
                    if apply_wins:
                        check(new['starts_at_local']==old['starts_at_local'] and new['accepted_terms']==old['accepted_terms'],'apply changed time/terms')
                    else:check(new['starts_at_local'].endswith('T20:00'),'amend final state partial')
                    check(not x['exception'],'mixed operation marked exception')

    def closure_all_write_paths_and_snapshot_counters(self):
        fx=policies.fixture(zone='UTC');other=copy.deepcopy(fx['restaurants'][0]);other['id']='other'
        for table in other['tables']:table['id']='o_'+table['id']
        other['combinable']=[['o_'+x for x in pair] for pair in other['combinable']]
        fx['restaurants'].append(other)
        a,t=self.fresh(fx);s,*_=self.adopt(3);row=s['occurrences'][1]['reservation'];day=row['starts_at_local'][:10]
        close={'table_id':'a','from':day+'T20:00:00Z','to':day+'T21:30:00Z'}
        plan=a.expect(201,'POST','/restaurants/r/replans',close,t,'plan')
        a.expect(201,'POST','/restaurants/r/replans/'+plan['plan_id']+'/apply',{},t,'apply')
        reference=s['occurrences'][1]['reference'];before=a.expect(200,'GET','/_test/export')
        pair_body={'restaurant_id':'r','table_ids':['a','z'],'starts_at_local':day+'T20:00','party_size':6}
        a.book(t,pair_body,'pair-close',409,'table_unavailable')
        a.expect(409,'PATCH','/reservations/'+reference,{'table_ids':['a','z'],'starts_at_local':day+'T20:00','party_size':6},t,code='table_unavailable')
        a.expect(409,'POST','/reservation-moves',{'moves':[{'reference':reference,'table_id':'a','starts_at_local':day+'T20:00'}]},t,'batch-close','table_unavailable')
        check(a.expect(200,'GET','/_test/export')==before,'closure rejection changed state or claimed failure key')
        slots=a.expect(200,'GET','/availability?restaurant_id=r&date='+day+'&party_size=1&explain=true')['slots']
        slot=next(x for x in slots if x['starts_at_local'].endswith('T20:00'))
        check('a' not in slot['available_table_ids'] and all('a' not in x['table_ids'] for x in slot['available_options']),'closure option members')
        reason=next(x for x in slot['explain'] if x['table_id']=='a');check(reason['rules'][1]['holds'] is False,'closure explanation')
        # Fresh a anchor at the prior week's20:00 fits, but its generated member hits closure.
        anchor=a.book(t,retained.prior.body(table='a',at='20:00'),'closure-anchor')
        before=a.expect(200,'GET','/_test/export')
        a.expect(409,'POST','/series',{'anchor_reference':anchor['reference'],'count':2,'interval_weeks':1},t,'adopt-close','table_unavailable')
        check(a.expect(200,'GET','/_test/export')==before,'closure adoption partially committed')
        snapshot=a.expect(200,'GET','/_test/export');self.dest.expect(204,'POST','/_test/import',snapshot)
        check(self.dest.expect(200,'GET','/_test/export')==snapshot,'native export/import lost plans/closures/counters or receipts')
        self.dest.book(t,pair_body,'pair-close',409,'table_unavailable')
        # Cross-restaurant changes cannot stale an r plan.
        fresh=a.expect(201,'POST','/restaurants/r/replans',{'table_id':'z','from':'2098-01-01T18:00:00Z','to':'2098-01-01T19:00:00Z'},t,'local')
        other=self.fx['restaurants'][1]['id'];other_table=self.fx['restaurants'][1]['tables'][0]['id']
        a.book(t,retained.prior.body(table=other_table,restaurant=other),'other-r')
        a.expect(201,'POST','/restaurants/r/replans/'+fresh['plan_id']+'/apply',{},t,'local-apply')

    def maximum_distinct_planning_contention_50(self):
        fx=policies.fixture(zone='UTC');r=fx['restaurants'][0]
        r.update(slot_minutes=15,reservation_duration_minutes=45,cancellation_cutoff_minutes=0,
                 tables=[{'id':x,'label':'Table '+x.upper(),'capacity':4} for x in 'abcdef'],
                 combinable=[['a','b'],['c','d'],['e','f'],['a','f']])
        a,t=self.fresh(fx);books=[]
        for i in range(6):
            at=(dt.datetime(2080,6,6,18)+dt.timedelta(minutes=45*i)).strftime('%H:%M')
            row=a.book(t,retained.prior.body(table='b',at=at),'six-'+str(i))
            books.append(model.Booking(reference=row['reference'],members=tuple(row['table_ids']),party=row['party_size'],
                                       starts=model.instant(row['starts_at']),ends=model.instant(row['ends_at']),capacities=row['accepted_terms']['capacities']))
        close={'table_id':'b','from':retained.DAY+'T18:00:00Z','to':retained.DAY+'T22:30:00Z'}
        expected=model.solve(tables=tuple('abcdef'),pairs=tuple(tuple(p) for p in r['combinable']),bookings=books,prior_closures=(),
                             proposed=model.Closure('b',model.instant(close['from']),model.instant(close['to'])))
        before=a.expect(200,'GET','/_test/export');counter=self.counter()
        results=retained.coordinated([lambda i=i:a.request('POST','/restaurants/r/replans',close,t,'max-'+str(i)) for i in range(50)])
        check(all(status==201 and value['assignments']==expected['assignments'] and value['moved_count']==expected['moved_count']
                  and value['unused_seats']==expected['unused_seats'] for status,value in results),'maximum concurrent planning differs from complete oracle')
        check(len({v['plan_id'] for status,v in results})==50 and self.counter()==counter,'distinct previews identity/counter')
        for row in books:check(a.current(row.reference,t)['table_ids']==list(row.members),'maximum preview mutated booking')

    def operator_expired_cutoff_multiple_series_and_unmoved(self):
        fx=policies.fixture(zone='UTC');fx['reservations']=[{'id':'old','reference':'PAST01','restaurant_id':'r','user_id':'bob',
             'table_ids':['z'],'starts_at_local':'2000-06-06T18:00','party_size':2}]
        a,t=self.fresh(fx);owner=self.tokens['bob'];old=a.current('PAST01',owner);history=a.history('PAST01',owner)
        a.expect(409,'PATCH','/reservations/PAST01',{'table_id':'a'},owner,code='cutoff_passed')
        close={'table_id':'z','from':old['starts_at'],'to':old['ends_at']}
        plan=a.expect(201,'POST','/restaurants/r/replans',close,t,'past')
        a.expect(201,'POST','/restaurants/r/replans/'+plan['plan_id']+'/apply',{},t,'past-apply')
        current=a.current('PAST01',owner)
        a.expect(404,'GET','/reservations/PAST01',token=t,code='not_found')
        a.expect(404,'GET','/reservations/PAST01/history',token=t,code='not_found')
        check(current['table_ids']==['a'] and current['accepted_terms']==old['accepted_terms'] and current['starts_at']==old['starts_at'],'operator repair respected diner cutoff or changed retained terms')
        check(a.history('PAST01',owner)[-1]['event']=='reassigned','past repair event')
        a,t=self.fresh();s,*_=self.adopt(3)
        reference=s['occurrences'][1]['reference'];a.expect(200,'PATCH','/reservations/'+reference,{'party_size':3},t)
        a.expect(200,'POST','/reservations/'+s['occurrences'][2]['reference']+'/cancel',token=t)
        other_anchor=a.book(t,retained.prior.body(table='q',party=2),'other-anchor')
        other=a.expect(201,'POST','/series',{'anchor_reference':other_anchor['reference'],'count':2,'interval_weeks':1},t,'other-series')
        before=a.expect(200,'GET','/series/'+s['series_id'],token=t);other_before=a.expect(200,'GET','/series/'+other['series_id'],token=t)
        originals={x['reference']:(a.current(x['reference'],t),a.history(x['reference'],t)) for x in before['occurrences']+other_before['occurrences']}
        close={'table_id':'z','from':retained.DAY+'T18:00:00Z','to':'2080-06-13T19:30:00Z'}
        plan=a.expect(201,'POST','/restaurants/r/replans',close,t,'multi')
        result=a.expect(201,'POST','/restaurants/r/replans/'+plan['plan_id']+'/apply',{},t,'multi-apply')
        after=a.expect(200,'GET','/series/'+s['series_id'],token=t);other_after=a.expect(200,'GET','/series/'+other['series_id'],token=t)
        check(after['revision']==before['revision']+1 and other_after==other_before,'application series deltas per affected series')
        check([x['exception'] for x in after['occurrences']]==[x['exception'] for x in before['occurrences']],'repair changed permanent exceptions')
        check(len(result['reservations'])==4 and len(plan['assignments'])==4,'all considered including unmoved other agreement missing')
        for x in after['occurrences']:
            old,events=originals[x['reference']];new=x['reservation'];history=a.history(x['reference'],t)
            if x['index']<2:
                check(new['revision']==old['revision']+1 and history[:-1]==events and history[-1]['event']=='reassigned','multi-member repair history/revision')
                check(new['accepted_terms']==old['accepted_terms'] and new['starts_at_local']==old['starts_at_local'],'repair terms or scheduled date changed')
            else:check((new,history)==(old,events),'cancelled excluded member changed')

    def distinct_objective_witness_and_http_metamorphisms(self):
        caps={'a':4,'b':6,'c':3,'d':4,'e':3,'f':2};pairs=(('b','e'),('a','e'),('b','f'),('c','d'))
        fx=policies.fixture(zone='UTC');r=fx['restaurants'][0]
        r.update(slot_minutes=1,reservation_duration_minutes=90,cancellation_cutoff_minutes=0,
                 opening_hours=[{'weekday':w,'opens':'00:00','closes':'23:59'} for w in retained.prior.WEEK],
                 tables=[{'id':x,'label':x.upper(),'capacity':cap} for x,cap in caps.items()],combinable=[list(p) for p in pairs])
        a,t=self.fresh(fx);refs=[]
        for i in range(3):refs.append(a.book(t,retained.prior.body(table='a',day='2081-01-0'+str(i+1)),'far-'+str(i))['reference'])
        books=[]
        for i,(table,party,start,duration) in enumerate([('a',3,0,100),('c',3,60,60),('b',5,60,40)]):
            policy=policies.policy(r,'2080-06-01',reservation_duration_minutes=duration)
            a.expect(201,'POST','/restaurants/r/policies',policy,t,'duration-'+str(i))
            ref=sorted(refs)[i];row=a.expect(200,'PATCH','/reservations/'+ref,
                       {'table_id':table,'party_size':party,'starts_at_local':core.timestamp(start)[:16]},t)
            books.append(model.model_booking(ref,table,party,caps,start,start+duration))
        self.owners={ref:t for ref in refs}
        case=dict(name='summed-vector',tables=tuple(caps),pairs=pairs,bookings=books,prior_closures=(),proposed=model.Closure('b',0,90))
        expected=model.solve(**model.as_args(case));wrong=model.solve(**model.as_args(case),variant='sum-ranks')
        check(expected['ranks']==(0,4,9) and wrong['ranks']==(3,2,7),'HTTP fixture is not an objective-distinguishing witness')
        self.assert_plan(case,'distinguishing')
        original=model.witnesses()[0]
        for variant in ('renamed','shifted','reordered','cancelled'):
            c=copy.deepcopy(original)
            if variant=='renamed':
                rename={x:'table_'+str(i) for i,x in enumerate(c['tables'])}
                c['tables']=tuple(rename[x] for x in c['tables']);c['pairs']=tuple(tuple(rename[x] for x in p) for p in c['pairs'])
                c['bookings']=[model.replace(b,members=tuple(rename[x] for x in b.members),capacities={rename[k]:v for k,v in b.capacities.items()}) for b in c['bookings']]
                c['proposed']=model.replace(c['proposed'],table=rename[c['proposed'].table])
            elif variant=='shifted':
                c['bookings']=[model.replace(b,starts=b.starts+60,ends=b.ends+60) for b in c['bookings']]
                c['proposed']=model.replace(c['proposed'],starts=c['proposed'].starts+60,ends=c['proposed'].ends+60)
            elif variant=='reordered':c['tables']=tuple(reversed(c['tables']))
            else:c['bookings'].append(model.replace(c['bookings'][0],reference='CANCEL1',status='cancelled'))
            self.assert_plan(self.prepare_witness(c),'metamorphic')

    def full_path_user_typed_json_receipts_and_gross_bodies(self):
        fx=policies.fixture(zone='UTC');fx['restaurants'][0]['manager_user_ids']=['ada','bob'];a,t=self.fresh(fx)
        close={'table_id':'z','from':'2099-01-01T18:00:00Z','to':'2099-01-01T19:00:00Z','ignored':core.Decimal('1e309')}
        plan=a.expect(201,'POST','/restaurants/r/replans',close,t,'shared')
        bob_plan=a.expect(201,'POST','/restaurants/r/replans',{**close,'table_id':'a'},self.tokens['bob'],'shared')
        check(bob_plan['plan_id']!=plan['plan_id'],'manager user namespace interacted')
        path='/restaurants/r/replans/'+plan['plan_id']+'/apply'
        a.expect(400,'POST',path,{},t,code='missing_idempotency_key')
        a.expect(422,'POST',path,{},t,'x'*256,'validation_failed')
        for path_bad in ('/restaurants/r/replans',path,'/series/unknown/amend'):
            for raw in (b'[1]',b'{',b'{"ignored":NaN}'):
                a.expect(400,'POST',path_bad,token=t,key='gross',raw=raw,code='malformed_request')
        applied=a.expect(201,'POST',path,{'ignored':core.Decimal('1e-309')},t,'shared')
        body=retained.prior.body();created=a.book(t,body,'shared')
        moves={'moves':[{'reference':created['reference'],'party_size':3}]}
        batch=a.expect(201,'POST','/reservation-moves',moves,t,'shared')
        policy=policies.policy(self.r,retained.DAY);published=a.expect(201,'POST','/restaurants/r/policies',policy,t,'shared')
        adoption={'anchor_reference':created['reference'],'count':2,'interval_weeks':1}
        series=a.expect(201,'POST','/series',adoption,t,'shared')
        amend={'expected_revision':core.Decimal('1.0'),'from_index':core.Decimal('0e7'),'local_time':'20:00','ignored':core.Decimal('1e309')}
        amendment=a.expect(201,'POST','/series/'+series['series_id']+'/amend',amend,t,'shared')
        paths=[('/reservations',body,created),('/reservation-moves',moves,batch),('/restaurants/r/policies',policy,published),
               ('/series',adoption,series),('/restaurants/r/replans',{**close,'ignored':core.Decimal('10e308')},plan),
               (path,{'ignored':core.Decimal('10e-310')},applied),('/series/'+series['series_id']+'/amend',
                 {**amend,'expected_revision':1,'from_index':0,'ignored':core.Decimal('10e308')},amendment)]
        for endpoint,request,value in paths:
            check(a.expect(200,'POST',endpoint,request,t,'shared')==value,'shared key different full-path receipt mismatch')
            a.expect(409,'POST',endpoint,{**request,'ignored':False},t,'shared','idempotency_key_reuse')
        snapshot=a.expect(200,'GET','/_test/export');self.dest.expect(204,'POST','/_test/import',snapshot)
        for endpoint,request,value in paths:check(self.dest.expect(200,'POST',endpoint,request,t,'shared')==value,'typed huge/tiny snapshot receipt identity changed')

    def preview_inactive_wrong_restaurant_and_stale_rollback(self):
        fx=policies.fixture(zone='UTC');other=copy.deepcopy(fx['restaurants'][0]);other['id']='other'
        for table in other['tables']:table['id']='o_'+table['id']
        other['combinable']=[['o_'+x for x in pair] for pair in other['combinable']];fx['restaurants'].append(other)
        a,t=self.fresh(fx);close={'table_id':'z','from':retained.DAY+'T18:00:00Z','to':retained.DAY+'T19:30:00Z'}
        plan=a.expect(201,'POST','/restaurants/r/replans',close,t,'preview')
        a.expect(404,'POST','/restaurants/other/replans/'+plan['plan_id']+'/apply',{},t,'wrong','not_found')
        row=a.book(t,retained.prior.body(),'after-preview')
        check(row['table_id']=='z','preview prematurely activated closure')
        before=a.expect(200,'GET','/_test/export')
        a.expect(409,'POST','/restaurants/r/replans/'+plan['plan_id']+'/apply',{},t,'stale','stale_plan')
        check(a.expect(200,'GET','/_test/export')==before,'stale apply changed closure/record/history/counters/key')
        a.expect(200,'PATCH','/reservations/'+row['reference'],{},t)
        current=a.expect(201,'POST','/restaurants/r/replans',close,t,'new-preview')
        a.expect(200,'PATCH','/reservations/'+row['reference'],{},t)
        applied=a.expect(201,'POST','/restaurants/r/replans/'+current['plan_id']+'/apply',{},t,'stale')
        check(applied['restaurant_revision']==current['restaurant_revision']+1,'failed apply key not reusable / noop staled preview')


CASES=['series_original_dates_repaired_tables_exclusions','series_control_types_privacy_empty_and_failure_keys',
       'series_expired_noop_and_per_date_policy','series_dst_precedence_and_closure_rollback',
       'optimizer_generated_metamorphic_and_maxima','direct_legacy_populated_transfers',
       'atomic_apply_and_series_snapshots_50','native_seven_receipts_transfer']
CASES += ['mixed_apply_create_amend_serial_outcomes_50','closure_all_write_paths_and_snapshot_counters',
          'maximum_distinct_planning_contention_50','operator_expired_cutoff_multiple_series_and_unmoved',
          'distinct_objective_witness_and_http_metamorphisms','full_path_user_typed_json_receipts_and_gross_bodies']
CASES += ['preview_inactive_wrong_restaurant_and_stale_rollback']


def main():
    p=argparse.ArgumentParser();p.add_argument('--released',action='store_true')
    for name in ('revision','source','destination','third','stage1','stage2','stage3','control','out'): p.add_argument('--'+name,required=True)
    p.add_argument('--cases',nargs='+',choices=CASES);a=p.parse_args()
    if not a.released or not core.re.fullmatch('[0-9a-f]{40}',a.revision):p.error('exact released FULL revision required')
    c=Campaign(a.source,a.destination,a.third,a.stage1,a.stage2,a.stage3,a.control)
    report=c.run(a.cases or CASES);report['production_revision']=a.revision
    report['requests']=sum(len(api.timings) for api in [c.api,c.dest,c.third,*c.legacy.values()])
    Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['all_passed'] else 1)

if __name__=='__main__':main()

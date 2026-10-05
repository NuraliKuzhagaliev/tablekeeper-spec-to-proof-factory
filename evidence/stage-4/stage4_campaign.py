"""Independent Stage 4 HTTP core. Explicit exact release is required before requests.

Secrets, exports and response bodies stay in memory. This core is supplemented by
the cumulative/API/browser/upgrade protocols in verification.md before any verdict.
"""
import argparse
import copy
import datetime as dt
from decimal import Decimal
import json
from pathlib import Path
import re
import sys
import time

import seating_oracle as model

sys.path.insert(0,str(Path(__file__).resolve().parent/'cumulative_stage3'))
import stage3_campaign as retained
import policy_oracle as policies

check=retained.check
BASE=dt.datetime(2080,6,1,18,tzinfo=dt.timezone.utc)


def timestamp(minutes):
    return (BASE+dt.timedelta(minutes=int(minutes))).isoformat()


class Campaign:
    def __init__(self,source,destination=None):
        self.api=retained.API(source)
        self.dest=retained.API(destination) if destination else None
        self.results=[]; self.probes=0

    def fresh(self,fx=None):
        self.fx=fx or policies.fixture(zone='UTC')
        self.r=self.fx['restaurants'][0]
        self.api.reset(self.fx)
        self.tokens={'ada':self.api.login(),'bob':self.api.login('bob')}
        self.token=self.tokens['ada']; self.publications=[]
        return self.api,self.token

    def counter(self):
        self.probes+=1
        value=self.api.expect(201,'POST','/restaurants/r/replans',
            {'table_id':self.r['tables'][0]['id'],'from':'2099-01-01T18:00:00Z','to':'2099-01-01T19:00:00Z'},
            self.token,'counter-probe-'+str(self.probes))
        check(value['assignments']==[] and value['moved_count']==0 and value['unused_seats']==0,'empty preview effect')
        return value['restaurant_revision']

    def closure_body(self,c):
        return {'table_id':c.table,'from':timestamp(c.starts),'to':timestamp(c.ends)}

    def prepare_witness(self,case):
        caps=dict(case['bookings'][0].capacities) if case['bookings'] else {x:2 for x in case['tables']}
        fx=policies.fixture(zone='UTC'); r=fx['restaurants'][0]
        r.update(slot_minutes=1,reservation_duration_minutes=90,cancellation_cutoff_minutes=0,
          opening_hours=[{'weekday':w,'opens':'00:00','closes':'23:59'} for w in retained.prior.WEEK],
          tables=[{'id':x,'label':'Seating '+str(i+1),'capacity':caps[x]} for i,x in enumerate(case['tables'])],
          combinable=[list(p) for p in case['pairs']])
        native=any(b.ends-b.starts!=90 for b in case['bookings'])
        owners={}
        if not native:
            fx['reservations']=[{'id':'seed-'+b.reference,'reference':b.reference,'user_id':'ada' if i%2==0 else 'bob',
               'restaurant_id':'r','table_ids':list(b.members),'party_size':int(b.party),
               'starts_at_local':timestamp(b.starts)[:16],'status':b.status} for i,b in enumerate(case['bookings'])]
        self.fresh(fx)
        books=[]
        for i,b in enumerate(case['bookings']):
            owner='ada' if i%2==0 else 'bob'; token=self.tokens[owner]
            if native:
                policy=policies.policy(r,'2080-06-01',reservation_duration_minutes=int(b.ends-b.starts))
                self.api.expect(201,'POST','/restaurants/r/policies',policy,self.token,'duration-'+str(i))
                row=self.api.book(token,{'restaurant_id':'r','table_ids':list(b.members),'party_size':int(b.party),
                               'starts_at_local':timestamp(b.starts)[:16]},'witness-'+str(i))
                b=model.replace(b,reference=row['reference'])
            row=self.api.current(b.reference,token)
            check(model.instant(row['ends_at'])-model.instant(row['starts_at'])==(b.ends-b.starts)*60,'setup retained interval differs')
            check(row['accepted_terms']['capacities']==b.capacities,'setup own accepted capacity map differs')
            owners[b.reference]=token; books.append(b)
        self.owners=owners
        case={**case,'bookings':books}
        for i,c in enumerate(case['prior_closures']):
            prior_plan=self.api.expect(201,'POST','/restaurants/r/replans',self.closure_body(c),self.token,'prior-'+str(i))
            check(prior_plan['moved_count']==0,'prior-closure setup unexpectedly moved a booking')
            self.api.expect(201,'POST','/restaurants/r/replans/'+prior_plan['plan_id']+'/apply',{},self.token,'prior-apply-'+str(i))
        return case

    def records(self):
        return {ref:(self.api.current(ref,token),self.api.history(ref,token)) for ref,token in self.owners.items()}

    def assert_plan(self,case,key='preview'):
        expected=model.solve(**model.as_args(case)); before=self.records(); revision=self.counter()
        body=self.closure_body(case['proposed'])
        value=self.api.expect(409 if expected is None else 201,'POST','/restaurants/r/replans',body,self.token,key,
                              'no_feasible_plan' if expected is None else None)
        check(self.records()==before,'preview mutated reservation/history')
        check(self.counter()==revision,'preview mutated restaurant revision')
        if expected is not None:
            check(value['assignments']==expected['assignments'],'optimizer assignments/flags/order differ')
            check(value['moved_count']==expected['moved_count'] and value['unused_seats']==expected['unused_seats'],'optimizer objective differs')
            check(value['restaurant_revision']==revision,'preview captured wrong revision')
            check(model.instant(value['closure']['from'])==model.instant(body['from'])
                  and model.instant(value['closure']['to'])==model.instant(body['to']),'closure instant changed')
        return value,expected,before,body

    def optimizer_witnesses_preview_neutrality(self):
        for case in model.witnesses():
            case=self.prepare_witness(case)
            plan,expected,before,body=self.assert_plan(case)
            if expected is not None:
                check(self.api.expect(200,'POST','/restaurants/r/replans',body,self.token,'preview')==plan,'preview replay changed')
                self.api.expect(409,'POST','/restaurants/r/replans',{**body,'ignored':1},self.token,'preview','idempotency_key_reuse')
            else:
                ref=next(iter(self.owners))
                self.api.expect(200,'POST','/reservations/'+ref+'/cancel',token=self.owners[ref])
                retried=self.api.expect(201,'POST','/restaurants/r/replans',body,self.token,'preview')
                check(retried['assignments']==[],'failed preview key not reusable after cancellation')

    def preview_permissions_intervals_and_keys(self):
        a,token=self.fresh(); body={'table_id':'z','from':'2080-06-01T18:00:00+02:00','to':'2080-06-01T17:00:00Z'}
        a.expect(401,'POST','/restaurants/r/replans',body,key='anon',code='unauthenticated')
        a.expect(403,'POST','/restaurants/r/replans',body,self.tokens['bob'],'foreign','forbidden')
        a.expect(404,'POST','/restaurants/unknown/replans',body,token,'unknown','not_found')
        a.expect(404,'POST','/restaurants/r/replans',{**body,'table_id':'unknown'},token,'table','not_found')
        a.expect(400,'POST','/restaurants/r/replans',body,token,code='missing_idempotency_key')
        a.expect(422,'POST','/restaurants/r/replans',body,token,'x'*256,'validation_failed')
        invalid=[{k:v for k,v in body.items() if k!=field} for field in body]
        invalid += [{**body,'from':v} for v in ['2080-06-01T18:00:00','2080-02-30T18:00:00Z','no-date']]
        invalid += [{**body,'from':'2080-06-01T18:00:00Z','to':'2080-06-01T18:00:00Z'},
                    {**body,'from':'2080-06-01T18:00:00Z','to':'2080-06-01T17:59:59Z'}]
        for i,value in enumerate(invalid): a.expect(422,'POST','/restaurants/r/replans',value,token,'bad-'+str(i),'validation_failed')
        for field in body:
            a.expect(400,'POST','/restaurants/r/replans',{**body,field:True},token,'type-'+field,'malformed_request')
        plan=a.expect(201,'POST','/restaurants/r/replans',body,token,'v'*255)
        check(plan['assignments']==[],'offset order treated lexically')
        check(a.expect(200,'POST','/restaurants/r/replans',dict(reversed(list(body.items()))),token,'v'*255)==plan,'parsed object equality')
        a.expect(409,'POST','/restaurants/r/replans',{'invalid':True},token,'v'*255,'idempotency_key_reuse')
        tiny={'table_id':'z','from':'2080-06-01T18:00:00.000000001Z','to':'2080-06-01T18:00:00.000000002Z'}
        exact_plan=a.expect(201,'POST','/restaurants/r/replans',tiny,token,'tiny')
        check(model.instant(exact_plan['closure']['from'])==model.instant(tiny['from'])
              and model.instant(exact_plan['closure']['to'])==model.instant(tiny['to']),'fractional interval truncated')

    def assert_application(self,plan,expected,before,response):
        check(response['plan_id']==plan['plan_id'] and response['restaurant_revision']==plan['restaurant_revision']+1,'whole apply counter')
        check([r['reference'] for r in response['reservations']]==[x['reference'] for x in expected['assignments']],'apply considered order')
        current=self.records()
        for assignment in expected['assignments']:
            ref=assignment['reference']; old,history=before[ref]; new,events=current[ref]
            for field in ('reservation_id','reference','restaurant_id','party_size','status','starts_at','ends_at','starts_at_local','created_at','accepted_terms'):
                check(new[field]==old[field],'operator repair changed retained field '+field)
            check(new['table_ids']==assignment['table_ids'],'applied assignment differs')
            if assignment['changed']:
                check(new['revision']==old['revision']+1 and len(events)==len(history)+1,'moved booking revision/history delta')
                check(events[:-1]==history and events[-1]['event']=='reassigned' and events[-1]['plan_id']==plan['plan_id'],'reassigned provenance')
                check(events[-1]['changes']==[{'field':'table_ids','from':old['table_ids'],'to':new['table_ids']}],'reassigned full set delta')
                check(events[-1]['accepted_terms']==old['accepted_terms'],'repair changed event terms')
            else: check((new,events)==(old,history),'unmoved booking changed')
        for ref in set(before)-{x['reference'] for x in expected['assignments']}:
            check(current[ref]==before[ref],'fixed booking changed')

    def apply_retained_history_closure_and_receipts(self):
        case=self.prepare_witness(model.witnesses()[0]); a=self.api
        plan,expected,before,body=self.assert_plan(case)
        path='/restaurants/r/replans/'+plan['plan_id']+'/apply'
        a.expect(401,'POST',path,{},key='anon',code='unauthenticated')
        a.expect(403,'POST',path,{},self.tokens['bob'],'foreign','forbidden')
        a.expect(404,'POST','/restaurants/r/replans/unknown/apply',{},self.token,'unknown','not_found')
        response=a.expect(201,'POST',path,{},self.token,'apply')
        self.assert_application(plan,expected,before,response)
        check(self.counter()==plan['restaurant_revision']+1,'apply counter more than once')
        check(a.expect(200,'POST',path,{},self.token,'apply')==response,'apply replay changed')
        a.expect(409,'POST',path,{},self.token,'different','plan_already_applied')
        a.expect(409,'POST',path,{'ignored':Decimal('1e309')},self.token,'apply','idempotency_key_reuse')
        check(a.expect(200,'POST','/restaurants/r/replans',body,self.token,'preview')==plan,'preview rewritten after apply')
        slots=a.slots('2080-06-01',1)
        row=next(s for s in slots if s['starts_at_local']=='2080-06-01T18:00')
        check('b' not in row['available_table_ids'] and all('b' not in x['table_ids'] for x in row['available_options']),'closure availability ignored')
        a.book(self.token,{'restaurant_id':'r','table_id':'b','party_size':1,'starts_at_local':'2080-06-01T18:00'},'closed',409,'table_unavailable')
        explained=a.expect(200,'GET','/availability?restaurant_id=r&date=2080-06-01&party_size=1&explain=true')['slots']
        reason=next(x for x in next(s for s in explained if s['starts_at_local']=='2080-06-01T18:00')['explain'] if x['table_id']=='b')
        check(reason['rules'][1]=={'rule':'no_overlap','holds':False},'closure explanation truth')
        ref=expected['assignments'][0]['reference']
        a.expect(200,'POST','/reservations/'+ref+'/cancel',token=self.owners[ref])
        check(a.expect(200,'POST',path,{},self.token,'apply')==response,'historical apply receipt changed after cancel')

    def local_staleness_and_zero_movement(self):
        a,t=self.fresh(); check(self.counter()==0,'reset revision not zero')
        body={'table_id':'z','from':'2080-06-01T18:00:00Z','to':'2080-06-01T19:00:00Z'}
        first=a.expect(201,'POST','/restaurants/r/replans',body,t,'first')
        second=a.expect(201,'POST','/restaurants/r/replans',body,t,'second')
        response=a.expect(201,'POST','/restaurants/r/replans/'+first['plan_id']+'/apply',{},t,'first-apply')
        check(response['reservations']==[] and response['restaurant_revision']==1,'zero-move apply failed to record closure once')
        a.expect(409,'POST','/restaurants/r/replans/'+second['plan_id']+'/apply',{},t,'second-apply','stale_plan')
        a.expect(409,'POST','/restaurants/r/replans/'+first['plan_id']+'/apply',{},t,'again','plan_already_applied')
        check(self.counter()==1,'failed apply changed counter')
        a.book(t,{'restaurant_id':'r','table_id':'z','party_size':1,'starts_at_local':'2080-06-01T18:00'},'blocked',409,'table_unavailable')
        a.book(t,{'restaurant_id':'r','table_id':'z','party_size':1,'starts_at_local':'2080-06-01T19:00'},'adjacent')
        check(self.counter()==2,'new booking not counted')

    def restaurant_counter_transitions(self):
        a,t=self.fresh(); check(self.counter()==0,'initial counter')
        first=a.book(t); ref=first['reference']; check(self.counter()==1,'create counter')
        a.expect(200,'PATCH','/reservations/'+ref,{},t); check(self.counter()==1,'noop counter')
        a.expect(200,'PATCH','/reservations/'+ref,{'party_size':3},t); check(self.counter()==2,'real PATCH counter')
        a.expect(201,'POST','/restaurants/r/policies',policies.policy(self.r,retained.DAY),t,'policy'); check(self.counter()==3,'publication counter')
        a.expect(200,'POST','/reservations/'+ref+'/cancel',token=t); check(self.counter()==4,'cancel counter')
        a.expect(200,'POST','/reservations/'+ref+'/cancel',token=t); check(self.counter()==4,'repeat cancel counter')
        anchor=a.book(t,key='anchor'); check(self.counter()==5,'second create counter')
        series=a.expect(201,'POST','/series',{'anchor_reference':anchor['reference'],'count':2,'interval_weeks':1},t,'series')
        check(self.counter()==6,'whole adoption counter')
        path='/series/'+series['series_id']+'/amend'; request={'expected_revision':series['revision'],'from_index':0,'local_time':'20:00'}
        changed=a.expect(201,'POST',path,request,t,'change'); check(self.counter()==7,'whole series amend counter')
        noop=a.expect(201,'POST',path,{**request,'expected_revision':changed['revision']},t,'noop')
        check(noop==changed and self.counter()==7,'series noop counter/record')
        moves={'moves':[{'reference':x['reference'],'table_id':'m'} for x in changed['occurrences']]}
        batch=a.expect(201,'POST','/reservation-moves',moves,t,'batch'); check(self.counter()==8,'whole real batch counter')
        a.expect(201,'POST','/reservation-moves',{'moves':[{'reference':x['reference']} for x in changed['occurrences']]},t,'noop-batch')
        check(self.counter()==8,'whole noop batch counter')
        check(a.expect(200,'POST','/reservation-moves',moves,t,'batch')==batch and self.counter()==8,'batch replay counter')

    def preview_apply_retry_contention_50(self):
        case=self.prepare_witness(model.witnesses()[0]); a=self.api
        body=self.closure_body(case['proposed']); before=self.records(); revision=self.counter()
        responses=retained.coordinated([lambda:a.request('POST','/restaurants/r/replans',body,self.token,'same-preview') for _ in range(50)])
        check(sum(s==201 for s,v in responses)==1 and sum(s==200 for s,v in responses)==49,'50 preview retry statuses')
        plan=responses[0][1]; check(all(v==plan for s,v in responses),'50 preview bodies differ')
        expected=model.solve(**model.as_args(case)); check(plan['assignments']==expected['assignments'],'concurrent preview optimum')
        check(self.records()==before and self.counter()==revision,'concurrent previews mutated state')
        path='/restaurants/r/replans/'+plan['plan_id']+'/apply'
        applied=retained.coordinated([lambda:a.request('POST',path,{},self.token,'same-apply') for _ in range(50)])
        check(sum(s==201 for s,v in applied)==1 and sum(s==200 for s,v in applied)==49,'50 apply retry statuses')
        check(all(v==applied[0][1] for s,v in applied),'50 apply bodies differ')
        self.assert_application(plan,expected,before,applied[0][1])
        check(self.counter()==revision+1,'50 apply effects more than once')

    def series_cas_contention_50(self):
        a,t=self.fresh(); anchor=a.book(t)
        adopted=a.expect(201,'POST','/series',{'anchor_reference':anchor['reference'],'count':4,'interval_weeks':1},t,'adopt')
        path='/series/'+adopted['series_id']+'/amend'; before_counter=self.counter()
        bodies=[{'expected_revision':adopted['revision'],'from_index':0,'local_time':['18:30','19:00','19:30','20:00','20:30'][i%5]} for i in range(50)]
        results=retained.coordinated([lambda i=i:a.request('POST',path,bodies[i],t,'cas-'+str(i)) for i in range(50)])
        winners=[i for i,(s,v) in enumerate(results) if s==201]
        check(len(winners)==1,'same expected revision changed more than once')
        check(all(s==409 and v['error']['code']=='stale_revision' for i,(s,v) in enumerate(results) if i not in winners),'CAS loser code')
        check(self.counter()==before_counter+1,'CAS restaurant count')
        current=a.expect(200,'GET','/series/'+adopted['series_id'],token=t)
        check(current['revision']==adopted['revision']+1 and all(not x['exception'] for x in current['occurrences']),'CAS series flags/revision')
        i=winners[0]; check(a.expect(200,'POST',path,bodies[i],t,'cas-'+str(i))==results[i][1],'CAS historical replay')
        loser=next(i for i in range(50) if i not in winners)
        replacement={**bodies[loser],'expected_revision':current['revision'],'local_time':'21:00'}
        a.expect(201,'POST',path,replacement,t,'cas-'+str(loser))

    def run(self,names):
        for name in names or CASES:
            began=time.monotonic()
            try:
                getattr(self,name)(); row={'case':name,'status':'PASS'}
            except AssertionError as exc:
                row={'case':name,'status':'FAIL','classification':'INCONCLUSIVE','detail':str(exc)}
            except (OSError,TimeoutError) as exc:
                row={'case':name,'status':'ERROR','classification':'INCONCLUSIVE','detail':type(exc).__name__}
            except Exception as exc:
                row={'case':name,'status':'ERROR','classification':'VERIFIER DEFECT','detail':type(exc).__name__}
            row['seconds']=round(time.monotonic()-began,3); self.results.append(row); print(json.dumps(row),flush=True)
        timings=self.api.timings+(self.dest.timings if self.dest else [])
        return {'scope':'Stage4 executable core checkpoint; cumulative protocols and formal verdict still required',
             'cases':self.results,'all_passed':all(r['status']=='PASS' for r in self.results),'requests':len(timings),
             'max_regular_seconds':max((v for p,v in timings if not p.startswith('/_test/')),default=0),
             'max_control_seconds':max((v for p,v in timings if p.startswith('/_test/')),default=0)}


CASES=['optimizer_witnesses_preview_neutrality','preview_permissions_intervals_and_keys',
       'apply_retained_history_closure_and_receipts','local_staleness_and_zero_movement',
       'restaurant_counter_transitions','preview_apply_retry_contention_50','series_cas_contention_50']


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['calibrate','http']); parser.add_argument('--released',action='store_true')
    for option in ('revision','source','destination','out'): parser.add_argument('--'+option)
    parser.add_argument('--cases',nargs='+',choices=CASES); args=parser.parse_args()
    if args.mode=='calibrate': print(json.dumps(model.calibrate())); return
    if not args.released or not re.fullmatch('[0-9a-f]{40}',args.revision or ''):
        parser.error('Conductor exact FULL Stage4 production SHA release required before candidate requests')
    if not args.source: parser.error('controlled candidate source required')
    report=Campaign(args.source,args.destination).run(args.cases); report['production_revision']=args.revision
    if args.out: Path(args.out).write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if report['all_passed'] else 1)


if __name__=='__main__': main()

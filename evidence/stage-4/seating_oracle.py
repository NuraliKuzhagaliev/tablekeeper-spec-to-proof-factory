"""Independent finite Stage 4 reference model; no production imports or decisions."""
from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal
from fractions import Fraction
from itertools import product
import copy
import re


def exact(value):
    if isinstance(value, bool):
        raise ValueError('boolean is not a JSON number')
    return Fraction(Decimal(value)) if isinstance(value, str) else Fraction(value)


def instant(value):
    """Exact RFC3339 instant, including submicrosecond fractions and year boundaries."""
    match = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d+)?(Z|[+-]\d{2}:\d{2})', value)
    if not match:
        raise ValueError('explicit-offset RFC3339 required')
    y, m, d, h, minute, sec = map(int, match.groups()[:6])
    if h > 23 or minute > 59 or sec > 59:
        raise ValueError('invalid clock')
    fraction = exact(match[7] or '0')
    offset = match[8]
    displacement = 0
    if offset != 'Z':
        oh, om = int(offset[1:3]), int(offset[4:6])
        if oh > 23 or om > 59:
            raise ValueError('invalid offset')
        displacement = (1 if offset[0] == '+' else -1) * (oh * 3600 + om * 60)
    return Fraction((date(y, m, d).toordinal() - date(1970, 1, 1).toordinal()) * 86400
                    + h * 3600 + minute * 60 + sec - displacement) + fraction


def overlap(a, b, c, d):
    return a < d and c < b


@dataclass(frozen=True)
class Booking:
    reference: str
    members: tuple
    party: Fraction
    starts: Fraction
    ends: Fraction
    capacities: dict
    status: str = 'confirmed'


@dataclass(frozen=True)
class Closure:
    table: str
    starts: Fraction
    ends: Fraction


def options(tables, pairs):
    """Global ranks retain fixture/declaration order even when individual options fail."""
    return tuple((rank, tuple(ids)) for rank, ids in enumerate([(x,) for x in tables] + list(pairs)))


def conflicts(left, left_members, right, right_members):
    return bool(set(left_members) & set(right_members)) and overlap(left.starts, left.ends, right.starts, right.ends)


def enumerate_plans(tables, pairs, bookings, prior_closures, proposed, variant=None, current_capacities=None):
    """Complete Cartesian enumeration. Inputs are one restaurant's independently observed state.

    Mandatory maximum is 10^6 candidate vectors. Offline model deliberately favors
    completeness over a production solver's pruning/search structure.
    """
    confirmed = [b for b in bookings if b.status == 'confirmed']
    considered = sorted((b for b in confirmed if overlap(b.starts, b.ends, proposed.starts, proposed.ends)), key=lambda b:b.reference)
    if variant == 'closed-table-only':
        considered = [b for b in considered if proposed.table in b.members]
    references = {b.reference for b in considered}
    fixed = [b for b in confirmed if b.reference not in references]
    ranked = options(tables, pairs)
    choices = []
    for booking in considered:
        admissible = []
        capacities = current_capacities if variant == 'current-capacities' else booking.capacities
        for rank, members in ranked:
            capacity = sum((exact(capacities[x]) for x in members), Fraction())
            if capacity < booking.party:
                continue
            interval = booking
            if variant == 'clip-to-proposal':
                interval = replace(booking, starts=max(booking.starts, proposed.starts), ends=min(booking.ends, proposed.ends))
            blocked = False
            for closure in [*prior_closures, proposed]:
                if closure.table not in members:
                    continue
                intersects = (interval.starts <= closure.ends and closure.starts <= interval.ends) if variant == 'closed-intervals' else overlap(interval.starts, interval.ends, closure.starts, closure.ends)
                if intersects:
                    blocked = True
            if blocked or any(conflicts(interval, members, other, other.members) for other in fixed):
                continue
            changed = members != booking.members if variant == 'array-identity' else set(members) != set(booking.members)
            admissible.append((rank, members, int(changed), capacity - booking.party))
        choices.append(admissible)
    for vector in product(*choices):
        if any(conflicts(considered[i], vector[i][1], considered[j], vector[j][1])
               for i in range(len(vector)) for j in range(i)):
            continue
        changes = sum(x[2] for x in vector)
        waste = sum((x[3] for x in vector), Fraction())
        ranks = tuple(x[0] for x in vector)
        score = (changes, waste, ranks)
        if variant == 'waste-first': score = (waste, changes, ranks)
        elif variant == 'sum-ranks': score = (changes, waste, sum(ranks), ranks)
        elif variant == 'weighted': score = (changes + waste, ranks)
        elif variant == 'greedy-ranks': score = ranks
        yield (score, {'assignments': [{'reference': b.reference, 'table_ids': list(v[1]), 'changed': bool(v[2])}
                            for b, v in zip(considered, vector)], 'moved_count': changes, 'unused_seats': waste,
                            'ranks': ranks, 'considered_count': len(considered)})


def solve(*args, **kwargs):
    best = min(enumerate_plans(*args, **kwargs), key=lambda x:x[0], default=None)
    return best[1] if best else None


def model_booking(reference, member, party, capacities, start=0, end=90, status='confirmed'):
    members = (member,) if isinstance(member, str) else tuple(member)
    return Booking(reference, members, exact(party), exact(start), exact(end), dict(capacities), status)


def witnesses():
    def case(name, capacities, specs, closed='b', pairs=(), prior=(), window=(0,90)):
        books=[model_booking(*spec, capacities) for spec in specs]
        return {'name': name, 'tables': tuple(capacities), 'pairs': tuple(pairs), 'bookings': books,
                'prior_closures': tuple(prior), 'proposed': Closure(closed, exact(window[0]), exact(window[1]))}
    cases = [
        case('changes-before-waste', {'a':4,'b':4,'c':2,'d':8}, [('AA0001','a',2),('BB0001','b',4)]),
        case('waste-before-rank', {'a':4,'b':4,'d':6,'c':4}, [('AA0001','a',2),('BB0001','b',4)]),
        case('reference-vector', {'a':4,'c':4,'b':4,'d':2}, [('AA0001','a',2),('BB0001','b',4),('CC0001','c',2)]),
        case('declared-pair-order', {'b':2,'a':2,'c':2}, [('AA0001',('a','b'),4)], closed='c', pairs=(('b','a'),('b','c'))),
        case('infeasible', {'a':2}, [('AA0001','a',2)], closed='a'),
        case('zero-considered', {'a':2,'b':2}, [], closed='b'),
        case('exact-large-capacity', {'a':10**309,'b':2,'c':1}, [('AA0001','b',2)], pairs=(('a','c'),)),
    ]
    caps={'b':4,'a':4,'c':4}
    full = {'name':'retained-full-interval', 'tables':tuple(caps),'pairs':(),
      'bookings':[model_booking('AA0001','b',4,caps,-30,90), model_booking('BB0001','a',4,caps,-40,0)],
      'prior_closures':(), 'proposed':Closure('b',exact(0),exact(60))}
    cases.append(full)
    cases.append({**full,'name':'prior-closure-outside-proposal', 'bookings':full['bookings'][:1],
                  'prior_closures':(Closure('a',exact(-30),exact(0)),)})
    cases.append(case('half-open-adjacency', {'a':2,'b':2}, [('AA0001','a',2)], closed='a', window=(90,100)))
    own = case('own-accepted-capacities', {'b':4,'a':2,'c':4}, [('AA0001','b',4)])
    cases.append(own)
    return cases


def as_args(case):
    return {k:case[k] for k in ('tables','pairs','bookings','prior_closures','proposed')}


def series_targets(series, scheduled_dates, expected_revision, from_index, local_time):
    """Independent eligibility/original-date/CAS model; semantic no-ops bypass old cutoff.

    Dates are retained independent known metadata, never inferred from a current anchor.
    Returned real candidates then need index-ordered accepted-cutoff/policy validation
    and a collective final occupancy check in the HTTP campaign.
    """
    def integer(value, low, high):
        if isinstance(value, (bool,str,dict,list)):
            return False
        try: number=exact(value)
        except (ValueError,TypeError,OverflowError): return False
        return number.denominator==1 and low<=number and (high is None or number<=high)
    occurrences=series['occurrences']
    if not integer(expected_revision,1,None) or not integer(from_index,0,len(occurrences)-1):
        return 'validation_failed', []
    if not isinstance(local_time,str) or not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d',local_time):
        return 'validation_failed', []
    if expected_revision != series['revision']:
        return 'stale_revision', []
    result=[]
    for occurrence in sorted(occurrences,key=lambda x:x['index']):
        index=occurrence['index']; old=occurrence['reservation']
        if index < from_index or occurrence['exception'] or old['status']=='cancelled':
            continue
        local=scheduled_dates[index]+'T'+local_time
        result.append({'index':index, 'reference':occurrence['reference'], 'starts_at_local':local,
            'table_ids':copy.deepcopy(old.get('table_ids',[old.get('table_id')])), 'party_size':old['party_size'],
            'changed':local != old['starts_at_local']})
    return None,result


def application_deltas(assignments, memberships):
    changed={a['reference'] for a in assignments if a['changed']}
    return {'restaurant':1, 'reservations':{ref:1 for ref in changed},
            'series':{sid:1 for ref,sid in memberships.items() if ref in changed}}


def amend_deltas(targets):
    changed={x['reference'] for x in targets if x['changed']}
    return {'restaurant':int(bool(changed)), 'series':int(bool(changed)),
            'reservations':{ref:1 for ref in changed}}


def series_transition(restaurant, publications, series, scheduled_dates, expected_revision,
                      from_index, local_time, now, fixed_bookings=(), closures=()):
    """Pure complete-result model using only the earlier independent verifier model.

    Real candidates validate in occurrence-index order before any final occupancy.
    Series no-ops deliberately do not call ordinary PATCH's editable-no-op cutoff.
    """
    from pathlib import Path
    import sys
    sys.path.insert(0,str(Path(__file__).resolve().parent/'cumulative_stage3'))
    import policy_oracle as policies
    error,targets=series_targets(series,scheduled_dates,expected_revision,from_index,local_time)
    if error: return error,copy.deepcopy(series),{}
    after=copy.deepcopy(series); by_index={x['index']:x for x in after['occurrences']}; deltas={}
    for target in targets:
        if not target['changed']: continue
        old=by_index[target['index']]['reservation']
        # The frozen reference uses absolute ordinal seconds; this model uses Unix epoch.
        ordinal_now=now+date(1970,1,1).toordinal()*86400
        error,candidate,changes=policies.amend(restaurant,publications,old,
                                            {'starts_at_local':target['starts_at_local']},ordinal_now)
        if error: return error,copy.deepcopy(series),{}
        by_index[target['index']]['reservation']=candidate
        deltas[target['reference']]=changes
    rows=[x['reservation'] for x in after['occurrences']]+list(fixed_bookings)
    active=[r for r in rows if r['status']=='confirmed']
    for i,row in enumerate(active):
        start,end=instant(row['starts_at']),instant(row['ends_at'])
        members=row.get('table_ids',[row.get('table_id')])
        if any(c.table in members and overlap(start,end,c.starts,c.ends) for c in closures):
            return 'table_unavailable',copy.deepcopy(series),{}
        for other in active[:i]:
            if set(members)&set(other.get('table_ids',[other.get('table_id')])) and overlap(start,end,instant(other['starts_at']),instant(other['ends_at'])):
                return 'table_unavailable',copy.deepcopy(series),{}
    after['revision']+=int(bool(deltas))
    return None,after,deltas


def apply_control(receipt, body_same, applied, captured, current):
    if receipt: return 'replay' if body_same else 'idempotency_key_reuse'
    if applied: return 'plan_already_applied'
    if captured != current: return 'stale_plan'
    return 'apply'


def calibrate():
    cases=witnesses(); observed={c['name']:solve(**as_args(c)) for c in cases}
    assert observed['changes-before-waste']['moved_count']==1 and observed['changes-before-waste']['unused_seats']==6
    assert observed['waste-before-rank']['assignments'][1]['table_ids']==['c']
    assert observed['reference-vector']['ranks']==(0,1,3)
    assert observed['reference-vector']['moved_count']==2 and observed['reference-vector']['unused_seats']==2
    assert observed['declared-pair-order']['assignments'][0]=={'reference':'AA0001','table_ids':['b','a'],'changed':False}
    assert observed['retained-full-interval']['assignments'][0]['table_ids']==['c']
    assert observed['prior-closure-outside-proposal']['assignments'][0]['table_ids']==['c']
    assert observed['infeasible'] is None and observed['zero-considered']['assignments']==[]
    wrong=[]
    controls=[('changes-before-waste','waste-first'),('changes-before-waste','weighted'),
              ('waste-before-rank','greedy-ranks'),
              ('changes-before-waste','closed-table-only'),('declared-pair-order','array-identity'),
              ('retained-full-interval','clip-to-proposal'),('prior-closure-outside-proposal','clip-to-proposal')]
    for name,variant in controls:
        c=next(x for x in cases if x['name']==name)
        assert solve(**as_args(c),variant=variant) != observed[name], 'VERIFIER COVERAGE GAP: '+variant
        wrong.append(name+':'+variant)
    own=next(c for c in cases if c['name']=='own-accepted-capacities')
    assert solve(**as_args(own),variant='current-capacities',current_capacities={'b':4,'a':4,'c':2}) != observed[own['name']]
    wrong.append('current-capacities')
    # Find a distinct summed-rank witness independently, with bounded seeded models.
    import random
    randomizer=random.Random(4404)
    sum_witness=None
    for trial in range(1500):
        capacities={x:randomizer.choice((2,3,4,6)) for x in 'abcdef'}
        pairs=randomizer.sample(list(__import__('itertools').combinations(capacities,2)),4)
        books=[model_booking('REF00'+str(i),x,randomizer.randint(1,capacities[x]),capacities,
                    randomizer.choice((0,30,60)),randomizer.choice((100,120,150)))
               for i,x in enumerate(randomizer.sample(list(capacities),3))]
        args=dict(tables=tuple(capacities),pairs=tuple(pairs),bookings=books,prior_closures=(),proposed=Closure('b',0,90))
        optimum=solve(**args); summed=solve(**args,variant='sum-ranks')
        if optimum is not None and summed != optimum:
            sum_witness={'trial':trial,'tables':capacities,'pairs':pairs,
                'books':[(b.reference,b.members,int(b.party),int(b.starts),int(b.ends)) for b in books],
                'expected_ranks':optimum['ranks'],'wrong_ranks':summed['ranks']}
            break
    assert sum_witness is not None,'VERIFIER COVERAGE GAP: sum-ranks'
    wrong.append('sum-ranks')
    assert instant('2026-09-28T18:00:00+02:00')==instant('2026-09-28T16:00:00Z')
    boundary=instant('2026-09-28T16:00:00.000000001Z')
    assert boundary-instant('2026-09-28T16:00:00Z')==Fraction(1,10**9)
    assert not overlap(0,1,1,2) and overlap(0,1,1-Fraction(1,10**9),2)
    assert apply_control(True,True,True,0,3)=='replay'
    assert apply_control(True,False,True,0,3)=='idempotency_key_reuse'
    assert apply_control(False,False,True,0,3)=='plan_already_applied'
    assert application_deltas([], {})=={'restaurant':1,'reservations':{},'series':{}}
    return {'status':'PASS','witnesses':len(cases),'controlled_faults_detected':len(wrong), 'faults':wrong,
            'scope':'offline verifier calibration only; candidate requests zero','sum_rank_witness':sum_witness,
            'rank_compaction_note':'Order-preserving rank compaction alone preserves lexicographic assignment decisions; internal rank-gap checks are not a claim that this equivalent behavior is a product defect.'}


if __name__ == '__main__':
    import json
    print(json.dumps(calibrate()))

"""Independent applied-seating browser continuity and response-guard checks."""
import argparse
import asyncio
import copy
import json
from pathlib import Path
import re
import sys
import time
from urllib.parse import urlsplit

import stage4_campaign as core
sys.path.insert(0,str(Path(__file__).parent/'cumulative_stage3/cumulative'))
import browser_campaign as base
from playwright.async_api import async_playwright,expect
check=core.check


class Traffic(base.Traffic):
    def __init__(self,origin,api):
        super().__init__(origin);self.api=api;self.repair=False;self.fail_current=False;self.current_reads=0

    async def handler(self,route):
        req=route.request;path=urlsplit(req.url).path
        if req.method=='GET' and re.fullmatch('/reservations/[^/]+',path):
            self.current_reads+=1
            if self.fail_current:
                self.fail_current=False;await route.abort('failed');return
        if req.method=='POST' and path=='/reservations' and self.repair:
            self.repair=False
            headers=await req.all_headers();body=json.loads(req.post_data)
            self.bookings.append({'body':copy.deepcopy(body),'effective_body':copy.deepcopy(body),
                'key':headers.get('idempotency-key'),'authorization':headers.get('authorization')})
            response=await route.fetch(timeout=5000);original=await response.json()
            check(response.status==201,'repair setup booking did not commit')
            self.original=original;token=headers['authorization'].removeprefix('Bearer ')
            closure={'table_id':original['table_ids'][0],'from':original['starts_at'],'to':original['ends_at']}
            plan=await asyncio.to_thread(self.api.expect,201,'POST','/restaurants/r/replans',closure,token,'browser-preview')
            self.plan=plan
            self.applied=await asyncio.to_thread(self.api.expect,201,'POST','/restaurants/r/replans/'+plan['plan_id']+'/apply',{},token,'browser-apply')
            self.current=await asyncio.to_thread(self.api.current,original['reference'],token)
            check(self.current['table_ids']!=original['table_ids'],'browser repair did not change seating')
            await route.fulfill(response=response);return
        await super().handler(route)


class Campaign(base.BrowserCampaign):
    async def fresh(self,width=1280,fx=None):
        fx=fx or core.policies.fixture(zone='UTC');await self.call(self.api.reset,fx)
        context=await self.browser.new_context(viewport={'width':width,'height':950},timezone_id='Asia/Tokyo')
        context.set_default_timeout(10000);traffic=Traffic(self.origin,core.retained.API(self.origin))
        self.traffics.append(traffic);await context.route('**/*',traffic.handler)
        page=await context.new_page();await page.goto(self.origin+'/');return context,page,traffic,fx

    async def close(self,context,traffic):
        if traffic.delayed:traffic.delayed['release'].set()
        await context.unroute_all(behavior='wait');await context.close()

    async def assert_current_confirmation(self,page,current,fx):
        await expect(page.get_by_test_id('confirmation-reference')).to_have_text(current['reference'])
        labels={x['id']:x['label'] for x in fx['restaurants'][0]['tables']}
        for tid in current['table_ids']:
            await expect(page.get_by_test_id('confirmation-tables')).to_contain_text(labels[tid])
            await expect(page.get_by_test_id('confirmation-details')).to_contain_text(labels[tid])
        check(await page.get_by_test_id('booking-error').count()==0 and await page.get_by_test_id('booking-uncertain').count()==0,'known success became refused/uncertain')

    async def repaired_success_original_retry_current_lookup_story(self):
        for width in (375,1280):
            for ids,party in [(('z',),2),(('a','z'),6)]:
                context,page,traffic,fx=await self.fresh(width)
                await self.login(page);await self.search(page,party);await self.select(page,ids)
                traffic.repair=True;await page.get_by_test_id('booking-submit').click()
                await expect(page.get_by_test_id('confirmation')).to_be_visible()
                current=traffic.current;await self.assert_current_confirmation(page,current,fx)
                check(traffic.current_reads==1,'successful create did not make one authoritative current read')
                check(await page.get_by_test_id('booking-form').count()==1,'repaired success discarded retry form')
                await page.get_by_test_id('booking-submit').click()
                await self.assert_current_confirmation(page,current,fx)
                deadline=time.monotonic()+5
                while len(traffic.bookings)<2 and time.monotonic()<deadline:await asyncio.sleep(.05)
                check(len(traffic.bookings)==2 and traffic.bookings[0]==traffic.bookings[1],'repaired success retry changed exact body/key')
                token=traffic.bookings[-1]['authorization'].removeprefix('Bearer ')
                receipt=await self.call(self.api.expect,200,'POST','/reservations',traffic.bookings[0]['body'],token,traffic.bookings[0]['key'])
                check(receipt==traffic.original,'browser server original receipt mutated')
                await page.goto(self.origin+'/lookup');await page.get_by_test_id('lookup-reference-input').fill(current['reference'])
                await page.get_by_test_id('lookup-submit').click();await expect(page.get_by_test_id('reservation-detail')).to_be_visible()
                labels={x['id']:x['label'] for x in fx['restaurants'][0]['tables']}
                for tid in current['table_ids']:await expect(page.get_by_test_id('reservation-tables')).to_contain_text(labels[tid])
                disclosure=page.get_by_test_id('provenance-disclosure');await disclosure.locator(':scope > summary').click()
                await expect(page.get_by_test_id('reservation-history')).to_be_visible()
                events=page.get_by_test_id('history-event');await expect(events).to_have_count(2)
                await expect(events.nth(1)).to_contain_text('Seating updated by the restaurant')
                await expect(events.nth(1)).to_contain_text(traffic.plan['plan_id'])
                # Full before and after human selections must be legible in the story.
                for tid in set(traffic.original['table_ids']+current['table_ids']):await expect(events.nth(1)).to_contain_text(labels[tid])
                history=await self.call(core.retained.API(self.origin).history,current['reference'],token)
                check(history[-1]['plan_id']==traffic.plan['plan_id'] and history[-1]['accepted_terms']==traffic.original['accepted_terms'],'reassigned story backend provenance')
                await self.visual(page,'reassigned-'+('pair' if len(ids)==2 else 'single')+'-'+str(width))
                await page.goto(self.origin+'/');await self.search(page,party)
                await expect(page.get_by_test_id('slot-'+traffic.original['table_ids'][0]+'-18:00')).to_have_attribute('data-available','false')
                check(not traffic.blocked_hosts,'reassigned flow attempted outbound assets')
                await self.close(context,traffic)

    async def failed_current_read_preserves_known_success(self):
        for ids,party in [(('z',),2),(('a','z'),6)]:
            context,page,traffic,fx=await self.fresh()
            await self.login(page);await self.search(page,party);await self.select(page,ids)
            traffic.repair=True;traffic.fail_current=True;await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('confirmation')).to_be_visible();ref=traffic.original['reference']
            await expect(page.get_by_test_id('confirmation-reference')).to_have_text(ref)
            check(await page.get_by_test_id('booking-error').count()==0 and await page.get_by_test_id('booking-uncertain').count()==0,'current-read failure invalidated original known success')
            await page.get_by_test_id('booking-submit').click();await self.assert_current_confirmation(page,traffic.current,fx)
            check(len(traffic.bookings)==2 and traffic.bookings[0]==traffic.bookings[1],'current-read retry made new reservation')
            await self.close(context,traffic)

    async def delayed_current_read_user_navigation_guards(self):
        for action in ('logout','navigate'):
            context,page,traffic,fx=await self.fresh()
            await self.login(page);await self.search(page,2);await self.select(page,('z',))
            traffic.repair=True
            gate=traffic.gate(lambda req:req.method=='GET' and re.fullmatch('/reservations/[^/]+',urlsplit(req.url).path) is not None)
            await page.get_by_test_id('booking-submit').click();await asyncio.wait_for(gate['started'].wait(),10)
            if action=='logout':await page.get_by_test_id('logout-button').click()
            else:await page.locator('a[href="/lookup"]').first.click()
            gate['release'].set();await asyncio.wait_for(gate['finished'].wait(),10)
            check(await page.get_by_test_id('confirmation').count()==0,'late current read restored obsolete confirmation')
            if action=='logout':check(await page.get_by_test_id('current-user').count()==0,'late current read restored old session')
            await self.close(context,traffic)

    async def delayed_current_read_new_intent_guard(self):
        context,page,traffic,fx=await self.fresh()
        await self.login(page);await self.search(page,2);await self.select(page,('z',))
        traffic.repair=True
        gate=traffic.gate(lambda req:req.method=='GET' and re.fullmatch('/reservations/[^/]+',urlsplit(req.url).path) is not None)
        await page.get_by_test_id('booking-submit').click();await asyncio.wait_for(gate['started'].wait(),10)
        await self.select(page,('z',),'20:00');await page.get_by_test_id('booking-submit').click()
        await expect(page.get_by_test_id('confirmation')).to_be_visible()
        await expect(page.get_by_test_id('confirmation-reference')).not_to_have_text(traffic.original['reference'])
        new_ref=await page.get_by_test_id('confirmation-reference').inner_text()
        check(traffic.bookings[-1]['key']!=traffic.bookings[0]['key'],'new selection retained old booking key')
        gate['release'].set();await asyncio.wait_for(gate['finished'].wait(),10)
        await expect(page.get_by_test_id('confirmation-reference')).to_have_text(new_ref)
        await expect(page.get_by_test_id('confirmation-details')).to_contain_text('20:00')
        await self.close(context,traffic)


async def main():
    p=argparse.ArgumentParser();p.add_argument('--released',action='store_true')
    for name in ('revision','source','destination','out'):p.add_argument('--'+name,required=True)
    names=('repaired_success_original_retry_current_lookup_story','failed_current_read_preserves_known_success','delayed_current_read_user_navigation_guards','delayed_current_read_new_intent_guard')
    p.add_argument('--cases',nargs='+',choices=names)
    a=p.parse_args()
    if not a.released or not re.fullmatch('[0-9a-f]{40}',a.revision):p.error('exact release required')
    out=Path(a.out);out.mkdir(exist_ok=True)
    async with async_playwright() as playwright:
        browser=await playwright.chromium.launch(headless=True,args=['--no-sandbox'])
        c=Campaign(browser,a.source,a.destination,None,out)
        for name in a.cases or names:
            began=time.monotonic()
            try:await getattr(c,name)();row={'case':name,'status':'PASS'}
            except Exception as e:row={'case':name,'status':'FAIL','classification':'INCONCLUSIVE','detail':str(e)}
            row['seconds']=round(time.monotonic()-began,3);c.results.append(row);print(json.dumps(row),flush=True)
        report={'production_revision':a.revision,'cases':c.results,'all_passed':all(x['status']=='PASS' for x in c.results),'visual_metrics':c.visual_metrics,'requests':len(c.api.timings)}
        (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');await browser.close()
    raise SystemExit(0 if report['all_passed'] else 1)

if __name__=='__main__':asyncio.run(main())

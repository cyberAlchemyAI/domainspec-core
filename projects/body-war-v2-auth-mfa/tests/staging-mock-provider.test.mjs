import test from 'node:test';import assert from 'node:assert/strict';import {installStagingMocks} from '../scripts/staging-mock-provider.mjs';
test('mock fixtures stay scoped, labeled, paginated and behind account/scope gates',async()=>{
 const calls=[];const real={listActivitySummaries:async(...a)=>{calls.push(a);return 'live-list'},getActivitySummary:async(...a)=>{calls.push(a);return 'live-detail'}};
 let account={status:'linked',scope:['activity:read read']};const repo={findProviderAccountByPrincipalId:async()=>account};
 installStagingMocks(real,repo,{principalId:'runner',activities:[{id:'mock-1',name:'MOCK Run 1'},{id:'mock-2',name:'MOCK Run 2'}]});
 assert.equal((await real.listActivitySummaries('runner','1','1')).value[0].id,'mock-1');assert.equal((await real.listActivitySummaries('runner','2','1')).value[0].id,'mock-2');assert.equal((await real.listActivitySummaries('runner','0','20')).ok,false);
 assert.equal((await real.getActivitySummary('runner','mock-1')).ok,true);assert.equal((await real.getActivitySummary('runner','mock-missing')).ok,false);assert.equal(calls.length,0);
 assert.equal(await real.getActivitySummary('other','mock-1'),'live-detail');assert.equal(await real.getActivitySummary('runner','123'),'live-detail');assert.equal(await real.listActivitySummaries('other','1','20'),'live-list');
 account={status:'linked',scope:[]};assert.equal((await real.getActivitySummary('runner','mock-1')).error.status,403);account=null;assert.equal((await real.listActivitySummaries('runner','1','20')).error.status,409);
});

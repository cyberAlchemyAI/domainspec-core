import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=resolve(fileURLToPath(new URL('..',import.meta.url)));
process.env.BODY_WAR_AUTH_BACKEND='memory';process.env.BODY_WAR_STRAVA_FAKE='1';process.env.BODY_WAR_APP_ROOT=join(root,'app');
const {handleRequest,resetAuthComponentsForTests,authComponents}=await import(pathToFileURL(join(root,'app/dist/server.js')));
resetAuthComponentsForTests();const server=createServer((req,res)=>void handleRequest(req,res));await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;
const cases=[];const record=(id,observed)=>cases.push({id,status:'passed',observed});
const cookie=r=>r.headers.getSetCookie().map(c=>c.split(';')[0]).join('; ');
try{
 const start=await fetch(base+'/api/auth/strava/start',{redirect:'manual'}),state=cookie(start),url=new URL(start.headers.get('location'),base);
 const callback=await fetch(url,{redirect:'manual',headers:{cookie:state}});assert.equal(callback.status,302);const aCookie=cookie(callback),csrf=decodeURIComponent(aCookie.match(/bw_csrf=([^;]+)/)[1]);
 const aProfile=await (await fetch(base+'/api/profile',{headers:{cookie:aCookie}})).json();const aId=aProfile.profile.principal_id;
 const replay=await fetch(url,{redirect:'manual',headers:{cookie:state}});assert.match(replay.headers.get('location'),/auth_error=.*state/);assert.ok(!cookie(replay).includes('bw_session='));record('oauth_replay',{successful_sessions:1,replay:'rejected'});
 const components=authComponents();
 async function principal(name,permissions){const p=await components.repos.principalRepo.create({identifier:'synthetic:'+name,subjectType:'user',roleKeys:[],directPermissions:permissions,credentialHash:'external:synthetic'});await components.bodyWarRepo.upsertRunnerProfile({principalId:p.id,displayName:name});await components.bodyWarRepo.upsertProviderAccount({provider:'strava',principalId:p.id,providerUserId:name,displayName:name,scope:['read','activity:read'],status:'linked',metadata:{}});const session=await components.browser.createSession({principalId:p.id});assert.equal(session.ok,true);return {id:p.id,cookie:'bw_session='+session.value.binding.sessionCookie+'; bw_csrf='+session.value.binding.csrfToken};}
 const b=await principal('Runner-B',['body-war.suggested-track.read']),denied=await principal('No-Permission',[]);
 const track=await components.bodyWarRepo.createSuggestedTrack({principalId:aId,name:'Private evidence test',placeLabel:'Synthetic',city:'Campinas'});
 const candidate=await components.bodyWarRepo.addActivityEvidenceCandidate({suggestedTrackId:track.id,principalId:aId,providerActivityId:'synthetic-private',redactedSummary:{name:'A-PRIVATE-EVIDENCE'},consentText:'synthetic consent',consentedAt:new Date().toISOString()});
 const detail=await fetch(base+'/api/suggested-tracks/'+track.id,{headers:{cookie:b.cookie}});assert.equal(detail.status,200);const bDetail=await detail.json();assert.deepEqual(bDetail.my_evidence_candidates,[]);assert.ok(!JSON.stringify(bDetail).includes('A-PRIVATE-EVIDENCE'));const profile=await (await fetch(base+'/api/profile',{headers:{cookie:b.cookie}})).json();assert.equal(profile.profile.principal_id,b.id);assert.notEqual(profile.profile.principal_id,aId);record('runner_isolation',{other_runner_candidates:0,own_profile:true});
 assert.equal((await fetch(base+'/api/suggested-tracks',{headers:{cookie:denied.cookie}})).status,403);assert.equal((await fetch(base+'/api/suggested-tracks')).status,401);record('permissions',{anonymous:401,authenticated_without_grant:403});
 const body={name:'Valid synthetic',place_label:'Synthetic',city:'Campinas'};const headers={'content-type':'application/json',cookie:aCookie,origin:'http://127.0.0.1:5174','x-csrf-token':csrf};
 for(const h of [{...headers,'x-csrf-token':''},{...headers,origin:'https://untrusted.invalid'}])assert.equal((await fetch(base+'/api/suggested-tracks',{method:'POST',headers:h,body:JSON.stringify(body)})).status,403);record('csrf_origin',{missing_csrf:403,untrusted_origin:403});
 const before=(await components.bodyWarRepo.listSuggestedTracks()).length;
 for(const [raw,status]of [['{broken',400],[JSON.stringify({...body,unexpected:true}),400],[JSON.stringify({...body,name:23}),400],[JSON.stringify({...body,name:'   '}),400],[JSON.stringify({...body,distance_hint_meters:0}),400],[JSON.stringify({...body,distance_hint_meters:1.5}),400],[JSON.stringify({...body,public_note:'x'.repeat(17000)}),413]])assert.equal((await fetch(base+'/api/suggested-tracks',{method:'POST',headers,body:raw})).status,status);
 assert.equal((await components.bodyWarRepo.listSuggestedTracks()).length,before);record('request_validation',{malformed:400,unknown_field:400,wrong_type:400,blank_required_text:400,nonpositive_distance:400,fractional_distance:400,oversized:413,writes:0});
 assert.equal(await components.bodyWarRepo.disposeActivityEvidenceCandidate({candidateId:candidate.id,reason:'consent_revocation'}),'disposed');assert.equal(await components.bodyWarRepo.disposeActivityEvidenceCandidate({candidateId:candidate.id,reason:'consent_revocation'}),'already_absent');assert.equal((await components.bodyWarRepo.listActivityEvidenceCandidates(track.id)).length,0);assert.equal((await components.bodyWarRepo.findSuggestedTrack(track.id)).status,'needs_evidence');record('consent_revocation',{candidate_erased:true,last_evidence_reset:true,retry:'already_absent',boundary:'internal repository operation; no public revoke endpoint'});
 const sha=p=>createHash('sha256').update(readFileSync(p)).digest('hex');writeFileSync(join(root,'evidence/critical-security.json'),JSON.stringify({status:'passed',cases,ontology_sha256:sha(join(root,'model/application-ontology.json')),test_sha256:sha(fileURLToPath(import.meta.url)),authority_effect:'none',open_questions_ref:'../README.md#open-questions'},null,2)+'\n');console.log(JSON.stringify({status:'passed',cases:cases.length}));
}finally{server.closeAllConnections();await new Promise(r=>server.close(r));}

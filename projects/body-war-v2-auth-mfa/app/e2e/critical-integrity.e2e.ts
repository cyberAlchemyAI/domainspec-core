import assert from 'node:assert/strict';
import {randomUUID,createHash} from 'node:crypto';
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {createBodyWarSqlClient,createBodyWarDatabase,closeBodyWarSqlClient} from '../src/infrastructure/postgres/database.js';
import {createDrizzleBodyWarAuthRepository} from '../src/auth/drizzle-repository.js';
export async function runCriticalIntegrity(){
 const clients=Array.from({length:12},()=>createBodyWarSqlClient());const repos=clients.map(c=>createDrizzleBodyWarAuthRepository(createBodyWarDatabase(c)));const sql=clients[0]!,repo=repos[0]!;const cases:Array<{id:string;status:string;observed:unknown}>=[];
 const record=(id:string,observed:unknown)=>cases.push({id,status:'passed',observed});
 try{
  const now=new Date(),state='critical-'+randomUUID();await repo.createOAuthState({state,nonce:state,redirectTarget:'/',createdAt:now.toISOString(),expiresAt:new Date(now.getTime()+60000).toISOString(),consumedAt:null});
  const consumed=await Promise.all(repos.map(r=>r.consumeOAuthState(state,now)));assert.equal(consumed.filter(Boolean).length,1);assert.equal(await repo.consumeOAuthState(state,now),null);
  const expired='expired-'+randomUUID();await repo.createOAuthState({state:expired,nonce:expired,redirectTarget:'/',createdAt:new Date(now.getTime()-60000).toISOString(),expiresAt:now.toISOString(),consumedAt:null});assert.equal(await repo.consumeOAuthState(expired,now),null);record('oauth_concurrency',{callers:12,successful_consumptions:1,expired_at_boundary:'rejected'});
  const owner=randomUUID(),other=randomUUID(),accountInput={provider:'strava' as const,principalId:owner,providerUserId:'owner-'+randomUUID(),displayName:'Synthetic owner',scope:['read'],status:'linked' as const,metadata:{}};
  await repo.upsertProviderAccount(accountInput);
  const takeover=await Promise.allSettled(repos.map(r=>r.upsertProviderAccount({...accountInput,principalId:other})));assert.equal(takeover.filter(x=>x.status==='fulfilled').length,0);assert.equal((await repo.findProviderAccountByPrincipalId(owner))?.providerUserId,accountInput.providerUserId);assert.equal(await repo.findProviderAccountByPrincipalId(other),null);
  await assert.rejects(()=>repo.upsertProviderAccount({...accountInput,providerUserId:'replacement-'+randomUUID()}));record('provider_owner_concurrency',{attempts:12,takeovers:0,principal_provider_unique:'enforced'});
  const principalId=randomUUID(),track=await repo.createSuggestedTrack({principalId,name:'Concurrent evidence',placeLabel:'Synthetic',city:'Campinas'});
  const input={suggestedTrackId:track.id,principalId,providerActivityId:'concurrent-activity',redactedSummary:{name:'synthetic'},consentText:'synthetic consent',consentedAt:now.toISOString()};
  const inserted=await Promise.allSettled(repos.map(r=>r.addActivityEvidenceCandidate(input)));assert.equal(inserted.filter(r=>r.status==='fulfilled').length,1);for(const r of inserted)if(r.status==='rejected')assert.equal((r.reason as {code:string}).code,'evidence_candidate_replay');
  assert.equal((await repo.listActivityEvidenceCandidates(track.id)).length,1);assert.equal((await repo.findSuggestedTrack(track.id))?.status,'evidence_submitted');
  await assert.rejects(()=>sql`insert into body_war_activity_evidence_candidates (suggested_track_id,principal_id,provider,provider_activity_id,redacted_summary,consent_text,consented_at) values (${track.id},${principalId},'strava','concurrent-activity','{}','synthetic',now())`,(e:any)=>e.code==='23505');
  await repo.addActivityEvidenceCandidate({...input,principalId:randomUUID()});assert.equal((await repo.listActivityEvidenceCandidates(track.id)).length,2);record('evidence_concurrency',{callers:12,insertions:1,replays:11,database_unique_constraint:'enforced',different_runner:'allowed'});
  const failure=await repo.createSuggestedTrack({principalId,name:'FAIL-ATOMIC',placeLabel:'Synthetic',city:'Campinas'});
  await sql.unsafe("CREATE FUNCTION critical_fail_update() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN IF NEW.name='FAIL-ATOMIC' THEN RAISE EXCEPTION 'synthetic transaction failure'; END IF; RETURN NEW; END $$");
  await sql.unsafe('CREATE TRIGGER critical_fail_update BEFORE UPDATE ON body_war_suggested_tracks FOR EACH ROW EXECUTE FUNCTION critical_fail_update()');
  try{await assert.rejects(()=>repo.addActivityEvidenceCandidate({...input,suggestedTrackId:failure.id}));assert.equal((await repo.listActivityEvidenceCandidates(failure.id)).length,0);assert.equal((await repo.findSuggestedTrack(failure.id))?.status,'needs_evidence');}finally{await sql.unsafe('DROP TRIGGER critical_fail_update ON body_war_suggested_tracks');await sql.unsafe('DROP FUNCTION critical_fail_update()');}
  const retry=await repo.addActivityEvidenceCandidate({...input,suggestedTrackId:failure.id});assert.ok(retry.id);assert.equal((await repo.listActivityEvidenceCandidates(failure.id)).length,1);record('atomic_rollback',{injected_failure:'between insert and track update',partial_rows:0,retry_rows:1});
  assert.equal(await repos[1]!.disposeActivityEvidenceCandidate({candidateId:retry.id,principalId:randomUUID(),reason:'consent_revocation'}),'already_absent');
  assert.equal((await repo.listActivityEvidenceCandidates(failure.id)).length,1);
  const race=await Promise.all([repos[1]!.disposeActivityEvidenceCandidate({candidateId:retry.id,principalId,reason:'consent_revocation'}),repos[2]!.addActivityEvidenceCandidate({...input,suggestedTrackId:failure.id,providerActivityId:'concurrent-replacement'})]);assert.equal(race[0],'disposed');assert.equal((await repo.listActivityEvidenceCandidates(failure.id)).length,1);assert.equal((await repo.findSuggestedTrack(failure.id))?.status,'evidence_submitted');
  const last=(await repo.listActivityEvidenceCandidates(failure.id))[0]!;await repo.disposeActivityEvidenceCandidate({candidateId:last.id,principalId,reason:'consent_revocation'});assert.equal((await repo.findSuggestedTrack(failure.id))?.status,'needs_evidence');record('concurrent_disposition',{replacement_survives:true,state_consistent:true,last_removal_resets:true});
  await Promise.all(clients.map(closeBodyWarSqlClient));
  const database=pathToFileURL(resolve('dist/src/infrastructure/postgres/database.js')).href;
  const repository=pathToFileURL(resolve('dist/src/auth/drizzle-repository.js')).href;
  const code=`import {createBodyWarSqlClient,createBodyWarDatabase} from ${JSON.stringify(database)};import {createDrizzleBodyWarAuthRepository} from ${JSON.stringify(repository)};const sql=createBodyWarSqlClient();try{const r=createDrizzleBodyWarAuthRepository(createBodyWarDatabase(sql));console.log(JSON.stringify({count:(await r.listActivityEvidenceCandidates(${JSON.stringify(track.id)})).length,status:(await r.findSuggestedTrack(${JSON.stringify(track.id)})).status}));}finally{await sql.end();}`;
  const child=spawnSync(process.execPath,['--input-type=module','-e',code],{encoding:'utf8',timeout:15000});assert.equal(child.status,0,child.stderr);assert.deepEqual(JSON.parse(child.stdout),{count:2,status:'evidence_submitted'});record('persistence_reopen',{new_process:true,persisted_rows:2,state:'evidence_submitted',database_process_restart:false});
  const sha=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');writeFileSync(resolve('../evidence/critical-postgres.json'),JSON.stringify({status:'passed',cases,ontology_sha256:sha(resolve('../model/application-ontology.json')),test_sha256:sha(resolve('e2e/critical-integrity.e2e.ts')),authority_effect:'none',open_questions_ref:'../README.md#open-questions'},null,2)+'\n');console.log(JSON.stringify({critical_postgres:'passed',cases:cases.length}));
 }finally{await Promise.all(clients.map(closeBodyWarSqlClient));}
}

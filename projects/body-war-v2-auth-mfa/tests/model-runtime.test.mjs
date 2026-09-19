import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdtempSync,mkdirSync,cpSync,rmSync,readdirSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {spawn,spawnSync} from 'node:child_process';
import {createServer} from 'node:net';
import {createHash} from 'node:crypto';
const root=process.cwd();
process.env.ALCHLANG_DOMAINSPEC_PACKAGE_ROOT=join(root,'.tools/compiler');
const alch=resolve(process.env.ALCHLANG_SOURCE_ROOT??'../../../cyberAlchemy-v2/language/capabilities/alchlang/plans/general-compiler-v1/implementation');
const {buildApplication,checkApplication}=await import(pathToFileURL(join(alch,'src/application-contract.ts')));
const cli=join(root,'.tools/compiler/dist/cli/main.js');
const evidence=[];
function fixture(){const dir=mkdtempSync(join(root,'.runtime/model-runtime-'));for(const name of ['body-war.alch','model','app/src','app/tests','app/ui','app/drizzle','app/static','app/server.ts','app/package.json','vendor/auth/src','scripts']){mkdirSync(join(dir,name,'..'),{recursive:true});cpSync(join(root,name),join(dir,name),{recursive:true});}rmSync(join(dir,'app/src/application'),{recursive:true,force:true});return dir;}
function replace(dir,p,a,b){const file=join(dir,p),s=readFileSync(file,'utf8');assert.ok(s.includes(a),a);writeFileSync(file,s.replace(a,b));}
const sha=x=>createHash('sha256').update(x).digest('hex');
function inventory(dir){const out={};function walk(p){for(const e of readdirSync(p,{withFileTypes:true})){const f=join(p,e.name);if(e.isDirectory())walk(f);else out[f.slice(dir.length+1)]=sha(readFileSync(f));}}walk(dir);return out;}
async function build(dir){return buildApplication(join(dir,'body-war.alch'),join(dir,'app/src/application'));}
async function server(dir,run){
 const port=await new Promise(r=>{const s=createServer();s.listen(0,'127.0.0.1',()=>{const p=s.address().port;s.close(()=>r(p));});});const base=`http://127.0.0.1:${port}`;
 const child=spawn(process.execPath,['--import',join(root,'node_modules/tsx/dist/loader.mjs'),'--input-type=module','-e','import {main} from '+JSON.stringify(pathToFileURL(join(dir,'app/server.ts')).href)+'; await main();'],{cwd:join(dir,'app'),env:{...process.env,BODY_WAR_HOST:'127.0.0.1',BODY_WAR_PORT:String(port),BODY_WAR_PUBLIC_BASE_URL:base,BODY_WAR_ALLOWED_ORIGINS:base,BODY_WAR_STRAVA_FAKE:'1',BODY_WAR_AUTH_BACKEND:'memory'},stdio:['ignore','pipe','pipe']});let stderr='';child.stderr.on('data',b=>stderr+=b);child.stdout.on('data',b=>stderr+=b);const exited=new Promise(r=>child.once('exit',r));
 try{let ready=false;for(let i=0;i<400;i++){if(child.exitCode!==null)throw Error(stderr);try{await fetch(base+'/api/no-such-route',{signal:AbortSignal.timeout(1000)});ready=true;break;}catch{}await new Promise(r=>setTimeout(r,30));}assert.ok(ready,stderr);return await run(base);}finally{child.kill();await exited;}
}
async function login(base){const start=await fetch(base+'/api/auth/strava/start',{redirect:'manual'});assert.equal(start.status,302);const state=start.headers.getSetCookie().map(c=>c.split(';')[0]).join('; ');const callback=await fetch(new URL(start.headers.get('location'),base),{redirect:'manual',headers:{cookie:state}});assert.equal(callback.status,302);return callback.headers.getSetCookie().map(c=>c.split(';')[0]).join('; ');}
test('AlchLang and direct DomainSpec application CLI generate byte-identical files',async()=>{const dir=fixture();try{
 await build(dir);const out=join(dir,'app/src/application'),before=inventory(out),input=join(dir,'application.json');writeFileSync(input,readFileSync(join(out,'application-ontology.json')));rmSync(out,{recursive:true});
 const r=spawnSync(process.execPath,[cli,'application-build',input,'--root',dir,'--target-root',out],{encoding:'utf8'});assert.equal(r.status,0,r.stderr);assert.deepEqual(inventory(out),before);
 await server(dir,async base=>{assert.equal((await fetch(base+'/api/status')).status,200);assert.equal((await fetch(base+'/api/suggested-tracks',{headers:{cookie:await login(base)}})).status,200);});
 evidence.push({id:'compiler-equivalence',status:'passed',artifacts:Object.keys(before).length,manifest_sha256:sha(JSON.stringify(before))});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('changing an authored route moves the live endpoint',async()=>{const dir=fixture();try{replace(dir,'model/identity.alch','path "/api/status"','path "/api/connection-status"');await build(dir);await server(dir,async base=>{assert.equal((await fetch(base+'/api/status')).status,404);assert.equal((await fetch(base+'/api/connection-status')).status,200);});evidence.push({id:'route-mutation',status:'passed',old_status:404,new_status:200});}finally{rmSync(dir,{recursive:true,force:true});}});
test('changing an authored permission denies an otherwise authenticated runner',async()=>{const dir=fixture();try{replace(dir,'model/tracks.alch','permission "body-war.suggested-track.read"','permission "body-war.operator-only"');await build(dir);await server(dir,async base=>{const r=await fetch(base+'/api/suggested-tracks',{headers:{cookie:await login(base)}});assert.equal(r.status,403,await r.text());});evidence.push({id:'permission-mutation',status:'passed',baseline:200,mutant:403});}finally{rmSync(dir,{recursive:true,force:true});}});
test('changing an authored response type rejects incompatible live adapter output',async()=>{const dir=fixture();try{replace(dir,'model/identity.alch','"scope":"string"','"scope":"number"');await build(dir);await server(dir,async base=>{const r=await fetch(base+'/api/status');assert.equal(r.status,500);assert.match(await r.text(),/APPLICATION_RESPONSE_CONTRACT/);});evidence.push({id:'response-mutation',status:'passed',baseline:200,mutant:500});}finally{rmSync(dir,{recursive:true,force:true});}});
test('changing an authored lifecycle changes the generated executable decision',async()=>{const dir=fixture();try{replace(dir,'model/tracks.alch','["needs_evidence","attach","evidence_submitted"]','["needs_evidence","attach","operator_review"]');await build(dir);const domain=await import(pathToFileURL(join(dir,'app/src/application/domain.ts')));assert.equal(domain.transition('TrackEvidenceLifecycle','needs_evidence','attach'),'operator_review');evidence.push({id:'lifecycle-mutation',status:'passed',baseline:'evidence_submitted',mutant:'operator_review'});}finally{rmSync(dir,{recursive:true,force:true});}});
test('both frontends reject invalid permission semantics; JSON input rejects stale sources and escaping core files',async()=>{const dir=fixture();try{
 replace(dir,'model/identity.alch','authentication "public"\n  permission null','authentication "public"\n  permission "forbidden"');await assert.rejects(()=>checkApplication(join(dir,'body-war.alch')),/public operation/);
 const baseline=JSON.parse(readFileSync(join(root,'model/application-ontology.json')));for(const kind of ['permission','source','core-path','normalization']){const p=structuredClone(baseline);if(kind==='normalization')p.declarations.find(d=>d.id==='CreateTrackRules').fields.name.max=0;if(kind==='permission')p.declarations.find(d=>d.id==='ReadStatus').permission='forbidden';if(kind==='source')p.sources['body-war.alch']='0'.repeat(64);if(kind==='core-path')p.core_projects.Consent['../../escape']='bad';const input=join(dir,kind+'.json');writeFileSync(input,JSON.stringify(p));const r=spawnSync(process.execPath,[cli,'application-check',input,'--root',root],{encoding:'utf8'});assert.notEqual(r.status,0);assert.match(r.stderr,/public operation|bound source drift|core project path|normalization/);}
 evidence.push({id:'invalid-inputs',status:'passed',rejected:5});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('authored request size limits reject a live write before persistence',async()=>{const dir=fixture();try{
 replace(dir,'model/tracks.alch','maxbytes 16384','maxbytes 16');await build(dir);
 await server(dir,async base=>{const cookie=await login(base),csrf=cookie.split('; ').find(x=>x.startsWith('bw_csrf=')).slice('bw_csrf='.length);const r=await fetch(base+'/api/suggested-tracks',{method:'POST',headers:{cookie,origin:base,'x-csrf-token':decodeURIComponent(csrf),'content-type':'application/json'},body:JSON.stringify({name:'Mutation route',place_label:'Park',city:'City'})});assert.equal(r.status,413,await r.text());});
 evidence.push({id:'request-limit-mutation',status:'passed',mutant:413});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('request normalization rejects incompatible types and invalid limits at compilation',async()=>{const dir=fixture();try{
 replace(dir,'model/tracks.alch','fields {"name":"string","place_label"','fields {"name":"number","place_label"');await assert.rejects(()=>checkApplication(join(dir,'body-war.alch')),/normalization bounds or type/);
 replace(dir,'model/tracks.alch','fields {"name":"number","place_label"','fields {"name":"string","place_label"');replace(dir,'model/tracks.alch','maxbytes 16384','maxbytes 0');await assert.rejects(()=>checkApplication(join(dir,'body-war.alch')),/request contract/);
 evidence.push({id:'request-type-mutation',status:'passed',incompatible_normalizer:'rejected',invalid_limit:'rejected'});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('authored normalization changes the persisted live value',async()=>{const dir=fixture();try{
 replace(dir,'model/tracks.alch','"name":{"kind":"text","min":1,"max":255}','"name":{"kind":"text","min":1,"max":3}');await build(dir);
 await server(dir,async base=>{const cookie=await login(base),csrf=decodeURIComponent(cookie.match(/bw_csrf=([^;]+)/)[1]);const r=await fetch(base+'/api/suggested-tracks',{method:'POST',headers:{cookie,origin:base,'x-csrf-token':csrf,'content-type':'application/json'},body:JSON.stringify({name:'  Mutation route  ',place_label:' Park ',city:' City '})});assert.equal(r.status,201,await r.clone().text());const created=(await r.json()).suggested_track;assert.equal(created.name,'Mut');assert.equal(created.place_label,'Park');const detail=await (await fetch(base+'/api/suggested-tracks/'+created.id,{headers:{cookie}})).json();assert.equal(detail.suggested_track.name,'Mut');});
 evidence.push({id:'normalization-mutation',status:'passed',persisted_name:'Mut'});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('authored nested type changes reject incompatible live response before flushing',async()=>{const dir=fixture();try{
 replace(dir,'model/tracks.alch','"distance_hint_meters":"number|null","status"','"distance_hint_meters":"string|null","status"');await build(dir);await server(dir,async base=>{const r=await fetch(base+'/api/suggested-tracks',{headers:{cookie:await login(base)}});assert.equal(r.status,500);assert.match(await r.text(),/APPLICATION_RESPONSE_CONTRACT/);});evidence.push({id:'nested-type-mutation',status:'passed',mutant:500});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('unexpected nested private fields cannot leave the live track endpoint',async()=>{const dir=fixture();try{
 replace(dir,'app/src/adapters/pilot-http.ts','suggested_by: track.suggestedByPrincipalId','access_token: "SYNTHETIC-PRIVATE-TOKEN", suggested_by: track.suggestedByPrincipalId');await build(dir);await server(dir,async base=>{const r=await fetch(base+'/api/suggested-tracks',{headers:{cookie:await login(base)}});assert.equal(r.status,500);const body=await r.text();assert.match(body,/APPLICATION_RESPONSE_CONTRACT/);assert.ok(!body.includes('SYNTHETIC-PRIVATE-TOKEN'));});evidence.push({id:'nested-private-field',status:'passed',mutant:500,private_value_returned:false});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('authored query bounds change live activity acceptance',async()=>{const dir=fixture();try{
 replace(dir,'model/activities.alch','"min":1,"max":10,"default":1','"min":1,"max":1,"default":1');await build(dir);await server(dir,async base=>{const cookie=await login(base);assert.equal((await fetch(base+'/api/activities?page=1',{headers:{cookie}})).status,200);for(const query of ['page=2','page=1&page=1','extra=1','per_page=0','page=1.5']){const r=await fetch(base+'/api/activities?'+query,{headers:{cookie}});assert.equal(r.status,400,await r.text());}});evidence.push({id:'query-bound-mutation',status:'passed',allowed:200,outside_authored_bound:400,duplicates:400,unknown_fields:400});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('authored identity nesting rejects incompatible live session type',async()=>{const dir=fixture();try{
 replace(dir,'model/identity.alch','"expires_at":"string"','"expires_at":"number"');await build(dir);await server(dir,async base=>{const r=await fetch(base+'/api/profile',{headers:{cookie:await login(base)}});assert.equal(r.status,500);assert.match(await r.text(),/APPLICATION_RESPONSE_CONTRACT/);});evidence.push({id:'identity-type-mutation',status:'passed',mutant:500});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('nested identity private fields are rejected before response delivery',async()=>{const dir=fixture();try{
 replace(dir,'app/src/adapters/pilot-http.ts','expires_at: input.auth.expiresAt,','expires_at: input.auth.expiresAt, access_token: "PRIVATE-IDENTITY-MUTANT",');await build(dir);await server(dir,async base=>{const r=await fetch(base+'/api/profile',{headers:{cookie:await login(base)}});assert.equal(r.status,500);const body=await r.text();assert.ok(!body.includes('PRIVATE-IDENTITY-MUTANT'));assert.match(body,/APPLICATION_RESPONSE_CONTRACT/);});evidence.push({id:'identity-private-field',status:'passed',mutant:500,private_value_returned:false});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('removed migration APIs return 404 and archive fields are rejected',async()=>{const dir=fixture();try{
 await build(dir);await server(dir,async base=>{
 for(const path of ['/api/tracks','/api/submissions','/api/migration/submissions'])assert.equal((await fetch(base+path)).status,404);
 assert.equal((await fetch(base+'/api/submissions',{method:'POST'})).status,404);
 const cookie=await login(base),csrf=decodeURIComponent(cookie.match(/bw_csrf=([^;]+)/)[1]);
 const r=await fetch(base+'/api/suggested-tracks/any/evidence-candidates',{method:'POST',headers:{cookie,origin:base,'x-csrf-token':csrf,'content-type':'application/json'},body:JSON.stringify({activity_id:'a',legacy_submission_id:'retired',consent_acknowledged:true,consent_text:'Synthetic consent'})});assert.equal(r.status,400);
 });evidence.push({id:'migration-removed',status:'passed',removed_endpoints:404,removed_field:400});
}finally{rmSync(dir,{recursive:true,force:true});}});
test('write complete mutation evidence',()=>{assert.equal(evidence.length,15);writeFileSync(join(root,'evidence/model-runtime.json'),JSON.stringify({status:'passed',source_sha256:sha(readFileSync(join(root,'model/application-ontology.json'))),checks:evidence,authority_effect:'none',open_questions_ref:'../README.md#open-questions'},null,2)+'\n');});

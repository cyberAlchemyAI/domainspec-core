import {spawn} from 'node:child_process';
import {createServer} from 'node:http';
import {readFileSync,writeFileSync,mkdtempSync,mkdirSync,rmSync} from 'node:fs';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
export async function runLocalRecovery(root){
 const sha=x=>createHash('sha256').update(x).digest('hex');
 const dir=mkdtempSync(join(root,'.runtime/recovery-'));const children=[];let gateway;
 async function worker(mode,target,fault='none'){
  const child=spawn(process.execPath,[join(root,'scripts/local-recovery-worker.mjs'),mode,target,fault],{cwd:join(root,'app'),env:{...process.env,BODY_WAR_STRAVA_FAKE:'1',BODY_WAR_AUTH_BACKEND:'memory'},stdio:['ignore','pipe','pipe']});children.push(child);child.exited=new Promise(r=>child.once('exit',r));let err='';child.stderr.on('data',b=>err+=b);
  const port=await new Promise((yes,no)=>{let raw='';const timer=setTimeout(()=>no(Error('Worker readiness timeout: '+err)),10000);child.stdout.on('data',b=>{raw+=b;const end=raw.indexOf('\n');if(end>=0){try{yes(JSON.parse(raw.slice(0,end)).port);clearTimeout(timer);}catch(e){clearTimeout(timer);no(e);}}});child.once('exit',()=>{clearTimeout(timer);no(Error(err));});});return {child,url:'http://127.0.0.1:'+port};
 }
 try{
  const stable=await worker('slot',join(root,'app/dist/server.js')),candidate=await worker('slot',join(root,'app/dist/server.js'),'unhealthy');
  const events=join(dir,'events.jsonl');writeFileSync(events,'');const collector=await worker('collector',events);
  let active=stable.url;gateway=createServer(async(req,res)=>{try{const upstream=await fetch(active+(req.url??'/'),{signal:AbortSignal.timeout(1500)});res.writeHead(upstream.status,{'content-type':'application/json'});res.end(await upstream.text());}catch{res.writeHead(502);res.end('{"error":"upstream_unavailable"}');}});await new Promise(r=>gateway.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+gateway.address().port;
  const observations=[];
  async function probe(phase,expected){const r=await fetch(base+'/api/status',{signal:AbortSignal.timeout(3000)});assert.equal(r.status,expected,phase);const event={phase,status:r.status};const exported=await fetch(collector.url+'/events',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(event),signal:AbortSignal.timeout(3000)});assert.equal(exported.status,202);observations.push(event);}
  await probe('stable',200);
  active=candidate.url;await probe('canary-fault',503);
  active=stable.url;await probe('rollback-after-canary',200);
  stable.child.kill('SIGKILL');await stable.child.exited;await probe('process-loss',502);
  const recovered=await worker('slot',join(root,'app/dist/server.js'));active=recovered.url;await probe('restart-recovery',200);
  const received=readFileSync(events,'utf8').trim().split('\n').map(x=>JSON.parse(x));assert.deepEqual(received,observations);
  const illegal=await fetch(collector.url+'/events',{method:'POST',body:JSON.stringify({phase:'synthetic',status:200,token:'synthetic-forbidden'})});assert.equal(illegal.status,500);assert.equal(readFileSync(events,'utf8').trim().split('\n').length,observations.length);
  const evidenceDir=join(root,'evidence/local-recovery');mkdirSync(evidenceDir,{recursive:true});writeFileSync(join(evidenceDir,'events.jsonl'),readFileSync(events));
  const result={status:'passed',mode:'isolated-local-rehearsal',app_sha256:sha(readFileSync(join(root,'app/dist/server.js'))),worker_sha256:sha(readFileSync(join(root,'scripts/local-recovery-worker.mjs'))),observations,telemetry:{offered:observations.length+1,queued:observations.length,exported:received.length,rejected:1,dropped:0,pending:0,partial_success:0},negative_controls:{unhealthy_canary:503,dead_process:502,forbidden_telemetry_field:'rejected-before-persistence'},events_sha256:sha(readFileSync(events)),independent_production_observation:false,authority_effect:'none',open_questions_ref:'../../README.md#open-questions'};writeFileSync(join(evidenceDir,'result.json'),JSON.stringify(result,null,2)+'\n');return result;
 }finally{
  if(gateway){gateway.closeAllConnections();await new Promise(r=>gateway.close(r));}
  for(const child of children){if(child.exitCode===null&&child.signalCode===null){child.kill('SIGTERM');const timer=setTimeout(()=>child.kill('SIGKILL'),2000);await child.exited;clearTimeout(timer);}}
  rmSync(dir,{recursive:true,force:true});
 }
}

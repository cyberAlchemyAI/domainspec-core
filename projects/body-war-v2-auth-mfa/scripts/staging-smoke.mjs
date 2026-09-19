import assert from 'node:assert/strict';import {readFileSync,writeFileSync} from 'node:fs';import {resolve,join} from 'node:path';import {spawn} from 'node:child_process';import {runtimeEnv,inspectSnapshot} from './staging.mjs';
const root=resolve(new URL('..',import.meta.url).pathname),stage=join(root,'.runtime/staging'),config=JSON.parse(readFileSync(join(stage,'config.json')));
// Anonymous local smoke only: strip credentials so this cannot contact a real provider.
const env=runtimeEnv(stage,{...config,stravaClientId:'',stravaClientSecret:''});
const child=spawn(process.execPath,[join(stage,'app/dist/server.js')],{cwd:join(stage,'app'),env,stdio:'ignore'});
let exited=false;child.once('exit',()=>{exited=true;});
try{
 let ready=false;for(let i=0;i<100;i++){if(exited)throw Error('Staging smoke process exited');try{const r=await fetch('http://127.0.0.1:5186/api/status',{signal:AbortSignal.timeout(1000)});if(r.status===200){ready=true;break;}}catch{}await new Promise(r=>setTimeout(r,100));}
 assert.ok(ready);assert.equal(exited,false);
 assert.equal((await fetch('http://127.0.0.1:5186/')).status,200);
 assert.equal((await fetch('http://127.0.0.1:5186/api/suggested-tracks')).status,401);
 const login=await fetch('http://127.0.0.1:5186/api/auth/strava/start',{redirect:'manual'});assert.equal(login.status,400);
 writeFileSync(join(root,'evidence/staging-smoke.json'),JSON.stringify({status:'passed',database:'isolated-postgres',provider:'real-adapter-without-credentials',provider_requests:0,anonymous_archive_read:401,unconfigured_login:400,...inspectSnapshot(stage),live_activity_evidence:'pending-runner-login-and-consent',authority_effect:'none',open_questions_ref:'../STAGING-PLAN.md#open-questions'},null,2)+'\n');console.log('Staging anonymous smoke passed');
}finally{if(!exited){child.kill('SIGTERM');await new Promise(r=>child.once('exit',r));}}

import test from 'node:test';
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdtempSync, writeFileSync, readFileSync, rmSync, mkdirSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createGlmClient, MODEL, hash} from './transport.mjs';
import {runGlmAgent} from './agent.mjs';
import {validateCalls} from './tools.mjs';
import {parseConfig} from './cli.mjs';
import {createReadOnlyToolRuntime} from '../read-only-tools.mjs';
import {snapshotTree} from '../verifier.mjs';
import {createSecretReference, createSecretProviderRegistry, createInjectedSecretProvider} from '../secret-provider.mjs';

const tc = (id = 'call1', name = 'read-file', args = {path: 'a.mjs'}) => ({id, type: 'function', function: {name, arguments: JSON.stringify(args)}});
const reply = (message, finish_reason = 'stop', usage = {}) => ({model: MODEL, choices: [{message: {role: 'assistant', ...message}, finish_reason}], usage: {prompt_tokens: 100, completion_tokens: 20, ...usage}});
async function setup(t, handler = null, extra = {}) {
  const dir = mkdtempSync(join(tmpdir(), 'are-glm-test-')); const root = join(dir,'repo'); mkdirSync(root);
  writeFileSync(join(root,'a.mjs'), 'export const a=1;\n');
  const base = snapshotTree(root);
  const candidate = {schema_version:'are.patch-set-candidate/v1', expected_base_tree_sha256:base.tree_sha256, changes:[{operation:'replace-file',path:'a.mjs',expected_file_sha256:base.files['a.mjs'],utf8:'export const a=2;\n'}], rationale:'test',authority_effect:'none'};
  const requests = [];
  const server = createServer(async (req,res) => {
    const chunks=[]; for await (const c of req) chunks.push(c);
    const body=JSON.parse(Buffer.concat(chunks)); requests.push({path:req.url,body,auth:req.headers.authorization});
    res.setHeader('content-type','application/json');
    const value=await handler?.({req,res,body,requests,candidate});
    if (res.writableEnded || res.destroyed) return;
    if (value === 'stall') return;
    res.end(JSON.stringify(value ?? (req.url.endsWith('/tokenizer') ? {usage:{prompt_tokens:100}} : reply({content:JSON.stringify(candidate)}))));
  });
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  t.after(async()=>{server.closeAllConnections(); await new Promise(r=>server.close(r)); rmSync(dir,{recursive:true,force:true});});
  const origin=`http://127.0.0.1:${server.address().port}`;
  const clientOpts={chat_endpoint:origin+'/chat/completions',tokenizer_endpoint:origin+'/tokenizer',...extra};
  const client=createGlmClient(clientOpts);
  const input={run_id:'test',request:'Change a to 2',fixture_root:root,client,observation_allowlist:['a.mjs'],mutation_allowlist:['a.mjs'],verification_command:[],
    tool_runtime:createReadOnlyToolRuntime({repository_root:root,observation_allowlist:['a.mjs']}), tool_policy:{allow:['read-file','read-context-evidence']},
    context_recycling:{directory:join(dir,'state'),context_limit:10000,recycle_at:9000,safety_margin:1000,state:{objective:'Change a to 2',constraints:[],completed:[],pending:[],facts:[],lessons:[],evidence_refs:['test']}}};
  return {input,requests,candidate,root,dir,clientOpts};
}

test('tokenizer reservation, native round trip, reasoning preservation, proposal only',async t=>{
 const x=await setup(t,({req,requests})=>{
  if(req.url.endsWith('/tokenizer'))return;
  const n=requests.filter(r=>r.path.endsWith('/chat/completions')).length;
  if(n===1)return reply({content:'',reasoning_content:'preserve verbatim',tool_calls:[tc()]},'tool_calls');
 });
 const r=await runGlmAgent(x.input); assert.equal(r.status,'AWAITING_APPROVAL'); assert.equal(r.history.length,2);
 const bodies=x.requests.filter(r=>r.path.endsWith('/chat/completions')).map(r=>r.body);
 assert.equal(bodies[1].messages[2].reasoning_content,'preserve verbatim');
 assert.equal(bodies[1].messages[3].tool_call_id,'call1');
 assert.equal(bodies[0].max_tokens,2048);assert.equal(bodies[0].model,MODEL);assert.equal(bodies[0].thinking.clear_thinking,false);
 assert.deepEqual(x.requests[0].body.tools,bodies[0].tools);
 assert.equal(readFileSync(join(x.root,'a.mjs'),'utf8'),'export const a=1;\n');
});

test('safe pause and fresh-client resume preserve complete exchange',async t=>{
 const x=await setup(t,({req,requests})=>req.url.endsWith('/chat/completions') && requests.filter(r=>r.path.endsWith('/chat/completions')).length===1 ? reply({content:'',tool_calls:[tc()]},'tool_calls'):undefined);
 const first=await runGlmAgent({...x.input,pause_after_steps:1});assert.equal(first.status,'PAUSED');
 const r=await runGlmAgent({...x.input,client:createGlmClient(x.clientOpts)});assert.equal(r.status,'AWAITING_APPROVAL');assert.equal(r.history.length,2);
});

test('forced recycle archives whole exchanges and retains bounded progress',async t=>{
 const x=await setup(t,({req,body,requests})=>{
  if(req.url.endsWith('/tokenizer'))return {usage:{prompt_tokens:body.messages.length>2?7000:100}};
  if(requests.filter(r=>r.path.endsWith('/chat/completions')).length===1)return reply({content:'',tool_calls:[tc()]},'tool_calls');
 });
 const r=await runGlmAgent(x.input);assert.equal(r.status,'AWAITING_APPROVAL');assert.equal(r.recycling.recycles,1);
 const last=x.requests.filter(r=>r.path.endsWith('/chat/completions')).at(-1).body.messages;
 assert.equal(last.length,2);assert.match(last[0].content,/recent_progress/);assert.match(last[0].content,/call/);
});

for(const [label,payload,reason] of [
 ['truncated',reply({content:''},'length'),'incomplete-output'],
 ['wrong-model',{...reply({content:'{}'}),model:'glm-4.7'},'model-mismatch'],
 ['input-overrun',reply({content:'{}'},'stop',{prompt_tokens:9999}),'input-reservation-exceeded'],
 ['output-overrun',reply({content:'{}'},'stop',{completion_tokens:9999}),'output-cap-exceeded'],
 ['bad-tool',reply({tool_calls:[tc('id','delete-all')]},'tool_calls'),'tool-denied'],
 ['bad-json-args',reply({tool_calls:[{...tc(),function:{name:'read-file',arguments:'{'}}]},'tool_calls'),'tool-arguments-invalid'],
 ['bad-final',reply({content:'not a patch'}),'candidate-invalid']]) {
 test(label+' blocks with no tool or mutation',async t=>{
  const x=await setup(t,({req})=>req.url.endsWith('/chat/completions')?payload:undefined);
  let invoked=0; const r=await runGlmAgent({...x.input,tool_runtime:{...x.input.tool_runtime,invoke(){invoked++;}}});
  assert.equal(r.status,'BLOCK');assert.ok(r.reason_codes.includes('glm.'+reason),JSON.stringify(r));assert.equal(invoked,0);
  assert.equal(readFileSync(join(x.root,'a.mjs'),'utf8'),'export const a=1;\n');
 });
}

test('batch validation rejects duplicate IDs before any execution',()=>{
 assert.throws(()=>validateCalls([tc(),tc()],['read-file'],new Set(),[]),/duplicate/);
 assert.throws(()=>validateCalls([tc('old')],['read-file'],new Set(['old']),[]),/duplicate/);
 assert.throws(()=>validateCalls([tc('id','run-command',{command:['sh','-c','echo nope']})],['run-command'],new Set(),['node','--test']),/command-not-exact/);
});

test('billing code is classified and never retried or leaked',async t=>{
 const x=await setup(t,({req,res})=>{if(req.url.endsWith('/chat/completions')){res.statusCode=429;return {error:{code:'1113',message:'sensitive-provider-diagnostic'}};}});
 const r=await runGlmAgent(x.input);assert.deepEqual(r.reason_codes,['glm.billing-unavailable']);assert.equal(x.requests.length,2);assert.doesNotMatch(JSON.stringify(r),/sensitive-provider/);
 const again=await runGlmAgent(x.input);assert.equal(again.status,'BLOCK');assert.equal(x.requests.length,2);
});

test('unknown tokenizer count prevents model dispatch',async t=>{
 const x=await setup(t,()=>({usage:{}}));const r=await runGlmAgent(x.input);assert.deepEqual(r.reason_codes,['glm.tokenizer-count-invalid']);assert.equal(x.requests.length,1);
});

test('fresh context over threshold never dispatches',async t=>{
 const x=await setup(t,({req})=>req.url.endsWith('/tokenizer')?{usage:{prompt_tokens:10000}}:undefined);
 const r=await runGlmAgent(x.input);assert.equal(r.status,'BLOCK');assert.equal(x.requests.length,1);
});

test('timeout includes stalled response body and no retry',async t=>{
 const x=await setup(t,({req,res})=>{if(req.url.endsWith('/chat/completions')){res.writeHead(200);res.write('{');return 'stall';}}, {timeout_ms:60});
 const r=await runGlmAgent(x.input);assert.deepEqual(r.reason_codes,['glm.deadline-exceeded']);assert.equal(x.requests.length,2);
});

test('redirect not followed',async t=>{
 const x=await setup(t,({res})=>{res.statusCode=302;res.setHeader('location','https://example.com/');return {};});
 const r=await runGlmAgent(x.input);assert.equal(r.status,'BLOCK');assert.equal(x.requests.length,1);
});

test('secret exists only in authenticated request, not receipt or checkpoint',async t=>{
 const secret='synthetic-secret-not-real';
 const provider=createInjectedSecretProvider({provider_id:'fixture',resolve:async()=>Buffer.from(secret)});
 const x=await setup(t,null,{api_key_ref:createSecretReference({provider_id:'fixture',locator:'fixture'}),secret_registry:createSecretProviderRegistry({providers:[provider]})});
 const r=await runGlmAgent(x.input);assert.equal(r.status,'AWAITING_APPROVAL');
 assert.equal(x.requests[0].auth,'Bearer '+secret);assert.doesNotMatch(JSON.stringify(r),new RegExp(secret));
 assert.doesNotMatch(readFileSync(join(x.dir,'state','checkpoint.json'),'utf8'),new RegExp(secret));
});

test('checkpoint corruption and changed scope block before network',async t=>{
 const x=await setup(t,({req})=>req.url.endsWith('/chat/completions')?reply({tool_calls:[tc()]},'tool_calls'):undefined);
 assert.equal((await runGlmAgent({...x.input,pause_after_steps:1})).status,'PAUSED');
 const count=x.requests.length;
 assert.equal((await runGlmAgent({...x.input,mutation_allowlist:[]})).status,'BLOCK');
 const path=join(x.dir,'state','checkpoint.json');const value=JSON.parse(readFileSync(path));value.history=[];writeFileSync(path,JSON.stringify(value));
 assert.equal((await runGlmAgent(x.input)).status,'BLOCK');assert.equal(x.requests.length,count);
});

test('writer lock after process loss prevents blind replay',async t=>{
 const x=await setup(t);mkdirSync(join(x.dir,'state'));writeFileSync(join(x.dir,'state','writer.lock'),'');
 assert.equal((await runGlmAgent(x.input)).status,'BLOCK');assert.equal(x.requests.length,0);
});

test('request cap and duplicate IDs across turns stop loop',async t=>{
 const x=await setup(t,({req})=>req.url.endsWith('/chat/completions')?reply({tool_calls:[tc()]},'tool_calls'):undefined);
 const r=await runGlmAgent(x.input);assert.deepEqual(r.reason_codes,['glm.duplicate-or-invalid-tool-id']);assert.equal(r.history.length,1);
});

test('config rejects embedded keys and alternative models',()=>{
 assert.throws(()=>parseConfig({api_key:'no'}));
 assert.throws(()=>createGlmClient({chat_endpoint:'https://example.com/chat/completions'}),/endpoint-forbidden/);
});

import {createFixture, verifyCandidate} from './canary.mjs';
test('independent queue verifier accepts correct implementation and rejects wrong one', t=>{
 const dir=mkdtempSync(join(tmpdir(),'are-glm-verifier-'));t.after(()=>rmSync(dir,{recursive:true,force:true}));
 const root=createFixture(dir),base=snapshotTree(root);
 const candidate={schema_version:'are.patch-set-candidate/v1',expected_base_tree_sha256:base.tree_sha256,changes:[{operation:'replace-file',path:'src/queue.mjs',expected_file_sha256:base.files['src/queue.mjs'],utf8:`export function createQueue(){const jobs=new Map();return {enqueue(job){if(!job||typeof job!=='object'||Array.isArray(job)||typeof job.id!=='string'||!job.id)throw new TypeError();if(jobs.has(job.id))return false;jobs.set(job.id,job);return true},dequeue(){if(!jobs.size)return null;const [id,job]=jobs.entries().next().value;jobs.delete(id);return job},size(){return jobs.size}}}`}],authority_effect:'none'};
 assert.equal(verifyCandidate(root,candidate,join(dir,'good')).status,'PATCH_CANDIDATE');
 candidate.changes[0].utf8='export function createQueue(){return {enqueue(){return true},dequeue(){return null},size(){return 0}}}';
 assert.equal(verifyCandidate(root,candidate,join(dir,'bad')).status,'BLOCK');
});

test('verification denies network and reading host secrets', t=>{
 const dir=mkdtempSync(join(tmpdir(),'are-glm-permission-'));t.after(()=>rmSync(dir,{recursive:true,force:true}));
 const root=createFixture(dir),base=snapshotTree(root);
 for(const [name,source] of [['read',"import {readFileSync} from 'node:fs';readFileSync('/etc/passwd');"],['network',"import net from 'node:net';net.connect(80,'127.0.0.1');"]]){
 const candidate={schema_version:'are.patch-set-candidate/v1',expected_base_tree_sha256:base.tree_sha256,changes:[{operation:'replace-file',path:'src/queue.mjs',expected_file_sha256:base.files['src/queue.mjs'],utf8:source+' export function createQueue(){}'}],authority_effect:'none'};
 const r=verifyCandidate(root,candidate,join(dir,name));assert.equal(r.status,'BLOCK');assert.match(r.verification.stdout+r.verification.stderr,/ERR_ACCESS_DENIED/);
 }
});

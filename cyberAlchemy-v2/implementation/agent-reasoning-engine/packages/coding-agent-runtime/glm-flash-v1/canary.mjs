import {mkdtempSync, mkdirSync, writeFileSync, readFileSync, cpSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {runConfiguredGlm} from './cli.mjs';
import {runTransactionalPatchSet} from '../patch-set-runtime.mjs';
import {snapshotTree} from '../verifier.mjs';
import {hash, MODEL} from './transport.mjs';

const specification = `Implement createQueue() in src/queue.mjs, exporting it as a named function.
Each queue is independent and exposes enqueue(job), dequeue(), and size().
A job must be a non-null, non-array object with a non-empty string id; otherwise enqueue throws TypeError.
enqueue returns true when added. If that id is already queued it returns false and preserves the original job.
dequeue returns the oldest queued job, or null if empty. Removing a job frees its id for reuse.
size returns the number of currently queued jobs. Preserve FIFO order and do not mutate caller objects.
Inspect the source and README through tools before proposing a patch. Change only src/queue.mjs.`;
const tests = `import test from 'node:test';
import assert from 'node:assert/strict';
import {createQueue} from '../src/queue.mjs';
test('empty',()=>{const q=createQueue();assert.equal(q.size(),0);assert.equal(q.dequeue(),null);});
test('fifo',()=>{const q=createQueue();const a={id:'a',payload:1},b={id:'b',payload:2};assert.equal(q.enqueue(a),true);assert.equal(q.enqueue(b),true);assert.equal(q.size(),2);assert.deepEqual(q.dequeue(),a);assert.deepEqual(q.dequeue(),b);assert.equal(q.size(),0);});
test('duplicates preserve original',()=>{const q=createQueue();q.enqueue({id:'x',payload:1});assert.equal(q.enqueue({id:'x',payload:2}),false);assert.equal(q.size(),1);assert.deepEqual(q.dequeue(),{id:'x',payload:1});});
test('reuse after removal',()=>{const q=createQueue();q.enqueue({id:'x'});q.dequeue();assert.equal(q.enqueue({id:'x'}),true);assert.equal(q.size(),1);});
test('invalid jobs',()=>{for(const bad of [null,undefined,[],1,'a',{}, {id:''},{id:5}])assert.throws(()=>createQueue().enqueue(bad),TypeError);});
test('independent instances',()=>{const a=createQueue(),b=createQueue();a.enqueue({id:'one'});assert.equal(b.size(),0);assert.equal(b.dequeue(),null);});
test('frozen input and tricky IDs',()=>{const q=createQueue();for(const id of ['__proto__','constructor','toString'])assert.equal(q.enqueue(Object.freeze({id})),true);assert.equal(q.size(),3);assert.equal(q.dequeue().id,'__proto__');});
`;
export function createFixture(directory) {
 const root=join(directory,'fixture');mkdirSync(join(root,'src'),{recursive:true});mkdirSync(join(root,'test'));
 writeFileSync(join(root,'README.md'),specification+'\n');
 writeFileSync(join(root,'src','queue.mjs'),'export function createQueue() { throw new Error("not implemented"); }\n');
 writeFileSync(join(root,'test','queue.test.mjs'),tests);
 return root;
}
export function verifyCandidate(root, candidate, destination) {
 cpSync(root,destination,{recursive:true});
 const command=[process.execPath,'--permission',`--allow-fs-read=${destination}`,'--test','--test-isolation=none','--test-reporter=tap','test/queue.test.mjs'];
 const sandbox={run(actual){
   if(JSON.stringify(actual)!==JSON.stringify(command))return {ok:false,reason_codes:['verification.command-denied']};
   const r=spawnSync(actual[0],actual.slice(1),{cwd:destination,env:{LANG:'C',LC_ALL:'C'},encoding:'utf8',timeout:10000,maxBuffer:65536});
   const complete=r.status===0 && /^# tests 7\s*$/m.test(r.stdout??'') && /^# pass 7\s*$/m.test(r.stdout??'') && /^# fail 0\s*$/m.test(r.stdout??'');
   return {ok:complete,reason_codes:complete?[]:['verification.tests-failed'],observed_exit:r.status,
     stdout:r.stdout??'',stderr:r.stderr??'',permissions:'read fixture only; no writes, network, subprocesses, workers or addons',authority_effect:'none'};
 }};
 const result=runTransactionalPatchSet({run_id:'glm-canary-verification',fixture_root:destination,raw_candidate:candidate,
   mutation_allowlist:['src/queue.mjs'],approve:true,verification_sandbox:sandbox,verification_command:command});
 return result;
}

export async function runCanary() {
 const dir=mkdtempSync(join(tmpdir(),'are-glm-flash-canary-'));
 const root=createFixture(dir);const before=snapshotTree(root);
 const config={schema_version:'are.glm-flash-config/v1',model:MODEL,
   credential:{provider_kind:'local-sops-age',provider_id:'local-model-secrets',locator:'model/zai-key'},
   run_id:'glm-flash-queue-'+Date.now(),request:specification,fixture_root:root,state_directory:join(dir,'state'),
   observation_allowlist:['README.md','src/queue.mjs'],mutation_allowlist:['src/queue.mjs'],context_limit:16384,recycle_at:12000,safety_margin:1024};
 writeFileSync(join(dir,'config.json'),JSON.stringify(config,null,2)+'\n',{mode:0o600});
 console.log(JSON.stringify({status:'RUNNING',directory:dir,model:MODEL,maximum_model_calls:12,maximum_output_tokens:2048}));
 const output=await runConfiguredGlm(config);
 writeFileSync(join(dir,'agent-result.json'),JSON.stringify(output,null,2)+'\n',{mode:0o600});
 const verification=output.status==='AWAITING_APPROVAL'?verifyCandidate(root,output.candidate,join(dir,'verification')):null;
 const modelReceipts=output.receipts.filter(r=>r.kind==='model');
 const receipt={schema_version:'are.glm-live-canary/v1',model:MODEL,directory:dir,
  status:verification?.status==='PATCH_CANDIDATE'?'PASS_BOUNDED':'BLOCK',agent_status:output.status,reasons:output.reason_codes??[],
  model_requests:modelReceipts.length,tokenizer_requests:output.receipts.filter(r=>r.kind==='tokenizer').length,
  model_usage:{input:modelReceipts.reduce((s,r)=>s+(r.input_tokens??0),0),output:modelReceipts.reduce((s,r)=>s+(r.output_tokens??0),0),reasoning:modelReceipts.reduce((s,r)=>s+(r.reasoning_tokens??0),0),cached:modelReceipts.reduce((s,r)=>s+(r.cached_tokens??0),0)},
  elapsed_model_ms:modelReceipts.reduce((s,r)=>s+r.latency_ms,0),recycles:output.recycling?.recycles,
  original_fixture_unchanged:snapshotTree(root).tree_sha256===before.tree_sha256,
  verification,agent_result_sha256:hash(readFileSync(join(dir,'agent-result.json'),'utf8')),cost_usd:null,authority_effect:'none',product_approval:'not-requested'};
 writeFileSync(join(dir,'receipt.json'),JSON.stringify(receipt,null,2)+'\n',{mode:0o600});
 console.log(JSON.stringify({...receipt,verification:verification?{status:verification.status,changed_paths:verification.changed_paths,observed_exit:verification.verification?.observed_exit}:null}));
 return receipt;
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{const r=await runCanary();process.exitCode=r.status==='PASS_BOUNDED'?0:1;}catch{console.error('Canary failed; inspect private run directory.');process.exitCode=1;}
}

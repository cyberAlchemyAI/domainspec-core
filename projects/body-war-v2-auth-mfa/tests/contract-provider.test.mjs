import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,rmSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {resolve} from 'node:path';
const workspace=resolve('assurance/evf');
const spec=JSON.parse(readFileSync(workspace+'/audit.json'));
const checks=spec.checks.filter(c=>c.id.startsWith('contract-'));
test('17 exact contract providers accept current generated code and detect their source mutants',()=>{
 assert.equal(checks.length,17);
 for(const c of checks)for(const variant of [c,...c.negative_controls]){
  const r=spawnSync(process.execPath,['provider.mjs',variant.input],{cwd:workspace,encoding:'utf8'});assert.equal(r.status,0,c.id+' '+r.stderr);assert.deepEqual(JSON.parse(r.stdout),variant.expected,c.id+' '+variant.input);
 }
});
test('contract provider rejects an input bound to a different obligation',()=>{
 const name=workspace+'/bad-contract-binding.json';try{const input=JSON.parse(readFileSync(workspace+'/'+checks[0].input));writeFileSync(name,JSON.stringify({...input,obligation_key:'unbound'}));const r=spawnSync(process.execPath,['provider.mjs',name],{cwd:workspace,encoding:'utf8'});assert.notEqual(r.status,0);assert.match(r.stderr,/UNBOUND_CONTRACT/);}finally{rmSync(name,{force:true});}
});

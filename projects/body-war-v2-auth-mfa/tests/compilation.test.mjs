import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,readFileSync,writeFileSync,cpSync,rmSync,existsSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {spawnSync} from 'node:child_process';
const root=process.cwd();
const cli=join(root,'.tools/compiler/dist/cli/main.js');
function run(args){return spawnSync(process.execPath,[cli,...args],{encoding:'utf8'});}
test('DomainSpec rejects a modified generated rule after a passing direct CLI build',()=>{
 const temp=mkdtempSync(join(root,'.runtime/negative-code-'));
 try{
  const project=join(root,'app/src/compiled/project'),target=join(temp,'output');
  const args=['--language','typescript','--target-root',target];
  const built=run(['build',project,...args]);assert.equal(built.status,0,built.stderr);
  const baseline=run(['verify',project,...args]);assert.equal(baseline.status,0,baseline.stdout+baseline.stderr);
  const file=join(target,'src/domainspec/typescript/body-war-pilot/evidence-consent-required.ts');
  const source=readFileSync(file,'utf8');
  assert.ok(source.includes('return domainspecEvaluate(domainspecRuleRoot, parameters);'));
  writeFileSync(file,source.replace('return domainspecEvaluate(domainspecRuleRoot, parameters);','return true;'));
  const broken=run(['verify',project,...args]);assert.notEqual(broken.status,0,'Modified rule unexpectedly verified');
 }finally{rmSync(temp,{recursive:true,force:true});}
});
test('AlchLang rejects a changed authored model with an unchanged meaning binding',()=>{
 const temp=mkdtempSync(join(root,'.runtime/negative-source-'));
 try{
  const source=join(temp,'pilot.alch');
  cpSync(join(root,'model/pilot.alch'),source);
  cpSync(join(root,'model/pilot.alch.domainspec.json'),source+'.domainspec.json');
  writeFileSync(source,readFileSync(source,'utf8')+'\n# changed after binding\n');
  const alch=resolve(process.env.ALCHLANG_SOURCE_ROOT??'../../../cyberAlchemy-v2/language/capabilities/alchlang/plans/general-compiler-v1/implementation');
  const result=spawnSync(process.execPath,['--import',join(root,'node_modules/tsx/dist/loader.mjs'),join(alch,'src/cli.ts'),'build',source,'--profile','domainspec-1.0.0','--out',join(temp,'output')],{env:{...process.env,ALCHLANG_DOMAINSPEC_PACKAGE_ROOT:join(root,'.tools/compiler')},encoding:'utf8'});
  assert.notEqual(result.status,0);assert.match(result.stderr,/DIGEST|SHA256|SOURCE_HASH|SOURCE_DIGEST/i,result.stderr);
  assert.equal(existsSync(join(temp,'output')),false);
 }finally{rmSync(temp,{recursive:true,force:true});}
});

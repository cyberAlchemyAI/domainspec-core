import {readFileSync,writeFileSync,copyFileSync,mkdirSync} from 'node:fs';
import {join} from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {contractCases} from '../assurance/contracts/catalog.mjs';
export function bindContractCases(root,audit,tde,spec){
 const sha=b=>createHash('sha256').update(b).digest('hex');
 const save=(p,v)=>writeFileSync(p,JSON.stringify(v,null,2)+'\n');
 assert.equal(contractCases.length,17);
 copyFileSync(join(root,'assurance/contracts/catalog.mjs'),join(audit,'contract-cases.mjs'));
 const files=['normalization.js','query.js','request.js','validation.js'];
 const runtime=join(audit,'contract-runtime');mkdirSync(runtime,{recursive:true});save(join(runtime,'package.json'),{type:'module'});
 const tools=['contract-cases.mjs','contract-provider.mjs','contract-runtime/package.json'];
 const sourceHashes={};for(const file of files){const bytes=readFileSync(join(root,'app/dist/src/application',file));writeFileSync(join(runtime,file),bytes);tools.push('contract-runtime/'+file);sourceHashes[file]=sha(bytes);}
 const ontology=JSON.parse(readFileSync(join(root,'model/system-ontology.json')));
 const bindings=[];
 for(const g of contractCases){
  if(g.kind==='record')assert.equal(ontology.declarations.find(d=>d.id===g.entity)?.fields[g.field],g.ftype,'Authored type drift');
  const matches=tde.filter(o=>g.kind==='record'?o.rule_type==='domain-field'&&o.canonical_params.entity===g.entity&&o.canonical_params.field===g.field&&o.canonical_params.ftype===g.ftype.replaceAll('|',' / ')&&o.canonical_params.constraint===g.constraint:o.source_anchor.startsWith('operations.md#'+g.owner+':')&&o.canonical_params.id===g.field&&o.canonical_params.formal===g.formal);
  assert.equal(matches.length,1,'Contract semantics drift: '+g.id);const obligation=matches[0];assert.ok(!spec.obligations.includes(obligation.obligation_key),'duplicate coverage');
  const mutantRoot=join(audit,'contract-mutants',g.id);mkdirSync(mutantRoot,{recursive:true});save(join(mutantRoot,'package.json'),{type:'module'});const mutantFiles=['contract-mutants/'+g.id+'/package.json'];
  let mutation;
  for(const file of files){let bytes=readFileSync(join(runtime,file),'utf8');let from,to;
   if(file==='normalization.js'&&g.kind==='normalize'){if(g.mutation==='zero-distance-accepted'){from='value > 0';to='value >= 0';}else{from=".trim().slice(0, rule.max)";to='';}}
   if(file==='query.js'&&g.kind==='query'){from='n > rule.max';to='n > rule.max + 1';}
   if(file==='validation.js'&&g.kind==='record'){from=JSON.stringify(g.field)+': '+JSON.stringify(g.ftype);to=JSON.stringify(g.field)+': "unknown"';}
   if(from!==undefined){const before=sha(bytes);if(g.kind==='record'){const start=bytes.indexOf(JSON.stringify(g.entity)+': {');assert.ok(start>=0);const end=bytes.indexOf('\n    }',start);assert.ok(end>start);const section=bytes.slice(start,end);assert.equal(section.split(from).length,2,'Mutation anchor drift: '+g.id);bytes=bytes.slice(0,start)+section.replace(from,to)+bytes.slice(end);}else{assert.equal(bytes.split(from).length,2,'Mutation anchor drift: '+g.id);bytes=bytes.replace(from,to);}mutation={file,from,to,before_sha256:before,after_sha256:sha(bytes)};}
   writeFileSync(join(mutantRoot,file),bytes);mutantFiles.push('contract-mutants/'+g.id+'/'+file);
  }
  assert.ok(mutation);
  const id='contract-'+g.id;save(join(audit,id+'.json'),{kind:'contract',group:g.id,obligation_key:obligation.obligation_key,mutant:false});save(join(audit,id+'-mutant.json'),{kind:'contract',group:g.id,obligation_key:obligation.obligation_key,mutant:true});
  spec.obligations.push(obligation.obligation_key);spec.checks.push({id,provider:'node-generated-pilot',obligations:[obligation.obligation_key],executable:process.execPath,args:['provider.mjs','{input}'],tool_files:[...tools,...mutantFiles],input:id+'.json',expected:{outcome:'pass',reason_code:'CONTRACT_CASES',cases:g.cases.length,failed_cases:0},negative_controls:[{id:id+'-mutant',input:id+'-mutant.json',expected:{outcome:'fail',reason_code:'CONTRACT_MUTANT',cases:g.cases.length,failed_cases:g.mutant_failures},reason_code:'CONTRACT_MUTANT'}]});
  spec.bindings.push(...mutantFiles);bindings.push({id:g.id,obligation_key:obligation.obligation_key,cases:g.cases.length,mutation,claim:'finite executable witness; not general formal discharge'});
 }
 spec.bindings.push(...tools);spec.bindings=[...new Set(spec.bindings)];spec.subject='TROQAR finite generated consent, lifecycle, normalization, query and nested record contracts';spec.claim_ceiling='Finite executable witnesses for '+spec.obligations.length+' exact obligations; no general formal discharge or whole-program claim';
 save(join(root,'evidence/contract-bindings.json'),{source_hashes:sourceHashes,oracle_sha256:sha(readFileSync(join(root,'assurance/contracts/catalog.mjs'))),bindings,authority_effect:'none',open_questions_ref:'../README.md#open-questions'});
}

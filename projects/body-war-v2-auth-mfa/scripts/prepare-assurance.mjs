import {bindContractCases} from './bind-contract-cases.mjs';
import {readFileSync,writeFileSync,appendFileSync,mkdirSync,copyFileSync,realpathSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const root=resolve(fileURLToPath(new URL('..',import.meta.url)));
const ds=resolve(root,'../domainspec-v2');
const {parse}=await import(pathToFileURL(join(ds,'impl/test-derivation-engine/src/grammar/index.ts')));
const {derive}=await import(pathToFileURL(join(ds,'impl/test-derivation-engine/src/rules/index.ts')));
const save=(p,v)=>writeFileSync(p,JSON.stringify(v,null,2)+'\n');
const rulePath=join(root,'app/src/compiled/project/specs/body-war-pilot/nodes/evidence-consent-required.json');
const rule=JSON.parse(readFileSync(rulePath));
const projection=join(root,'assurance/consent-tde');mkdirSync(projection,{recursive:true});
// This bridge deliberately accepts only this boolean conjunction profile, and rejects other AST shapes.
function render(node){
 if(node.op==='all' && Array.isArray(node.terms) && node.terms.length)return node.terms.map(render).join(' and ');
 if(node.op==='eq' && node.left?.op==='path' && node.left.properties.length===0 && node.right?.op==='literal' && node.right.type==='Bool' && node.right.value===true)return node.left.root+' == true';
 throw Error('Unsupported consent obligation AST');
}
const expression=render(rule.body.typed_contract.expression);
if(expression!=='consent_acknowledged == true and activity_present == true and consent_text_present == true')throw Error('Unsupported consent obligation projection');
writeFileSync(join(projection,'operations.md'),'# Compiled consent projection\n\n## AttachActivityEvidenceCandidate\n\n### Rules\n\n| ID | Rule | Formal |\n| --- | --- | --- |\n| R1 | Explicit consent and activity identification precede persistence | `'+expression+'` |\n\n## Open Questions\n\nSee ../../README.md#open-questions.\n');
const parsed=parse(projection);if(parsed.violations.length)throw Error(parsed.violations.join('\n'));
const obligations=derive(parsed.graph);if(!obligations.length)throw Error('Empty consent obligation set');
const broader={};for(const feature of ['parque-taquaral-online-mvp','strava-linked-pilot']){const x=parse(join(root,'spec/pilot',feature));broader[feature]={violations:x.violations,obligations:derive(x.graph)};}
const ontologyPath=join(root,'model/system-ontology.json');
const declarations=JSON.parse(readFileSync(ontologyPath)).declarations;
const appProjection=join(root,'assurance/application-tde');mkdirSync(appProjection,{recursive:true});
const cell=x=>String(x).replaceAll('|',' / ').replaceAll('\n',' ');
const suffix='\n## Open Questions\n\nSee ../../README.md#open-questions.\n';
const records=declarations.filter(d=>d.kind==='record');
writeFileSync(join(appProjection,'domain.md'),'# Application domain\n\n## Entities\n\n'+records.map(d=>'### '+d.id+'\n\n| Field | Type | Constraint |\n| --- | --- | --- |\n'+Object.entries(d.fields).map(([k,t])=>'| '+k+' | '+cell(t)+' | '+(t.endsWith('?')?'optional':'required')+' |').join('\n')).join('\n\n')+suffix);
const ops=declarations.filter(d=>d.kind==='operation');
writeFileSync(join(appProjection,'operations.md'),'# Application operations\n\n'+ops.map(d=>'## '+d.id+'\n\n### Rules\n\n| ID | Rule | Formal |\n| --- | --- | --- |\n| AUTH | '+cell(d.meaning)+' | '+cell(JSON.stringify({authentication:d.authentication,permission:d.permission}))+' |\n'+d.effects.map((e,i)=>'| EFFECT'+i+' | Bound adapter effect | '+cell(e)+' |').join('\n')).join('\n\n')+suffix);
writeFileSync(join(appProjection,'states.md'),'# Application lifecycles\n\n'+declarations.filter(d=>d.kind==='lifecycle').map(d=>'## '+d.record+'\n\n### Transition Table\n\n| From | Event | To | Guard | Effect |\n| --- | --- | --- | --- | --- |\n'+d.transitions.map(t=>'| '+t.map(cell).join(' | ')+' | true | generated transition |').join('\n')).join('\n\n')+suffix);
writeFileSync(join(appProjection,'interfaces.md'),'# Application interfaces\n\n'+declarations.filter(d=>d.kind==='route').map(d=>'### '+d.method+' '+d.path+'\n\n**Responses:**\n\n| Status | Condition | Body |\n| --- | --- | --- |\n'+[...d.success.map(x=>'| '+x+' | success | '+ops.find(o=>o.id===d.operation).output+' |'),...d.errors.map(x=>'| '+x+' | adapter error | error response |')].join('\n')).join('\n\n')+suffix);
const criticalRequirements=declarations.find(d=>d.id==='CriticalRequirements')?.values.requirements??[];
appendFileSync(join(appProjection,'operations.md'),'\n## PilotCriticalRequirements\n\n### Rules\n\n| ID | Rule | Formal |\n| --- | --- | --- |\n'+criticalRequirements.map(r=>'| '+r.id+' | '+cell(r.formal)+' | '+cell(r.formal)+' |').join('\n')+'\n');
for(const n of declarations.filter(d=>d.kind==='normalization'))appendFileSync(join(appProjection,'operations.md'),'\n## '+n.id+'\n\n### Rules\n\n| ID | Rule | Formal |\n| --- | --- | --- |\n'+Object.entries(n.fields).map(([field,rule])=>'| '+field+' | '+cell(n.meaning)+' | '+cell(JSON.stringify({operation:n.operation,field,rule,error:n.error}))+' |').join('\n')+'\n');
for(const q of declarations.filter(d=>d.kind==='query'))appendFileSync(join(appProjection,'operations.md'),'\n## '+q.id+'\n\n### Rules\n\n| ID | Rule | Formal |\n| --- | --- | --- |\n'+Object.entries(q.fields).map(([field,rule])=>'| '+field+' | '+cell(q.meaning)+' | '+cell(JSON.stringify({operation:q.operation,field,rule,error:q.error}))+' |').join('\n')+'\n');
const appParsed=parse(appProjection);if(appParsed.violations.length)throw Error(appParsed.violations.join('\n'));
const appObligations=derive(appParsed.graph);if(!appObligations.length)throw Error('Empty application TDE obligations');
const application={ontology_sha256:createHash('sha256').update(readFileSync(ontologyPath)).digest('hex'),projection:'assurance/application-tde',violations:appParsed.violations,obligations:appObligations,critical_requirements:criticalRequirements,test_bindings:ops.map(d=>({operation:d.id,tests:d.tests,posture:'declared suite binding, not automatic obligation discharge'}))};
save(join(root,'evidence/tde.json'),{authority_effect:'none',application,compiled_rule_sha256:createHash('sha256').update(readFileSync(rulePath)).digest('hex'),projection:'compiled typed-rule AST to bounded exact consent conjunction; candidate bridge, not a general compiler adapter',obligations,broader,open_questions_ref:'../README.md#open-questions'});
const audit=join(root,'assurance/evf');mkdirSync(audit,{recursive:true});
copyFileSync(join(root,'app/dist/src/compiled/generated/src/domainspec/typescript/body-war-pilot/evidence-consent-required.js'),join(audit,'generated-rule.mjs'));
copyFileSync(rulePath,join(audit,'compiled-rule.json'));
copyFileSync(join(root,'evidence/tde.json'),join(audit,'tde.json'));
copyFileSync(join(root,'model/pilot.alch'),join(audit,'pilot.alch'));
save(join(audit,'positive.json'),{mutant:false});save(join(audit,'negative.json'),{mutant:true});
writeFileSync(join(audit,'obligation.md'),'# Consent requirement\nAccept only the all-true combination of acknowledged consent, activity identification and consent text. Exhaust all eight boolean combinations against the generated executable. A deliberately bypassed consent decision must be rejected. This proves only this finite rule, not authentication, provider consent or the whole application.\n\n## Open Questions\nSee ../../README.md#open-questions.\n');
const ids=obligations.map((_,i)=>'BW2-CONSENT-'+(i+1));
save(join(audit,'audit.json'),{schema_version:'evf.audit-spec/v1',audit_id:'body-war-v2-consent',subject:'TROQAR generated consent predicate',claim_ceiling:'Eight boolean combinations, candidate explicit TDE binding, no whole application or live provider claim',sources:['obligation.md','pilot.alch','tde.json'],bindings:['generated-rule.mjs','compiled-rule.json','provider.mjs'],obligations:ids,checks:[{id:'consent-truth-table',provider:'node-generated-rule',obligations:ids,executable:realpathSync(process.execPath),args:['provider.mjs','{input}'],tool_files:['generated-rule.mjs'],input:'positive.json',expected:{outcome:'pass',reason_code:'CONSENT_TRUTH_TABLE',cases:8,failed_cases:0},negative_controls:[{id:'bypass-consent',input:'negative.json',expected:{outcome:'fail',reason_code:'CONSENT_BYPASS',cases:8,failed_cases:7},reason_code:'CONSENT_BYPASS'}]}]});
// Exact obligation-key bindings for bounded generated consumers.
copyFileSync(join(root,'app/dist/src/application/domain.js'),join(audit,'generated-domain.mjs'));
copyFileSync(join(root,'app/dist/src/application/validation.js'),join(audit,'generated-validation.mjs'));
const auditSpec=JSON.parse(readFileSync(join(audit,'audit.json')));
const selected=appObligations.filter(o=>o.rule_type==='valid-transition'&&o.source_anchor.startsWith('states.md#SuggestedTrack:')||o.rule_type==='domain-field'&&o.canonical_params.entity==='LogoutResponse'&&o.canonical_params.field==='ok');
if(selected.length!==11)throw Error('Application obligation selection changed; review provider coverage');
auditSpec.subject='TROQAR bounded generated consent, lifecycle and response contracts';
auditSpec.claim_ceiling='Finite executable witnesses for 12 exact obligations; no general formal discharge or whole-program claim';
auditSpec.obligations=[obligations[0].obligation_key,...selected.map(o=>o.obligation_key)];
auditSpec.checks[0].obligations=[obligations[0].obligation_key];
auditSpec.bindings.push('application-provider.mjs','generated-domain.mjs','generated-validation.mjs');
for(const o of selected){const kind=o.rule_type==='valid-transition'?'transition':'logout-field',id='application-'+o.obligation_key;
 const input={kind,params:o.canonical_params,obligation_key:o.obligation_key,mutant:false};save(join(audit,id+'.json'),input);save(join(audit,id+'-mutant.json'),{...input,mutant:true});
 auditSpec.checks.push({id,provider:'node-generated-application',obligations:[o.obligation_key],executable:realpathSync(process.execPath),args:['application-provider.mjs','{input}'],tool_files:['generated-domain.mjs','generated-validation.mjs'],input:id+'.json',expected:{outcome:'pass',reason_code:'APPLICATION_CONTRACT',cases:kind==='transition'?1:5,failed_cases:0},negative_controls:[{id:id+'-bypass',input:id+'-mutant.json',expected:{outcome:'fail',reason_code:'APPLICATION_MUTANT',cases:kind==='transition'?1:5,failed_cases:kind==='transition'?1:3},reason_code:'APPLICATION_MUTANT'}]});
}
for(const check of auditSpec.checks){check.provider='node-generated-pilot';check.args=['provider.mjs','{input}'];check.tool_files=['application-provider.mjs','generated-rule.mjs','generated-domain.mjs','generated-validation.mjs'];}
bindContractCases(root,audit,appObligations,auditSpec);
save(join(audit,'audit.json'),auditSpec);
console.log(JSON.stringify({status:'prepared',application_obligations:appObligations.length,application_violations:appParsed.violations.length,consent_obligations:obligations.length,broader:Object.fromEntries(Object.entries(broader).map(([k,v])=>[k,{obligations:v.obligations.length,violations:v.violations.length}]))}));

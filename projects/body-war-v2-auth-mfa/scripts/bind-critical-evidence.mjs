import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const read=p=>JSON.parse(readFileSync(p)),sha=p=>createHash('sha256').update(readFileSync(p)).digest('hex');
const tde=read('evidence/tde.json'),ontology=sha('model/application-ontology.json'),coverage=read('evidence/obligation-coverage.json');
const requirements=tde.application.critical_requirements;
assert.equal(requirements.length,11);const bindings=[];
for(const req of requirements){
 assert.ok(['evidence/critical-security.json','evidence/critical-postgres.json'].includes(req.evidence));
 assert.ok(['scripts/critical-security.mjs','app/e2e/critical-integrity.e2e.ts'].includes(req.test));
 const evidence=read(req.evidence);assert.equal(evidence.status,'passed');assert.equal(evidence.ontology_sha256,ontology,'stale ontology binding');assert.equal(evidence.test_sha256,sha(req.test),'stale test binding');
 const cases=evidence.cases.filter(c=>c.id===req.case);assert.equal(cases.length,1);assert.equal(cases[0].status,'passed');
 const obligations=tde.application.obligations.filter(o=>o.source_anchor.startsWith('operations.md#PilotCriticalRequirements:')&&o.canonical_params.id===req.id&&o.canonical_params.formal===req.formal);assert.equal(obligations.length,1,'requirement drift');
 const obligation=coverage.obligations.find(o=>o.obligation_key===obligations[0].obligation_key);assert.ok(obligation);obligation.status='bounded-integration-verified';obligation.check=req.case;obligation.evidence=req.evidence;obligation.formal_discharge=false;
 bindings.push({requirement:req.id,obligation_key:obligation.obligation_key,case:req.case,evidence:req.evidence,evidence_sha256:sha(req.evidence),test:req.test,observed:cases[0].observed,formal_discharge:false});
}
coverage.bounded_integration_verified=bindings.length;coverage.unverified=coverage.obligations.filter(o=>o.status==='unverified').length;
assert.equal(coverage.total,coverage.bounded_executable_verified+coverage.bounded_integration_verified+coverage.unverified);
writeFileSync('evidence/obligation-coverage.json',JSON.stringify(coverage,null,2)+'\n');writeFileSync('evidence/critical-coverage.json',JSON.stringify({status:'passed',bindings,claim_ceiling:'Exact synthetic security and PostgreSQL integration witnesses; no general formal or production qualification',authority_effect:'none',open_questions_ref:'../README.md#open-questions'},null,2)+'\n');console.log(JSON.stringify({critical_requirements:bindings.length,total:coverage.total,unverified:coverage.unverified}));

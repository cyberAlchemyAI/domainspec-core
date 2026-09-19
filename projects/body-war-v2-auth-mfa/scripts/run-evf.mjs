import {execFileSync} from 'node:child_process';
import {readFileSync,writeFileSync,realpathSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('..',import.meta.url));
const evf=resolve(root,'.tools/evf/evf-audit-kit-0.4.0/evf'),workspace=resolve(root,'assurance/evf');
const prefix=['--runtime',dirname(realpathSync(process.execPath))];
const run=(args)=>JSON.parse(execFileSync(evf,[...prefix,...args],{encoding:'utf8',maxBuffer:8*1024*1024}));
const frozen=run(['freeze','--workspace',workspace]);
const executed=run(['run','--workspace',workspace,'--profile',frozen.profile,'--trust-local-providers']);
const verified=run(['verify','--workspace',workspace,'--evidence',executed.evidence]);
writeFileSync(resolve(root,'evidence/evf.json'),JSON.stringify({frozen,executed,verified,authority_effect:'none',open_questions_ref:'../README.md#open-questions'},null,2)+'\n');
if(executed.status!=='passed'||verified.verdict!=='passed')throw Error('EVF did not pass');
console.log(JSON.stringify({status:executed.status,verdict:verified.verdict,evidence:executed.evidence}));

const tde=JSON.parse(readFileSync(resolve(root,'evidence/tde.json'))),audit=JSON.parse(readFileSync(resolve(workspace,'audit.json')));
const coverage=[...tde.application.obligations,...tde.obligations].map(o=>{const check=audit.checks.find(c=>c.obligations.includes(o.obligation_key));return {obligation_key:o.obligation_key,source_anchor:o.source_anchor,rule_type:o.rule_type,status:check?'bounded-executable-verified':'unverified',check:check?.id??null,evidence:check?executed.evidence:null,formal_discharge:false};});
writeFileSync(resolve(root,'evidence/obligation-coverage.json'),JSON.stringify({total:coverage.length,bounded_executable_verified:coverage.filter(o=>o.status==='bounded-executable-verified').length,unverified:coverage.filter(o=>o.status==='unverified').length,formally_discharged:0,evf_verdict:verified.verdict,obligations:coverage,authority_effect:'none',open_questions_ref:'../README.md#open-questions'},null,2)+'\n');

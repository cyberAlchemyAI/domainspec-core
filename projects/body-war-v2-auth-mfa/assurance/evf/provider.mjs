import {readFileSync} from 'node:fs';
import {evidenceConsentRequired} from './generated-rule.mjs';
const input=JSON.parse(readFileSync(process.argv[2],'utf8'));
if(input.kind==='contract'){await import('./contract-provider.mjs');}else if(input.kind){await import('./application-provider.mjs');}else{
const {mutant}=input;
let failed=0;
for(let mask=0;mask<8;mask++){
 const actual=mutant?true:evidenceConsentRequired({consent_acknowledged:Boolean(mask&1),activity_present:Boolean(mask&2),consent_text_present:Boolean(mask&4)});
 if(actual!==(mask===7))failed++;
}
console.log(JSON.stringify({outcome:failed?'fail':'pass',reason_code:failed?'CONSENT_BYPASS':'CONSENT_TRUTH_TABLE',cases:8,failed_cases:failed}));

}

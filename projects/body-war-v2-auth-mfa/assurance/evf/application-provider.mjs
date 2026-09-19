import {readFileSync} from 'node:fs';
import {transition} from './generated-domain.mjs';
import {assertRecord} from './generated-validation.mjs';
const input=JSON.parse(readFileSync(process.argv[2],'utf8'));
let cases=0,failed=0;
if(input.kind==='transition'){
 cases=1;const p=input.params;let actual;try{actual=input.mutant?'BROKEN_TRANSITION':transition('TrackEvidenceLifecycle',p.from,p.event);}catch{actual='THREW';}if(actual!==p.to)failed++;
}else if(input.kind==='logout-field'){
 for(const [value,expected]of [[{ok:true},true],[{ok:false},true],[{},false],[{ok:'true'},false],[{ok:true,token:'synthetic'},false]]){cases++;let accepted=true;try{if(!input.mutant)assertRecord('LogoutResponse',value);}catch{accepted=false;}if(accepted!==expected)failed++;}
}else throw Error('UNSUPPORTED_OBLIGATION');
console.log(JSON.stringify({outcome:failed?'fail':'pass',reason_code:failed?'APPLICATION_MUTANT':'APPLICATION_CONTRACT',cases,failed_cases:failed}));

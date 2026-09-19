import {readFileSync} from 'node:fs';
import {isDeepStrictEqual} from 'node:util';
import {contractCases} from './contract-cases.mjs';
const input=JSON.parse(readFileSync(process.argv[2],'utf8'));
const group=contractCases.find(g=>g.id===input.group);
if(!group)throw Error('UNKNOWN_CONTRACT_CASE');
const obligation=JSON.parse(readFileSync(new URL('./tde.json',import.meta.url),'utf8')).application.obligations.find(o=>o.obligation_key===input.obligation_key);
if(!obligation||(group.kind==='record'?obligation.canonical_params.entity!==group.entity||obligation.canonical_params.field!==group.field||obligation.canonical_params.ftype!==group.ftype.replaceAll('|',' / ')||obligation.canonical_params.constraint!==group.constraint:!obligation.source_anchor.startsWith('operations.md#'+group.owner+':')||obligation.canonical_params.id!==group.field||obligation.canonical_params.formal!==group.formal))throw Error('UNBOUND_CONTRACT');
const moduleName=group.kind==='normalize'?'normalization':group.kind==='query'?'query':'validation';
const runtime=await import((input.mutant?'./contract-mutants/'+group.id+'/':'./contract-runtime/')+moduleName+'.js');
let failed=0;
for(const c of group.cases){
 if(group.kind==='record'){let accepted=true;try{runtime.assertRecord(group.entity,c.input);}catch(error){if(!error.message.startsWith('APPLICATION_RESPONSE_CONTRACT:'))throw error;accepted=false;}if(accepted!==c.accepted)failed++;}
 else{let actual;try{const value=group.kind==='query'?runtime.readQuery(new URL('http://localhost/?'+c.query),group.operation):runtime.normalizeRequest(group.operation,c.input);actual={value:value[group.field]};}catch(error){if(typeof error.code!=='string')throw error;actual={error:error.code};}if(!isDeepStrictEqual(actual,Object.hasOwn(c,'error')?{error:c.error}:{value:c.value}))failed++;}
}
console.log(JSON.stringify({outcome:failed?'fail':'pass',reason_code:failed?'CONTRACT_MUTANT':'CONTRACT_CASES',cases:group.cases.length,failed_cases:failed}));

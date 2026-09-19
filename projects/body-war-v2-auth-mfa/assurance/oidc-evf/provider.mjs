import {readFileSync} from 'node:fs';
const input=JSON.parse(readFileSync(process.argv[2],'utf8'));
const {stateStatus,authenticationTime}=await import(input.mutant?'./policy-mutant.mjs':'./policy.mjs');
let failed=0;const s={status:'active',last:100,absolute:28900};
const cases=[()=>stateStatus(s,999)==='active',()=>stateStatus(s,1000)==='session_expired',()=>stateStatus({...s,last:28899},28900)==='session_expired',()=>stateStatus({...s,status:'ended'},101)==='invalid_session',()=>stateStatus(undefined,101)==='invalid_session'];
for(const [auth,issued,fresh,time,expected] of [[100,100,true,101,true],[99,100,true,101,false],[102,100,true,101,false],[undefined,100,true,101,false],['100',100,true,101,false],[0,100,false,28801,false],[0,100,false,28800,true]])cases.push(()=>{let accepted=true;try{authenticationTime(auth,issued,fresh,time)}catch{accepted=false}return accepted===expected});
for(const run of cases)if(!run())failed++;
console.log(JSON.stringify({outcome:failed?'fail':'pass',reason_code:failed?'OIDC_POLICY_MUTANT':'OIDC_POLICY_BOUNDARIES',cases:cases.length,failed_cases:failed}));

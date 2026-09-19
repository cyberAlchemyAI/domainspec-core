import {test} from 'node:test';
import assert from 'node:assert/strict';
import {generateKeyPair,SignJWT,type JWTPayload} from 'jose';
import {authenticationTime,createAccessVerifier,OIDC_POLICY,stateStatus} from '../src/auth/oidc.js';
import {createMemoryBodyWarAuthRepository} from '../src/auth/memory-repository.js';
test('OIDC profile validates real signature and rejects cross-app identity tokens',async()=>{
 const keys=await generateKeyPair('RS256'),verify=createAccessVerifier(keys.publicKey),now=Math.floor(Date.now()/1000);
 const base={iss:OIDC_POLICY.issuer,sub:'alice',aud:OIDC_POLICY.audience,azp:OIDC_POLICY.client,typ:'Bearer',iat:now,exp:now+300,jti:crypto.randomUUID()};
 const token=(p:JWTPayload)=>new SignJWT(p).setProtectedHeader({alg:'RS256'}).sign(keys.privateKey);
 assert.equal((await verify(await token(base))).sub,'alice');
 for(const patch of [{aud:'prototype-api'},{azp:'prototype-browser'},{iss:'https://attacker.invalid'},{typ:'ID'},{exp:now-1},{exp:now+301},{iat:now+1}])await assert.rejects(()=>token({...base,...patch}).then(verify));
 const other=await generateKeyPair('RS256');await assert.rejects(()=>new SignJWT(base).setProtectedHeader({alg:'RS256'}).sign(other.privateKey).then(verify));
});
test('authentication freshness and session deadlines fail at their exact boundaries',()=>{
 authenticationTime(100,100,true,101);for(const value of [99,102,undefined,'100'])assert.throws(()=>authenticationTime(value,100,true,101));
 const state={status:'active' as const,last:100,absolute:28900};assert.equal(stateStatus(state,999),'active');assert.equal(stateStatus(state,1000),'session_expired');assert.equal(stateStatus({...state,last:28899},28900),'session_expired');assert.equal(stateStatus({...state,status:'ended'},101),'invalid_session');
});
test('provider account ownership cannot be stolen by an upsert',async()=>{
 const repo=createMemoryBodyWarAuthRepository();const input={provider:'strava' as const,principalId:'alice',providerUserId:'123',displayName:'Alice',scope:['read'],status:'linked' as const,metadata:{}};
 await repo.upsertProviderAccount(input);await assert.rejects(()=>repo.upsertProviderAccount({...input,principalId:'bob'}));await assert.rejects(()=>repo.upsertProviderAccount({...input,providerUserId:'456'}));
 assert.equal((await repo.findProviderAccountByPrincipalId('alice'))?.providerUserId,'123');assert.equal(await repo.findProviderAccountByPrincipalId('bob'),null);
});

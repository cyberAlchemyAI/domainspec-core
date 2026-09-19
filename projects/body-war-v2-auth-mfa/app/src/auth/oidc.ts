import {randomBytes,createHash} from 'node:crypto';
import * as oauth from 'openid-client';
import {createRemoteJWKSet,jwtVerify} from 'jose';
import type {MutableAuthRepositorySet} from '@domainspec/auth-user-management';
import type {createBrowserSessionAdapter,AuthenticateBrowserRequestInput} from './browser-session.js';
import type {BodyWarAuthRepository} from './body-war-repository.js';
import {seedRunnerPermissions} from './strava-oauth.js';
import {appError,type CookieMap} from './types.js';
import type {IncomingMessage,ServerResponse} from 'node:http';

import {OIDC_POLICY,authenticationTime,stateStatus} from './oidc-policy.js';
export {OIDC_POLICY,authenticationTime,stateStatus} from './oidc-policy.js';
export const SESSION_COOKIE='__Host-bw_session',LOGIN_COOKIE='__Host-bw_login';
const wall=()=>Math.floor(Date.now()/1000),random=()=>randomBytes(32).toString('base64url');
export const cookie=(name:string,value:string,age:number)=>`${name}=${value}; Secure; HttpOnly; SameSite=Lax; Path=/; Max-Age=${Math.max(0,age)}`;
export function requestCookies(req:IncomingMessage):CookieMap {const out:CookieMap={};for(const part of (req.headers.cookie??'').split(';')){const index=part.indexOf('=');if(index<0)continue;const key=part.slice(0,index).trim();if(Object.hasOwn(out,key))throw Error('Duplicate cookie');out[key]=part.slice(index+1);}return out;}
export function createAccessVerifier(keys?:Parameters<typeof jwtVerify>[1]){
 const jwks=keys??createRemoteJWKSet(new URL(OIDC_POLICY.issuer+'/protocol/openid-connect/certs'),{timeoutDuration:3000});
 return async(token:string)=>{const {payload:p}=await jwtVerify(token,jwks,{issuer:OIDC_POLICY.issuer,audience:OIDC_POLICY.audience,algorithms:['RS256'],requiredClaims:['iss','sub','aud','iat','exp','jti'],clockTolerance:0});if(p.typ!=='Bearer'||p.azp!==OIDC_POLICY.client||!Number.isInteger(p.iat)||!Number.isInteger(p.exp)||p.iat!>wall()||p.exp!-p.iat!>300)throw Error('Token profile rejected');return p;};
}
type Local=ReturnType<typeof createBrowserSessionAdapter>;
type State={key:string;subject:string;issuerSession:unknown;created:number;last:number;absolute:number;tokenDeadline:number;accessToken:string;idToken:string;status:'active'|'ended';tail:Promise<unknown>};
type Transaction={state:string;nonce:string;verifier:string;issued:number;expires:number;parent:State|undefined;renew:boolean;consumed:boolean;cancelled:boolean};


export function createOidcBoundary(deps:{browser:Local;repos:MutableAuthRepositorySet;bodyWarRepo:BodyWarAuthRepository;secret:string;clock?:(()=>number)|undefined}) {
 if(!deps.secret||deps.secret.length<32)throw Error('OIDC client secret required');
 const now=deps.clock??wall,states=new Map<string,State>(),transactions=new Map<string,Transaction>(),verify=createAccessVerifier();
 let configPromise:Promise<oauth.Configuration>|undefined;
 const config=()=>configPromise??=(oauth.discovery(new URL(OIDC_POLICY.issuer),OIDC_POLICY.client,deps.secret,undefined,{timeout:3}).catch(e=>{configPromise=undefined;throw e;}));
 const status=(s:State|undefined)=>stateStatus(s,now());
 function cancel(id:string|undefined){if(!id)return;const t=transactions.get(id);if(t)t.cancelled=true;transactions.delete(id);}
 function invalidate(s:State|undefined){if(!s)return;s.status='ended';states.delete(s.key);for(const [id,t] of transactions)if(t.parent===s)cancel(id);}
 function clean(){for(const [id,t] of transactions)if(t.expires<=now())cancel(id);for(const s of states.values())if(status(s)!=='active')invalidate(s);}
 async function tokenActive(s:State){const p=await verify(s.accessToken),r=await oauth.tokenIntrospection(await config(),s.accessToken);if(!r.active||r.sub!==p.sub||r.client_id!==OIDC_POLICY.client||r.exp!==p.exp)throw Error('Inactive identity');}
 async function guard(cookies:CookieMap,allowExpiredToken=false){clean();const s=states.get(cookies[SESSION_COOKIE]??'');if(status(s)!=='active')throw appError('session_expired',401,'Your session expired. Sign in again.');if(!allowExpiredToken&&s!.tokenDeadline<=now())throw appError('session_renewal_required',401,'Continue sign-in to renew your session.');if(!allowExpiredToken)await tokenActive(s!);if(status(s)!=='active'||states.get(s!.key)!==s)throw appError('session_expired',401,'Your session expired. Sign in again.');return s!;}
 function redirect(res:ServerResponse,to:string,values:string[]=[]){res.writeHead(303,{location:to,'cache-control':'no-store','set-cookie':values});res.end();}
 function failed(res:ServerResponse){redirect(res,'/?auth_error=oidc_sign_in_failed',[cookie(LOGIN_COOKIE,'',0)]);}
 async function lease<T>(s:State,work:()=>Promise<T>):Promise<T>{const previous=s.tail;let release!:()=>void;s.tail=new Promise<void>(r=>{release=r});await previous;try{if(status(s)!=='active'||states.get(s.key)!==s)throw Error('Session ended');return await work();}finally{release();}}
 const browser:Local={...deps.browser,
  async authenticate(input:AuthenticateBrowserRequestInput){
   const local=await deps.browser.authenticate(input);if(!local.ok)return local;
   try{await guard(input.cookies,input.route==='POST /api/auth/logout');return local;}catch(error){return {ok:false,error:typeof error==='object'&&error&&'code' in error?error as ReturnType<typeof appError>:appError('identity_unavailable',401,'Identity could not be verified')};}
  },
  async logout(cookies:CookieMap){const s=states.get(cookies[SESSION_COOKIE]??'');invalidate(s);cancel(cookies[LOGIN_COOKIE]);if(s)await s.tail;await deps.browser.logout(cookies);},
 };
 return {browser,
  async start(req:IncomingMessage,res:ServerResponse){try{
   clean();if(transactions.size>=256||states.size>=256)throw Error('Capacity');
   const cookies=requestCookies(req),candidate=states.get(cookies[SESSION_COOKIE]??''),parent=status(candidate)==='active'?candidate:undefined;
   const renew=Boolean(parent&&parent.tokenDeadline<=now());const conf=await config();
   if(parent&&status(parent)!=='active')throw Error('Session expired');
   cancel(cookies[LOGIN_COOKIE]);const id=random(),t:Transaction={state:oauth.randomState(),nonce:oauth.randomNonce(),verifier:oauth.randomPKCECodeVerifier(),issued:wall(),expires:now()+180,parent,renew,consumed:false,cancelled:false};
   if(transactions.size>=256)throw Error('Capacity');transactions.set(id,t);
   const url=oauth.buildAuthorizationUrl(conf,{redirect_uri:OIDC_POLICY.origin+'/api/auth/oidc/callback',scope:'openid',state:t.state,nonce:t.nonce,code_challenge:await oauth.calculatePKCECodeChallenge(t.verifier),code_challenge_method:'S256',max_age:renew?String(OIDC_POLICY.max):'0',prompt:renew?'none':'login',...(renew?{id_token_hint:parent!.idToken}:{})});
   redirect(res,url.href,[cookie(LOGIN_COOKIE,id,180)]);
  }catch{failed(res);}},
  async callback(req:IncomingMessage,res:ServerResponse,url:URL){let newCookie:string|undefined;let phase="transaction";try{
   clean();const cookies=requestCookies(req),id=cookies[LOGIN_COOKIE],t=transactions.get(id??'');if(!t||t.consumed||t.cancelled||t.expires<=now())throw Error('Transaction');t.consumed=true;
   phase="code_exchange";const tokens=await oauth.authorizationCodeGrant(await config(),url,{pkceCodeVerifier:t.verifier,expectedState:t.state,expectedNonce:t.nonce,idTokenExpected:true});
   phase="token_profile";const claims=tokens.claims(),p=await verify(tokens.access_token);if(!claims||claims.sub!==p.sub)throw Error('Identity mismatch');phase="freshness";authenticationTime(claims.auth_time,t.issued,!t.renew);
   phase="introspection";const r=await oauth.tokenIntrospection(await config(),tokens.access_token);if(!r.active||r.sub!==p.sub||r.client_id!==OIDC_POLICY.client||r.exp!==p.exp)throw Error('Inactive');
   const check=()=>{if(t.cancelled||t.expires<=now()||transactions.get(id!)!==t||(t.parent&&(status(t.parent)!=='active'||states.get(t.parent.key)!==t.parent||cookies[SESSION_COOKIE]!==t.parent.key)))throw Error('Cancelled');if(t.renew&&(t.parent!.subject!==p.sub||t.parent!.issuerSession!==claims.sid))throw Error('Renewal identity mismatch');};check();
   phase="local_identity";const identifier='oidc:'+createHash('sha256').update(JSON.stringify([OIDC_POLICY.issuer,p.sub])).digest('hex');
   let principal=await deps.repos.principalRepo.findByIdentifier(identifier);
   if(!principal){try{principal=await deps.repos.principalRepo.create({identifier,subjectType:'user',roleKeys:['runner'],directPermissions:['body-war.profile.read'],credentialHash:'external:oidc'});}catch(error){principal=await deps.repos.principalRepo.findByIdentifier(identifier);if(!principal)throw error;}}
   await seedRunnerPermissions(deps.repos);if(!await deps.bodyWarRepo.findRunnerProfile(principal.id))await deps.bodyWarRepo.upsertRunnerProfile({principalId:principal.id,displayName:'Runner'});
   check();const absolute=t.renew?t.parent!.absolute:now()+OIDC_POLICY.max;
   const created=await deps.browser.createSession({principalId:principal.id,ttlSeconds:Math.max(1,absolute-now()),metadata:{provider:'oidc',issuer:OIDC_POLICY.issuer}});if(!created.ok)throw Error('Local session');newCookie=created.value.binding.sessionCookie;
   check();if(states.size>=256&&!t.parent)throw Error('Capacity');
   const next:State={key:newCookie,subject:p.sub!,issuerSession:claims.sid,created:t.renew?t.parent!.created:now(),last:t.renew?t.parent!.last:now(),absolute,tokenDeadline:now()+Math.max(0,p.exp!-wall()),accessToken:tokens.access_token,idToken:tokens.id_token!,status:'active',tail:Promise.resolve()};
   cancel(id);invalidate(t.parent);states.set(newCookie,next);
   redirect(res,'/',[deps.browser.sessionCookieHeader(created.value.binding,absolute-now()),deps.browser.csrfCookieHeader(created.value.binding,absolute-now()),cookie(LOGIN_COOKIE,'',0)]);newCookie=undefined;
  }catch(error){console.error(JSON.stringify({event:"oidc_callback_rejected",phase,code:error instanceof Error&&"code" in error?String(error.code):"validation_failed"}));if(newCookie)await deps.browser.logout({[SESSION_COOKIE]:newCookie});failed(res);}},
  touch(cookies:CookieMap){const s=states.get(cookies[SESSION_COOKIE]??'');if(status(s)==='active')s!.last=now();},
  async linkBinding(cookies:CookieMap){const s=await guard(cookies),local=await deps.browser.authenticate({cookies,method:'GET'});if(!local.ok)throw Error('Local session');return {principalId:local.value.principalId,nonce:local.value.principalId+':'+createHash('sha256').update(s.key).digest('hex'),commit:<T>(work:()=>Promise<T>)=>lease(s,work)};},
 };
}

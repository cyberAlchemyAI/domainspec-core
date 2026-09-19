import {createOidc,createStore,createSecurityHandler,SessionError,policy} from '@auth-foundation/session-core';
import {createHash} from 'node:crypto';
import type {MutableAuthRepositorySet} from '@domainspec/auth-user-management';
import type {createBrowserSessionAdapter,AuthenticateBrowserRequestInput} from './browser-session.js';
import type {BodyWarAuthRepository} from './body-war-repository.js';
import {seedRunnerPermissions} from './strava-oauth.js';
import {appError,type CookieMap} from './types.js';
import {OIDC_POLICY} from './oidc-policy.js';
import {cookie,requestCookies,SESSION_COOKIE,LOGIN_COOKIE} from './oidc.js';
import type {IncomingMessage,ServerResponse} from 'node:http';
type Local=ReturnType<typeof createBrowserSessionAdapter>;
export function createDurableOidcBoundary(deps:{browser:Local;repos:MutableAuthRepositorySet;bodyWarRepo:BodyWarAuthRepository;secret:string;clock?:(()=>number)|undefined}){
 const databaseUrl=process.env.BODY_WAR_DATABASE_URL,key=process.env.BODY_WAR_DURABLE_KEY;
 if(!databaseUrl||!key||process.env.BODY_WAR_AUTH_BACKEND!=='postgres')throw Error('Durable identity requires explicit PostgreSQL and encryption key');
 const store=createStore({databaseUrl,namespace:'body-war',key,clock:deps.clock});
 const core=createOidc({profile:{...OIDC_POLICY,callback:'/api/auth/oidc/callback',securityPath:'/api/auth/security',secret:deps.secret},store,provision:async(identity,ttl)=>{
  const identifier='oidc:'+createHash('sha256').update(JSON.stringify([identity.issuer,identity.subject])).digest('hex');
  let principal=await deps.repos.principalRepo.findByIdentifier(identifier);
  if(!principal){try{principal=await deps.repos.principalRepo.create({identifier,subjectType:'user',roleKeys:['runner'],directPermissions:['body-war.profile.read'],credentialHash:'external:oidc'});}catch(error){principal=await deps.repos.principalRepo.findByIdentifier(identifier);if(!principal)throw error;}}
  await seedRunnerPermissions(deps.repos);if(!await deps.bodyWarRepo.findRunnerProfile(principal.id))await deps.bodyWarRepo.upsertRunnerProfile({principalId:principal.id,displayName:'Runner'});
  const local=await deps.browser.createSession({principalId:principal.id,ttlSeconds:ttl,metadata:{provider:'oidc',issuer:identity.issuer}});if(!local.ok)throw Error('Local identity rejected');
  return {principalId:principal.id,localCookie:local.value.binding.sessionCookie,csrf:local.value.binding.csrfToken};
 }});
 const mapped=(error:unknown)=>error instanceof SessionError?appError(error.code,error.status,'Your session could not be used. Sign in again.'):appError('identity_unavailable',503,'Identity service is unavailable');
 const browser:Local={...deps.browser,
  clearCookieHeaders:()=>[cookie(SESSION_COOKIE,"",0),"bw_csrf=; Secure; SameSite=Lax; Path=/; Max-Age=0",cookie(LOGIN_COOKIE,"",0)],
  async authenticate(input:AuthenticateBrowserRequestInput){try{
   const handle=input.cookies[SESSION_COOKIE];if(!handle)return {ok:false,error:appError('auth_required',401,'Sign in required')};
   let s;
   if(input.route==='POST /api/auth/logout'){
    if(input.headers?.origin!==OIDC_POLICY.origin)throw new SessionError('origin_not_allowed',403);
    const csrf=input.cookies.bw_csrf;if(!csrf||csrf!==input.headers?.['x-csrf-token'])throw new SessionError('csrf_required',403);
    s=await core.checkLogout(handle,csrf);if(!s)return {ok:false,error:appError('invalid_session',401,'Already signed out')};
   }else s=await core.authenticate(handle);
   if(!s.localCookie)throw Error('Local binding unavailable');
   if(!['GET','HEAD','OPTIONS'].includes(input.method.toUpperCase())&&input.route!=='POST /api/auth/logout'&&input.cookies.bw_csrf!==s.csrf)throw new SessionError('csrf_required',403);
   return deps.browser.authenticate({...input,cookies:{...input.cookies,[SESSION_COOKIE]:s.localCookie}});
  }catch(error){return {ok:false,error:mapped(error)};}},
  async logout(cookies:CookieMap){const s=await core.logout(cookies[SESSION_COOKIE],cookies[LOGIN_COOKIE]);if(s?.localCookie)await deps.browser.logout({[SESSION_COOKIE]:s.localCookie});},
 };
 const redirect=(res:ServerResponse,url:string,values:string[])=>{res.writeHead(303,{location:url,'cache-control':'no-store','set-cookie':values});res.end();};
 const failed=(res:ServerResponse)=>redirect(res,'/?auth_error=oidc_sign_in_failed',[cookie(LOGIN_COOKIE,'',0),cookie(SESSION_COOKIE,'',0),"bw_csrf=; Secure; SameSite=Lax; Path=/; Max-Age=0"]);
 return {browser,store,security:createSecurityHandler({core,path:'/api/auth/security',sessionCookie:SESSION_COOKIE,loginCookie:LOGIN_COOKIE,cookies:requestCookies}),
  async start(req:IncomingMessage,res:ServerResponse){try{const c=requestCookies(req),t=await core.start(c[SESSION_COOKIE],c[LOGIN_COOKIE],{fresh:new URL(req.url!,OIDC_POLICY.origin).searchParams.get('renew')!=='1'});redirect(res,t.url,[cookie(LOGIN_COOKIE,t.login,policy.transaction)]);}catch{failed(res);}},
  async callback(req:IncomingMessage,res:ServerResponse,url:URL){try{const c=requestCookies(req),s=await core.complete(url,c[SESSION_COOKIE],c[LOGIN_COOKIE]??'');const age=Math.max(0,Math.floor(s.absolute-s.now));redirect(res,s.returnTo??'/',[cookie(SESSION_COOKIE,s.id!,age),`bw_csrf=${s.csrf}; Secure; SameSite=Lax; Path=/; Max-Age=${age}`,cookie(LOGIN_COOKIE,'',0)]);}catch(error){if(error instanceof SessionError&&error.code==='renewal_login_required'){const c=requestCookies(req),t=await core.start(undefined,c[LOGIN_COOKIE],{fresh:true});return redirect(res,t.url,[cookie(SESSION_COOKIE,'',0),cookie(LOGIN_COOKIE,t.login,policy.transaction)]);}if(error instanceof SessionError&&error.code==='invalid_login'){try{await core.authenticate(requestCookies(req)[SESSION_COOKIE]);return redirect(res,'/',[]);}catch{}}if(error instanceof SessionError&&error.code==='security_action_finished'){redirect(res,'/?auth_error=security_action_finished',[cookie(SESSION_COOKIE,'',0),cookie(LOGIN_COOKIE,'',0)]);}else failed(res);}},
  touch(c:CookieMap){void core.touch(c[SESSION_COOKIE]).catch(()=>{});},
  async linkBinding(c:CookieMap){const s=await core.authenticate(c[SESSION_COOKIE]);if(!s.principalId)throw Error('Missing local principal');return {principalId:s.principalId,nonce:s.principalId+':'+createHash('sha256').update(c[SESSION_COOKIE]??'').digest('hex'),commit:<T>(work:()=>Promise<T>)=>core.withSession(c[SESSION_COOKIE],async current=>{if(current.family!==s.family||current.generation!==s.generation)throw Error('Session changed');return work();})};},
 };
}

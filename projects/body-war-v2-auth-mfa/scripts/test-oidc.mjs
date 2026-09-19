import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve} from 'node:path';
import {launchBrowser} from '../../auth-foundation/implementation/authentication-https/scripts/browser.mjs';
import {fixture,root} from './oidc-env.mjs';
const foundation=resolve(root,'../auth-foundation/implementation/authentication-https');
const owner=JSON.parse(readFileSync(resolve(foundation,'.runtime/config.json')));
const browser=await launchBrowser(),checks=[];
function passed(id){checks.push({id,status:'passed'});console.log('PASS '+id);}
async function request(page,path,method='GET',body,csrf=true){return page.evaluate(async({path,method,body,csrf})=>{const token=document.cookie.split('; ').find(c=>c.startsWith('bw_csrf='))?.slice(8);const r=await fetch(path,{method,headers:{...(body!==undefined?{'content-type':'application/json'}:{}),...(csrf&&token?{'x-csrf-token':decodeURIComponent(token)}:{})},...(body!==undefined?{body:JSON.stringify(body)}:{})});return {status:r.status,body:await r.json()};},{path,method,body,csrf});}
async function login(username,password){const context=await browser.newContext(),page=await context.newPage();await page.goto(fixture.origin);await page.locator('#connect').click();await page.locator('#username').fill(username);await page.locator('#password').fill(password);await page.locator('#kc-login').click();await page.waitForURL(u=>u.origin===fixture.origin,{timeout:15000});await page.waitForFunction(async()=>{const s=await(await fetch('/api/status')).json();return s.authenticated});return {context,page};}
try{
 const {context:a,page}=await login('alice',owner.userPassword);
 const initial=await request(page,'/api/status');assert.equal(initial.body.authenticated,true);assert.equal(initial.body.identity_mode,'oidc');assert.equal((await request(page,'/api/profile')).status,200);passed('real-oidc-primary-identity');
 const cookies=await a.cookies(fixture.origin),session=cookies.find(c=>c.name==='__Host-bw_session');assert.ok(session?.secure&&session.httpOnly&&session.sameSite==='Lax'&&session.path==='/'&&session.domain==='body-war.localhost');assert.equal(await page.evaluate(()=>JSON.stringify({...localStorage,...sessionStorage})),'{}');passed('host-isolated-http-only-session-no-browser-token-storage');
 assert.equal((await request(page,'/api/auth/strava/start')).status,405);assert.equal((await request(page,'/api/auth/strava/link','POST',{},false)).status,403);passed('legacy-entry-disabled-and-link-csrf-required');
 const principal=(await request(page,'/api/profile')).body;assert.equal(typeof principal.profile.principal_id,'string');
 if(!initial.body.connected){await page.locator('#link-strava').click();await page.waitForURL(u=>u.searchParams.get('connected')==='1');}
 await page.waitForFunction(async()=> (await(await fetch('/api/status')).json()).connected);
 assert.equal((await request(page,'/api/activities')).status,200);const linked=(await request(page,'/api/profile')).body;assert.equal(linked.profile.principal_id,principal.profile.principal_id);passed('strava-link-preserves-oidc-identity-and-unlocks-activities');
 const current=(await a.cookies(fixture.origin)).find(c=>c.name==='__Host-bw_session');assert.equal(current.value,session.value);passed('provider-callback-does-not-issue-session');
 await page.goto(fixture.origin+'/api/auth/oidc/callback?code=replayed&state=wrong');assert.equal(new URL(page.url()).searchParams.get('auth_error'),'oidc_sign_in_failed');assert.equal((await request(page,'/api/status')).body.authenticated,true);passed('unsolicited-oidc-callback-rejected-without-replacing-session');
 await new Promise(r=>setTimeout(r,2500));
 const {context:b,page:bob}=await login('body-war-test-bob',fixture.bobPassword);assert.equal((await request(bob,'/api/status')).body.connected,false);assert.ok((await request(bob,'/api/activities')).status>=400);
 await bob.locator('#link-strava').click();await bob.waitForURL(u=>u.searchParams.has('auth_error'));assert.equal(new URL(bob.url()).searchParams.get('auth_error'),'provider_link_rejected');assert.equal((await request(bob,'/api/status')).body.connected,false);assert.equal((await request(page,'/api/status')).body.connected,true);passed('second-identity-cannot-steal-strava-account');
 assert.equal((await request(page,'/api/auth/logout','POST',{})).status,200);assert.equal((await request(page,'/api/profile')).status,401);
 const replay=await browser.newContext();await replay.addCookies(cookies);const rp=await replay.newPage();await rp.goto(fixture.origin);assert.equal((await request(rp,'/api/profile')).status,401);await replay.close();passed('logout-revokes-copied-session-cookie');
 await page.goto(fixture.origin+'/api/auth/oidc/start');await page.locator('#kc-login').waitFor();assert.equal(new URL(page.url()).origin,new URL(fixture.issuer).origin);passed('post-logout-entry-requires-fresh-login');
 await request(bob,'/api/auth/logout','POST',{});await b.close();await a.close();
 const anon=await browser.newContext(),ap=await anon.newPage();await ap.goto(fixture.origin);assert.equal((await request(ap,'/api/auth/strava/link','POST',{})).status,401);await ap.goto(fixture.origin+'/api/auth/strava/callback?code=fake&state=unrequested');assert.equal((await request(ap,'/api/status')).body.authenticated,false);passed('strava-callback-cannot-create-primary-identity');await anon.close();
}finally{await browser.close();mkdirSync(resolve(root,'evidence'),{recursive:true});writeFileSync(resolve(root,'evidence/oidc-live.json'),JSON.stringify({status:checks.length===10?'passed':'incomplete',checks,issuer:'real local Keycloak',tls:'trusted CA; no verification bypass',provider:'fake Strava only',authority_effect:'none',open_questions_ref:'../OIDC-PROTOTYPE.md#open-questions'},null,2)+'\n');}
assert.equal(checks.length,10);

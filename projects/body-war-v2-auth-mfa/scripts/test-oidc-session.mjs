// Test-only in-process clock. No HTTP endpoint or environment variable can advance it.
import assert from 'node:assert/strict';import {readFileSync,writeFileSync} from 'node:fs';import {resolve} from 'node:path';
import {configure,fixture,root} from './oidc-env.mjs';
import {launchBrowser} from '../../auth-foundation/implementation/authentication-https/scripts/browser.mjs';
configure();let offset=0;const clock=()=>Math.floor(Date.now()/1000)+offset;
const {resetAuthComponentsForTests}=await import('../app/dist/server.js');resetAuthComponentsForTests(clock);
const {server}=await import('./start-oidc.mjs');if(!server.listening)await new Promise(r=>server.once('listening',r));
const owner=JSON.parse(readFileSync(resolve(root,'../auth-foundation/implementation/authentication-https/.runtime/config.json'))),browser=await launchBrowser(),context=await browser.newContext(),page=await context.newPage(),checks=[];
const pass=id=>{checks.push({id,status:'passed'});console.log('PASS '+id)};
async function get(path='/api/status'){return page.evaluate(async p=>{const r=await fetch(p);return {status:r.status,body:await r.json()}},path)}
async function fresh(){await page.goto(fixture.origin+'/api/auth/oidc/start');if(await page.locator('#username').isVisible())await page.locator('#username').fill('alice');await page.locator('#password').fill(owner.userPassword);await page.locator('#kc-login').click();await page.waitForURL(u=>u.origin===fixture.origin);await page.waitForLoadState("networkidle");assert.equal((await get()).body.authenticated,true);}
async function post(path){return page.evaluate(async p=>{const csrf=document.cookie.split('; ').find(c=>c.startsWith('bw_csrf='))?.slice(8);const r=await fetch(p,{method:'POST',headers:{'content-type':'application/json','x-csrf-token':decodeURIComponent(csrf)},body:'{}'});return {status:r.status,body:await r.json()}},path)}
try{
 await fresh();const before=(await context.cookies(fixture.origin)).find(c=>c.name==='__Host-bw_session').value;
 offset+=301;assert.equal((await get('/api/profile')).body.error,'session_renewal_required');
 let passwordPage=false;page.on('framenavigated',frame=>{if(frame===page.mainFrame()&&frame.url().includes('/login-actions/authenticate'))passwordPage=true});
 await page.goto(fixture.origin+'/api/auth/oidc/start');await page.waitForURL(u=>u.origin===fixture.origin);await page.waitForLoadState("networkidle");assert.equal((await get('/api/profile')).status,200);assert.equal(passwordPage,false);const after=(await context.cookies(fixture.origin)).find(c=>c.name==='__Host-bw_session').value;assert.notEqual(after,before);pass('active-session-renews-through-real-oidc-and-rotates-cookie');
 // Status polling must never count as activity; token renewal itself also preserves the activity deadline.
 offset+=901;assert.equal((await get()).body.authenticated,false);assert.equal((await get('/api/profile')).body.error,'session_expired');pass('background-status-does-not-prevent-idle-expiration');
 await page.goto(fixture.origin+'/api/auth/oidc/start');await page.locator('#kc-login').waitFor();pass('idle-expiry-requires-password-despite-issuer-sso');
 if(await page.locator('#username').isVisible())await page.locator('#username').fill('alice');await page.locator('#password').fill(owner.userPassword);await page.locator('#kc-login').click();await page.waitForURL(u=>u.origin===fixture.origin);await page.waitForLoadState("networkidle");assert.equal((await get()).body.authenticated,true);
 const link=await post('/api/auth/strava/link');assert.equal(link.status,200);assert.equal((await post('/api/auth/logout')).status,200);await page.goto(new URL(link.body.url,fixture.origin).href);assert.equal((await get()).body.authenticated,false);assert.equal(new URL(page.url()).searchParams.get('auth_error'),'provider_link_session_expired');pass('logout-cancels-inflight-provider-link-without-restoring-identity');
 await fresh();offset+=28800;assert.equal((await get('/api/profile')).body.error,'session_expired');pass('absolute-expiry-rejects-local-cookie');
 assert.equal((await post('/api/auth/logout')).status,200);pass('expired-session-logout-is-idempotent');
}finally{await browser.close();await new Promise(r=>server.close(r));writeFileSync(resolve(root,'evidence/oidc-session.json'),JSON.stringify({status:checks.length===6?'passed':'incomplete',checks,clock:'in-process test dependency; real Keycloak and TLS',provider:'fake Strava',authority_effect:'none',open_questions_ref:'../OIDC-PROTOTYPE.md#open-questions'},null,2)+'\n');}
assert.equal(checks.length,6);

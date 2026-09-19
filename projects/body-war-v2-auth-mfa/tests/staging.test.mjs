import test from 'node:test';import assert from 'node:assert/strict';
import {runtimeEnv} from '../scripts/staging.mjs';
test('staging ignores inherited production, fake-provider and OIDC settings',()=>{
 const c={sessionSecret:'a'.repeat(64),tokenProtectionSecret:'b'.repeat(64),databasePassword:'c'.repeat(64),stravaClientId:'123',stravaClientSecret:'private-test'};
 const env=runtimeEnv('/isolated',c,{PATH:'/usr/bin',BODY_WAR_DATABASE_URL:'production',DATABASE_URL:'production',BODY_WAR_STRAVA_FAKE:'1',BODY_WAR_IDENTITY_MODE:'oidc',BODY_WAR_OIDC_CLIENT_SECRET:'other',NODE_OPTIONS:'--import=bad',STRAVA_REDIRECT_URI:'https://other.invalid'});
 assert.equal(env.BODY_WAR_STRAVA_FAKE,'0');assert.equal(env.BODY_WAR_IDENTITY_MODE,'strava-pilot');assert.equal(env.BODY_WAR_HOST,'127.0.0.1');assert.equal(env.DATABASE_URL,undefined);assert.equal(env.BODY_WAR_OIDC_CLIENT_SECRET,undefined);assert.equal(env.NODE_OPTIONS,undefined);assert.match(env.BODY_WAR_DATABASE_URL,/@127\.0\.0\.1:55486\/body_war_staging$/);assert.equal(env.STRAVA_REDIRECT_URI,'http://127.0.0.1:5186/api/auth/strava/callback');assert.equal(env.PATH,'/usr/bin');
 assert.throws(()=>runtimeEnv('/isolated',{...c,sessionSecret:'dev-secret'}),/Invalid/);
});

import {mkdtempSync,mkdirSync,writeFileSync,rmSync,readFileSync,statSync} from 'node:fs';import {join} from 'node:path';import {tmpdir} from 'node:os';import {prepare,inspectSnapshot} from '../scripts/staging.mjs';
test('snapshot preserves archives, refuses overwrites, and detects changed code or source archives',()=>{
 const base=mkdtempSync(join(tmpdir(),'bw-stage-test-')),source=join(base,'source'),dest=join(base,'stage');
 try{
  for(const p of ['app/dist/server.js','app/static/index.html','app/drizzle/0000.sql','vendor/auth/dist/index.js','vendor/auth/drizzle/0000.sql','vendor/auth/package.json','app/data/tracks.json','app/data/track-submissions.json','package-lock.json']){mkdirSync(join(source,p,'..'),{recursive:true});writeFileSync(join(source,p),'{}');}
  prepare(source,dest);assert.equal(inspectSnapshot(dest).archives_unchanged,true);assert.equal(statSync(join(dest,'config.json')).mode&0o077,0);assert.throws(()=>prepare(source,dest),/refusing/);
  assert.equal(readFileSync(join(source,'app/data/track-submissions.json'),'utf8'),'{}');
  writeFileSync(join(dest,'app/dist/server.js'),'changed');assert.throws(()=>inspectSnapshot(dest),/integrity mismatch/);writeFileSync(join(dest,'app/dist/server.js'),'{}');
  writeFileSync(join(source,'app/data/tracks.json'),'changed');assert.throws(()=>inspectSnapshot(dest),/source:app\/data\/tracks/);
 }finally{rmSync(base,{recursive:true,force:true});}
});

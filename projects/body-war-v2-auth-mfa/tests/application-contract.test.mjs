import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdtempSync,mkdirSync,cpSync,rmSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
const root=process.cwd();
process.env.ALCHLANG_DOMAINSPEC_PACKAGE_ROOT=join(root,'.tools/compiler');
const alch=resolve(process.env.ALCHLANG_SOURCE_ROOT??'../../../cyberAlchemy-v2/language/capabilities/alchlang/plans/general-compiler-v1/implementation');
const {loadApplication}=await import(pathToFileURL(join(alch,'src/application-contract.ts')));
// Current pilot routes and separately configured OIDC/link routes.
const expected=['POST /api/evidence-candidates/:id/withdraw','GET /api/auth/security','POST /api/auth/security','GET /api/auth/oidc/start','GET /api/auth/oidc/callback','POST /api/auth/strava/link','GET /api/status','GET /api/profile','GET /api/auth/strava/start','GET /api/auth/strava/callback','GET /api/activities','GET /api/suggested-tracks','POST /api/suggested-tracks','GET /api/suggested-tracks/:idOrSlug','POST /api/suggested-tracks/:idOrSlug/evidence-candidates','POST /api/auth/logout'].sort();
test('model describes exactly the entire independently inventoried pilot HTTP surface',async()=>{
 const p=await loadApplication(join(root,'body-war.alch'));
 assert.deepEqual(p.declarations.filter(d=>d.kind==='route').map(d=>d.method+' '+d.path).sort(),expected);
 for(const id of ['ProviderAccount','RunnerProfile','OAuthState','ProviderTokenRecord','ActivitySummary','SuggestedTrack','ActivityEvidenceCandidate'])assert.equal(p.byId[id].kind,'record');
 for(const id of ['TdeAssurance','EvfAssurance','OrodiAssurance'])assert.equal(p.byId[id].required,true);
 assert.deepEqual(p.byId.PilotUi.pages,['/','/profile']);
 assert.equal(p.byId.AttachEvidence.authentication,'connected');
 assert.equal(p.byId.AttachEvidence.permission,'body-war.suggested-track-evidence.create');
});
async function mutated(edit,expectedError){const tmp=mkdtempSync(join(root,'.runtime/application-negative-'));try{
 for(const name of ['body-war.alch','model','app/src','app/tests','app/ui','app/drizzle','vendor/auth/src','scripts']){mkdirSync(join(tmp,name,'..'),{recursive:true});cpSync(join(root,name),join(tmp,name),{recursive:true});}
 edit(tmp);await assert.rejects(()=>loadApplication(join(tmp,'body-war.alch')),expectedError);
}finally{rmSync(tmp,{recursive:true,force:true});}}
function replace(tmp,path,a,b){const f=join(tmp,path),s=readFileSync(f,'utf8');assert.ok(s.includes(a));writeFileSync(f,s.replace(a,b));}
test('unknown adapter export is rejected before generation',()=>mutated(t=>replace(t,'model/identity.alch','entry "handleStatus"','entry "missingHandler"'),/unbound export/));
// Tests below mutate meaning-bearing declarations, not generated receipts.
test('unbound operation cannot be dispatched',()=>mutated(t=>replace(t,'model/tracks.alch','operation "ReadTrack"','operation "MissingHandler"'),/unknown operation/));
test('storage mapping cannot omit a domain field',()=>mutated(t=>replace(t,'model/infrastructure.alch','"principalId":"principal_id",',''),/storage field coverage/));
test('duplicate normalized routes are rejected',()=>mutated(t=>{const f=join(t,'model/tracks.alch');writeFileSync(f,readFileSync(f,'utf8')+'\nroute DuplicateRoute:\n  meaning "Deliberate ambiguous route."\n  method "GET"\n  path "/api/suggested-tracks/:other"\n  operation "ReadTrack"\n  success [200]\n  errors [404]\n');},/duplicate or ambiguous/));
test('path escape is rejected',()=>mutated(t=>replace(t,'model/ui.alch','../app/ui/index.html','../../outside.html'),/source escapes/));

test('normalization rejects invalid bounds, unknown fields and arbitrary rule kinds',async()=>{
 for(const [a,b] of [['"min":1,"max":255','"min":256,"max":255'],['"name":{"kind":"text"','"missing":{"kind":"text"'],['"kind":"text"','"kind":"eval"']])await mutated(t=>replace(t,'model/tracks.alch',a,b),/normalization/);
});

test('query rejects invalid defaults, missing coverage and unknown kinds',async()=>{
 for(const [a,b] of [['"max":10,"default":1','"max":10,"default":11'],['"page":{"kind":"integer"','"missing":{"kind":"integer"'],['"kind":"integer"','"kind":"execute"']])await mutated(t=>replace(t,'model/activities.alch',a,b),/query/);
});

import {spawnSync} from 'node:child_process';
import {readFileSync,writeFileSync,mkdirSync,readdirSync,existsSync} from 'node:fs';
import {resolve,join,relative} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=resolve(fileURLToPath(new URL('..',import.meta.url)));
process.chdir(root);
const id=new Date().toISOString().replaceAll(/[:.]/g,'-');
const dir=join(root,'evidence/runs',id);mkdirSync(dir,{recursive:true});
const stages=[];
function stage(name,command,args,needs=[]){
 if(needs.some(n=>stages.find(s=>s.name===n)?.status!=='passed')){stages.push({name,status:'not_evaluable',blockers:needs.filter(n=>stages.find(s=>s.name===n)?.status!=='passed')});return false;}
 console.log('Running '+name);
 const started=new Date().toISOString();
 const r=spawnSync(command,args,{cwd:root,encoding:'utf8',maxBuffer:24*1024*1024,timeout:600000,env:{...process.env,BODY_WAR_STRAVA_FAKE:'1',BODY_WAR_AUTH_BACKEND:'memory',BODY_WAR_CHROMIUM_EXECUTABLE:process.env.BODY_WAR_CHROMIUM_EXECUTABLE??join(root,'.tools/chromium-1217/chrome-linux64/chrome'),LD_LIBRARY_PATH:join(root,'.tools/browser-libs/root/usr/lib/x86_64-linux-gnu')}});
 const log=relative(root,join(dir,name+'.log'));writeFileSync(log,(r.stdout??'')+'\n'+(r.stderr??'')+(r.error?'\n'+r.error.stack:''));
 stages.push({name,status:r.status===0?'passed':'failed',exit_code:r.status,signal:r.signal,command:[command,...args],started,ended:new Date().toISOString(),log});return r.status===0;
}
const sha=b=>createHash('sha256').update(b).digest('hex');
function snapshot(){const files={};const excluded=new Set(['.git','node_modules','.tools','.runtime','evidence','dist','dist-test','data','test-results','playwright-report','.evf-runs','.evf-profiles']);function walk(d){for(const e of readdirSync(d,{withFileTypes:true})){if(excluded.has(e.name)||e.name.startsWith('.env'))continue;const f=join(d,e.name);if(e.isSymbolicLink())throw Error('Unexpected source symlink: '+f);if(e.isDirectory())walk(f);else files[relative(root,f)]=sha(readFileSync(f));}}walk(root);return Object.fromEntries(Object.entries(files).sort());}
function assuranceSources(){const files={};for(const rel of ['impl/test-derivation-engine/src','impl/operational-resilience/src','impl/operational-resilience/contracts']){const base=resolve(root,'../domainspec-v2',rel);function walk(d){for(const e of readdirSync(d,{withFileTypes:true})){const f=join(d,e.name);if(e.isSymbolicLink())throw Error('Assurance source symlink');if(e.isDirectory())walk(f);else files[f]=sha(readFileSync(f));}}walk(base);}return Object.fromEntries(Object.entries(files).sort());}
const archiveBefore=Object.fromEntries(['app/data/track-submissions.json','app/data/tracks.json'].filter(existsSync).map(p=>[p,sha(readFileSync(p))]));
const assuranceBefore=assuranceSources();
writeFileSync('provenance/assurance.json',JSON.stringify({files:assuranceBefore,authority_effect:'none',open_questions_ref:'../README.md#open-questions'},null,2)+'\n');
let candidate=null;
stage('model',process.execPath,['scripts/build-model.mjs']);
stage('compiler-negatives',process.execPath,['--test','tests/compilation.test.mjs'],['model']);
stage('application-contracts',process.execPath,['--import','tsx','--test','tests/application-contract.test.mjs','tests/generated-contracts.test.mjs'],['model']);
stage('build','npm',['run','build'],['model']);
stage('model-runtime',process.execPath,['--import','tsx','--test','--test-concurrency=1','tests/model-runtime.test.mjs'],['build']);
stage('native-cli-regression',process.execPath,['--import','tsx','--test','--test-name-pattern','product discovery|oversized project sources','.tools/compiler/test/cli/main.test.ts'],['model']);
stage('structure','sh',['app/scripts/validate.sh','--structure-only']);
stage('unit','npm',['test'],['build']);
stage('critical-security',process.execPath,['scripts/critical-security.mjs'],['build']);
stage('postgres','npm',['run','test:postgres'],['build']);
stage('browser','npm',['run','test:ui'],['build']);
stage('evf-setup',process.execPath,['scripts/prepare-evf.mjs']);
stage('oidc-policy-evf',process.execPath,['scripts/run-oidc-evf.mjs'],['build','evf-setup']);
stage('tde',process.execPath,['--import','tsx','scripts/prepare-assurance.mjs'],['build']);
if(stages.find(s=>s.name==='tde')?.status==='passed'){
 const files=snapshot();candidate={schema_version:'body-war-v2.candidate/v1',id,source_digest:sha(JSON.stringify(files)),files,authority_effect:'none',open_questions_ref:'../README.md#open-questions'};
 writeFileSync('evidence/candidate.json',JSON.stringify(candidate,null,2)+'\n');
}
stage('contract-providers',process.execPath,['--test','tests/contract-provider.test.mjs'],['tde']);
stage('evf',process.execPath,['scripts/run-evf.mjs'],['tde','evf-setup','contract-providers']);
stage('orodi',process.execPath,['--import','tsx','scripts/run-orodi.mjs'],['build','tde']);
const modelInput=existsSync('model/application-ontology.json')?JSON.parse(readFileSync('model/application-ontology.json')):null;
const staleInputs=modelInput?Object.entries(modelInput.sources).filter(([p,d])=>!existsSync(p)||sha(readFileSync(p))!==d).map(([p])=>p):[];
stages.push({name:'model-input-currentness',status:!modelInput?'not_evaluable':staleInputs.length?'failed':'passed',changed:staleInputs});
stage('critical-obligations',process.execPath,['scripts/bind-critical-evidence.mjs'],['critical-security','postgres','tde','evf']);
const assuranceAfter=assuranceSources();
stages.push({name:'assurance-source-currentness',status:JSON.stringify(assuranceBefore)===JSON.stringify(assuranceAfter)?'passed':'failed'});
if(candidate){const now=snapshot();const drift=Object.keys({...candidate.files,...now}).filter(k=>candidate.files[k]!==now[k]);stages.push({name:'source-currentness',status:drift.length?'failed':'passed',changed:drift});}else stages.push({name:'source-currentness',status:'not_evaluable',blockers:['tde']});
const gaps=[
 {id:'whole-application-generation',state:'partial',detail:'All current routes and domain/storage/UI/assurance contracts are authored in AlchLang. Dispatch, domain types, request normalization, recursive response guards, lifecycle, redaction and UI configuration are generated; IO and rendering remain explicitly bound adapters.'},
 {id:'whole-pilot-tde',state:'derived-not-discharged',detail:'Exact current counts are in obligation-coverage.json; finite EVF and critical integration witnesses remain distinct from general formal discharge. Inherited documents retain separate diagnostics.'},
 {id:'full-orodi',state:'not_evaluable',detail:'C01-C16 full operational readiness is rejected. Local canary failure, rollback, process loss/restart and collector export are exercised. Independent production deployment and remaining controls are unexecuted.'},
 {id:'live-strava',state:'not_run',detail:'User-selected local pilot validation uses fake Strava; real accounts are outside this campaign.'},
 {id:'additional-platform-capabilities',state:'not_bound',detail:'RWO, conformance factory/BTE and managed secrets are not wired into this retained pilot; see model/application-bindings.json.'},
 {id:'formal-and-release',state:'not_run',detail:'No Lean certification, general formal-provider campaign, release qualification or enterprise standards assessment.'}
];
const archiveChanged=Object.entries(archiveBefore).filter(([p,d])=>!existsSync(p)||sha(readFileSync(p))!==d).map(([p])=>p);
stages.push({name:'migration-archive-currentness',status:archiveChanged.length?'failed':'passed',changed:archiveChanged});
writeFileSync('evidence/migration-archive.json',JSON.stringify({files:archiveBefore,changed:archiveChanged,authority_effect:'none',open_questions_ref:'../README.md#open-questions'},null,2)+'\n');
const passed=stages.every(s=>s.status==='passed');
const result={schema_version:'body-war-v2.validation/v1',id,status:passed?'bounded-pilot-passed':'failed',whole_flow_status:'incomplete',candidate_digest:candidate?.source_digest??null,stages,gaps,authority_effect:'none',open_questions_ref:'../README.md#open-questions'};
writeFileSync(join(dir,'result.json'),JSON.stringify(result,null,2)+'\n');writeFileSync('evidence/validation.json',JSON.stringify(result,null,2)+'\n');
// Bind all current executable artifacts and retained evidence without digesting this inventory itself.
const artifacts={};for(const prefix of ['app/dist','vendor/auth/dist',relative(root,dir),'evidence/migration-archive.json','evidence/contract-bindings.json','evidence/critical-security.json','evidence/critical-postgres.json','evidence/critical-coverage.json','evidence/model-runtime.json','evidence/obligation-coverage.json','evidence/local-recovery','evidence/tde.json','evidence/evf.json','evidence/oidc-evf.json','evidence/orodi.json','evidence/candidate.json']){
 function record(f){const st=existsSync(f);if(!st)return;try{for(const e of readdirSync(f,{withFileTypes:true})){const child=join(f,e.name);if(e.isDirectory())record(child);else artifacts[child]=sha(readFileSync(child));}}catch(e){if(e.code!=='ENOTDIR')throw e;artifacts[f]=sha(readFileSync(f));}}record(prefix);
}
writeFileSync('evidence/artifacts.json',JSON.stringify({candidate_digest:result.candidate_digest,files:artifacts,authority_effect:'none',open_questions_ref:'../README.md#open-questions'},null,2)+'\n');
console.log(JSON.stringify({status:result.status,whole_flow_status:result.whole_flow_status,stages:stages.map(s=>({name:s.name,status:s.status})),result:'evidence/validation.json'},null,2));
process.exitCode=!passed?1:process.argv.includes('--pilot')?0:2;

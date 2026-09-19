import {cpSync,existsSync,mkdirSync,readFileSync,writeFileSync,readdirSync,statSync,lstatSync,symlinkSync} from 'node:fs';
import {resolve,join,relative} from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {createHash,randomBytes} from 'node:crypto';
import {spawnSync,spawn} from 'node:child_process';

const root=resolve(fileURLToPath(new URL('..',import.meta.url)));
const runtime=join(root,'.runtime/staging');
const sha=p=>createHash('sha256').update(readFileSync(p)).digest('hex');
const read=p=>JSON.parse(readFileSync(p,'utf8'));
function save(p,value){writeFileSync(p,JSON.stringify(value,null,2)+'\n',{mode:0o600,flag:'wx'});}
function files(dir){const out=[];for(const e of readdirSync(dir,{withFileTypes:true})){const p=join(dir,e.name);if(e.isSymbolicLink())throw Error('Snapshot source cannot contain symlinks');if(e.isDirectory())out.push(...files(p));else out.push(p);}return out;}
export function prepare(source,destination){
  if(existsSync(destination))throw Error('Staging already exists; refusing to overwrite data or secrets');
  for(const p of ['app/dist/server.js','app/static/index.html','app/drizzle','vendor/auth/dist','vendor/auth/drizzle'])if(!existsSync(join(source,p)))throw Error('Build the application before preparing staging');
  mkdirSync(destination,{recursive:true,mode:0o700});
  const copied=['app/dist','app/static','app/drizzle','vendor/auth/dist','vendor/auth/drizzle','vendor/auth/package.json'];
  for(const p of copied){mkdirSync(join(destination,p,'..'),{recursive:true});cpSync(join(source,p),join(destination,p),{recursive:true});}
  mkdirSync(join(destination,'app/data'),{recursive:true,mode:0o700});
  const archives={};
  for(const name of ['tracks.json','track-submissions.json']){
    const p=join(source,'app/data',name);if(!existsSync(p))throw Error('Source archive missing');
    if(lstatSync(p).isSymbolicLink())throw Error('Archive symlinks are not supported');
    archives['app/data/'+name]=sha(p);cpSync(p,join(destination,'app/data',name));
  }
  const hashes={};for(const p of copied)for(const f of statSync(join(destination,p)).isDirectory()?files(join(destination,p)):[join(destination,p)])hashes[relative(destination,f)]=sha(f);
  // Bind the copied auth package; other installed dependencies retain the existing lockfile.
  mkdirSync(join(destination,'node_modules/@domainspec'),{recursive:true});
  symlinkSync('../../vendor/auth',join(destination,'node_modules/@domainspec/auth-user-management'),'dir');
  save(join(destination,'snapshot.json'),{files:hashes,archives,package_lock_sha256:sha(join(source,'package-lock.json')),source,authority_effect:'none',open_questions_ref:'../../STAGING-PLAN.md#open-questions'});
  const config={stravaClientId:'',stravaClientSecret:'',sessionSecret:randomBytes(32).toString('hex'),tokenProtectionSecret:randomBytes(32).toString('hex'),databasePassword:randomBytes(32).toString('hex')};
  save(join(destination,'config.json'),config);
  save(join(destination,'compose.json'),{name:'body-war-live-staging',services:{postgres:{image:'postgres:16-alpine',environment:{POSTGRES_DB:'body_war_staging',POSTGRES_USER:'body_war_staging',POSTGRES_PASSWORD:config.databasePassword},ports:['127.0.0.1:55486:5432'],volumes:['staging-db:/var/lib/postgresql/data'],healthcheck:{test:['CMD-SHELL','pg_isready -U body_war_staging -d body_war_staging'],interval:'1s',timeout:'5s',retries:30}}},volumes:{'staging-db':{}}});
  return {status:'prepared',url:'http://127.0.0.1:5186',credentials_required:true};
}
export function inspectSnapshot(destination){
  const snapshot=read(join(destination,'snapshot.json'));const changed=[];
  for(const [p,h] of Object.entries({...snapshot.files,...snapshot.archives}))if(!existsSync(join(destination,p))||sha(join(destination,p))!==h)changed.push(p);
  for(const [p,h] of Object.entries(snapshot.archives))if(!existsSync(join(snapshot.source,p))||sha(join(snapshot.source,p))!==h)changed.push('source:'+p);
  if(sha(join(snapshot.source,'package-lock.json'))!==snapshot.package_lock_sha256)changed.push('package-lock.json');
  if(changed.length)throw Error('Staging integrity mismatch: '+changed.join(', '));
  return {snapshot_files:Object.keys(snapshot.files).length,archives_unchanged:true};
}
export function runtimeEnv(destination,config,parent=process.env){
  const clean=Object.fromEntries(Object.entries(parent).filter(([k])=>!k.startsWith('BODY_WAR_')&&!k.startsWith('STRAVA_')&&!['DATABASE_URL','SESSION_SECRET','NODE_ENV','NODE_OPTIONS'].includes(k)));
  if(![config.sessionSecret,config.tokenProtectionSecret,config.databasePassword].every(v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v)))throw Error('Invalid staging secret configuration');
  return {...clean,NODE_ENV:'development',BODY_WAR_APP_ROOT:join(destination,'app'),BODY_WAR_HOST:'127.0.0.1',BODY_WAR_PORT:'5186',BODY_WAR_PUBLIC_BASE_URL:'http://127.0.0.1:5186',BODY_WAR_ALLOWED_ORIGINS:'http://127.0.0.1:5186',STRAVA_REDIRECT_URI:'http://127.0.0.1:5186/api/auth/strava/callback',BODY_WAR_AUTH_BACKEND:'postgres',BODY_WAR_IDENTITY_MODE:'strava-pilot',BODY_WAR_STRAVA_FAKE:'0',BODY_WAR_SECURE_COOKIES:'0',BODY_WAR_SESSION_SECRET:config.sessionSecret,BODY_WAR_TOKEN_PROTECTION_SECRET:config.tokenProtectionSecret,BODY_WAR_DATABASE_URL:'postgres://body_war_staging:'+config.databasePassword+'@127.0.0.1:55486/body_war_staging',STRAVA_CLIENT_ID:config.stravaClientId,STRAVA_CLIENT_SECRET:config.stravaClientSecret};
}
function config(){const p=join(runtime,'config.json');if(statSync(p).mode&0o077)throw Error('Staging config must be private (chmod 600)');return read(p);}
function command(exe,args,env){const r=spawnSync(exe,args,{cwd:runtime,env,encoding:'utf8'});if(r.status!==0)throw Error('Staging command failed: '+exe+' (details suppressed to protect credentials)');}
async function main(action){
  if(action==='prepare'){console.log(JSON.stringify(prepare(root,runtime)));return;}
  if(!['status','database','serve','verify','stop-db'].includes(action))throw Error('Usage: node scripts/staging.mjs prepare|status|database|serve|verify|stop-db');
  const integrity=inspectSnapshot(runtime),c=config(),env=runtimeEnv(runtime,c);
  const credentials=typeof c.stravaClientId==='string'&&/^[1-9][0-9]*$/.test(c.stravaClientId)&&typeof c.stravaClientSecret==='string'&&c.stravaClientSecret.trim().length>0;
  if(action==='status'){console.log(JSON.stringify({...integrity,credentials_configured:credentials,url:env.BODY_WAR_PUBLIC_BASE_URL,live_activity_evidence:'not_yet_verified'}));return;}
  if(action==='stop-db'){command('docker',['compose','-f',join(runtime,'compose.json'),'stop'],env);console.log('Staging database stopped; volume retained');return;}
  if(action==='database'){
    command('docker',['compose','-f',join(runtime,'compose.json'),'up','-d','--wait'],env);
    command(process.execPath,[join(runtime,'app/dist/src/infrastructure/postgres/migrate-cli.js')],env);
    console.log('Isolated staging database ready; migrations applied');return;
  }
  if(action==='serve'){
    if(!credentials)throw Error('Set stravaClientId and stravaClientSecret in .runtime/staging/config.json; do not paste secrets into chat');
    const child=spawn(process.execPath,[join(runtime,'app/dist/server.js')],{cwd:join(runtime,'app'),env,stdio:'inherit'});
    for(const signal of ['SIGINT','SIGTERM'])process.on(signal,()=>child.kill(signal));
    child.on('exit',code=>{process.exitCode=code??1;});return;
  }
  const {default:postgres}=await import('postgres');const sql=postgres(env.BODY_WAR_DATABASE_URL,{max:1,onnotice:()=>{}});
  try{
    const migrations=await sql`select scope,filename from body_war_schema_migrations order by scope,filename`;
    const [counts]=await sql`select count(*)::int as total,count(distinct principal_id)::int as runners from body_war_activity_evidence_candidates`;
    const [privacy]=await sql`select count(*)::int as unexpected_summary_fields from body_war_activity_evidence_candidates c where exists(select 1 from jsonb_object_keys(c.redacted_summary::jsonb) k where k not in ('id','name','sport_type','type','distance','moving_time','average_speed','start_date'))`;
    const report={...integrity,migrations,counts,...privacy,live_provider_verified:false,manual_evidence_required:['Runner confirms successful live fetch','One selected activity and destination','Fresh consent','Cross-track replay rejected without second write'],authority_effect:'none',open_questions_ref:'../../STAGING-PLAN.md#open-questions'};
    writeFileSync(join(runtime,'verification.json'),JSON.stringify(report,null,2)+'\n',{mode:0o600});console.log(JSON.stringify(report));
  }finally{await sql.end();}
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))main(process.argv[2]).catch(()=>{console.error('Staging operation failed. Check private configuration, build prerequisites, snapshot integrity, Docker and port availability. No data was reset.');process.exitCode=1;});

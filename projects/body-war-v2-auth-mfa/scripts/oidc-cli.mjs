import {spawn} from 'node:child_process';import {resolve} from 'node:path';
const root=resolve(new URL('..',import.meta.url).pathname),foundation=resolve(root,'../auth-foundation/implementation/authentication-https');
const tasks={start:'start-oidc.mjs',live:'test-oidc.mjs',session:'test-oidc-session.mjs'};const task=tasks[process.argv[2]];if(!task)throw Error('Use start, live or session');
const child=spawn(process.execPath,[resolve(root,'scripts',task)],{cwd:root,stdio:'inherit',env:{...process.env,NODE_EXTRA_CA_CERTS:resolve(foundation,'.runtime/tls/ca.crt'),LD_LIBRARY_PATH:resolve(foundation,'.runtime/browser-libs/root/usr/lib/x86_64-linux-gnu')}});
for(const signal of ['SIGTERM','SIGINT'])process.on(signal,()=>child.kill(signal));child.once('exit',(code,signal)=>{process.exitCode=code??(signal?1:0)});child.once('error',error=>{console.error(error.message);process.exitCode=1});

import https from 'node:https';import {readFileSync} from 'node:fs';import {resolve} from 'node:path';import {configure,runtime} from './oidc-env.mjs';
configure();const {handleRequest}=await import('../app/dist/server.js');
export const server=https.createServer({key:readFileSync(resolve(runtime,'server.key')),cert:readFileSync(resolve(runtime,'server.crt')),minVersion:'TLSv1.2',maxVersion:'TLSv1.3'},(req,res)=>{
 res.setHeader('cache-control','no-store');res.setHeader('x-content-type-options','nosniff');res.setHeader('referrer-policy','strict-origin');res.setHeader('content-security-policy',"default-src 'self'; img-src 'self' https: data:; frame-ancestors 'none'; base-uri 'none'; object-src 'none'; form-action 'self'");
 if(req.headers.host!=='body-war.localhost:14443'||Object.keys(req.headers).some(k=>k==='forwarded'||k.startsWith('x-forwarded-'))){res.writeHead(400);res.end();return;}
 void handleRequest(req,res);
});server.requestTimeout=5000;server.headersTimeout=5000;server.maxHeadersCount=40;server.listen(14443,'127.0.0.1',()=>console.log('Body War v2: https://body-war.localhost:14443'));
for(const signal of ['SIGINT','SIGTERM'])process.on(signal,()=>server.close(()=>process.exit(0)));

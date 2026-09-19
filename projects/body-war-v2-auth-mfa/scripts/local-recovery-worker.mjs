import {createServer} from 'node:http';
import {appendFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
const [mode,target,fault]=process.argv.slice(2);
let handle;
if(mode==='slot'){
 const app=await import(pathToFileURL(target));handle=app.handleRequest;
}else if(mode!=='collector')throw Error('Unknown recovery worker');
const server=createServer(async(req,res)=>{
 try{
  if(mode==='collector'){
   if(req.method!=='POST'||req.url!=='/events'){res.writeHead(404);res.end();return;}
   let raw='';for await(const chunk of req){raw+=chunk;if(raw.length>4096)throw Error('EVENT_TOO_LARGE');}
   const event=JSON.parse(raw);if(Object.keys(event).sort().join(',')!=='phase,status'||typeof event.phase!=='string'||!Number.isInteger(event.status))throw Error('EVENT_SCHEMA');
   appendFileSync(target,JSON.stringify(event)+'\n');res.writeHead(202);res.end();
  }else if(fault==='unhealthy'){res.writeHead(503,{'content-type':'application/json'});res.end(JSON.stringify({error:'synthetic_canary_fault'}));}
  else await handle(req,res);
 }catch{res.writeHead(500);res.end();}
});
server.listen(0,'127.0.0.1',()=>process.stdout.write(JSON.stringify({port:server.address().port})+'\n'));
process.on('SIGTERM',()=>server.close(()=>process.exit(0)));

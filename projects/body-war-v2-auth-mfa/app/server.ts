import { createServer } from "node:http";
import { handleRequest } from "./src/application/router.js";
import { HOST, PORT, STRAVA_REDIRECT_URI } from "./src/adapters/pilot-http.js";
export * from "./src/adapters/pilot-http.js";
export { handleRequest };
export async function main(): Promise<void> {
  const server=createServer((request,response)=>{void handleRequest(request,response);});
  server.listen(PORT,HOST,()=>{console.log(`Body War pilot app: http://${HOST}:${PORT}`);console.log(`Strava callback URL: ${STRAVA_REDIRECT_URI}`);});
}
if(process.argv[1]?.endsWith("server.js"))void main();

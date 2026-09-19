// Generated bounded JSON request parser; adapters consume the cached value.
import type {IncomingMessage} from 'node:http';
import {assertRecord} from './validation.js';
import {normalizeRequest,ApplicationDomainError} from './normalization.js';
const contracts:Record<string,{record:string;maxbytes:number;error:string}>={
  "CreateTrack": {
    "record": "CreateTrackRequest",
    "maxbytes": 16384,
    "error": "invalid_suggested_track"
  },
  "AttachEvidence": {
    "record": "AttachEvidenceRequest",
    "maxbytes": 16384,
    "error": "invalid_evidence_request"
  },
  "WithdrawEvidence": {
    "record": "EmptyRequest",
    "maxbytes": 16384,
    "error": "invalid_withdrawal_request"
  }
};
export class ApplicationRequestError extends Error {constructor(public code:string,public status:number){super(code);}}
const cache=new WeakMap<IncomingMessage,{operation:string;value:Promise<Record<string,unknown>>}>();
export function readRequest(request:IncomingMessage,operation:string):Promise<Record<string,unknown>>{const prior=cache.get(request);if(prior){if(prior.operation!==operation)throw Error('REQUEST_BINDING_MISMATCH');return prior.value;}const c=contracts[operation];if(!c)throw Error('UNKNOWN_REQUEST_CONTRACT');const value=new Promise<Record<string,unknown>>((resolve,reject)=>{const chunks:Buffer[]=[];let size=0,overflow=false;request.on('data',(chunk:Buffer)=>{size+=chunk.length;if(size>c.maxbytes){if(!overflow){overflow=true;chunks.length=0;reject(new ApplicationRequestError('request_too_large',413));}return;}chunks.push(Buffer.from(chunk));});request.once('aborted',()=>reject(new ApplicationRequestError(c.error,400)));request.once('error',()=>reject(new ApplicationRequestError(c.error,400)));request.once('end',()=>{if(overflow)return;try{const text=Buffer.concat(chunks).toString('utf8');const parsed=text?JSON.parse(text):{};assertRecord(c.record,parsed);resolve(normalizeRequest(operation,parsed));}catch(error){reject(new ApplicationRequestError(error instanceof ApplicationDomainError?error.code:c.error,400));}});});cache.set(request,{operation,value});return value;}

// Generated closed integer query contracts. Numeric conversion preserves the pilot's Number semantics.
import {ApplicationRequestError} from './request.js';
const contracts:Record<string,{fields:Record<string,{kind:string;default:number;min:number;max:number}>;error:string}>={
  "ListActivities": {
    "fields": {
      "page": {
        "kind": "integer",
        "min": 1,
        "max": 10,
        "default": 1
      },
      "per_page": {
        "kind": "integer",
        "min": 1,
        "max": 100,
        "default": 20
      }
    },
    "error": "strava_provider_bounds_invalid"
  }
};
export function readQuery(url:URL,operation:string):Record<string,string>{const c=contracts[operation];if(!c)throw Error('UNKNOWN_QUERY_CONTRACT');const reject=():never=>{throw new ApplicationRequestError(c.error,400);};for(const key of url.searchParams.keys())if(!Object.hasOwn(c.fields,key))reject();const result:Record<string,string>={};for(const [field,rule]of Object.entries(c.fields)){const values=url.searchParams.getAll(field);if(values.length>1)reject();const n=values.length?Number(values[0]):rule.default;if(!Number.isSafeInteger(n)||n<rule.min||n>rule.max)reject();result[field]=String(n);}return result;}

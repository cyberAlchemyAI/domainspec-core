import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
const files=['app/data/tracks.json','app/data/track-submissions.json'];
const inventory=files.map(path=>{if(!existsSync(path))return {path,status:'absent'};const bytes=readFileSync(path),sha256=createHash('sha256').update(bytes).digest('hex');try{const parsed=JSON.parse(bytes);const rows=parsed.submissions??parsed.tracks;return {path,sha256,status:Array.isArray(rows)?'readable':'invalid-shape',records:Array.isArray(rows)?rows.length:null};}catch{return {path,sha256,status:'invalid-json'};}});
console.log(JSON.stringify({inventory,posture:'Read-only archive inventory; no consent, ownership or migration inferred',authority_effect:'none',open_questions_ref:'../MIGRATION-PLAN.md#open-questions'},null,2));

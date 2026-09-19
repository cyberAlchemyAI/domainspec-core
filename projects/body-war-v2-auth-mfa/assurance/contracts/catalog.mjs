// Independent finite oracle fixtures. Do not derive expected results from the compiler or TDE.
const clone=x=>structuredClone(x);
const trackInput={name:'Route',place_label:'Park',city:'City'};
const groups=[];
for(const [id,operation,field,min,max] of [
 ['CreateTrackRules','CreateTrack','name',1,255],['CreateTrackRules','CreateTrack','place_label',1,255],['CreateTrackRules','CreateTrack','city',1,120],['CreateTrackRules','CreateTrack','public_note',0,500],['EvidenceInputRules','AttachEvidence','activity_id',0,255],['EvidenceInputRules','AttachEvidence','consent_text',0,500]]){
 const error=operation==='CreateTrack'?'invalid_suggested_track':'invalid_evidence_request';
 const base=operation==='CreateTrack'?trackInput:{activity_id:'123',consent_text:'Consent'};
 const values=[['trim','  Run  ','Run'],['blank','   ',''],['at-limit','x'.repeat(max),'x'.repeat(max)],['over-limit','x'.repeat(max+1),'x'.repeat(max)],['absent',undefined,'']];
 const cases=values.map(([name,value,expected])=>{const input={...base};if(value===undefined)delete input[field];else input[field]=value;return {name,input,...(expected.length<min?{error}:{value:expected})};});
 groups.push({id:id+'-'+field,kind:'normalize',owner:id,field,operation,formal:JSON.stringify({operation,field,rule:{kind:'text',min,max},error}),cases,mutation:'text-normalization-bypass',mutant_failures:3});
}
{
 const field='distance_hint_meters',operation='CreateTrack',error='invalid_suggested_track';
 groups.push({id:'CreateTrackRules-'+field,owner:'CreateTrackRules',field,operation,kind:'normalize',formal:JSON.stringify({operation,field,rule:{kind:'positive-integer'},error}),cases:[{name:'absent',input:trackInput,value:null},...[[null,null],[1,1],[0,undefined],[-1,undefined],[1.5,undefined]].map(([v,value])=>({name:String(v),input:{...trackInput,[field]:v},...(value===undefined?{error}:{value})}))],mutation:'zero-distance-accepted',mutant_failures:1});
}
for(const [field,max,defaultValue]of [['page',10,1],['per_page',100,20]]){
 const operation='ListActivities',error='strava_provider_bounds_invalid';
 const cases=[{name:'default',query:'',value:String(defaultValue)},...[1,max].map(n=>({name:'valid-'+n,query:field+'='+n,value:String(n)})),...[max+1,0,1.5,'NaN'].map(n=>({name:'invalid-'+n,query:field+'='+n,error})),{name:'duplicate',query:field+'=1&'+field+'=1',error},{name:'unknown',query:'extra=1',error}];
 groups.push({id:'ActivityPagination-'+field,owner:'ActivityPagination',field,operation,kind:'query',formal:JSON.stringify({operation,field,rule:{kind:'integer',min:1,max,default:defaultValue},error}),cases,mutation:'query-upper-bound-off-by-one',mutant_failures:1});
}
const noClaim={route_geometry:'not_claimed',scoring:'not_claimed'},redaction={provider_tokens:'server_only',raw_private_payload:'omitted',maps:'omitted',notes:'omitted'};
const athlete={id:123,scope:['read'],provider:'strava',status:'linked',strava_profile_url:null};
const session={expires_at:'2026-09-07T12:00:00.000Z'};
const connection={connected:true,account:athlete,profile_url:null};
const profile={principal_id:'runner',display_name:'Runner',principal_status:'active',session,strava:connection,privacy:{provider_tokens:'server_only',activity_import:'redacted_summaries',csrf:'required_for_unsafe_methods'},validation:{taquaral_activity:'consent_required',route_geometry:'deferred',scoring:'deferred'}};
const track={id:'t',slug:'track',name:'Track',place_label:'Park',city:'City',country:'BR',distance_hint_meters:null,status:'needs_evidence',geometry_authority:'needs_evidence',suggested_by:'seed',public_note:'',created_at:'date',updated_at:'date',authority:{...noClaim,pilot_ready:'not_claimed'}};
const activity={id:'a',name:'Run',distance:100,moving_time:20,average_speed:5,start_date:'date'};
const evidence={id:'e',suggested_track_id:'t',provider:'strava',provider_activity_id:'a',redacted_summary:activity,consented_at:'date',status:'submitted',created_at:'date',updated_at:'date',authority:{...noClaim,activity_summary:'redacted_candidate'}};
const receipt={source:'strava',principal_id:'runner',imported_at:'date',summary_count:1,redaction,consent:{friend_fixture:'required'},authority:{...noClaim,activity_summary:'imported'}};
const selected=[
 ['ProfileResponse','profile','PublicRunnerProfile',{profile},profile],
 ['PublicRunnerProfile','session','PublicSession',profile,session],
 ['PublicRunnerProfile','strava','PublicConnection',profile,connection],
 ['StatusResponse','athlete','PublicAthlete|null',{configured:true,authenticated:true,connected:true,athlete,redirect_uri:'local',scope:'read'},athlete],
 ['TrackResponse','suggested_track','PublicTrack',{suggested_track:track},track],
 ['TrackResponse','my_evidence_candidates','PublicEvidence[]?',{suggested_track:track,my_evidence_candidates:[evidence]},[evidence]],
 ['EvidenceResponse','evidence_candidate','PublicEvidence',{evidence_candidate:evidence},evidence],
 ['ActivitiesResponse','receipt','ActivityImportReceipt',{activities:[activity],receipt},receipt],
];
for(const [entity,field,ftype,base,value]of selected){
 const cases=[{name:'valid',input:base,accepted:true}];const omitted=clone(base);delete omitted[field];cases.push({name:'missing',input:omitted,accepted:ftype.endsWith('?')});
 cases.push({name:'wrong-type',input:{...clone(base),[field]:false},accepted:false});
 const polluted=typeof value==='number'?{access_token:'SYNTHETIC'}:Array.isArray(value)?[{...clone(value[0]),access_token:'SYNTHETIC'}]:{...clone(value),access_token:'SYNTHETIC'};
 cases.push({name:'nested-private-field',input:{...clone(base),[field]:polluted},accepted:false});
 if(ftype.includes('|null'))cases.push({name:'nullable',input:{...clone(base),[field]:null},accepted:true});
 groups.push({id:entity+'-'+field,kind:'record',entity,field,ftype,constraint:ftype.endsWith('?')?'optional':'required',cases,mutation:'field-validator-replaced-with-unknown',mutant_failures:ftype.endsWith('?')?2:3});
}
export const contractCases=groups;

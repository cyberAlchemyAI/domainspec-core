// Explicit staging fixture adapter. This is not a live Strava provider.
export function installStagingMocks(strava,repo,fixture){
 const list=strava.listActivitySummaries.bind(strava),detail=strava.getActivitySummary.bind(strava);
 const activities=fixture.activities.map(a=>({...a}));
 if(!fixture.principalId||activities.length!==2||activities.some(a=>!a.id.startsWith('mock-')||!a.name.startsWith('MOCK')))throw Error('Invalid staging mock fixture');
 async function access(){const a=await repo.findProviderAccountByPrincipalId(fixture.principalId);if(!a||a.status!=='linked')return {ok:false,error:{code:'strava_not_connected',status:409,message:'Account is not connected'}};if(!a.scope.flatMap(s=>s.split(/[\s,]+/)).some(s=>['activity:read','activity:read_all'].includes(s)))return {ok:false,error:{code:'strava_scope_denied',status:403,message:'Activity access was not granted'}};return null;}
 strava.listActivitySummaries=async(principal,page,perPage)=>{
  if(principal!==fixture.principalId)return list(principal,page,perPage);
  const denied=await access();if(denied)return denied;
  const p=Number(page),n=Number(perPage);if(!Number.isInteger(p)||p<1||p>10||!Number.isInteger(n)||n<1||n>100)return {ok:false,error:{code:'strava_provider_bounds_invalid',status:400,message:'Invalid pagination'}};
  return {ok:true,value:activities.slice((p-1)*n,p*n).map(a=>({...a}))};
 };
 strava.getActivitySummary=async(principal,id)=>{
  if(principal!==fixture.principalId||!id.startsWith('mock-'))return detail(principal,id);
  const denied=await access();if(denied)return denied;
  const a=activities.find(a=>a.id===id);return a?{ok:true,value:{...a}}:{ok:false,error:{code:'invalid_activity',status:400,message:'Mock activity not found'}};
 };
}

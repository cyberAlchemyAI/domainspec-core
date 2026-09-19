import {test} from 'node:test';
import assert from 'node:assert/strict';
import {project,transition} from '../app/src/application/domain.ts';
import {assertRecord} from '../app/src/application/validation.ts';
import {apiPath} from '../app/src/application/static/ui-config.js';
test('redaction removes geometry, credentials and inherited properties without invoking getters',()=>{
 const input=Object.assign(Object.create({start_date:'inherited'}),{id:42,name:'Run',distance:1000,access_token:'secret',map:{polyline:'private'}});
 Object.defineProperty(input,'sport_type',{get(){throw Error('Getter must not run');}});
 assert.deepEqual(project('RedactedActivity',input),{id:42,name:'Run',distance:1000,sport_type:'Run',type:'Run'});
});
test('lifecycle rejects undeclared transitions and preserves reviewed state when attaching',()=>{
 assert.equal(transition('TrackEvidenceLifecycle','needs_evidence','attach'),'evidence_submitted');
 assert.equal(transition('TrackEvidenceLifecycle','source_backed','attach'),'source_backed');
 assert.equal(transition('TrackEvidenceLifecycle','source_backed','last-evidence-removed'),'needs_evidence');
 assert.throws(()=>transition('TrackEvidenceLifecycle','needs_evidence','verify'),/INVALID_TRANSITION/);
});
test('closed generated response schema rejects credential leaks and wrong field types',()=>{
 assert.doesNotThrow(()=>assertRecord('LogoutResponse',{ok:true}));
 assert.throws(()=>assertRecord('LogoutResponse',{ok:true,access_token:'secret'}),/APPLICATION_RESPONSE_CONTRACT/);
 assert.throws(()=>assertRecord('LogoutResponse',{ok:'true'}),/APPLICATION_RESPONSE_CONTRACT/);
});
test('UI path binding encodes identifiers and rejects missing ones',()=>{
 assert.equal(apiPath('ReadTrack',{idOrSlug:'a/b'}),'/api/suggested-tracks/a%2Fb');
 assert.throws(()=>apiPath('ReadTrack'),/MISSING_PATH_PARAMETER/);
});

import {normalizeRequest} from '../app/src/application/normalization.ts';
test('generated domain rules preserve boundary normalization and reject invalid distance',()=>{
 const body={name:'  Route  ',place_label:'  Park  ',city:' City '};
 assert.deepEqual(normalizeRequest('CreateTrack',body),{name:'Route',place_label:'Park',city:'City',public_note:'',distance_hint_meters:null});
 assert.equal(normalizeRequest('CreateTrack',{...body,name:'x'.repeat(256)}).name.length,255);
 for(const distance of [0,-1,1.2,NaN,Infinity])assert.throws(()=>normalizeRequest('CreateTrack',{...body,distance_hint_meters:distance}),/invalid_suggested_track/);
 assert.throws(()=>normalizeRequest('CreateTrack',{...body,name:'   '}),/invalid_suggested_track/);
 assert.equal(normalizeRequest('CreateTrack',{...body,distance_hint_meters:1}).distance_hint_meters,1);
});
test('nested receipt and evidence records reject private data and wrong scalar types',()=>{
 const receipt={source:'strava',principal_id:'p',imported_at:'date',summary_count:1,redaction:{provider_tokens:'server_only',raw_private_payload:'omitted',maps:'omitted',notes:'omitted'},consent:{friend_fixture:'required'},authority:{activity_summary:'imported',route_geometry:'not_claimed',scoring:'not_claimed'}};
 assert.doesNotThrow(()=>assertRecord('ActivitiesResponse',{activities:[],receipt}));
 assert.throws(()=>assertRecord('ActivitiesResponse',{activities:[],receipt:{...receipt,redaction:{...receipt.redaction,access_token:'private'}}}),/APPLICATION_RESPONSE_CONTRACT/);
 assert.throws(()=>assertRecord('ActivitiesResponse',{activities:[],receipt:{...receipt,summary_count:'1'}}),/APPLICATION_RESPONSE_CONTRACT/);
 assert.throws(()=>assertRecord('ActivitiesResponse',{activities:[],receipt:{...receipt,authority:{...receipt.authority,scoring:'certified'}}}),/APPLICATION_RESPONSE_CONTRACT/);
});

import {readQuery} from '../app/src/application/query.ts';
test('generated pagination applies defaults, preserves numeric conversion and rejects ambiguous queries',()=>{
 const parse=q=>readQuery(new URL('http://localhost/api/activities'+q),'ListActivities');
 assert.deepEqual(parse(''),{page:'1',per_page:'20'});assert.deepEqual(parse('?page=1e1&per_page=100'),{page:'10',per_page:'100'});
 for(const q of ['?page=11','?page=0','?page=','?page=NaN','?page=Infinity','?page=1.1','?per_page=101','?page=1&page=2','?unknown=1'])assert.throws(()=>parse(q),/strava_provider_bounds_invalid/);
});
test('closed public athlete union preserves scalar ids and excludes arbitrary metadata',()=>{
 const athlete={id:123,strava_profile_url:null,scope:[],provider:'strava',status:'linked'};
 assert.doesNotThrow(()=>assertRecord('PublicAthlete',athlete));assert.doesNotThrow(()=>assertRecord('PublicAthlete',{...athlete,id:'123'}));
 for(const id of [{access_token:'private'},[],true])assert.throws(()=>assertRecord('PublicAthlete',{...athlete,id}),/APPLICATION_RESPONSE_CONTRACT/);
 assert.throws(()=>assertRecord('PublicAthlete',{...athlete,metadata:{secret:'private'}}),/APPLICATION_RESPONSE_CONTRACT/);
});

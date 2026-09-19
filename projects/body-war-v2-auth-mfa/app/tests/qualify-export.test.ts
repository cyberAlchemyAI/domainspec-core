import test from 'node:test';
import assert from 'node:assert/strict';
import {qualifyGeometryExport} from '../src/geometry/qualify-export.js';
function fixture(){const ref='a'.repeat(24),meta={schema:'body-war-strava-geometry-export/v1',source:'strava_activity_streams',generated_at:'2026-09-07T00:00:00Z',exported_activity_count:1};return {geo:{type:'FeatureCollection',body_war_export:meta,features:[{type:'Feature',properties:{provider:'strava',source_activity_ref:ref,point_count:2,coordinate_distances_meters:[0,100],coordinate_times_seconds:[0,30],stream_distance_meters:100,elapsed_seconds:30},geometry:{type:'LineString',coordinates:[[0,0],[0.001,0]]}}]},report:{...meta,outcomes:[{source_activity_ref:ref,status:'exported',point_count:2}]}};}
test('recorded export qualification returns only counts and hashes; never asserts authenticity',()=>{const f=fixture(),r=qualifyGeometryExport(JSON.stringify(f.geo),JSON.stringify(f.report));assert.equal(r.activities,1);assert.equal(r.authenticity,'requires-source-provenance');assert.equal(JSON.stringify(r).includes('coordinates'),false);});
test('qualification rejects malformed coordinates, streams, duplicate references and mismatched reports',()=>{
 const mutations=[(f:any)=>f.geo.features[0].geometry.coordinates[0][1]=91,(f:any)=>f.geo.features[0].properties.coordinate_times_seconds=[0],(f:any)=>f.geo.features[0].properties.coordinate_distances_meters=[101,100],(f:any)=>f.geo.features.push(f.geo.features[0]),(f:any)=>f.report.outcomes[0].status='failed',(f:any)=>f.geo.features[0].properties.source_activity_ref='fixture-id'];
 for(const mutate of mutations){const f=fixture();mutate(f);assert.throws(()=>qualifyGeometryExport(JSON.stringify(f.geo),JSON.stringify(f.report)));}
});

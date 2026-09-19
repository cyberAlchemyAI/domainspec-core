import {readFileSync} from 'node:fs';
import {qualifyGeometryExport} from '../app/dist/src/geometry/qualify-export.js';
const [geometry,report]=process.argv.slice(2);
if(!geometry||!report){console.error('Usage: node scripts/qualify-geometry.mjs <private-geojson> <private-export-report>');process.exit(2);}
try{console.log(JSON.stringify(qualifyGeometryExport(readFileSync(geometry,'utf8'),readFileSync(report,'utf8')),null,2));}
catch {console.error('Export qualification failed; no private data emitted. Inspect locally with the qualifier tests.');process.exitCode=1;}

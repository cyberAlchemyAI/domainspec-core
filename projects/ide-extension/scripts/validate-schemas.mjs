import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadModuleManifests } from '../src/kernel/registry.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const schemaDir = path.join(projectRoot, 'schemas');
const moduleDir = path.join(projectRoot, 'src/modules');

const schemaFiles = (await readdir(schemaDir))
  .filter((file) => file.endsWith('.json'))
  .sort();

for (const file of schemaFiles) {
  JSON.parse(await readFile(path.join(schemaDir, file), 'utf8'));
}

const manifests = await loadModuleManifests(moduleDir);
console.log(`validated ${schemaFiles.length} schemas and ${manifests.length} module manifests`);

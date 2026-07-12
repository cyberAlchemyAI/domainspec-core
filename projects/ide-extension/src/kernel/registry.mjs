import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { assertModuleManifest } from './schema-validation.mjs';

export function validateModuleManifest(manifest, source = '<memory>') {
  return assertModuleManifest(manifest, source);
}

export async function loadModuleManifests(modulesDir) {
  const entries = await readdir(modulesDir, { withFileTypes: true });
  const files = entries
    .filter((entry) => entry.isFile() && entry.name.endsWith('.manifest.json'))
    .map((entry) => entry.name)
    .sort();

  const manifests = [];
  for (const file of files) {
    const fullPath = path.join(modulesDir, file);
    const parsed = JSON.parse(await readFile(fullPath, 'utf8'));
    manifests.push(await validateModuleManifest(parsed, fullPath));
  }

  return manifests;
}

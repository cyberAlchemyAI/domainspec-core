import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

const REQUIRED_FIELDS = [
  'module_id',
  'display_name',
  'owner_route',
  'source_refs',
  'capabilities',
  'allowed_effects',
  'required_gates',
  'forbidden_effects',
  'expected_receipts'
];

export function validateModuleManifest(manifest, source = '<memory>') {
  const errors = [];

  if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest)) {
    throw new Error(`${source}: manifest must be an object`);
  }

  for (const field of REQUIRED_FIELDS) {
    if (!(field in manifest)) errors.push(`missing ${field}`);
  }

  if (typeof manifest.module_id !== 'string' || !/^[a-z0-9][a-z0-9._-]*$/.test(manifest.module_id || '')) {
    errors.push('module_id must be a stable lowercase id');
  }

  for (const field of REQUIRED_FIELDS.filter((field) => Array.isArray(manifest[field]))) {
    if (!manifest[field].every((value) => typeof value === 'string' && value.trim() !== '')) {
      errors.push(`${field} must contain only non-empty strings`);
    }
  }

  for (const field of ['source_refs', 'capabilities', 'allowed_effects', 'required_gates', 'forbidden_effects', 'expected_receipts']) {
    if (!Array.isArray(manifest[field])) errors.push(`${field} must be an array`);
  }

  if (errors.length) {
    throw new Error(`${source}: ${errors.join('; ')}`);
  }

  return manifest;
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
    manifests.push(validateModuleManifest(parsed, fullPath));
  }

  return manifests;
}


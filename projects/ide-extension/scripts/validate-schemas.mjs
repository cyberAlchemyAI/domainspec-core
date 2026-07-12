import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadModuleManifests } from '../src/kernel/registry.mjs';
import { getSchemaValidators, SCHEMA_FILES } from '../src/kernel/schema-validation.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const schemaDir = path.join(projectRoot, 'schemas');
const moduleDir = path.join(projectRoot, 'src/modules');
const fixtureDir = path.join(projectRoot, 'tests/fixtures/schemas');

const schemaFiles = (await readdir(schemaDir))
  .filter((file) => file.endsWith('.json'))
  .sort();
const expectedSchemaFiles = Object.values(SCHEMA_FILES).sort();

if (JSON.stringify(schemaFiles) !== JSON.stringify(expectedSchemaFiles)) {
  throw new Error(
    `schema registry mismatch: expected ${expectedSchemaFiles.join(', ')}, found ${schemaFiles.join(', ')}`
  );
}

const validators = await getSchemaValidators();
const manifests = await loadModuleManifests(moduleDir);
const fixtureFiles = (await readdir(fixtureDir))
  .filter((file) => file.endsWith('.json'))
  .sort();

for (const file of fixtureFiles) {
  const schemaName = validators.schema_names.find((name) => file.startsWith(`${name}.`));
  if (!schemaName) throw new Error(`fixture does not name a registered schema: ${file}`);

  const fixture = JSON.parse(await readFile(path.join(fixtureDir, file), 'utf8'));
  const result = validators.validate(schemaName, fixture);
  const expectedValid = file.includes('.valid.');

  if (result.valid !== expectedValid) {
    throw new Error(
      `${file}: expected valid=${expectedValid}, got valid=${result.valid}: ${JSON.stringify(result.errors)}`
    );
  }
}

console.log(
  `validated ${validators.schema_names.length} runtime schemas, `
  + `${manifests.length} module manifests, and ${fixtureFiles.length} schema fixtures`
);

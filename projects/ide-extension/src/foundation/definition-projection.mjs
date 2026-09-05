import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const SOURCE_REF = 'definitions/DEFINITIONS.md';
const OWNER_ROUTE = 'foundation-definitions-owner';
const BOUNDARY = 'candidate-definitions-read-only';
const CLAIM_CEILING = 'projection-not-source-truth';

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

export function parseFoundationDefinitions(source, sourceSha256) {
  const lines = source.split(/\r?\n/);
  const definitions = [];
  for (let index = 0; index < lines.length; index += 1) {
    const match = /^## (CAF-D\d+): (.+)$/.exec(lines[index]);
    if (!match) continue;
    let disposition = 'unspecified';
    let summary = '';
    for (index += 1; index < lines.length && !lines[index].startsWith('## '); index += 1) {
      const line = lines[index].trim();
      if (line.startsWith('Disposition: ')) disposition = line.slice('Disposition: '.length);
      else if (line && !summary && !line.startsWith('#')) summary = line;
    }
    index -= 1;
    definitions.push({
      definition_id: match[1],
      title: match[2],
      disposition,
      summary,
      source_ref: SOURCE_REF,
      source_sha256: sourceSha256,
      currentness: 'verified-current',
      owner_route: OWNER_ROUTE,
      boundary: BOUNDARY,
      claim_ceiling: CLAIM_CEILING
    });
  }
  return definitions;
}

export async function loadFoundationDefinitionProjection(foundationRoot, options = {}) {
  const sourcePath = path.join(foundationRoot, SOURCE_REF);
  let bytes;
  try {
    bytes = await readFile(sourcePath);
  } catch (error) {
    const unavailable = new Error('Foundation definition source is unavailable');
    unavailable.code = 'foundation_definitions_unavailable';
    unavailable.cause = error;
    throw unavailable;
  }
  const digest = sha256(bytes);
  const currentness = options.expectedSha256 && options.expectedSha256 !== digest
    ? 'stale'
    : 'verified-current';
  const definitions = parseFoundationDefinitions(bytes.toString('utf8'), digest)
    .map((definition) => ({ ...definition, currentness }));
  return {
    schema_version: 'caf.definition-workspace-projection/v1',
    status: currentness === 'verified-current' ? 'available' : 'stale',
    source: {
      ref: SOURCE_REF,
      sha256: digest,
      currentness,
      owner_route: OWNER_ROUTE,
      boundary: BOUNDARY,
      claim_ceiling: CLAIM_CEILING
    },
    definitions,
    authority_effect: 'none'
  };
}

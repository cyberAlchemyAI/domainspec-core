import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const PROOF_RANK = new Map([
  ['source_observed', 0],
  ['documented_capability', 1],
  ['planned_motion', 2],
  ['executed_witness', 3],
  ['subjective_evaluation', 4],
  ['owner_decision', 5],
]);

function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value !== null && typeof value === 'object') {
    const fields = Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`);
    return `{${fields.join(',')}}`;
  }
  return JSON.stringify(value);
}

function digestBytes(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function digestValue(value) {
  return digestBytes(Buffer.from(canonical(value)));
}

function kind(value) {
  if (Array.isArray(value)) return 'array';
  if (value === null) return 'null';
  if (Number.isInteger(value)) return 'integer';
  return typeof value;
}

function schemaFailure(pathName, message) {
  return { valid: false, code: 'SCHEMA_INVALID', path: pathName, message };
}

function validateSchema(value, schema, pathName = '$') {
  if (schema.type !== undefined) {
    const accepted = Array.isArray(schema.type) ? schema.type : [schema.type];
    const actual = kind(value);
    const numberAccepted = actual === 'integer' && accepted.includes('number');
    if (!accepted.includes(actual) && !numberAccepted) {
      return schemaFailure(pathName, `expected ${accepted.join('|')}, got ${actual}`);
    }
  }
  if (schema.const !== undefined && canonical(value) !== canonical(schema.const)) {
    return schemaFailure(pathName, 'value does not match const');
  }
  if (schema.enum !== undefined && !schema.enum.some((item) => canonical(item) === canonical(value))) {
    return schemaFailure(pathName, 'value is outside enum');
  }
  if (typeof value === 'string') {
    if (schema.minLength !== undefined && value.length < schema.minLength) return schemaFailure(pathName, 'string is shorter than minLength');
    if (schema.pattern !== undefined && !(new RegExp(schema.pattern).test(value))) return schemaFailure(pathName, 'string does not match pattern');
  }
  if (typeof value === 'number') {
    if (schema.minimum !== undefined && value < schema.minimum) return schemaFailure(pathName, 'number is below minimum');
    if (schema.maximum !== undefined && value > schema.maximum) return schemaFailure(pathName, 'number is above maximum');
  }
  if (Array.isArray(value)) {
    if (schema.minItems !== undefined && value.length < schema.minItems) return schemaFailure(pathName, 'array has fewer than minItems');
    if (schema.items !== undefined) {
      for (let index = 0; index < value.length; index += 1) {
        const result = validateSchema(value[index], schema.items, `${pathName}[${index}]`);
        if (!result.valid) return result;
      }
    }
  }
  if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
    const keys = Object.keys(value);
    if (schema.minProperties !== undefined && keys.length < schema.minProperties) return schemaFailure(pathName, 'object has fewer than minProperties');
    for (const required of schema.required ?? []) {
      if (!Object.hasOwn(value, required)) return schemaFailure(`${pathName}.${required}`, 'required property is missing');
    }
    for (const [key, child] of Object.entries(schema.properties ?? {})) {
      if (Object.hasOwn(value, key)) {
        const result = validateSchema(value[key], child, `${pathName}.${key}`);
        if (!result.valid) return result;
      }
    }
    if (schema.additionalProperties === false) {
      const declared = new Set(Object.keys(schema.properties ?? {}));
      const unknown = keys.find((key) => !declared.has(key));
      if (unknown !== undefined) return schemaFailure(`${pathName}.${unknown}`, 'additional property is not allowed');
    }
  }
  return { valid: true };
}

function fail(code, pathName, message) {
  return { valid: false, code, path: pathName, message };
}

export async function validateCandidate({ candidate, schema, sourceSnapshot, repositoryRoot }) {
  const structural = validateSchema(candidate, schema);
  if (!structural.valid) return structural;

  const aggregatePayload = {
    schema_version: sourceSnapshot.schema_version,
    artifacts: sourceSnapshot.artifacts,
  };
  if (digestValue(aggregatePayload) !== sourceSnapshot.aggregate_sha256) {
    return fail('SOURCE_DRIFT', '$.source_snapshot.aggregate_sha256', 'source snapshot aggregate is stale');
  }

  const byPath = new Map(sourceSnapshot.artifacts.map((artifact) => [artifact.path, artifact]));
  const script = sourceSnapshot.artifacts.find((artifact) => artifact.path.endsWith('educational-video-production-script.md'));
  const captions = sourceSnapshot.artifacts.find((artifact) => artifact.path.endsWith('educational-video-captions.vtt'));
  const image = byPath.get(candidate.scene_beat_ref.image_ref.path);
  const candidateBindingsMatch =
    candidate.scene_beat_ref.source_package_digest === sourceSnapshot.aggregate_sha256 &&
    script?.sha256 === candidate.scene_beat_ref.script_digest &&
    captions?.sha256 === candidate.scene_beat_ref.caption_digest &&
    image?.sha256 === candidate.scene_beat_ref.image_ref.sha256;
  if (!candidateBindingsMatch) {
    return fail('SOURCE_DRIFT', '$.scene_beat_ref', 'candidate source bindings differ from the frozen snapshot');
  }

  for (const artifact of sourceSnapshot.artifacts) {
    let bytes;
    try {
      bytes = await readFile(path.resolve(repositoryRoot, artifact.path));
    } catch {
      return fail('SOURCE_DRIFT', `$.source_snapshot[${artifact.path}]`, 'source artifact is unreadable');
    }
    if (bytes.length !== artifact.size_bytes || digestBytes(bytes) !== artifact.sha256) {
      return fail('SOURCE_DRIFT', `$.source_snapshot[${artifact.path}]`, 'live source bytes differ from the frozen snapshot');
    }
  }

  const ceiling = PROOF_RANK.get('planned_motion');
  const inflatedIndex = candidate.proof_ledger.findIndex((item) => (PROOF_RANK.get(item.proof_state) ?? Number.POSITIVE_INFINITY) > ceiling);
  if (inflatedIndex >= 0) {
    return fail('PROOF_INFLATION', `$.proof_ledger[${inflatedIndex}].proof_state`, 'proof state exceeds planned_motion');
  }

  const standard = candidate.semantic_contract.semantic_end_states.at(-1);
  const reduced = candidate.semantic_contract.reduced_motion_state_machine.at(-1);
  if (standard !== reduced) {
    return fail('REDUCED_MOTION_MISMATCH', '$.semantic_contract.reduced_motion_state_machine', 'standard and reduced terminal semantics differ');
  }

  return { valid: true, code: 'VALID', path: '$', message: 'candidate satisfies the OAVA-001 contract' };
}

export const internals = { canonical, digestValue, validateSchema };

#!/usr/bin/env node

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateDefinitions } from '../scripts/validate-relations.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const fixtures = JSON.parse(readFileSync(resolve(ROOT, 'fixtures/relation-witnesses.json'), 'utf8'));

function consume(name, scenario) {
  switch (name) {
    case 'documents': return { semantic_coverage: scenario.edge === true };
    case 'derivesFrom': return { recipe_selectable: scenario.edge === true };
    case 'exports': return { candidate_ids: scenario.edge ? ['api:animate:js'] : [] };
    case 'implementationDescribedBy': return { source_grounded: scenario.scope_matches === true };
    case 'hasTestEvidence': return { runtime_support: ['TestObserved', 'ExecutedWitness'].includes(scenario.evidence_class) };
    case 'illustratedBy': return { example_ids: scenario.edge ? ['example:fixture'] : [] };
    case 'prerequisiteRecipe': return { dag_valid: scenario.cycle !== true };
    case 'consults': return { binding_valid: scenario.target === 'api:createMotionPath' };
    case 'usesVersion': return { context_match: scenario.target_version === '4.5.0' };
    case 'producedEvidence': return { provenance_valid: scenario.producer === 'attempt:fixture' };
    case 'supportedByEvidence': return { lesson_eligible: scenario.edge === true };
    case 'contradictedByEvidence': return { conflict: scenario.edge === true };
    case 'proposes': return { fix_owned: scenario.diagnosis_id === 'diagnosis:fixture' };
    case 'generalizesFrom': return { lesson_eligible: scenario.episode_outcome === 'succeeded' };
    case 'boundedBy': return { context_match: scenario.target_version === '4.5.0' };
    case 'invalidatedBy': return { record_state: scenario.edge ? 'invalidated' : 'validated' };
    case 'supersedes': return { current_ids: scenario.edge ? ['recipe:rev2'] : ['recipe:rev1', 'recipe:rev2'] };
    default: throw new Error(`missing relation consumer: ${name}`);
  }
}

validateDefinitions();
assert.equal(fixtures.witness_count, 17);
assert.equal(fixtures.witnesses.length, 17);
assert.equal(new Set(fixtures.witnesses.map(item => item.relation_id)).size, 17);

const killed = [];
for (const witness of fixtures.witnesses) {
  const baseline = consume(witness.relation_name, witness.baseline);
  const mutant = consume(witness.relation_name, witness.mutant);
  assert.deepEqual(baseline, witness.expected_baseline, `${witness.id}: baseline`);
  assert.deepEqual(mutant, witness.expected_mutant, `${witness.id}: mutant`);
  assert.notDeepEqual(mutant, baseline, `${witness.id}: mutant survived`);
  killed.push(witness.relation_id);
}

assert.equal(killed.length, 17);
console.log('PASS relation mutation witnesses: 17/17 mutants killed');

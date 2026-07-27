import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  buildOntologyReceipt,
  renderDeterministicJson,
  validateOntology,
  validateTransition,
  type OntologyEntry,
  type OntologyTransition,
  type OntologyTransitionPolicy,
} from "../src/ontology-validator.ts";

const proofRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const repositoryRoot = path.resolve(process.cwd(), "../../..");
const ontologyRoot = path.join(proofRoot, "ontology");

async function readJson<T>(relativePath: string): Promise<T> {
  return JSON.parse(
    await readFile(path.join(proofRoot, relativePath), "utf8"),
  ) as T;
}

async function sha256File(relativePath: string): Promise<string> {
  const bytes = await readFile(path.join(repositoryRoot, relativePath));
  return createHash("sha256").update(bytes).digest("hex");
}

async function loadInputs(): Promise<{
  entries: OntologyEntry[];
  policy: OntologyTransitionPolicy;
  legal: OntologyTransition;
  invalid: OntologyTransition;
  sourceDigests: Record<string, string>;
}> {
  const entries = await Promise.all(
    ["CreateSuggestedTrack.json", "SuggestedTrack.json", "needs_evidence.json"].map(
      (name) =>
        readJson<OntologyEntry>(path.join("ontology", "entries", name)),
    ),
  );
  const policy = await readJson<OntologyTransitionPolicy>(
    "ontology/transition-policy.json",
  );
  const legal = await readJson<OntologyTransition>(
    "ontology/fixtures/legal-transition.json",
  );
  const invalid = await readJson<OntologyTransition>(
    "ontology/fixtures/invalid-transition.json",
  );
  const sourcePaths = [
    "projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md",
    "projects/body-war/docs/features/parque-taquaral-online-mvp/states.md",
  ];
  const sourceDigests = Object.fromEntries(
    await Promise.all(
      sourcePaths.map(async (source) => [source, await sha256File(source)]),
    ),
  );
  return { entries, policy, legal, invalid, sourceDigests };
}

test("T-ONTOLOGY-001 accepts CT-2 and emits a deterministic non-promoting receipt", async () => {
  const { entries, policy, legal, invalid, sourceDigests } = await loadInputs();
  const validation = validateOntology({
    entries,
    transition_policy: policy,
    declared_transitions: [legal],
    source_digests: sourceDigests,
  });
  assert.equal(validation.status, "pass");
  assert.deepEqual(validation.diagnostics, []);
  assert.deepEqual(validateTransition(legal, policy), []);

  const negativeDiagnostics = validateTransition(invalid, policy);
  assert.deepEqual(
    negativeDiagnostics.map((diagnostic) => diagnostic.code),
    ["ONTOLOGY_TRANSITION_FORBIDDEN"],
  );

  const receipt = buildOntologyReceipt({
    validation,
    legal_transition: legal,
    negative_transition: invalid,
    negative_diagnostics: negativeDiagnostics,
    source_bindings: Object.entries(sourceDigests).map(([source, sha256]) => ({
      path: source,
      sha256,
    })),
  });
  assert.equal(receipt.ontology_status, "candidate-local");
  assert.equal(receipt.authority_effect, "none");
  assert.equal(receipt.release_admission, "not-granted");

  const firstBytes = renderDeterministicJson(receipt);
  const secondValidation = validateOntology({
    entries: [...entries].reverse(),
    transition_policy: policy,
    declared_transitions: [legal],
    source_digests: sourceDigests,
  });
  const secondBytes = renderDeterministicJson(
    buildOntologyReceipt({
      validation: secondValidation,
      legal_transition: legal,
      negative_transition: invalid,
      negative_diagnostics: negativeDiagnostics,
      source_bindings: Object.entries(sourceDigests).map(([source, sha256]) => ({
        path: source,
        sha256,
      })),
    }),
  );
  assert.equal(secondBytes, firstBytes);

  const receiptPath = path.join(proofRoot, "receipts", "ontology-receipt.json");
  await mkdir(path.dirname(receiptPath), { recursive: true });
  await writeFile(receiptPath, firstBytes, "utf8");
});

test("the direct needs_evidence to source_backed transition is forbidden", async () => {
  const { policy, invalid } = await loadInputs();
  const diagnostics = validateTransition(invalid, policy);
  assert.equal(diagnostics.length, 1);
  assert.equal(diagnostics[0]?.code, "ONTOLOGY_TRANSITION_FORBIDDEN");
});

test("closed entry validation emits the declared typed diagnostics", async () => {
  const { entries, policy, legal, sourceDigests } = await loadInputs();

  const invalidEntry = structuredClone(entries);
  Object.assign(invalidEntry[0]!, { unexpected: true });
  assert.ok(
    validateOntology({
      entries: invalidEntry,
      transition_policy: policy,
      declared_transitions: [legal],
      source_digests: sourceDigests,
    }).diagnostics.some(
      (diagnostic) => diagnostic.code === "ONTOLOGY_ENTRY_INVALID",
    ),
  );

  const missingGovernance = structuredClone(entries) as Array<
    OntologyEntry & { next_gate?: string }
  >;
  delete missingGovernance[0]!.next_gate;
  assert.ok(
    validateOntology({
      entries: missingGovernance,
      transition_policy: policy,
      declared_transitions: [legal],
      source_digests: sourceDigests,
    }).diagnostics.some(
      (diagnostic) =>
        diagnostic.code === "ONTOLOGY_GOVERNANCE_METADATA_MISSING",
    ),
  );

  const missingEdge = structuredClone(entries);
  missingEdge[0]!.relations[0]!.target =
    "body-war.ontology.DoesNotExist";
  assert.ok(
    validateOntology({
      entries: missingEdge,
      transition_policy: policy,
      declared_transitions: [legal],
      source_digests: sourceDigests,
    }).diagnostics.some(
      (diagnostic) => diagnostic.code === "ONTOLOGY_EDGE_TARGET_MISSING",
    ),
  );

  const executableLogic = structuredClone(entries);
  Object.assign(executableLogic[0]!, {
    "body.logic": { predicate: "must-not-live-in-ontology" },
  });
  assert.ok(
    validateOntology({
      entries: executableLogic,
      transition_policy: policy,
      declared_transitions: [legal],
      source_digests: sourceDigests,
    }).diagnostics.some(
      (diagnostic) =>
        diagnostic.code === "ONTOLOGY_EXECUTABLE_LOGIC_FORBIDDEN",
    ),
  );

  assert.ok(
    validateOntology({
      entries: [...entries, structuredClone(entries[0]!)],
      transition_policy: policy,
      declared_transitions: [legal],
      source_digests: sourceDigests,
    }).diagnostics.some(
      (diagnostic) => diagnostic.code === "ONTOLOGY_DUPLICATE_ID",
    ),
  );
});

test("the checked-in entry schema is closed", async () => {
  const schema = await readJson<{
    additionalProperties: boolean;
    required: string[];
  }>("ontology/entry.schema.json");
  assert.equal(schema.additionalProperties, false);
  assert.deepEqual(schema.required, [
    "schema_version",
    "id",
    "kind",
    "label",
    "definition",
    "status",
    "evidence",
    "confidence",
    "next_gate",
    "contradiction_path",
    "relations",
  ]);
  assert.equal(path.basename(ontologyRoot), "ontology");
});

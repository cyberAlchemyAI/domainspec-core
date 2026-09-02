import { describe, expect, it } from "vitest";

import manifest from "../../IMPLEMENTATION-MANIFEST.candidate.json";

const validatorModulePath = "../../scripts/check-implementation-manifest.mjs";

async function validator() {
  return import(validatorModulePath);
}

describe("Workspace implementation manifest", () => {
  it("returns PASS only for the exact current candidate binding", async () => {
    const { checkImplementationManifest } = await validator();
    const report = checkImplementationManifest({ manifest });

    expect(report).toMatchObject({
      status: "PASS",
      authority_effect: "none",
      canonical_generation_claim: false,
      retained_blockers: ["WORKSPACE_CATALOG_SNAPSHOT_DRIFT"],
    });
    expect(report.bindings.preserved_explore_snapshot.snapshot_id).not.toBe(
      report.bindings.ontology_canvas_graph.graph_epoch_sha256,
    );
  });

  it("fails closed when a bound source digest drifts", async () => {
    const { checkImplementationManifest } = await validator();
    const driftedManifest = structuredClone(manifest);
    driftedManifest.bindings.ontology_canvas_graph.nodes.sha256 = "0".repeat(64);

    expect(() =>
      checkImplementationManifest({ manifest: driftedManifest }),
    ).toThrowError(
      expect.objectContaining({
        code: "SOURCE_DIGEST_DRIFT",
      }),
    );
  });
});

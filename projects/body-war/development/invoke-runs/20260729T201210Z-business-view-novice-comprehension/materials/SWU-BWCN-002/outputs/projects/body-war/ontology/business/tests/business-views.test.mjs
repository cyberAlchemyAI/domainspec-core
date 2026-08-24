import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

import {
  featuredRelationExamples,
  graphViews,
  journeyStories,
  lifecycleViewPolicyIds,
  predicatePhrases,
  relationPhraseOverrides,
} from "../authoring/view-catalog.mjs";

const execFileAsync = promisify(execFile);
const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);

test("generated business views are current and source-resolved", async () => {
  const { stdout } = await execFileAsync(
    process.execPath,
    [path.join(packageRoot, "scripts/generate-views.mjs"), "--check"],
    { cwd: path.resolve(packageRoot, "../../../..") },
  );
  assert.match(stdout, /business views current/);
});

test("view projection explains branches, arrows, lifecycles, and authority boundaries", async () => {
  const markdown = await readFile(
    path.join(packageRoot, "BUSINESS-VIEWS.md"),
    "utf8",
  );
  assert.match(markdown, /## Which CAV2 view exists here\?/);
  assert.match(markdown, /System view \| \*\*Not yet modeled\.\*\*/);
  assert.match(markdown, /## Business view map/);
  assert.match(markdown, /## Arrow phrase glossary/);
  assert.match(markdown, /## Authority and next-view boundary/);
  assert.match(markdown, /generated\/views\/import-activities\.svg/);
  assert.match(markdown, /\[print-friendly HTML gallery\]\(BUSINESS-VIEWS\.html\)/);
  assert.match(
    markdown,
    /\[interactive journey experiment\]\(BUSINESS-JOURNEY-EXPERIMENT\.html\)/,
  );
  assert.match(
    markdown,
    /\[Import Activities\]\(nodes\/operation\.import-activities\.json\) \*\*uses as input\*\* \[ProviderAccount\]\(nodes\/entity\.provider-account\.json\)\. Typed predicate: `consumes`; relation: `body-war\.relation\.operation-7`\./,
  );
  assert.match(markdown, /does not promote/);
  assert.ok((markdown.match(/```mermaid/g) ?? []).length >= 11);
  for (const view of graphViews) {
    assert.match(
      markdown,
      new RegExp(`generated/views/${view.view_id}\\.svg`),
    );
  }
});

test("every graph and lifecycle view has an explicit question or policy identity", () => {
  assert.equal(graphViews.length, 6);
  assert.equal(featuredRelationExamples.length, 1);
  assert.equal(lifecycleViewPolicyIds.length, 5);
  for (const view of [...featuredRelationExamples, ...graphViews]) {
    assert.ok(view.question.length > 0);
    assert.ok(view.represents.length > 0);
    assert.ok(view.forbidden_claim.length > 0);
    assert.ok(view.relation_ids.length > 0);
  }
});

test("SVG relation sentences preserve readable and typed meanings", async () => {
  const exampleSvg = await readFile(
    path.join(packageRoot, "generated/views/import-activities.svg"),
    "utf8",
  );
  assert.match(exampleSvg, /role="img"/);
  assert.match(exampleSvg, /<title[^>]*>Import Activities relation sentences<\/title>/);
  assert.match(exampleSvg, /<desc[^>]*>/);
  assert.match(exampleSvg, />Import Activities<\/tspan>/);
  assert.match(exampleSvg, />uses as input<\/text>/);
  assert.match(exampleSvg, />consumes<\/text>/);
  assert.match(exampleSvg, />ProviderAccount<\/tspan>/);
  assert.match(exampleSvg, />creates or emits<\/text>/);
  assert.match(exampleSvg, />produces<\/text>/);
  assert.match(exampleSvg, />RunActivity<\/tspan>/);
  assert.match(exampleSvg, /Generated projection from nodes \+ relations\.json/);

  for (const view of graphViews) {
    const svg = await readFile(
      path.join(packageRoot, `generated/views/${view.view_id}.svg`),
      "utf8",
    );
    assert.match(svg, /role="img"/);
    assert.match(svg, new RegExp(`<title[^>]*>${view.title}</title>`));
  }
});

test("printable HTML contains paginating relation rows and lifecycle transitions", async () => {
  const html = await readFile(
    path.join(packageRoot, "BUSINESS-VIEWS.html"),
    "utf8",
  );
  assert.match(html, /<!doctype html>/);
  assert.match(html, /Printable relation-sentence gallery/);
  assert.match(html, /@page\{size:A4 landscape/);
  assert.match(html, /@media print/);
  assert.match(html, /class="print-relation"/);
  assert.match(html, /role="img"/);
  assert.match(html, /Import Activities/);
  assert.match(html, /consumes/);
  assert.match(html, /ProviderAccount/);
  assert.match(html, /Lifecycle transition views/);
  assert.match(html, /<th aria-label="transitions to">→<\/th>/);
});

test("journey stories are bounded review paths over existing relations", async () => {
  assert.equal(journeyStories.length, 2);
  const relationSet = JSON.parse(
    await readFile(
      path.join(packageRoot, "relations/relations.json"),
      "utf8",
    ),
  );
  const relationIds = new Set(
    relationSet.relations.map((relation) => relation.relation_id),
  );
  const expectedStoryCounts = new Map([
    ["login-to-score-preview", 32],
    ["activity-to-territory-preview", 15],
  ]);

  for (const story of journeyStories) {
    assert.ok(story.question.length > 0);
    assert.ok(story.summary.length > 0);
    assert.match(story.forbidden_claim, /does not prove|does not/i);
    const storyRelationIds = story.chapters.flatMap(
      (chapter) => chapter.relation_ids,
    );
    assert.equal(
      storyRelationIds.length,
      expectedStoryCounts.get(story.story_id),
    );
    assert.equal(
      new Set(storyRelationIds).size,
      storyRelationIds.length,
      `${story.story_id} repeats a relation`,
    );
    for (const relationId of storyRelationIds) {
      assert.ok(
        relationIds.has(relationId),
        `${story.story_id} references missing relation ${relationId}`,
      );
    }
  }
});

test("interactive journey experiment defaults to plain language with inspectable ontology details", async () => {
  const html = await readFile(
    path.join(packageRoot, "BUSINESS-JOURNEY-EXPERIMENT.html"),
    "utf8",
  );
  assert.match(html, /<title>Body War — Journey Ontology Experiment<\/title>/);
  assert.match(html, /<body>/);
  assert.equal((html.match(/<a class="story-tab"/g) ?? []).length, 2);
  assert.equal((html.match(/data-story-panel=/g) ?? []).length, 2);
  assert.doesNotMatch(html, /<button[^>]+role="tab"/);
  assert.match(html, /setAttribute\('role','tab'\)/);
  assert.match(html, /setAttribute\('role','tabpanel'\)/);
  assert.match(html, /Expand all ontology details/);
  assert.match(html, /<details class="ontology-details">/);
  assert.doesNotMatch(
    html,
    /<details class="ontology-details" open>/,
  );
  assert.match(html, /chapter order is a guided explanation/i);
  assert.match(html, /Sibling branch A/);
  assert.match(html, /Sibling branch B/);
  assert.match(
    html,
    /href="#activity-to-territory-preview-preview-evidence"><span>A<\/span>Review/,
  );
  assert.match(
    html,
    /href="#activity-to-territory-preview-controller-preview"><span>B<\/span>Project/,
  );
  assert.match(html, /Neither branch feeds the other/);
  assert.doesNotMatch(html, /After EvidenceSubmission/);
  assert.match(html, /0 new ontology edges/);
  assert.match(html, /data-relation-id="body-war\.relation\.select-reads-track"/);
  assert.match(
    html,
    /data-relation-id="body-war\.relation\.confirm-consumes-activity"/,
  );
  assert.match(html, /data-relation-id="body-war\.relation\.operation-7"/);
  assert.match(html, /Import Activities/);
  assert.match(html, /uses as input/);
  assert.match(html, /ProviderAccount/);
  assert.match(html, /<code>consumes<\/code>/);
  assert.match(html, /body-war\.product-ontology-owner/);
  assert.match(html, /<ul class="relation-list">/);
  assert.doesNotMatch(html, /<ol class="relation-list">/);
  assert.match(html, /Blocked — owner decision required/);
  assert.match(html, /Explicitly does not promote/);
  assert.match(html, /Projection only/);
  assert.match(html, /<dt>Relation owner<\/dt>/);
  assert.match(html, /<dt>Blocking owner<\/dt>/);
  assert.match(html, /<dt>Next gate<\/dt>/);
  assert.match(html, /data-residue-id="body-war\.residue\.geometry-privacy"/);
  assert.match(html, /data-residue-id="body-war\.residue\.geometry-promotion"/);
  assert.match(html, /body-war\.data-privacy-owner/);
  assert.match(html, /DEC-JSP-002 decision-gate/);
  assert.match(html, /status: candidate-local/);
  assert.match(html, /authority_effect: none/);
  assert.match(html, /release_admission: not-granted/);
  assert.doesNotMatch(html, /class="mermaid"|```mermaid/);
  assert.match(html, /ArrowRight/);
  assert.match(html, /prefers-reduced-motion/);
  assert.match(html, /@media print/);
});

test("journey residue joins preserve zero, one, and multiple endpoint matches", async () => {
  const relationSet = JSON.parse(
    await readFile(
      path.join(packageRoot, "relations/relations.json"),
      "utf8",
    ),
  );
  const residue = JSON.parse(
    await readFile(path.join(packageRoot, "residue.json"), "utf8"),
  );
  const matchCount = (relationId) => {
    const relation = relationSet.relations.find(
      (candidate) => candidate.relation_id === relationId,
    );
    assert.ok(relation);
    return residue.items.filter((item) =>
      item.affected_concepts.some(
        (conceptId) =>
          conceptId === relation.source_concept ||
          conceptId === relation.target_concept,
      ),
    ).length;
  };
  assert.equal(matchCount("body-war.relation.visitor-authenticates"), 0);
  assert.equal(
    matchCount("body-war.relation.calculate-preview-consumes-policy"),
    1,
  );
  assert.equal(matchCount("body-war.relation.candidate-supports-geometry"), 2);
});

test("plain-language phrases cover the admitted relation vocabulary", async () => {
  const relationSet = JSON.parse(
    await readFile(
      path.join(packageRoot, "relations/relations.json"),
      "utf8",
    ),
  );
  const predicates = new Set(
    relationSet.relations.map((relation) => relation.predicate),
  );
  assert.deepEqual(
    [...predicates].filter(
      (predicate) => !(predicate in predicatePhrases),
    ),
    [],
  );
  for (const relationId of Object.keys(relationPhraseOverrides)) {
    assert.ok(
      relationSet.relations.some(
        (relation) => relation.relation_id === relationId,
      ),
      `phrase override references missing relation ${relationId}`,
    );
  }
});

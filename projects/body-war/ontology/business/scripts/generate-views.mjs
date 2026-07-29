import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  featuredRelationExamples,
  graphViews,
  journeyStories,
  lifecycleViewPolicyIds,
  predicatePhrases,
  relationPhraseOverrides,
} from "../authoring/view-catalog.mjs";

const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const nodeRoot = path.join(packageRoot, "nodes");
const lifecycleRoot = path.join(packageRoot, "lifecycle-policies");
const outputPath = path.join(packageRoot, "BUSINESS-VIEWS.md");
const htmlOutputPath = path.join(packageRoot, "BUSINESS-VIEWS.html");
const journeyExperimentOutputPath = path.join(
  packageRoot,
  "BUSINESS-JOURNEY-EXPERIMENT.html",
);
const generatedViewRoot = path.join(packageRoot, "generated", "views");

async function readJson(absolutePath) {
  return JSON.parse(await readFile(absolutePath, "utf8"));
}

function escapeMermaid(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeXml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

function escapeHtml(value) {
  return escapeXml(value);
}

function nodeFilename(conceptId) {
  return `${conceptId.replace("body-war.business.", "")}.json`;
}

function statusClass(status) {
  return status.replaceAll("-", "_");
}

function phraseFor(relation) {
  return (
    relationPhraseOverrides[relation.relation_id] ??
    predicatePhrases[relation.predicate]
  );
}

const nodeNames = (await readdir(nodeRoot))
  .filter((name) => name.endsWith(".json") && name !== "manifest.json")
  .sort();
const nodes = await Promise.all(
  nodeNames.map((name) => readJson(path.join(nodeRoot, name))),
);
const nodeById = new Map(nodes.map((node) => [node.concept_id, node]));

const relationSet = await readJson(
  path.join(packageRoot, "relations/relations.json"),
);
const packageProfile = await readJson(path.join(packageRoot, "profile.json"));
const residueProjection = await readJson(path.join(packageRoot, "residue.json"));
const relationById = new Map(
  relationSet.relations.map((relation) => [
    relation.relation_id,
    relation,
  ]),
);

const lifecycleNames = (await readdir(lifecycleRoot))
  .filter((name) => name.endsWith(".json"))
  .sort();
const lifecyclePolicies = await Promise.all(
  lifecycleNames.map((name) => readJson(path.join(lifecycleRoot, name))),
);
const lifecycleById = new Map(
  lifecyclePolicies.map((policy) => [policy.policy_id, policy]),
);

const missingPhrases = [
  ...new Set(relationSet.relations.map((relation) => relation.predicate)),
].filter((predicate) => !(predicate in predicatePhrases));
if (missingPhrases.length > 0) {
  throw new Error(
    `Missing plain-language predicate phrases: ${missingPhrases.join(", ")}`,
  );
}

function relationsForView(view) {
  return view.relation_ids.map((relationId) => {
    const relation = relationById.get(relationId);
    if (!relation) {
      throw new Error(
        `View ${view.view_id} references missing relation ${relationId}`,
      );
    }
    if (
      !nodeById.has(relation.source_concept) ||
      !nodeById.has(relation.target_concept)
    ) {
      throw new Error(
        `View ${view.view_id} relation ${relationId} has a missing endpoint`,
      );
    }
    return relation;
  });
}

function renderGraphView(view) {
  const relations = relationsForView(view);
  const conceptIds = [
    ...new Set(
      relations.flatMap((relation) => [
        relation.source_concept,
        relation.target_concept,
      ]),
    ),
  ].sort();
  const aliases = new Map(
    conceptIds.map((conceptId, index) => [conceptId, `N${index}`]),
  );
  const lines = [
    `## ${view.title}`,
    "",
    `**Question:** ${view.question}`,
    "",
    `**Represents:** ${view.represents}`,
    "",
    `![${view.title}: typed relation sentences](generated/views/${view.view_id}.svg)`,
    "",
    "<details>",
    "<summary>Open Mermaid network projection</summary>",
    "",
    "```mermaid",
    "flowchart LR",
  ];

  for (const conceptId of conceptIds) {
    const node = nodeById.get(conceptId);
    const alias = aliases.get(conceptId);
    lines.push(
      `  ${alias}["${escapeMermaid(node.label)}<br/>${escapeMermaid(node.business_kind)} · ${escapeMermaid(node.candidate_status)}"]`,
    );
  }

  for (const relation of relations) {
    const source = aliases.get(relation.source_concept);
    const target = aliases.get(relation.target_concept);
    const phrase = escapeMermaid(phraseFor(relation));
    if (
      relation.authority_effect === "blocked" ||
      relation.predicate === "does_not_promote"
    ) {
      lines.push(`  ${source} -. "${phrase}" .-> ${target}`);
    } else if (relation.authority_effect === "projection") {
      lines.push(`  ${source} -. "${phrase}" .-> ${target}`);
    } else {
      lines.push(`  ${source} -->|"${phrase}"| ${target}`);
    }
  }

  lines.push(
    "  classDef reviewed_candidate fill:#e8f5e9,stroke:#2e7d32,color:#16351b",
    "  classDef candidate fill:#fff8e1,stroke:#f9a825,color:#4a3500",
    "  classDef blocked fill:#ffebee,stroke:#c62828,color:#5a1010",
    "  classDef deferred fill:#eceff1,stroke:#607d8b,color:#263238",
    "  classDef projected fill:#e3f2fd,stroke:#1565c0,color:#0d315f",
  );
  for (const conceptId of conceptIds) {
    const node = nodeById.get(conceptId);
    lines.push(
      `  class ${aliases.get(conceptId)} ${statusClass(node.candidate_status)}`,
    );
  }
  lines.push(
    "```",
    "",
    "</details>",
    "",
    "### Read the arrows as sentences",
    "",
  );

  for (const relation of relations) {
    const source = nodeById.get(relation.source_concept);
    const target = nodeById.get(relation.target_concept);
    lines.push(
      `- [${source.label}](nodes/${nodeFilename(source.concept_id)}) **${phraseFor(relation)}** [${target.label}](nodes/${nodeFilename(target.concept_id)}). Typed predicate: \`${relation.predicate}\`; relation: \`${relation.relation_id}\`.`,
    );
  }
  lines.push("", `**Boundary:** ${view.forbidden_claim}`, "");
  return lines;
}

const statusPalette = {
  "reviewed-candidate": {
    fill: "#e8f5e9",
    stroke: "#2e7d32",
    text: "#16351b",
  },
  candidate: {
    fill: "#fff8e1",
    stroke: "#f9a825",
    text: "#4a3500",
  },
  blocked: {
    fill: "#ffebee",
    stroke: "#c62828",
    text: "#5a1010",
  },
  deferred: {
    fill: "#eceff1",
    stroke: "#607d8b",
    text: "#263238",
  },
  projected: {
    fill: "#e3f2fd",
    stroke: "#1565c0",
    text: "#0d315f",
  },
};

function paletteFor(status) {
  return (
    statusPalette[status] ?? {
      fill: "#f8fafc",
      stroke: "#64748b",
      text: "#0f172a",
    }
  );
}

function wrapWords(value, limit = 31) {
  const words = String(value).split(/\s+/);
  const lines = [];
  let current = "";
  for (const word of words) {
    const candidate = current ? `${current} ${word}` : word;
    if (candidate.length > limit && current) {
      lines.push(current);
      current = word;
    } else {
      current = candidate;
    }
  }
  if (current) lines.push(current);
  return lines.slice(0, 2);
}

function renderTextLines(lines, x, firstY, className, lineHeight = 20) {
  return [
    `<text x="${x}" y="${firstY}" class="${className}">`,
    ...lines.map(
      (line, index) =>
        `<tspan x="${x}" dy="${index === 0 ? 0 : lineHeight}">${escapeXml(line)}</tspan>`,
    ),
    "</text>",
  ].join("");
}

function relationPresentation(relation) {
  if (
    relation.authority_effect === "blocked" ||
    relation.predicate === "does_not_promote"
  ) {
    return { className: "edge blocked-edge", label: "blocked meaning" };
  }
  if (relation.authority_effect === "projection") {
    return { className: "edge projection-edge", label: "projection-only meaning" };
  }
  return { className: "edge", label: "admitted candidate meaning" };
}

function renderNodeCard(node, x, y) {
  const palette = paletteFor(node.candidate_status);
  const labelLines = wrapWords(node.label);
  return [
    `<g class="node-card">`,
    `<rect x="${x}" y="${y}" width="350" height="104" rx="14" fill="${palette.fill}" stroke="${palette.stroke}" stroke-width="2"/>`,
    renderTextLines(labelLines, x + 18, y + 29, "node-label"),
    `<text x="${x + 18}" y="${y + 73}" class="node-meta" fill="${palette.text}">${escapeXml(node.business_kind)} · ${escapeXml(node.candidate_status)}</text>`,
    `<text x="${x + 18}" y="${y + 91}" class="node-id">${escapeXml(node.concept_id)}</text>`,
    "</g>",
  ].join("");
}

function renderRelationRow(relation, y, markerId) {
  const source = nodeById.get(relation.source_concept);
  const target = nodeById.get(relation.target_concept);
  const phrase = phraseFor(relation);
  const presentation = relationPresentation(relation);
  const accessibleSentence = `${source.label} ${phrase} ${target.label}. Typed predicate ${relation.predicate}. Authority effect ${relation.authority_effect}. Owner route ${relation.owner_route}. Relation ${relation.relation_id}.`;
  return [
    `<g transform="translate(0 ${y})" aria-label="${escapeXml(accessibleSentence)}">`,
    `<rect x="20" y="4" width="1240" height="146" rx="16" class="relation-row"/>`,
    renderNodeCard(source, 40, 16),
    `<line x1="408" y1="59" x2="872" y2="59" class="${presentation.className}" marker-end="url(#${markerId})"/>`,
    `<text x="640" y="41" text-anchor="middle" class="relation-phrase">${escapeXml(phrase)}</text>`,
    `<rect x="552" y="69" width="176" height="25" rx="12" class="predicate-pill"/>`,
    `<text x="640" y="86" text-anchor="middle" class="predicate">${escapeXml(relation.predicate)}</text>`,
    `<text x="640" y="108" text-anchor="middle" class="relation-effect">${escapeXml(`${presentation.label} · authority_effect: ${relation.authority_effect}`)}</text>`,
    renderNodeCard(target, 890, 16),
    `<text x="640" y="139" text-anchor="middle" class="relation-id">${escapeXml(`${relation.relation_id} · owner: ${relation.owner_route}`)}</text>`,
    "</g>",
  ].join("\n");
}

function renderRelationSvg(view) {
  const relations = relationsForView(view);
  const width = 1280;
  const headerHeight = 128;
  const rowHeight = 154;
  const footerHeight = 54;
  const height = headerHeight + relations.length * rowHeight + footerHeight;
  const markerId = `arrow-${view.view_id}`;
  const sentences = relations
    .map((relation) => {
      const source = nodeById.get(relation.source_concept);
      const target = nodeById.get(relation.target_concept);
      return `${source.label} ${phraseFor(relation)} ${target.label}. Typed predicate ${relation.predicate}; authority effect ${relation.authority_effect}; owner route ${relation.owner_route}; relation ID ${relation.relation_id}.`;
    })
    .join(" ");
  return [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="${view.view_id}-title ${view.view_id}-desc">`,
    `<title id="${view.view_id}-title">${escapeXml(view.title)}</title>`,
    `<desc id="${view.view_id}-desc">${escapeXml(`${view.represents} ${sentences} Boundary: ${view.forbidden_claim}`)}</desc>`,
    "<defs>",
    `<marker id="${markerId}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">`,
    '<path d="M 0 0 L 10 5 L 0 10 z" fill="#334155"/>',
    "</marker>",
    "</defs>",
    "<style>",
    "text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,\"Segoe UI\",sans-serif}",
    ".canvas{fill:#f8fafc}.header-rule{stroke:#cbd5e1;stroke-width:1}",
    ".title{font-size:28px;font-weight:750;fill:#0f172a}.question{font-size:16px;fill:#475569}",
    ".relation-row{fill:#ffffff;stroke:#e2e8f0}.node-label{font-size:17px;font-weight:700;fill:#0f172a}.node-meta{font-size:12px;font-weight:650}.node-id{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:8.5px;fill:#475569}",
    ".edge{stroke:#334155;stroke-width:3;fill:none}.blocked-edge{stroke:#c62828;stroke-dasharray:9 7}.projection-edge{stroke:#1565c0;stroke-dasharray:9 7}",
    ".relation-phrase{font-size:16px;font-weight:700;fill:#0f172a}.predicate-pill{fill:#eef2ff;stroke:#818cf8}",
    ".predicate{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;font-weight:700;fill:#3730a3}",
    ".relation-effect{font-size:10px;fill:#64748b}.relation-id{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:9px;fill:#334155}.footer{font-size:12px;fill:#475569}",
    "</style>",
    `<rect width="${width}" height="${height}" class="canvas"/>`,
    `<text x="40" y="45" class="title">${escapeXml(view.title)}</text>`,
    `<text x="40" y="77" class="question">${escapeXml(view.question)}</text>`,
    `<text x="40" y="103" class="question">source node — plain-language phrase —▶ target node · typed predicate appears below the arrow</text>`,
    '<line x1="40" y1="118" x2="1240" y2="118" class="header-rule"/>',
    ...relations.map((relation, index) =>
      renderRelationRow(relation, headerHeight + index * rowHeight, markerId),
    ),
    `<text x="40" y="${height - 20}" class="footer">Generated projection from nodes + relations.json. It explains meaning; it is not authority or runtime proof.</text>`,
    "</svg>",
    "",
  ].join("\n");
}

function renderHtmlRelationRow(relation, index, viewId) {
  const markerId = `html-arrow-${viewId}-${index}`;
  const source = nodeById.get(relation.source_concept);
  const target = nodeById.get(relation.target_concept);
  const sentence = `${source.label} ${phraseFor(relation)} ${target.label}. Typed predicate: ${relation.predicate}; authority effect: ${relation.authority_effect}; owner route: ${relation.owner_route}; relation: ${relation.relation_id}.`;
  return [
    '<div class="print-relation">',
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 154" role="img" aria-label="${escapeHtml(sentence)}">`,
    "<defs>",
    `<marker id="${markerId}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">`,
    '<path d="M 0 0 L 10 5 L 0 10 z" fill="#334155"></path>',
    "</marker>",
    "</defs>",
    renderRelationRow(relation, 0, markerId),
    "</svg>",
    `<p class="relation-text">${escapeHtml(sentence)}</p>`,
    "</div>",
  ].join("\n");
}

function renderLifecycleHtml(policy) {
  const label = nodeById.get(policy.subject_concept)?.label ?? policy.policy_id;
  return [
    '<section class="view lifecycle">',
    `<h2>${escapeHtml(label)}</h2>`,
    `<p><strong>Owner route:</strong> <code>${escapeHtml(policy.owner_route)}</code> · <strong>Authority effect:</strong> <code>${escapeHtml(policy.authority_effect)}</code></p>`,
    "<table>",
    "<thead><tr><th>From</th><th aria-label=\"transitions to\">→</th><th>To</th><th>Trigger</th><th>Availability</th></tr></thead>",
    "<tbody>",
    ...policy.transitions.map(
      (transition) =>
        `<tr><td><code>${escapeHtml(transition.from)}</code></td><td>→</td><td><code>${escapeHtml(transition.to)}</code></td><td>${escapeHtml(transition.trigger)}</td><td><code>${escapeHtml(transition.prototype_availability)}</code></td></tr>`,
    ),
    "</tbody>",
    "</table>",
    `<p class="boundary"><strong>Boundary:</strong> ${escapeHtml(policy.forbidden_collapse.join(" "))}</p>`,
    "</section>",
  ].join("\n");
}

function renderPrintableHtml() {
  const allRelationViews = [...featuredRelationExamples, ...graphViews];
  return [
    "<!doctype html>",
    '<html lang="en">',
    "<head>",
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    "<title>Body War Business Ontology — Printable Relation Views</title>",
    "<style>",
    ":root{color-scheme:light;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,\"Segoe UI\",sans-serif;color:#0f172a;background:#e2e8f0}",
    "*{box-sizing:border-box}body{margin:0}.page{max-width:1440px;margin:0 auto;padding:32px;background:#fff}",
    "h1{font-size:2rem;margin:.2rem 0}h2{font-size:1.45rem;margin:0 0 .35rem}p{line-height:1.45}.lede{color:#475569;max-width:85ch}",
    ".view{margin:36px 0;padding-top:22px;border-top:2px solid #cbd5e1}.question{font-weight:700}.represents{color:#334155}.boundary{padding:12px 14px;border-left:4px solid #c62828;background:#fff1f2}",
    ".print-relation{break-inside:avoid;margin:8px 0}.print-relation svg{display:block;width:100%;height:auto}.relation-text{margin:2px 24px 12px;color:#334155;font-size:.8rem}",
    ".relation-row{fill:#fff;stroke:#e2e8f0}.node-label{font-size:17px;font-weight:700;fill:#0f172a}.node-meta{font-size:12px;font-weight:650}.node-id{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:8.5px;fill:#475569}",
    ".edge{stroke:#334155;stroke-width:3;fill:none}.blocked-edge{stroke:#c62828;stroke-dasharray:9 7}.projection-edge{stroke:#1565c0;stroke-dasharray:9 7}",
    ".relation-phrase{font-size:16px;font-weight:700;fill:#0f172a}.predicate-pill{fill:#eef2ff;stroke:#818cf8}.predicate{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;font-weight:700;fill:#3730a3}",
    ".relation-effect{font-size:10px;fill:#64748b}.relation-id{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:9px;fill:#334155}",
    "table{width:100%;border-collapse:collapse;font-size:.88rem}th,td{border:1px solid #cbd5e1;padding:7px;text-align:left}th{background:#f1f5f9}",
    "code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9em}",
    "@page{size:A4 landscape;margin:10mm}",
    "@media print{body{background:#fff}.page{max-width:none;padding:0}.view{break-before:page;margin:0;padding-top:0;border-top:0}.view:first-of-type{break-before:auto}.print-relation{margin:4mm 0}a{color:inherit;text-decoration:none}}",
    "</style>",
    "</head>",
    "<body>",
    '<main class="page">',
    "<h1>Body War Business Ontology</h1>",
    "<p class=\"lede\">Printable relation-sentence gallery generated from the business ontology nodes, typed relations, and lifecycle policies. It is a review projection, not a definition store, promotion decision, DomainSpec graph, implementation claim, or runtime proof.</p>",
    ...allRelationViews.flatMap((view) => {
      const relations = relationsForView(view);
      return [
        `<section class="view" id="${escapeHtml(view.view_id ?? view.example_id)}">`,
        `<h2>${escapeHtml(view.title)}</h2>`,
        `<p class="question">Question: ${escapeHtml(view.question)}</p>`,
        `<p class="represents">${escapeHtml(view.represents)}</p>`,
        ...relations.map((relation, index) =>
          renderHtmlRelationRow(
            relation,
            index,
            view.view_id ?? view.example_id,
          ),
        ),
        `<p class="boundary"><strong>Boundary:</strong> ${escapeHtml(view.forbidden_claim)}</p>`,
        "</section>",
      ];
    }),
    '<section class="view">',
    "<h2>Lifecycle transition views</h2>",
    "<p>Lifecycle status is separate from ontology candidate status. Each row reads from-state → to-state under a named trigger.</p>",
    "</section>",
    ...lifecycleViewPolicyIds.map((policyId) => {
      const policy = lifecycleById.get(policyId);
      if (!policy) throw new Error(`Missing lifecycle policy ${policyId}`);
      return renderLifecycleHtml(policy);
    }),
    "</main>",
    "</body>",
    "</html>",
    "",
  ].join("\n");
}

function relationsForChapter(story, chapter) {
  return relationsForView({
    view_id: `${story.story_id}/${chapter.chapter_id}`,
    relation_ids: chapter.relation_ids,
  });
}

function journeyRelationTone(relation) {
  const source = nodeById.get(relation.source_concept);
  const target = nodeById.get(relation.target_concept);
  if (relation.predicate === "does_not_promote") {
    return {
      className: "nonpromotion",
      label: "Explicitly does not promote",
    };
  }
  if (
    relation.authority_effect === "projection" ||
    relation.predicate === "projects" ||
    source.candidate_status === "projected" ||
    target.candidate_status === "projected"
  ) {
    return { className: "projection", label: "Projection only" };
  }
  const residueMatches = residueForRelation(relation);
  if (
    relation.authority_effect === "blocked" ||
    source.candidate_status === "blocked" ||
    target.candidate_status === "blocked" ||
    residueMatches.some((item) => item.status === "blocked")
  ) {
    return {
      className: "gate",
      label: "Blocked — owner decision required",
    };
  }
  return { className: "candidate", label: "Candidate meaning" };
}

function residueForRelation(relation) {
  const endpoints = new Set([
    relation.source_concept,
    relation.target_concept,
  ]);
  return residueProjection.items.filter((item) =>
    item.affected_concepts.some((conceptId) => endpoints.has(conceptId)),
  );
}

function renderJourneyRelationCard(relation) {
  const source = nodeById.get(relation.source_concept);
  const target = nodeById.get(relation.target_concept);
  const phrase = phraseFor(relation);
  const tone = journeyRelationTone(relation);
  const residueMatches = residueForRelation(relation);
  const accessibleSentence = `${source.label} ${phrase} ${target.label}. Typed predicate ${relation.predicate}.`;
  return [
    `<li class="relation-card ${tone.className}" data-relation-id="${escapeHtml(relation.relation_id)}">`,
    `<div class="relation-reading" aria-label="${escapeHtml(accessibleSentence)}">`,
    '<div class="friendly-node source-node">',
    `<span class="node-kind">${escapeHtml(source.business_kind)}</span>`,
    `<strong>${escapeHtml(source.label)}</strong>`,
    "</div>",
    '<div class="friendly-arrow">',
    `<span>${escapeHtml(phrase)}</span>`,
    '<svg viewBox="0 0 180 28" aria-hidden="true" focusable="false"><line x1="4" y1="14" x2="164" y2="14"></line><path d="M154 4 L168 14 L154 24"></path></svg>',
    `<small>${escapeHtml(tone.label)}</small>`,
    "</div>",
    '<div class="friendly-node target-node">',
    `<span class="node-kind">${escapeHtml(target.business_kind)}</span>`,
    `<strong>${escapeHtml(target.label)}</strong>`,
    "</div>",
    "</div>",
    '<details class="ontology-details">',
    "<summary>Inspect ontology details</summary>",
    "<dl>",
    `<div><dt>Predicate</dt><dd><code>${escapeHtml(relation.predicate)}</code></dd></div>`,
    `<div><dt>Authority effect</dt><dd><code>${escapeHtml(relation.authority_effect)}</code></dd></div>`,
    `<div><dt>Relation</dt><dd><code>${escapeHtml(relation.relation_id)}</code></dd></div>`,
    `<div><dt>Relation owner</dt><dd><code>${escapeHtml(relation.owner_route)}</code></dd></div>`,
    ...residueMatches.map(
      (item) =>
        `<div class="wide blocking-context" data-residue-id="${escapeHtml(item.residue_id)}" data-residue-status="${escapeHtml(item.status)}"><dt>Blocking owner</dt><dd><code>${escapeHtml(item.owner_route)}</code></dd><dt>Next gate</dt><dd>${escapeHtml(item.next_gate)}</dd></div>`,
    ),
    `<div class="wide"><dt>Source concept</dt><dd><code>${escapeHtml(source.concept_id)}</code></dd></div>`,
    `<div class="wide"><dt>Target concept</dt><dd><code>${escapeHtml(target.concept_id)}</code></dd></div>`,
    "</dl>",
    "</details>",
    "</li>",
  ].join("\n");
}

function renderJourneyChapter(story, chapter, chapterIndex) {
  const relations = relationsForChapter(story, chapter);
  const sectionId = `${story.story_id}-${chapter.chapter_id}`;
  return [
    `<section class="chapter" id="${escapeHtml(sectionId)}" aria-labelledby="${escapeHtml(sectionId)}-title">`,
    '<div class="chapter-heading">',
    `<span class="chapter-number" aria-hidden="true">${escapeHtml(chapter.marker ?? chapterIndex + 1)}</span>`,
    "<div>",
    `<p class="chapter-kicker">${escapeHtml(chapter.review_label ?? `Review chapter ${chapterIndex + 1}`)} · ${relations.length} typed ${relations.length === 1 ? "relation" : "relations"}</p>`,
    `<h3 id="${escapeHtml(sectionId)}-title">${escapeHtml(chapter.title)}</h3>`,
    `<p>${escapeHtml(chapter.summary)}</p>`,
    "</div>",
    "</div>",
    '<ul class="relation-list">',
    ...relations.map(renderJourneyRelationCard),
    "</ul>",
    "</section>",
  ].join("\n");
}

function renderJourneyStory(story, storyIndex) {
  const relationCount = story.chapters.reduce(
    (total, chapter) => total + chapter.relation_ids.length,
    0,
  );
  return [
    `<article class="story-panel" id="story-${escapeHtml(story.story_id)}" data-story-panel="${escapeHtml(story.story_id)}">`,
    '<header class="story-header">',
    `<p class="eyebrow">${escapeHtml(story.eyebrow)}</p>`,
    `<h2>${escapeHtml(story.title)}</h2>`,
    `<p class="story-question">${escapeHtml(story.question)}</p>`,
    `<p>${escapeHtml(story.summary)}</p>`,
    `<div class="story-facts"><span>${story.chapters.length} review chapters</span><span>${relationCount} exact typed relations</span><span>0 new ontology edges</span></div>`,
    "</header>",
    `<nav class="chapter-nav" aria-label="${escapeHtml(story.title)} chapters">`,
    "<p>Jump to a chapter</p>",
    "<ol>",
    ...story.chapters.map(
      (chapter, chapterIndex) =>
        `<li><a href="#${escapeHtml(`${story.story_id}-${chapter.chapter_id}`)}"><span>${escapeHtml(chapter.marker ?? chapterIndex + 1)}</span>${escapeHtml(chapter.short_label)}</a></li>`,
    ),
    "</ol>",
    "</nav>",
    '<div class="sequence-note" role="note"><strong>How to read this:</strong> chapter order is a guided explanation. Only each labeled arrow is an ontology relation; the page does not assert operation-to-operation runtime sequence.</div>',
    ...(story.reading_note
      ? [
          `<div class="branch-note" role="note"><strong>Branching meaning:</strong> ${escapeHtml(story.reading_note)}</div>`,
        ]
      : []),
    ...story.chapters.map((chapter, chapterIndex) =>
      renderJourneyChapter(story, chapter, chapterIndex),
    ),
    '<aside class="story-boundary">',
    "<span>What this story cannot prove</span>",
    `<p>${escapeHtml(story.forbidden_claim)}</p>`,
    "</aside>",
    "</article>",
  ].join("\n");
}

function renderJourneyExperimentHtml() {
  const relationCount = journeyStories.reduce(
    (storyTotal, story) =>
      storyTotal +
      story.chapters.reduce(
        (chapterTotal, chapter) =>
          chapterTotal + chapter.relation_ids.length,
        0,
      ),
    0,
  );
  return [
    "<!doctype html>",
    '<html lang="en">',
    "<head>",
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    "<title>Body War — Journey Ontology Experiment</title>",
    "<style>",
    ":root{color-scheme:light;--ink:#10243e;--muted:#5e6d7d;--paper:#f7f7f2;--card:#fff;--line:#dce2e6;--accent:#ff5d3b;--accent-dark:#b92e18;--blue:#176b87;--green:#26734d;--amber:#9a5b00;--red:#a92d29;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,\"Segoe UI\",sans-serif}",
    "*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--paper)}button,input,a{font:inherit}a{color:var(--blue)}",
    ".site-header{background:linear-gradient(135deg,#10243e 0%,#163b52 62%,#176b87 100%);color:#fff;padding:24px clamp(20px,6vw,88px) 54px}.topline{display:flex;align-items:center;justify-content:space-between;gap:20px;max-width:1240px;margin:0 auto 60px}.brand{font-weight:850;letter-spacing:.04em}.projection-badge{display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(255,255,255,.38);border-radius:999px;padding:7px 12px;font-size:.78rem;font-weight:750}.projection-badge::before{content:\"\";width:8px;height:8px;border-radius:50%;background:#ffb59f}",
    ".hero{max-width:900px;margin:0 auto 0 0}.hero .eyebrow,.story-header .eyebrow{margin:0 0 10px;text-transform:uppercase;letter-spacing:.13em;font-size:.74rem;font-weight:850;color:#ffb59f}.hero h1{max-width:760px;margin:0;font-size:clamp(2.4rem,6vw,5.2rem);line-height:.96;letter-spacing:-.055em}.hero p{max-width:760px;margin:24px 0 0;font-size:clamp(1rem,2vw,1.25rem);line-height:1.6;color:#d9e6eb}",
    ".workspace{max-width:1240px;margin:-28px auto 80px;padding:0 24px}.control-deck{position:sticky;top:12px;z-index:10;display:grid;grid-template-columns:1fr auto;gap:20px;align-items:center;padding:18px;background:rgba(255,255,255,.94);backdrop-filter:blur(16px);border:1px solid var(--line);border-radius:20px;box-shadow:0 18px 50px rgba(16,36,62,.13)}",
    ".story-tabs{display:flex;gap:8px;flex-wrap:wrap}.story-tabs .story-tab{appearance:none;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--ink);padding:11px 15px;font-weight:780;cursor:pointer;text-decoration:none}.story-tabs .story-tab[aria-selected=\"true\"]{color:#fff;background:var(--ink);border-color:var(--ink)}.story-tabs .story-tab:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #ffad98;outline-offset:3px}",
    ".detail-toggle{display:flex;align-items:center;gap:10px;color:var(--muted);font-size:.88rem;font-weight:750;white-space:nowrap}.detail-toggle input{width:20px;height:20px;accent-color:var(--accent)}",
    ".story-panel{padding-top:42px}.js .story-panel[hidden]{display:none}.story-header{max-width:900px}.story-header .eyebrow{color:var(--accent-dark)}.story-header h2{margin:0;font-size:clamp(2rem,4vw,3.6rem);line-height:1;letter-spacing:-.04em}.story-question{font-size:1.2rem;font-weight:720;line-height:1.45}.story-header>p:last-of-type{color:var(--muted);line-height:1.6}.story-facts{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}.story-facts span{border:1px solid var(--line);border-radius:999px;background:#fff;padding:7px 11px;font-size:.8rem;font-weight:760;color:var(--muted)}",
    ".chapter-nav{margin:32px 0;padding:18px 20px;background:#edf4f4;border-radius:18px}.chapter-nav>p{margin:0 0 12px;font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;font-weight:850;color:var(--muted)}.chapter-nav ol{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin:0;padding:0}.chapter-nav a{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--ink);font-weight:780;padding:10px;border-radius:10px}.chapter-nav a:hover{background:#fff}.chapter-nav a span{display:grid;place-items:center;width:27px;height:27px;border-radius:50%;background:var(--ink);color:#fff;font-size:.75rem}",
    ".sequence-note{margin:24px 0 42px;padding:16px 18px;border-left:4px solid var(--blue);background:#e9f3f6;color:#24485a;line-height:1.5}.chapter{scroll-margin-top:120px;margin:0 0 64px}.chapter-heading{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:start;margin-bottom:20px}.chapter-number{display:grid;place-items:center;width:46px;height:46px;border-radius:14px;background:var(--accent);color:#fff;font-size:1.1rem;font-weight:900;box-shadow:0 8px 20px rgba(255,93,59,.25)}.chapter-kicker{margin:0 0 5px;text-transform:uppercase;letter-spacing:.08em;font-size:.72rem;font-weight:850;color:var(--accent-dark)}.chapter h3{margin:0;font-size:clamp(1.4rem,3vw,2rem);letter-spacing:-.025em}.chapter-heading p:last-child{margin:8px 0 0;color:var(--muted);line-height:1.5}",
    ".relation-list{list-style:none;margin:0;padding:0;display:grid;gap:14px;min-width:0}.relation-card{position:relative;min-width:0;padding:18px;border:1px solid var(--line);border-left:5px solid var(--green);border-radius:18px;background:var(--card);box-shadow:0 8px 24px rgba(16,36,62,.055)}.relation-card.gate{border-left-color:var(--amber)}.relation-card.projection{border-left-color:var(--blue)}.relation-card.nonpromotion{border-left-color:var(--red);background:#fff9f8}",
    ".relation-reading{display:grid;grid-template-columns:minmax(0,1fr) minmax(150px,.72fr) minmax(0,1fr);gap:18px;align-items:center;min-width:0}.friendly-node{min-width:0;min-height:86px;display:flex;flex-direction:column;justify-content:center;padding:14px 16px;border:1px solid var(--line);border-radius:13px;background:#fafbf8}.friendly-node strong{font-size:1rem;line-height:1.25;overflow-wrap:anywhere}.node-kind{margin-bottom:6px;text-transform:uppercase;letter-spacing:.08em;font-size:.64rem;font-weight:850;color:var(--muted)}",
    ".friendly-arrow{text-align:center;color:var(--ink)}.friendly-arrow>span{display:block;font-weight:850;font-size:.9rem}.friendly-arrow svg{display:block;width:100%;height:28px;overflow:visible}.friendly-arrow line{stroke:currentColor;stroke-width:2.5}.friendly-arrow path{fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:2.5}.friendly-arrow small{display:inline-block;margin-top:3px;color:var(--green);font-size:.68rem;font-weight:820;text-transform:uppercase;letter-spacing:.05em}.gate .friendly-arrow small{color:var(--amber)}.projection .friendly-arrow small{color:var(--blue)}.nonpromotion .friendly-arrow small{color:var(--red)}",
    ".ontology-details{margin:16px 0 0;padding-top:14px;border-top:1px dashed var(--line)}.ontology-details summary{width:max-content;max-width:100%;cursor:pointer;color:var(--blue);font-size:.76rem;font-weight:800}.ontology-details dl{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin:12px 0 0}.ontology-details dl div{min-width:0;padding:8px 10px;border-radius:9px;background:#f2f4f5}.ontology-details .wide{grid-column:span 2}.ontology-details .blocking-context{border:1px solid #e5c792;background:#fff8e9}.ontology-details dt{font-size:.65rem;font-weight:850;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}.ontology-details dd{margin:4px 0 8px;overflow-wrap:anywhere;font-size:.72rem}.ontology-details code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}",
    ".branch-note{margin:-24px 0 42px;padding:16px 18px;border:1px solid #cbd8b9;border-radius:14px;background:#f2f7e9;color:#3f522c;line-height:1.5}",
    ".package-ceiling{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0}.package-ceiling span{border:1px solid #b9c7ce;border-radius:999px;background:#fff;padding:7px 11px;font:700 .78rem ui-monospace,SFMono-Regular,Menlo,monospace}.story-boundary{margin-top:30px;padding:24px;border-radius:18px;background:#241f24;color:#fff}.story-boundary span{font-size:.74rem;text-transform:uppercase;letter-spacing:.1em;font-weight:850;color:#ffb59f}.story-boundary p{margin:9px 0 0;line-height:1.55}.support-links{display:flex;flex-wrap:wrap;gap:12px;margin-top:48px;padding-top:24px;border-top:1px solid var(--line)}.support-links a{font-weight:760}",
    "@media(max-width:760px){.site-header{padding:20px 20px 48px}.topline{margin-bottom:44px}.workspace{padding:0 14px}.control-deck{position:relative;top:auto;grid-template-columns:1fr}.story-tabs{display:grid}.story-tabs .story-tab{text-align:left}.relation-reading{grid-template-columns:1fr;gap:8px}.friendly-arrow{display:grid;grid-template-columns:1fr auto;align-items:center;gap:10px;text-align:left;padding:0 12px}.friendly-arrow svg{width:48px;transform:rotate(90deg)}.friendly-arrow small{grid-column:1/-1}.ontology-details dl{grid-template-columns:1fr 1fr}.ontology-details .wide{grid-column:1/-1}.chapter-nav ol{grid-template-columns:1fr 1fr}}",
    "@media(max-width:420px){.topline{align-items:flex-start;flex-direction:column}.chapter-nav ol{grid-template-columns:1fr}.ontology-details dl{grid-template-columns:1fr}.ontology-details .wide{grid-column:1}}",
    "@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}",
    "@media print{.site-header{padding:16mm;color:#000;background:#fff}.topline{margin-bottom:15mm}.projection-badge{border-color:#777}.hero p{color:#333}.workspace{max-width:none;margin:0;padding:0 12mm}.control-deck,.support-links{display:none}.js .story-panel[hidden]{display:block}.story-panel{break-before:page}.story-panel:first-of-type{break-before:auto}.chapter{break-before:page}.relation-card{break-inside:avoid;box-shadow:none}.ontology-details>dl{display:grid!important}}",
    "</style>",
    "</head>",
    "<body>",
    '<header class="site-header">',
    '<div class="topline"><div class="brand">BODY WAR · BUSINESS ONTOLOGY</div><div class="projection-badge">Experimental generated view</div></div>',
    '<div class="hero">',
    '<p class="eyebrow">Start with the story, inspect the ontology when needed</p>',
    "<h1>See how Body War meaning connects.</h1>",
    "<p>This experiment turns exact ontology relations into short visual sentences. It helps people review the intended business story without beginning with IDs, predicates, or one giant graph.</p>",
    "</div>",
    "</header>",
    '<main class="workspace">',
    '<aside class="package-ceiling" aria-label="Package authority ceiling">',
    `<span>status: ${escapeHtml(packageProfile.status)}</span>`,
    `<span>authority_effect: ${escapeHtml(packageProfile.authority_effect)}</span>`,
    `<span>release_admission: ${escapeHtml(packageProfile.release_admission)}</span>`,
    "</aside>",
    '<section class="control-deck" aria-label="Experiment controls">',
    '<nav class="story-tabs" aria-label="Choose a business story">',
    ...journeyStories.map(
      (story) =>
        `<a class="story-tab" id="tab-${escapeHtml(story.story_id)}" href="#story-${escapeHtml(story.story_id)}" data-story-target="${escapeHtml(story.story_id)}">${escapeHtml(story.title)}</a>`,
    ),
    "</nav>",
    '<label class="detail-toggle" for="ontology-detail-toggle"><input id="ontology-detail-toggle" type="checkbox"><span>Expand all ontology details</span></label>',
    "</section>",
    '<noscript><p class="sequence-note">JavaScript is disabled. Both complete stories remain visible and the ordinary story and chapter links continue to work.</p></noscript>',
    ...journeyStories.map(renderJourneyStory),
    '<footer class="support-links">',
    `<span>${journeyStories.length} stories · ${relationCount} displayed relation occurrences · generated from existing ontology data.</span>`,
    '<a href="BUSINESS-VIEWS.html">Open the printable relation gallery</a>',
    '<a href="BUSINESS-VIEWS.md">Open the complete ontology review</a>',
    "</footer>",
    "</main>",
    "<script>",
    "document.documentElement.classList.add('js');",
    "const tablist=document.querySelector('.story-tabs');const tabs=[...document.querySelectorAll('.story-tab')];",
    "const panels=[...document.querySelectorAll('[data-story-panel]')];",
    "tablist.setAttribute('role','tablist');for(const [index,tab] of tabs.entries()){tab.setAttribute('role','tab');tab.setAttribute('aria-controls',`story-${tab.dataset.storyTarget}`);tab.setAttribute('aria-selected',String(index===0));tab.tabIndex=index===0?0:-1}for(const panel of panels){panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby',`tab-${panel.dataset.storyPanel}`)}",
    "function activateStory(storyId,{focus=false}={}){for(const tab of tabs){const active=tab.dataset.storyTarget===storyId;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;if(active&&focus)tab.focus()}for(const panel of panels){panel.hidden=panel.id!==`story-${storyId}`}}",
    "tabs.forEach((tab,index)=>{tab.addEventListener('click',(event)=>{event.preventDefault();activateStory(tab.dataset.storyTarget)});tab.addEventListener('keydown',(event)=>{let next=index;if(event.key==='ArrowRight')next=(index+1)%tabs.length;else if(event.key==='ArrowLeft')next=(index-1+tabs.length)%tabs.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=tabs.length-1;else return;event.preventDefault();activateStory(tabs[next].dataset.storyTarget,{focus:true})})});",
    "const detailToggle=document.querySelector('#ontology-detail-toggle');const ontologyDetails=[...document.querySelectorAll('details.ontology-details')];detailToggle.addEventListener('change',()=>{for(const detail of ontologyDetails)detail.open=detailToggle.checked});",
    "activateStory(tabs[0].dataset.storyTarget);",
    "window.addEventListener('beforeprint',()=>{for(const detail of ontologyDetails)detail.open=true});",
    "</script>",
    "</body>",
    "</html>",
    "",
  ].join("\n");
}

function localStateId(policy, stateConcept) {
  const prefix = `body-war.business.state.${policy.policy_id.replace(
    "body-war.lifecycle.",
    "",
  )}.`;
  if (!stateConcept.startsWith(prefix)) {
    throw new Error(
      `${policy.policy_id} state is outside its lifecycle prefix: ${stateConcept}`,
    );
  }
  return stateConcept.slice(prefix.length);
}

function renderLifecycle(policy) {
  if (!policy) throw new Error("Missing lifecycle policy");
  const states = policy.state_concepts.map((conceptId, index) => {
    const node = nodeById.get(conceptId);
    if (!node) {
      throw new Error(
        `${policy.policy_id} references missing state node ${conceptId}`,
      );
    }
    return {
      conceptId,
      localId: localStateId(policy, conceptId),
      alias: `S${index}`,
      node,
    };
  });
  const byLocalId = new Map(states.map((state) => [state.localId, state]));
  const lines = [
    `### ${nodeById.get(policy.subject_concept)?.label ?? policy.policy_id}`,
    "",
    `Owner route: \`${policy.owner_route}\` · Authority effect: \`${policy.authority_effect}\``,
    "",
    "```mermaid",
    "stateDiagram-v2",
  ];
  for (const state of states) {
    lines.push(
      `  state "${escapeMermaid(state.node.label)}" as ${state.alias}`,
    );
  }
  for (const transition of policy.transitions) {
    const source =
      transition.from === "none"
        ? "[*]"
        : transition.from === "any-active-state"
          ? "ACTIVE"
          : byLocalId.get(transition.from)?.alias;
    const target = byLocalId.get(transition.to)?.alias;
    if (!source || !target) {
      throw new Error(
        `${policy.policy_id} transition references unknown state ${transition.from} -> ${transition.to}`,
      );
    }
    if (source === "ACTIVE") {
      lines.push('  state "Any active state" as ACTIVE');
    }
    lines.push(
      `  ${source} --> ${target}: ${escapeMermaid(transition.trigger)} [${transition.prototype_availability}]`,
    );
  }
  lines.push("```", "", "Transition phrases:", "");
  for (const transition of policy.transitions) {
    lines.push(
      `- \`${transition.from} -> ${transition.to}\`: ${transition.trigger} Availability: \`${transition.prototype_availability}\`.`,
    );
  }
  lines.push("", `Boundary: ${policy.forbidden_collapse.join(" ")}`, "");
  return lines;
}

function renderPredicateGlossary() {
  const exampleByPredicate = new Map();
  for (const relation of relationSet.relations) {
    if (!exampleByPredicate.has(relation.predicate)) {
      exampleByPredicate.set(relation.predicate, relation);
    }
  }
  return [
    "## Arrow phrase glossary",
    "",
    "These phrases translate the project-local predicates into ordinary sentences.",
    "They explain graph edges; they do not redefine the relation schema.",
    "",
    "| Predicate | Read the arrow as | Example relation |",
    "| --- | --- | --- |",
    ...[...exampleByPredicate.entries()]
      .sort(([left], [right]) => left.localeCompare(right))
      .map(
        ([predicate, relation]) =>
          `| \`${predicate}\` | ${predicatePhrases[predicate]} | \`${relation.relation_id}\` |`,
      ),
    "",
  ];
}

const lines = [
  "# Body War Business Ontology Views",
  "",
  "Status: `generated-projection`",
  "",
  "This document instantiates the CyberAlchemy v2 branch-as-view pattern for the",
  "Body War `business` meaning branch. It is generated from validated nodes,",
  "relations, and lifecycle policies. It is navigation and explanation, not a",
  "definition store, promotion decision, DomainSpec graph, or runtime proof.",
  "",
  "## Which CAV2 view exists here?",
  "",
  "| CAV2 view role | Body War state | What it can answer |",
  "| --- | --- | --- |",
  "| Ontology / meaning view | **Instantiated here** as the `business` branch. | What the business concepts mean, how they relate, their confidence/status, and which owner gate remains. |",
  "| System view | **Not yet modeled.** | Would require typed components, services, endpoints, schemas, tests, telemetry, and runtime constraints with current evidence. |",
  "| Business-system bridge view | **Not yet modeled.** | Would require evidence-backed `realized_by`, `tested_by`, `observed_by`, `constrained_by`, `drifts_from`, or `traced_to` edges on both sides. |",
  "",
  "The absence of system and bridge views is deliberate. Existing application code",
  "must not be inferred into ontology alignment without a separate source-bound map",
  "and bridge validation.",
  "",
  "## How to read the diagrams",
  "",
  "- Boxes are candidate ontology nodes. The second line is `business_kind · candidate_status`.",
  "- Solid arrows are admitted non-blocked relations.",
  "- Dotted arrows are blocked, projection-only, or explicit `does_not_promote` relations.",
  "- Green means `reviewed-candidate`; amber means `candidate`; red means `blocked`; gray means `deferred`; blue means `projected`.",
  "- An arrow states business meaning only. It does not prove implementation or runtime behavior.",
  "",
  "A [print-friendly HTML gallery](BUSINESS-VIEWS.html) contains the same relation",
  "sentences as individually paginating rows.",
  "",
  "For a progressive-disclosure review, open the",
  "[interactive journey experiment](BUSINESS-JOURNEY-EXPERIMENT.html). It begins",
  "with ordinary-language stories and reveals ontology metadata on request.",
  "",
  "## Relation sentence example",
  "",
  "The visible phrase makes the business meaning readable; the predicate under the",
  "arrow preserves the exact typed relation.",
  "",
  ...featuredRelationExamples.flatMap((example) => [
    `![${example.title}](generated/views/${example.example_id}.svg)`,
    "",
    ...relationsForView(example).map((relation) => {
      const source = nodeById.get(relation.source_concept);
      const target = nodeById.get(relation.target_concept);
      return `- [${source.label}](nodes/${nodeFilename(source.concept_id)}) **${phraseFor(relation)}** [${target.label}](nodes/${nodeFilename(target.concept_id)}). Typed predicate: \`${relation.predicate}\`; relation: \`${relation.relation_id}\`.`;
    }),
    "",
    `**Boundary:** ${example.forbidden_claim}`,
    "",
  ]),
  "## Business view map",
  "",
  "```mermaid",
  "flowchart TB",
  '  B["Body War business meaning branch"]',
  '  B --> C["Capability branches<br/>who owns what"]',
  '  B --> J["Runner journey<br/>login to ScorePreview"]',
  '  B --> E["Evidence chain<br/>activity to controller"]',
  '  B --> T["Territory loop<br/>control, invasion, defense"]',
  '  B --> P["Progression loop<br/>challenges, XP, clans, seasons"]',
  '  B --> L["Lifecycle views<br/>what may change state"]',
  '  S["System branch<br/>not yet modeled"]',
  '  G["Business-system bridge<br/>not yet modeled"]',
  "  B -. requires later source-bound map .-> S",
  "  B -. requires two-sided evidence .-> G",
  "  S -. contributes system evidence .-> G",
  "```",
  "",
  "The business branch explains **what Body War means**. A future system branch",
  "would explain **what software exists**. A future bridge would show **which",
  "software realizes, constrains, observes, or tests which business meaning**.",
  "",
  ...graphViews.flatMap(renderGraphView),
  "## Lifecycle views",
  "",
  "Lifecycle status is independent from ontology `candidate_status`. These diagrams",
  "show what a business object may transition through; they do not promote the node",
  "record itself.",
  "",
  ...lifecycleViewPolicyIds.flatMap((policyId) => {
    const policy = lifecycleById.get(policyId);
    if (!policy) throw new Error(`Missing lifecycle policy ${policyId}`);
    return renderLifecycle(policy);
  }),
  ...renderPredicateGlossary(),
  "## Authority and next-view boundary",
  "",
  "```mermaid",
  "flowchart LR",
  '  SRC["Source documents + selectors"] --> CAND["Candidate business nodes + relations"]',
  '  CAND --> REVIEW["Body War product ontology review"]',
  '  REVIEW --> DECIDE{"Owner decision required?"}',
  '  DECIDE -->|no| READY["Reviewed candidate meaning"]',
  '  DECIDE -->|yes| BLOCKED["Blocked or deferred residue"]',
  '  READY -. "later exact digest bridge" .-> DS["DomainSpec mapping<br/>not part of this package"]',
  '  BLOCKED --> GATE["Decision gate / named owner route"]',
  '  GATE -. "only after explicit decision" .-> READY',
  '  GEO["GeometryCandidate"] -. "does not promote" .-> SOURCEBACKED["Source-backed track"]',
  '  SCORE["ScorePreview"] -. "does not promote" .-> SOURCEBACKED',
  "```",
  "",
  "Next view work should be a separate system-branch inventory of the Body War app,",
  "followed by a two-sided bridge validation. That future work must not be generated",
  "from business intent alone.",
  "",
];

const rendered = lines.join("\n");
const svgArtifacts = [
  ...featuredRelationExamples.map((example) => ({
    outputPath: path.join(generatedViewRoot, `${example.example_id}.svg`),
    content: renderRelationSvg({
      ...example,
      view_id: example.example_id,
    }),
  })),
  ...graphViews.map((view) => ({
    outputPath: path.join(generatedViewRoot, `${view.view_id}.svg`),
    content: renderRelationSvg(view),
  })),
];
const htmlRendered = renderPrintableHtml();
const journeyExperimentRendered = renderJourneyExperimentHtml();
const artifacts = [
  { outputPath, content: rendered },
  { outputPath: htmlOutputPath, content: htmlRendered },
  {
    outputPath: journeyExperimentOutputPath,
    content: journeyExperimentRendered,
  },
  ...svgArtifacts,
];

if (process.argv.includes("--check")) {
  for (const artifact of artifacts) {
    let current;
    try {
      current = await readFile(artifact.outputPath, "utf8");
    } catch {
      throw new Error(
        `${path.relative(packageRoot, artifact.outputPath)} is missing; run generate-views.mjs`,
      );
    }
    if (current !== artifact.content) {
      throw new Error(
        `${path.relative(packageRoot, artifact.outputPath)} is stale; run scripts/generate-views.mjs`,
      );
    }
  }
  const expectedSvgNames = svgArtifacts
    .map((artifact) => path.basename(artifact.outputPath))
    .sort();
  const actualSvgNames = (await readdir(generatedViewRoot))
    .filter((name) => name.endsWith(".svg"))
    .sort();
  if (JSON.stringify(actualSvgNames) !== JSON.stringify(expectedSvgNames)) {
    throw new Error(
      `generated/views SVG set is stale; expected ${expectedSvgNames.join(", ")}, found ${actualSvgNames.join(", ")}`,
    );
  }
  process.stdout.write(
    `business views current: ${graphViews.length} graph views, ${featuredRelationExamples.length} featured relation example, ${journeyStories.length} journey stories, ${lifecycleViewPolicyIds.length} lifecycle views, and 2 HTML projections\n`,
  );
} else {
  await mkdir(generatedViewRoot, { recursive: true });
  await Promise.all(
    artifacts.map((artifact) =>
      writeFile(artifact.outputPath, artifact.content),
    ),
  );
  process.stdout.write(
    `generated ${graphViews.length} graph views, ${featuredRelationExamples.length} featured relation example, ${journeyStories.length} journey stories, ${lifecycleViewPolicyIds.length} lifecycle views, and 2 HTML projections\n`,
  );
}

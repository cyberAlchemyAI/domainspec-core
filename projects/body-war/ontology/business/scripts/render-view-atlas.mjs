function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function nodeDomId(conceptId) {
  return `node-${encodeURIComponent(conceptId)}`;
}

function relationDomId(relationId) {
  return `relation-${encodeURIComponent(relationId)}`;
}

function lensDomId(lensId) {
  return `lens-${lensId}`;
}

function cssToken(value) {
  return String(value ?? "none")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function sourceRefs(refs) {
  return (refs ?? [])
    .map(
      (ref) =>
        `<li><code>${escapeHtml(ref.path)}</code><span>${escapeHtml(ref.selector)}</span><code>${escapeHtml(ref.sha256)}</code></li>`,
    )
    .join("");
}

function renderItems(items, emptyText) {
  return items.length > 0
    ? `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`
    : `<p>${escapeHtml(emptyText)}</p>`;
}

function relationSentence(relation, nodeById, phraseFor) {
  const source = nodeById.get(relation.source_concept);
  const target = nodeById.get(relation.target_concept);
  return `<a href="#${nodeDomId(source.concept_id)}">${escapeHtml(source.label)}</a> <strong>${escapeHtml(phraseFor(relation))}</strong> <a href="#${nodeDomId(target.concept_id)}">${escapeHtml(target.label)}</a>`;
}

export function renderRelationArrow({
  relation,
  source,
  target,
  phrase,
  portal = false,
}) {
  if (!source?.concept_id || !target?.concept_id) {
    throw new Error(
      `ATLAS_ARROW_ENDPOINT_MISSING: ${relation?.relation_id ?? "unknown relation"}`,
    );
  }
  if (!relation?.predicate || !relation?.authority_effect) {
    throw new Error(
      `ATLAS_ARROW_RELATION_INVALID: ${relation?.relation_id ?? "unknown relation"}`,
    );
  }
  const effectClass = `relation-effect-${cssToken(relation.authority_effect)}`;
  return [
    `<div class="relation-arrow ${effectClass}${portal ? " relation-arrow--portal" : ""}" data-arrow-relation-id="${escapeHtml(relation.relation_id)}">`,
    `<a class="relation-arrow__endpoint relation-arrow__source" href="#${nodeDomId(source.concept_id)}"><span>Source</span><strong>${escapeHtml(source.label)}</strong></a>`,
    `<span class="relation-arrow__predicate"><svg class="relation-arrow__geometry" viewBox="0 0 120 24" aria-hidden="true" focusable="false"><line x1="4" y1="12" x2="104" y2="12"></line><path d="M 104 5 L 116 12 L 104 19 Z"></path></svg><code>${escapeHtml(relation.predicate)}</code><span>${escapeHtml(phrase)}</span></span>`,
    `<a class="relation-arrow__endpoint relation-arrow__target" href="#${nodeDomId(target.concept_id)}"><span>Target</span><strong>${escapeHtml(target.label)}</strong></a>`,
    `</div>`,
  ].join("");
}

const overviewCoordinates = new Map([
  ["participants-boundaries", [10, 24]],
  ["responsibilities", [34, 8]],
  ["behavior", [72, 24]],
  ["business-objects", [72, 68]],
  ["governance-lifecycle", [34, 84]],
  ["hypotheses-outcomes", [10, 68]],
]);

export function renderLensFlowOverview(projection) {
  const expectedLensIds = [...overviewCoordinates.keys()];
  const actualLensIds = projection.lenses.map((lens) => lens.lens_id);
  if (
    actualLensIds.length !== expectedLensIds.length ||
    actualLensIds.some((lensId, index) => lensId !== expectedLensIds[index])
  ) {
    throw new Error(
      `ATLAS_OVERVIEW_LENS_SET_MISMATCH: expected ${expectedLensIds.join(",")}; received ${actualLensIds.join(",")}`,
    );
  }
  if (
    projection.lens_flows.length !== 13 ||
    projection.lens_flows.reduce(
      (total, flow) => total + flow.relation_count,
      0,
    ) !== 109
  ) {
    throw new Error("ATLAS_OVERVIEW_FLOW_PARTITION_MISMATCH");
  }

  const lensById = new Map(
    projection.lenses.map((lens) => [lens.lens_id, lens]),
  );
  const geometry = projection.lens_flows
    .map((flow) => {
      const [sourceX, sourceY] = overviewCoordinates.get(flow.source_lens_id);
      const [targetX, targetY] = overviewCoordinates.get(flow.target_lens_id);
      return `<path d="M ${sourceX + 8} ${sourceY + 4} L ${targetX + 8} ${targetY + 4}" data-flow-source="${escapeHtml(flow.source_lens_id)}" data-flow-target="${escapeHtml(flow.target_lens_id)}" marker-end="url(#overview-arrowhead)"></path>`;
    })
    .join("");
  const nodes = expectedLensIds
    .map((lensId) => {
      const lens = lensById.get(lensId);
      const [left, top] = overviewCoordinates.get(lensId);
      return `<a class="overview-lens-node" style="--lens-left:${left}%;--lens-top:${top}%" href="#${lensDomId(lensId)}" data-overview-lens-id="${escapeHtml(lensId)}">${escapeHtml(lens.title)}</a>`;
    })
    .join("");
  const lanes = projection.lens_flows
    .map((flow) => {
      const source = lensById.get(flow.source_lens_id);
      const target = lensById.get(flow.target_lens_id);
      return [
        `<li class="semantic-lane" data-flow-source="${escapeHtml(flow.source_lens_id)}" data-flow-target="${escapeHtml(flow.target_lens_id)}">`,
        `<p><a href="#${lensDomId(flow.source_lens_id)}">${escapeHtml(source.title)}</a> → <a href="#${lensDomId(flow.target_lens_id)}">${escapeHtml(target.title)}</a> · <strong>${flow.relation_count}</strong> relations</p>`,
        `<details><summary>Show ${flow.relation_count} exact relation IDs</summary><ul>${flow.relation_ids.map((relationId) => `<li><a href="#${relationDomId(relationId)}"><code>${escapeHtml(relationId)}</code></a></li>`).join("")}</ul></details>`,
        `</li>`,
      ].join("");
    })
    .join("");

  return [
    `<section class="lens-flow-overview" aria-labelledby="lens-flow-overview-title">`,
    `<h3 id="lens-flow-overview-title">Directed flow overview <span>6 lenses · 13 lanes · 109 portal relations</span></h3>`,
    `<div class="overview-spatial" data-overview-map="six-lens">`,
    `<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false"><defs><marker id="overview-arrowhead" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0,0 L5,2.5 L0,5 Z"></path></marker></defs>${geometry}</svg>`,
    `<div class="overview-lens-nodes">${nodes}</div></div>`,
    `<ol class="semantic-lanes">${lanes}</ol>`,
    `</section>`,
  ].join("");
}

function renderNode({
  node,
  incidentRelationIds,
  relationById,
  disposition,
  dispositionLabels,
}) {
  const outgoingRelationIds = incidentRelationIds.filter(
    (relationId) =>
      relationById.get(relationId).source_concept === node.concept_id,
  );
  const incomingRelationIds = incidentRelationIds.filter(
    (relationId) =>
      relationById.get(relationId).target_concept === node.concept_id,
  );
  const relationLinks = (relationIds, direction) =>
    relationIds
      .map((relationId) => {
        const relation = relationById.get(relationId);
        return `<li><a href="#${relationDomId(relationId)}">${escapeHtml(direction)} · ${escapeHtml(relation.predicate)} · ${escapeHtml(relationId)}</a></li>`;
      })
      .join("");
  const blockingQuestions =
    node.challenge_contract?.blocking_questions ?? [];
  const residue = node.residue ?? [];
  const isolate = disposition
    ? [
        `<p class="zero-degree"><strong>No admitted explicit relation.</strong> This describes current graph incidence only.</p>`,
        `<p class="research-disposition"><span>Research disposition</span> ${escapeHtml(dispositionLabels[disposition] ?? disposition)}</p>`,
      ].join("")
    : "";
  return [
    `<article class="node-card" id="${nodeDomId(node.concept_id)}" data-concept-id="${escapeHtml(node.concept_id)}" data-business-kind="${escapeHtml(node.business_kind)}" tabindex="-1">`,
    `<header><p class="kind">${escapeHtml(node.business_kind)}</p><h4>${escapeHtml(node.label)}</h4></header>`,
    `<p>${escapeHtml(node.definition)}</p>`,
    isolate,
    `<details class="reference-brief reference-brief--node" data-reference-kind="node" open><summary>Exact node metadata</summary><div class="reference-brief__content">`,
    `<p><strong>Definition:</strong> ${escapeHtml(node.definition)}</p>`,
    `<dl><div><dt>Concept ID</dt><dd><code>${escapeHtml(node.concept_id)}</code></dd></div>`,
    `<div><dt>Candidate status</dt><dd>${escapeHtml(node.candidate_status ?? "absent")}</dd></div>`,
    `<div><dt>Concept role</dt><dd>${escapeHtml(node.concept_role)}</dd></div>`,
    `<div><dt>Business kind</dt><dd>${escapeHtml(node.business_kind)}</dd></div>`,
    `<div><dt>Owner route</dt><dd><code>${escapeHtml(node.owner_route)}</code></dd></div>`,
    `<div><dt>Resolution gate</dt><dd><code>${escapeHtml(node.challenge_contract?.resolution_gate ?? "not-recorded")}</code></dd></div>`,
    `<div><dt>Outgoing incidence</dt><dd>${outgoingRelationIds.length}</dd></div>`,
    `<div><dt>Incoming incidence</dt><dd>${incomingRelationIds.length}</dd></div>`,
    `<div><dt>Authority</dt><dd>none — candidate projection only</dd></div></dl>`,
    `<h5>Blocking questions</h5>${renderItems(
      blockingQuestions,
      node.candidate_status === "blocked"
        ? "No blocking question recorded"
        : "No blocking question applies",
    )}`,
    `<h5>Residue</h5>${renderItems(residue, "No residue recorded")}`,
    `<h5>Outgoing relations (${outgoingRelationIds.length})</h5>${outgoingRelationIds.length > 0 ? `<ul>${relationLinks(outgoingRelationIds, "outgoing")}</ul>` : "<p>None.</p>"}`,
    `<h5>Incoming relations (${incomingRelationIds.length})</h5>${incomingRelationIds.length > 0 ? `<ul>${relationLinks(incomingRelationIds, "incoming")}</ul>` : "<p>None.</p>"}`,
    `<h5>Source references</h5><ul class="source-refs">${sourceRefs(node.source_refs)}</ul>`,
    `<h5>Forbidden collapse</h5><ul>${(node.forbidden_collapse ?? []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`,
    `</div></details>`,
    incidentRelationIds.length > 0
      ? `<details><summary>${incidentRelationIds.length} admitted relation${incidentRelationIds.length === 1 ? "" : "s"}</summary><ul>${relationLinks(outgoingRelationIds, "outgoing")}${relationLinks(incomingRelationIds, "incoming")}</ul></details>`
      : "",
    `</article>`,
  ].join("");
}

function renderRelation({
  relation,
  nodeById,
  nodeLensById,
  phraseFor,
  portal,
}) {
  const source = nodeById.get(relation.source_concept);
  const target = nodeById.get(relation.target_concept);
  const sourceLens = nodeLensById.get(source.concept_id);
  const targetLens = nodeLensById.get(target.concept_id);
  return [
    `<article class="relation-card${portal ? " portal-relation" : ""}" id="${relationDomId(relation.relation_id)}" data-relation-id="${escapeHtml(relation.relation_id)}" tabindex="-1">`,
    renderRelationArrow({
      relation,
      source,
      target,
      phrase: phraseFor(relation),
      portal: Boolean(portal),
    }),
    `<p class="relation-sentence">${relationSentence(relation, nodeById, phraseFor)}</p>`,
    `<p class="relation-orientation"><span>Original direction</span> <a href="#${lensDomId(sourceLens)}">${escapeHtml(sourceLens)}</a> → <a href="#${lensDomId(targetLens)}">${escapeHtml(targetLens)}</a></p>`,
    portal
      ? `<p class="portal-actions"><a href="#${nodeDomId(source.concept_id)}">Open source endpoint</a><a href="#${nodeDomId(target.concept_id)}">Open target endpoint</a></p>`
      : "",
    `<details class="reference-brief reference-brief--relation" data-reference-kind="relation" open><summary>Exact relation metadata</summary><div class="reference-brief__content">`,
    `<p><strong>Exact tuple:</strong> ${escapeHtml(source.label)} → ${escapeHtml(phraseFor(relation))} → ${escapeHtml(target.label)}</p>`,
    `<p><span class="projection-label">Projection wording</span> ${escapeHtml(phraseFor(relation))}</p>`,
    `<dl><div><dt>Relation ID</dt><dd><code>${escapeHtml(relation.relation_id)}</code></dd></div>`,
    `<div><dt>Source</dt><dd><code>${escapeHtml(relation.source_concept)}</code></dd></div>`,
    `<div><dt>Predicate</dt><dd><code>${escapeHtml(relation.predicate)}</code></dd></div>`,
    `<div><dt>Reading phrase</dt><dd>${escapeHtml(phraseFor(relation))} <span class="projection-label">projection wording</span></dd></div>`,
    `<div><dt>Target</dt><dd><code>${escapeHtml(relation.target_concept)}</code></dd></div>`,
    `<div><dt>Direction</dt><dd>${escapeHtml(relation.direction)}</dd></div>`,
    `<div><dt>Authority effect</dt><dd>${escapeHtml(relation.authority_effect)}</dd></div>`,
    `<div><dt>Value effect</dt><dd>${escapeHtml(relation.value_effect)}</dd></div>`,
    `<div><dt>Cycle policy</dt><dd>${escapeHtml(relation.cycle_policy)}</dd></div>`,
    `<div><dt>Owner route</dt><dd><code>${escapeHtml(relation.owner_route)}</code></dd></div></dl>`,
    `<h5>Evidence references</h5><ul class="source-refs">${sourceRefs(relation.evidence_refs)}</ul>`,
    `<h5>Forbidden collapse</h5><ul>${(relation.forbidden_collapse ?? []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`,
    `</div></details></article>`,
  ].join("");
}

export function renderViewAtlasHtml({
  projection,
  nodes,
  relations,
  profile,
  dispositionLabels,
  boundary,
  phraseFor,
}) {
  const nodeById = new Map(nodes.map((node) => [node.concept_id, node]));
  const relationById = new Map(
    relations.map((relation) => [relation.relation_id, relation]),
  );
  const portalById = new Map(
    projection.portals.map((portal) => [portal.relation_id, portal]),
  );
  const dispositionById = new Map(
    projection.isolate_dispositions.map((row) => [
      row.concept_id,
      row.disposition,
    ]),
  );
  const nodeLensById = new Map(
    projection.lenses.flatMap((lens) =>
      lens.core_node_ids.map((conceptId) => [conceptId, lens.lens_id]),
    ),
  );
  const incidentByNodeId = new Map(
    nodes.map((node) => [node.concept_id, []]),
  );
  for (const relation of relations) {
    incidentByNodeId.get(relation.source_concept).push(relation.relation_id);
    incidentByNodeId.get(relation.target_concept).push(relation.relation_id);
  }
  for (const relationIds of incidentByNodeId.values()) {
    relationIds.sort((left, right) => left.localeCompare(right));
  }

  const predicateBriefs = [...new Set(relations.map((relation) => relation.predicate))]
    .sort((left, right) => left.localeCompare(right))
    .map((predicate) => {
      const matches = relations.filter(
        (relation) => relation.predicate === predicate,
      );
      const phrases = [
        ...new Set(matches.map((relation) => phraseFor(relation))),
      ].sort((left, right) => left.localeCompare(right));
      const examples = matches.slice(0, 3).map((relation) => {
        const source = nodeById.get(relation.source_concept);
        const target = nodeById.get(relation.target_concept);
        return `<li><a href="#${relationDomId(relation.relation_id)}">${escapeHtml(source.label)} → ${escapeHtml(target.label)}</a></li>`;
      });
      return [
        `<details class="reference-brief reference-brief--predicate" data-reference-kind="predicate" id="predicate-${encodeURIComponent(predicate)}" open>`,
        `<summary><code>${escapeHtml(predicate)}</code> · ${matches.length} uses</summary><div class="reference-brief__content">`,
        `<p><span class="projection-label">Projection wording</span> ${phrases.map(escapeHtml).join("; ")}</p>`,
        `<p>This is bounded atlas wording, not a canonical predicate definition.</p>`,
        `<h4>Examples</h4><ul>${examples.join("")}</ul>`,
        `</div></details>`,
      ].join("");
    })
    .join("");

  const lensCards = projection.lenses
    .map(
      (lens) => [
        `<li><a class="lens-card" href="#${lensDomId(lens.lens_id)}">`,
        `<span class="eyebrow">${lens.business_kinds.length} literal kinds</span>`,
        `<strong>${escapeHtml(lens.title)}</strong>`,
        `<span>${escapeHtml(lens.question)}</span>`,
        `<span class="counts">${lens.core_node_ids.length} nodes · ${lens.internal_relation_ids.length} internal · ${lens.outbound_portal_ids.length} outgoing · ${lens.inbound_portal_ids.length} incoming · ${lens.zero_degree_node_ids.length} zero-degree</span>`,
        `</a></li>`,
      ].join(""),
    )
    .join("");
  const lensFlowOverview = renderLensFlowOverview(projection);

  const lensNavigation = projection.lenses
    .map(
      (lens) =>
        `<li><a href="#${lensDomId(lens.lens_id)}">${escapeHtml(lens.title)}</a></li>`,
    )
    .join("");

  const lensSections = projection.lenses
    .map((lens) => {
      const kindSections = lens.business_kinds
        .map((kind) => {
          const kindNodes = lens.core_node_ids
            .map((conceptId) => nodeById.get(conceptId))
            .filter((node) => node.business_kind === kind)
            .sort(
              (left, right) =>
                left.label.localeCompare(right.label) ||
                left.concept_id.localeCompare(right.concept_id),
            );
          return [
            `<section class="kind-group" aria-labelledby="kind-${lens.lens_id}-${kind}">`,
            `<h3 id="kind-${lens.lens_id}-${kind}">${escapeHtml(kind)} <span>${kindNodes.length} nodes</span></h3>`,
            `<div class="node-grid">`,
            ...kindNodes.map((node) =>
              renderNode({
                node,
                incidentRelationIds: incidentByNodeId.get(node.concept_id),
                relationById,
                disposition: dispositionById.get(node.concept_id),
                dispositionLabels,
              }),
            ),
            `</div></section>`,
          ].join("");
        })
        .join("");
      const internalRelations = lens.internal_relation_ids
        .map((relationId) =>
          renderRelation({
            relation: relationById.get(relationId),
            nodeById,
            nodeLensById,
            phraseFor,
            portal: null,
          }),
        )
        .join("");
      const outgoingRelations = lens.outbound_portal_ids
        .map((relationId) =>
          renderRelation({
            relation: relationById.get(relationId),
            nodeById,
            nodeLensById,
            phraseFor,
            portal: portalById.get(relationId),
          }),
        )
        .join("");
      const incomingIndex = lens.inbound_portal_ids
        .map((relationId) => {
          const relation = relationById.get(relationId);
          const source = nodeById.get(relation.source_concept);
          return `<li><a href="#${relationDomId(relationId)}">${escapeHtml(source.label)} · ${escapeHtml(phraseFor(relation))} · ${escapeHtml(relationById.get(relationId).predicate)}</a></li>`;
        })
        .join("");
      const lensFlows = projection.lens_flows.filter(
        (flow) =>
          flow.source_lens_id === lens.lens_id ||
          flow.target_lens_id === lens.lens_id,
      );
      const lensBrief = [
        `<details class="reference-brief reference-brief--lens" data-reference-kind="lens" open><summary>Lens reference brief</summary><div class="reference-brief__content">`,
        `<p><strong>Question:</strong> ${escapeHtml(lens.question)}</p>`,
        `<p>${escapeHtml(lens.description)}</p>`,
        `<dl><div><dt>Core nodes</dt><dd>${lens.core_node_ids.length}</dd></div><div><dt>Internal relations</dt><dd>${lens.internal_relation_ids.length}</dd></div><div><dt>Outgoing portals</dt><dd>${lens.outbound_portal_ids.length}</dd></div><div><dt>Incoming portals</dt><dd>${lens.inbound_portal_ids.length}</dd></div></dl>`,
        `<h4>Directed flows</h4><ul>${lensFlows
          .map(
            (flow) =>
              `<li>${escapeHtml(flow.source_lens_id)} → ${escapeHtml(flow.target_lens_id)} · ${flow.relation_count} relations</li>`,
          )
          .join("")}</ul>`,
        `</div></details>`,
      ].join("");
      return [
        `<section class="atlas-lens" id="${lensDomId(lens.lens_id)}" data-lens-id="${escapeHtml(lens.lens_id)}" tabindex="-1" aria-labelledby="${lens.lens_id}-title">`,
        `<header class="lens-header"><a href="#atlas-overview">← All lenses</a><p class="eyebrow">Editorial navigation lens · not an ontology branch</p>`,
        `<h2 id="${lens.lens_id}-title">${escapeHtml(lens.title)}</h2>`,
        `<p class="question">${escapeHtml(lens.question)}</p><p>${escapeHtml(lens.description)}</p>`,
        `<p class="counts">${lens.core_node_ids.length} core nodes · ${lens.internal_relation_ids.length} internal relations · ${lens.outbound_portal_ids.length} outgoing portals · ${lens.inbound_portal_ids.length} incoming portals · ${lens.zero_degree_node_ids.length} zero-degree</p>${lensBrief}</header>`,
        kindSections,
        `<section aria-labelledby="${lens.lens_id}-internal"><h3 id="${lens.lens_id}-internal">Relations inside this lens <span>${lens.internal_relation_ids.length}</span></h3><div class="relation-list">${internalRelations || "<p>None.</p>"}</div></section>`,
        `<section aria-labelledby="${lens.lens_id}-outgoing"><h3 id="${lens.lens_id}-outgoing">Outgoing portals to other lenses <span>${lens.outbound_portal_ids.length}</span></h3><div class="relation-list">${outgoingRelations || "<p>None.</p>"}</div></section>`,
        `<section aria-labelledby="${lens.lens_id}-incoming"><h3 id="${lens.lens_id}-incoming">Incoming portal index <span>${lens.inbound_portal_ids.length}</span></h3>${incomingIndex ? `<ul>${incomingIndex}</ul>` : "<p>None.</p>"}</section>`,
        `</section>`,
      ].join("");
    })
    .join("");

  return [
    "<!doctype html>",
    '<html lang="en"><head><meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    "<title>Body War Business Ontology View Atlas</title>",
    "<style>",
    ":root{color-scheme:dark;--bg:#0a1018;--panel:#111b28;--panel2:#172536;--text:#edf4fb;--muted:#a7b7c8;--line:#334a62;--accent:#67d8ff;--good:#86efac;--warn:#facc15;--danger:#fca5a5;--max:1480px;font-family:Inter,ui-sans-serif,system-ui,sans-serif}",
    "*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 20% 0,#19314c 0,transparent 34rem),var(--bg);color:var(--text);line-height:1.55}",
    "a{color:var(--accent);text-underline-offset:.2em}a:focus-visible,summary:focus-visible,input:focus-visible{outline:3px solid #fff;outline-offset:4px;border-radius:.2rem}.skip-link{position:absolute;left:1rem;top:-8rem;background:#fff;color:#000;padding:.75rem;z-index:20}.skip-link:focus{top:1rem}",
    ".shell{width:min(var(--max),calc(100% - 2rem));margin:auto}.site-header{padding:3rem 0 1.5rem}.eyebrow,.kind,.projection-label,.research-disposition span,.relation-orientation span{font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}h1{font-size:clamp(2.2rem,6vw,5rem);line-height:1;margin:.3rem 0 1rem;max-width:16ch}h2{font-size:clamp(1.8rem,4vw,3.2rem);line-height:1.1}h3{margin-top:2rem;border-bottom:1px solid var(--line);padding-bottom:.5rem}h3 span{font-size:.8rem;color:var(--muted)}",
    ".ceiling{border:1px solid var(--warn);background:#2c260d;padding:1rem;border-radius:.8rem;max-width:78rem}.lens-nav{position:sticky;top:0;z-index:10;background:#0a1018ed;border-block:1px solid var(--line);backdrop-filter:blur(12px)}.lens-nav ul{display:flex;gap:.5rem;overflow:auto;list-style:none;padding:.75rem 0;margin:0}.lens-nav a{display:block;white-space:nowrap;padding:.45rem .7rem;border:1px solid var(--line);border-radius:999px;text-decoration:none}",
    "#atlas-overview{padding:2rem 0}.overview-grid{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr));gap:1rem}.lens-card{min-height:14rem;display:flex;flex-direction:column;gap:.8rem;padding:1.2rem;background:linear-gradient(145deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:1rem;text-decoration:none}.lens-card strong{font-size:1.4rem}.lens-card .counts,.counts{color:var(--muted);font-size:.9rem}.lens-flow-overview{margin-block:2rem}.overview-spatial{position:relative;min-height:34rem;border:1px solid var(--line);border-radius:1rem;background:radial-gradient(circle at 50% 50%,#1a3045,var(--panel));overflow:hidden}.overview-spatial svg,.overview-lens-nodes{position:absolute;inset:0;width:100%;height:100%}.overview-spatial svg path[data-flow-source]{fill:none;stroke:var(--accent);stroke-width:.65;opacity:.72}.overview-spatial svg marker path{fill:var(--accent)}.overview-lens-node{position:absolute;left:var(--lens-left);top:var(--lens-top);width:18%;min-height:4.5rem;display:grid;place-items:center;padding:.55rem;text-align:center;border:1px solid var(--accent);border-radius:.65rem;background:var(--panel2);text-decoration:none;transform:translate(-10%,-10%)}.semantic-lanes{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,21rem),1fr));gap:.75rem;padding-left:1.5rem}.semantic-lane{padding:.65rem .8rem;border:1px solid var(--line);border-radius:.55rem;background:var(--panel)}.semantic-lane p{margin:.2rem 0}.semantic-lane details{max-height:14rem;overflow:auto}.search{display:grid;gap:.5rem;max-width:52rem;margin:2rem 0}.search input{width:100%;font:inherit;padding:.9rem 1rem;color:var(--text);background:var(--panel);border:1px solid var(--line);border-radius:.6rem}.search-results{max-height:20rem;overflow:auto}",
    ".atlas-lens{padding:2rem 0 5rem;scroll-margin-top:5rem}.lens-header{padding:1.4rem;background:var(--panel);border:1px solid var(--line);border-radius:1rem}.question{font-size:1.25rem}.node-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,23rem),1fr));gap:1rem}.node-card,.relation-card{background:var(--panel);border:1px solid var(--line);border-radius:.8rem;padding:1rem;scroll-margin-top:6rem}.node-card:target,.relation-card:target,.atlas-lens:target{border-color:var(--accent);box-shadow:0 0 0 3px #67d8ff55}.node-card h4{font-size:1.15rem;margin:.2rem 0}.kind{color:var(--accent);margin:0}.zero-degree{border-left:4px solid var(--warn);padding:.65rem;background:#29230d}.research-disposition{color:var(--warn)}details{border-top:1px solid var(--line);margin-top:.8rem;padding-top:.7rem}summary{cursor:pointer;font-weight:700}.reference-brief{position:relative}.reference-brief__content{padding:.35rem .6rem .2rem;border-left:2px solid var(--accent)}.reference-brief:hover>.reference-brief__content,.reference-brief:focus-within>.reference-brief__content{display:block}.predicate-briefs{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,18rem),1fr));gap:.75rem;margin-block:1rem 2rem}.predicate-briefs .reference-brief{padding:.7rem;border:1px solid var(--line);border-radius:.55rem;background:var(--panel)}dl div{display:grid;grid-template-columns:minmax(8rem,12rem) 1fr;gap:.7rem;padding:.35rem 0;border-bottom:1px dotted var(--line)}dt{color:var(--muted)}dd{margin:0;overflow-wrap:anywhere}code{overflow-wrap:anywhere}.source-refs li{display:grid;gap:.2rem;margin-bottom:.6rem}",
    ".relation-list{display:grid;gap:.8rem}.relation-arrow{display:grid;grid-template-columns:minmax(9rem,1fr) minmax(10rem,1.2fr) minmax(9rem,1fr);align-items:center;gap:.8rem;padding:.75rem;border:1px solid var(--line);border-radius:.65rem;background:#0b1520}.relation-arrow__endpoint{display:grid;gap:.15rem;min-width:0;padding:.55rem;border-radius:.45rem;background:var(--panel2);text-decoration:none}.relation-arrow__endpoint span{color:var(--muted);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em}.relation-arrow__endpoint strong{overflow-wrap:anywhere}.relation-arrow__predicate{display:grid;justify-items:center;gap:.2rem;text-align:center}.relation-arrow__predicate>span{color:var(--muted);font-size:.82rem}.relation-arrow__geometry{width:100%;height:1.5rem;overflow:visible}.relation-arrow__geometry line,.relation-arrow__geometry path{stroke:var(--accent);fill:var(--accent);stroke-width:2}.relation-effect-blocked .relation-arrow__geometry line,.relation-effect-projection .relation-arrow__geometry line{stroke-dasharray:6 5}.relation-arrow--portal{border-color:var(--accent)}.relation-sentence{font-size:1.08rem}.relation-orientation,.portal-actions{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap}.portal-actions a{border:1px solid var(--accent);padding:.35rem .6rem;border-radius:.4rem;text-decoration:none}.portal-relation{border-left:4px solid var(--accent)}.projection-label{margin-left:.4rem}",
    ".boundary-footer{border-top:1px solid var(--line);padding:2rem 0 4rem}.js .atlas-lens{display:none}.js .atlas-lens.is-active{display:block}.status{min-height:1.5rem;color:var(--good)}",
    "@media(max-width:760px){.overview-spatial{display:none}.semantic-lanes{grid-template-columns:1fr}}@media(max-width:600px){.shell{width:min(100% - 1rem,var(--max))}.site-header{padding-top:2rem}dl div{grid-template-columns:1fr}.node-grid{grid-template-columns:1fr}.lens-card{min-height:0}.lens-nav{position:static}.relation-arrow{grid-template-columns:1fr}.relation-arrow__predicate{justify-items:stretch}.relation-arrow__geometry{transform:rotate(90deg);width:3.5rem;justify-self:center}.relation-arrow__target{text-align:right}}",
    "@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}",
    "@media print{*{color:#000!important;background:#fff!important;box-shadow:none!important}.lens-nav,.search,.skip-link,.overview-spatial{display:none!important}.semantic-lanes{grid-template-columns:1fr}.atlas-lens,.js .atlas-lens{display:block!important;break-before:page}.node-card,.relation-card{break-inside:avoid;border-color:#777!important}details{display:block}details>*{display:block}.shell{width:100%}}",
    "</style></head><body>",
    '<a class="skip-link" href="#atlas-main">Skip to atlas</a>',
    '<header class="site-header shell"><p class="eyebrow">Generated candidate projection · authority effect none</p>',
    "<h1>Body War business ontology atlas</h1>",
    `<p>Six editorial lenses organize all ${projection.coverage.node_count} nodes and ${projection.coverage.relation_count} admitted relations. They preserve ${projection.coverage.business_kind_count} literal business kinds; they do not replace them.</p>`,
    `<p class="ceiling"><strong>Boundary:</strong> ${escapeHtml(boundary.lens_note)} ${escapeHtml(boundary.isolate_note)} Status <code>${escapeHtml(profile.status)}</code>; release <code>${escapeHtml(profile.release_admission)}</code>.</p></header>`,
    `<nav class="lens-nav" aria-label="Ontology atlas lenses"><div class="shell"><ul><li><a href="#atlas-overview">Overview</a></li>${lensNavigation}</ul></div></nav>`,
    '<main id="atlas-main" class="shell">',
    '<section id="atlas-overview" tabindex="-1"><p class="eyebrow">Whole ontology</p><h2>Choose a lens</h2>',
    `<p>Every node has one core home. Every relation is rendered once: ${projection.coverage.internal_relation_count} stay inside a lens and ${projection.coverage.portal_relation_count} cross between lenses.</p>`,
    '<div class="search" role="search"><label for="atlas-search">Search exact labels, IDs, kinds, predicates, and relation readings</label><input id="atlas-search" type="search" autocomplete="off"><p id="atlas-status" class="status" role="status" aria-live="polite"></p><ul id="atlas-search-results" class="search-results"></ul></div>',
    `<ul class="overview-grid">${lensCards}</ul>${lensFlowOverview}<section aria-labelledby="predicate-briefs-title"><h3 id="predicate-briefs-title">Predicate reference briefs <span>23 projection tokens</span></h3><div class="predicate-briefs">${predicateBriefs}</div></section></section>`,
    lensSections,
    "</main>",
    `<footer class="boundary-footer"><div class="shell"><h2>How to read this atlas</h2><p>${escapeHtml(boundary.zero_degree_note)}</p><p>${escapeHtml(boundary.isolate_note)}</p><p>Relation sentences show projection wording beside exact predicates and retain the original directed source and target. Layout and lens order do not imply workflow, causality, lifecycle, ownership, or promotion.</p><p><strong>Claim ceiling:</strong> Generated source-bound candidate navigation only. No comprehension, accessibility conformance, implementation, runtime, release, deployment, or production evidence.</p></div></footer>`,
    "<script>",
    "document.documentElement.classList.add('js');",
    "const lenses=[...document.querySelectorAll('.atlas-lens')];const overview=document.getElementById('atlas-overview');const status=document.getElementById('atlas-status');",
    "function reveal(hash,{focus=false}={}){const id=decodeURIComponent((hash||'#atlas-overview').slice(1));const target=document.getElementById(id);lenses.forEach(l=>l.classList.remove('is-active'));overview.hidden=false;if(!target){status.textContent='Unknown atlas location. Showing the overview.';return;}const lens=target.classList.contains('atlas-lens')?target:target.closest('.atlas-lens');if(lens){overview.hidden=true;lens.classList.add('is-active');}status.textContent=lens?`Opened ${lens.querySelector('h2').textContent}${target!==lens?` · ${target.querySelector('h4')?.textContent||target.dataset.relationId||''}`:''}`:'Showing all six editorial lenses.';if(focus)target.focus({preventScroll:true});}",
    "addEventListener('hashchange',()=>reveal(location.hash,{focus:true}));reveal(location.hash);",
    "const search=document.getElementById('atlas-search');const results=document.getElementById('atlas-search-results');const candidates=[...document.querySelectorAll('[data-concept-id],[data-relation-id]')];search.addEventListener('input',()=>{const q=search.value.trim().toLocaleLowerCase();results.replaceChildren();if(!q){status.textContent='';return;}const matches=candidates.filter(el=>el.textContent.toLocaleLowerCase().includes(q)||(el.dataset.conceptId||el.dataset.relationId||'').toLocaleLowerCase().includes(q)).slice(0,40);for(const el of matches){const li=document.createElement('li');const a=document.createElement('a');a.href=`#${el.id}`;a.textContent=el.dataset.conceptId?`${el.querySelector('h4').textContent} · ${el.dataset.businessKind}`:`${el.dataset.relationId}`;li.append(a);results.append(li);}status.textContent=`${matches.length} result${matches.length===1?'':'s'} shown${matches.length===40?' (first 40)':''}.`;});",
    "const referenceBriefs=[...document.querySelectorAll('.reference-brief')];for(const brief of referenceBriefs)brief.open=false;for(const brief of referenceBriefs){const summary=brief.querySelector(':scope>summary');let pinned=false;let preview=false;const previewOpen=()=>{if(pinned||brief.open)return;preview=true;brief.dataset.previewOpen='true';brief.open=true;};const previewClose=()=>{if(!preview||pinned||brief.matches(':hover')||brief.contains(document.activeElement))return;preview=false;delete brief.dataset.previewOpen;brief.open=false;};brief.addEventListener('mouseenter',previewOpen);brief.addEventListener('mouseleave',previewClose);brief.addEventListener('focusin',previewOpen);brief.addEventListener('focusout',()=>setTimeout(previewClose));summary.addEventListener('click',event=>{if(preview){event.preventDefault();preview=false;delete brief.dataset.previewOpen;pinned=true;brief.open=true;return;}queueMicrotask(()=>{pinned=brief.open;});});}let printBriefStates=null;const setPrintBriefState=printing=>{if(printing&&!printBriefStates){printBriefStates=referenceBriefs.map(brief=>brief.open);for(const brief of referenceBriefs)brief.open=true;}else if(!printing&&printBriefStates){referenceBriefs.forEach((brief,index)=>{brief.open=printBriefStates[index];});printBriefStates=null;}};const printMedia=matchMedia('print');printMedia.addEventListener('change',event=>setPrintBriefState(event.matches));addEventListener('beforeprint',()=>setPrintBriefState(true));addEventListener('afterprint',()=>setPrintBriefState(false));",
    "</script></body></html>",
  ].join("");
}

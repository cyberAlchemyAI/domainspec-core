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

function sourceRefs(refs) {
  return (refs ?? [])
    .map(
      (ref) =>
        `<li><code>${escapeHtml(ref.path)}</code><span>${escapeHtml(ref.selector)}</span><code>${escapeHtml(ref.sha256)}</code></li>`,
    )
    .join("");
}

function relationSentence(relation, nodeById, phraseFor) {
  const source = nodeById.get(relation.source_concept);
  const target = nodeById.get(relation.target_concept);
  return `<a href="#${nodeDomId(source.concept_id)}">${escapeHtml(source.label)}</a> <strong>${escapeHtml(phraseFor(relation))}</strong> <a href="#${nodeDomId(target.concept_id)}">${escapeHtml(target.label)}</a>`;
}

function renderNode({
  node,
  incidentRelationIds,
  relationById,
  disposition,
  dispositionLabels,
}) {
  const relationLinks = incidentRelationIds
    .map((relationId) => {
      const relation = relationById.get(relationId);
      const direction =
        relation.source_concept === node.concept_id ? "outgoing" : "incoming";
      return `<li><a href="#${relationDomId(relationId)}">${escapeHtml(direction)} · ${escapeHtml(relation.predicate)} · ${escapeHtml(relationId)}</a></li>`;
    })
    .join("");
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
    `<details><summary>Exact node metadata</summary>`,
    `<dl><div><dt>Concept ID</dt><dd><code>${escapeHtml(node.concept_id)}</code></dd></div>`,
    `<div><dt>Candidate status</dt><dd>${escapeHtml(node.candidate_status ?? "absent")}</dd></div>`,
    `<div><dt>Concept role</dt><dd>${escapeHtml(node.concept_role)}</dd></div>`,
    `<div><dt>Owner route</dt><dd><code>${escapeHtml(node.owner_route)}</code></dd></div>`,
    `<div><dt>Authority</dt><dd>none — candidate projection only</dd></div></dl>`,
    `<h5>Source references</h5><ul class="source-refs">${sourceRefs(node.source_refs)}</ul>`,
    `<h5>Forbidden collapse</h5><ul>${(node.forbidden_collapse ?? []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`,
    `</details>`,
    incidentRelationIds.length > 0
      ? `<details><summary>${incidentRelationIds.length} admitted relation${incidentRelationIds.length === 1 ? "" : "s"}</summary><ul>${relationLinks}</ul></details>`
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
    `<p class="relation-sentence">${relationSentence(relation, nodeById, phraseFor)}</p>`,
    `<p class="relation-orientation"><span>Original direction</span> <a href="#${lensDomId(sourceLens)}">${escapeHtml(sourceLens)}</a> → <a href="#${lensDomId(targetLens)}">${escapeHtml(targetLens)}</a></p>`,
    portal
      ? `<p class="portal-actions"><a href="#${nodeDomId(source.concept_id)}">Open source endpoint</a><a href="#${nodeDomId(target.concept_id)}">Open target endpoint</a></p>`
      : "",
    `<details><summary>Exact relation metadata</summary>`,
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
    `</details></article>`,
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
      return [
        `<section class="atlas-lens" id="${lensDomId(lens.lens_id)}" data-lens-id="${escapeHtml(lens.lens_id)}" tabindex="-1" aria-labelledby="${lens.lens_id}-title">`,
        `<header class="lens-header"><a href="#atlas-overview">← All lenses</a><p class="eyebrow">Editorial navigation lens · not an ontology branch</p>`,
        `<h2 id="${lens.lens_id}-title">${escapeHtml(lens.title)}</h2>`,
        `<p class="question">${escapeHtml(lens.question)}</p><p>${escapeHtml(lens.description)}</p>`,
        `<p class="counts">${lens.core_node_ids.length} core nodes · ${lens.internal_relation_ids.length} internal relations · ${lens.outbound_portal_ids.length} outgoing portals · ${lens.inbound_portal_ids.length} incoming portals · ${lens.zero_degree_node_ids.length} zero-degree</p></header>`,
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
    "#atlas-overview{padding:2rem 0}.overview-grid{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr));gap:1rem}.lens-card{min-height:14rem;display:flex;flex-direction:column;gap:.8rem;padding:1.2rem;background:linear-gradient(145deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:1rem;text-decoration:none}.lens-card strong{font-size:1.4rem}.lens-card .counts,.counts{color:var(--muted);font-size:.9rem}.search{display:grid;gap:.5rem;max-width:52rem;margin:2rem 0}.search input{width:100%;font:inherit;padding:.9rem 1rem;color:var(--text);background:var(--panel);border:1px solid var(--line);border-radius:.6rem}.search-results{max-height:20rem;overflow:auto}",
    ".atlas-lens{padding:2rem 0 5rem;scroll-margin-top:5rem}.lens-header{padding:1.4rem;background:var(--panel);border:1px solid var(--line);border-radius:1rem}.question{font-size:1.25rem}.node-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,23rem),1fr));gap:1rem}.node-card,.relation-card{background:var(--panel);border:1px solid var(--line);border-radius:.8rem;padding:1rem;scroll-margin-top:6rem}.node-card:target,.relation-card:target,.atlas-lens:target{border-color:var(--accent);box-shadow:0 0 0 3px #67d8ff55}.node-card h4{font-size:1.15rem;margin:.2rem 0}.kind{color:var(--accent);margin:0}.zero-degree{border-left:4px solid var(--warn);padding:.65rem;background:#29230d}.research-disposition{color:var(--warn)}details{border-top:1px solid var(--line);margin-top:.8rem;padding-top:.7rem}summary{cursor:pointer;font-weight:700}dl div{display:grid;grid-template-columns:minmax(8rem,12rem) 1fr;gap:.7rem;padding:.35rem 0;border-bottom:1px dotted var(--line)}dt{color:var(--muted)}dd{margin:0;overflow-wrap:anywhere}code{overflow-wrap:anywhere}.source-refs li{display:grid;gap:.2rem;margin-bottom:.6rem}",
    ".relation-list{display:grid;gap:.8rem}.relation-sentence{font-size:1.08rem}.relation-orientation,.portal-actions{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap}.portal-actions a{border:1px solid var(--accent);padding:.35rem .6rem;border-radius:.4rem;text-decoration:none}.portal-relation{border-left:4px solid var(--accent)}.projection-label{margin-left:.4rem}",
    ".boundary-footer{border-top:1px solid var(--line);padding:2rem 0 4rem}.js .atlas-lens{display:none}.js .atlas-lens.is-active{display:block}.status{min-height:1.5rem;color:var(--good)}",
    "@media(max-width:600px){.shell{width:min(100% - 1rem,var(--max))}.site-header{padding-top:2rem}dl div{grid-template-columns:1fr}.node-grid{grid-template-columns:1fr}.lens-card{min-height:0}.lens-nav{position:static}}",
    "@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}",
    "@media print{*{color:#000!important;background:#fff!important;box-shadow:none!important}.lens-nav,.search,.skip-link{display:none!important}.atlas-lens,.js .atlas-lens{display:block!important;break-before:page}.node-card,.relation-card{break-inside:avoid;border-color:#777!important}details{display:block}details>*{display:block}.shell{width:100%}}",
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
    `<ul class="overview-grid">${lensCards}</ul></section>`,
    lensSections,
    "</main>",
    `<footer class="boundary-footer"><div class="shell"><h2>How to read this atlas</h2><p>${escapeHtml(boundary.zero_degree_note)}</p><p>${escapeHtml(boundary.isolate_note)}</p><p>Relation sentences show projection wording beside exact predicates and retain the original directed source and target. Layout and lens order do not imply workflow, causality, lifecycle, ownership, or promotion.</p><p><strong>Claim ceiling:</strong> Generated source-bound candidate navigation only. No comprehension, accessibility conformance, implementation, runtime, release, deployment, or production evidence.</p></div></footer>`,
    "<script>",
    "document.documentElement.classList.add('js');",
    "const lenses=[...document.querySelectorAll('.atlas-lens')];const overview=document.getElementById('atlas-overview');const status=document.getElementById('atlas-status');",
    "function reveal(hash,{focus=false}={}){const id=decodeURIComponent((hash||'#atlas-overview').slice(1));const target=document.getElementById(id);lenses.forEach(l=>l.classList.remove('is-active'));overview.hidden=false;if(!target){status.textContent='Unknown atlas location. Showing the overview.';return;}const lens=target.classList.contains('atlas-lens')?target:target.closest('.atlas-lens');if(lens){overview.hidden=true;lens.classList.add('is-active');}status.textContent=lens?`Opened ${lens.querySelector('h2').textContent}${target!==lens?` · ${target.querySelector('h4')?.textContent||target.dataset.relationId||''}`:''}`:'Showing all six editorial lenses.';if(focus)target.focus({preventScroll:true});}",
    "addEventListener('hashchange',()=>reveal(location.hash,{focus:true}));reveal(location.hash);",
    "const search=document.getElementById('atlas-search');const results=document.getElementById('atlas-search-results');const candidates=[...document.querySelectorAll('[data-concept-id],[data-relation-id]')];search.addEventListener('input',()=>{const q=search.value.trim().toLocaleLowerCase();results.replaceChildren();if(!q){status.textContent='';return;}const matches=candidates.filter(el=>el.textContent.toLocaleLowerCase().includes(q)||(el.dataset.conceptId||el.dataset.relationId||'').toLocaleLowerCase().includes(q)).slice(0,40);for(const el of matches){const li=document.createElement('li');const a=document.createElement('a');a.href=`#${el.id}`;a.textContent=el.dataset.conceptId?`${el.querySelector('h4').textContent} · ${el.dataset.businessKind}`:`${el.dataset.relationId}`;li.append(a);results.append(li);}status.textContent=`${matches.length} result${matches.length===1?'':'s'} shown${matches.length===40?' (first 40)':''}.`;});",
    "</script></body></html>",
  ].join("");
}


import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { comprehensionTask } from "../authoring/comprehension-task-catalog.mjs";

const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const outputPath = path.join(packageRoot, "BUSINESS-COMPREHENSION-TASK.html");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderTask() {
  return [
    "<!doctype html>",
    '<html lang="en">',
    "<head>",
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    `<title>${escapeHtml(comprehensionTask.title)}</title>`,
    "<style>",
    ":root{color-scheme:light;--ink:#132238;--muted:#5f6d7a;--paper:#f5f4ef;--card:#fff;--line:#d9dee2;--accent:#c63e26;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,\"Segoe UI\",sans-serif}*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--paper)}a{color:#126887}.page{max-width:920px;margin:0 auto;padding:48px 22px 80px}.eyebrow{text-transform:uppercase;letter-spacing:.1em;font-size:.75rem;font-weight:800;color:var(--accent)}h1{font-size:clamp(2.2rem,6vw,4.6rem);line-height:1;margin:.25em 0}.lede{font-size:1.15rem;line-height:1.6;color:var(--muted)}.stimulus{margin:28px 0;padding:18px;border-left:5px solid var(--accent);background:#fff}.tasks{display:grid;gap:18px;padding:0;list-style:none;counter-reset:task}.task{counter-increment:task;padding:22px;border:1px solid var(--line);border-radius:16px;background:var(--card)}.task h2{margin:0 0 10px;font-size:1.25rem}.task h2::before{content:counter(task) \". \";color:var(--accent)}.task p{line-height:1.55}.answer{display:block;width:100%;min-height:8rem;margin-top:15px;padding:12px;border:1px solid #aeb8bf;border-radius:10px;background:#fff;font:inherit}.boundary{margin-top:34px;padding:18px;border-radius:14px;background:#202936;color:#fff;line-height:1.55}@media print{body{background:#fff}.page{max-width:none;padding:12mm}.task{break-inside:avoid}.answer{min-height:45mm}}",
    "</style>",
    "</head>",
    "<body>",
    '<main class="page">',
    `<p class="eyebrow">${escapeHtml(comprehensionTask.audience)}</p>`,
    `<h1>${escapeHtml(comprehensionTask.title)}</h1>`,
    `<p class="lede">${escapeHtml(comprehensionTask.prompt)}</p>`,
    '<section class="stimulus" aria-labelledby="stimulus-title">',
    '<h2 id="stimulus-title">Reading stimulus</h2>',
    `<p><a href="${escapeHtml(comprehensionTask.stimulus.path)}">${escapeHtml(comprehensionTask.stimulus.label)}</a></p>`,
    `<p>${escapeHtml(comprehensionTask.response_note)}</p>`,
    "</section>",
    '<ol class="tasks">',
    ...comprehensionTask.loci.map(
      (locus) =>
        `<li class="task" data-locus="${escapeHtml(locus.locus_id)}"><h2>${escapeHtml(locus.label)}</h2><p>${escapeHtml(locus.prompt)}</p><label>Answer<textarea class="answer" name="${escapeHtml(locus.locus_id)}"></textarea></label></li>`,
    ),
    "</ol>",
    `<p>${escapeHtml(comprehensionTask.submission)}</p>`,
    `<aside class="boundary"><strong>Evidence boundary:</strong> ${escapeHtml(comprehensionTask.evidence_ceiling)}</aside>`,
    "</main>",
    "</body>",
    "</html>",
    "",
  ].join("\n");
}

const rendered = renderTask();

if (process.argv.includes("--check")) {
  const current = await readFile(outputPath, "utf8");
  if (current !== rendered) {
    throw new Error(
      "BUSINESS-COMPREHENSION-TASK.html is stale; run generate-comprehension-task.mjs",
    );
  }
  process.stdout.write(
    `business comprehension task current: ${comprehensionTask.loci.length} learner loci\n`,
  );
} else {
  await writeFile(outputPath, rendered);
  process.stdout.write(
    `generated business comprehension task with ${comprehensionTask.loci.length} learner loci\n`,
  );
}


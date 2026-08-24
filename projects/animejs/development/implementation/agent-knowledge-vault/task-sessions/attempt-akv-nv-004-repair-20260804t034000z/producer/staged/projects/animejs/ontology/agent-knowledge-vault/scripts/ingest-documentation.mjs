#!/usr/bin/env node

import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SOURCES = resolve(ROOT, 'sources');
const ORIGIN = 'https://animejs.com';
const EXPECTED_SEMANTIC = '681f004e04a91ab1a3462e882edff24d09454297f34a41863e81df06e20066fb';
const EXPECTED_RAW_SET = '63125e931350f5dbf8552a289ac80d687bb1867e7c94c1e2d6e33904f16befcd';

const sha256 = value => createHash('sha256').update(value).digest('hex');
const canonicalPath = raw => `${new URL(raw, ORIGIN).pathname.replace(/\/+$/, '')}/`;

function decode(value) {
  return value.replace(/<[^>]*>/g, ' ')
    .replace(/&(?:nbsp|#160);/gi, ' ').replace(/&amp;/gi, '&')
    .replace(/&#39;|&apos;/gi, "'").replace(/&quot;/gi, '"')
    .replace(/\s+/g, ' ').trim();
}

const attrs = value => Object.fromEntries(
  [...value.matchAll(/([\w:-]+)=(?:"([^"]*)"|'([^']*)')/g)].map(match => [match[1], match[2] ?? match[3]])
);

function articleSlice(html) {
  return (html.match(/<article id="docs-info">([\s\S]*?)<\/article>/i) || [])[1] || '';
}

function headingRows(article) {
  const content = (article.match(/<div class="docs-info-content text-layout">([\s\S]*?)<\/div>\s*(?:<section|<!--)/i) || [])[1] || article;
  return [...content.matchAll(/<(h[1-6])([^>]*)>([\s\S]*?)<\/\1>/gi)]
    .map(match => ({ level: Number(match[1][1]), id: attrs(match[2]).id || null, text: decode(match[3]) }))
    .filter(row => row.text);
}

function relatedTargets(article, current) {
  const links = [...article.matchAll(/<(?:a)[^>]+href="(\/documentation\/[^"#?]+)"[^>]*>([\s\S]*?)<\/a>/gi)]
    .map(match => ({ path: match[1].endsWith('/') ? match[1] : `${match[1]}/`, label: decode(match[2]) }));
  return [...new Map(links.filter(row => row.path !== current).map(row => [row.path, row])).values()];
}

function topicKind(path) {
  const depth = path.split('/').length - 2;
  return depth === 1 ? 'family'
    : /callbacks?\//.test(path) ? 'callback'
      : /methods?\//.test(path) ? 'method'
        : /properties(?:\/|$)/.test(path) ? 'property'
          : /(?:settings|parameters)(?:\/|$)/.test(path) ? 'parameter-or-setting'
            : /usage\//.test(path) ? 'recipe'
              : /gotchas/.test(path) ? 'pitfall-guide'
                : /targets(?:\/|$)/.test(path) ? 'target-kind'
                  : /keyframes(?:\/|$)/.test(path) ? 'keyframe-guide'
                    : /easing|easings|ease/.test(path) ? 'easing-topic'
                      : 'guide-or-api-topic';
}

function extract(path, html, rawDigest) {
  const article = articleSlice(html);
  const headings = headingRows(article);
  const normalizedHeadings = headings.map(row => row.text.toLowerCase());
  const related = relatedTargets(article, path);
  const h1 = headings.find(row => row.level === 1)?.text ?? null;
  const versions = [...article.matchAll(/class="docs-breadcrumb-version"[^>]*>([\s\S]*?)<\/a>/gi)].map(match => decode(match[1]));
  return {
    canonical_path: path,
    title: decode(html.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i)?.[1] ?? ''),
    h1,
    heading_selectors: headings.filter(row => row.id).map(row => `#${row.id}`),
    headings: headings.map(row => row.text),
    topic_kind: topicKind(path.replace(/\/$/, '')),
    parameters: normalizedHeadings.some(value => ['parameters', 'parameter', 'accepts'].includes(value)) ? 'present' : 'absent',
    returns: normalizedHeadings.some(value => ['return', 'returns'].includes(value)) ? 'present' : 'absent',
    related_topics: { disposition: related.length ? 'present' : 'absent', targets: related },
    examples: /class="code-preview"/.test(article) ? 'present-source-only' : 'absent',
    version_notes: { disposition: versions.length ? 'present' : 'absent', notes: versions },
    badges: { js: /\(JS\)/.test(article), waapi: /\(WAAPI\)/.test(article), new: /\bNEW\b/.test(h1 || '') },
    status: 'semantic-observed',
    http_status: 200,
    raw_sha256: rawDigest,
  };
}

async function parallel(values, limit, operation) {
  const results = new Array(values.length); let cursor = 0;
  await Promise.all(Array.from({ length: limit }, async () => {
    while (cursor < values.length) { const index = cursor++; results[index] = await operation(values[index]); }
  }));
  return results;
}

async function build() {
  const seed = await fetch(`${ORIGIN}/documentation/`);
  assert.equal(seed.status, 200);
  const seedHtml = await seed.text();
  const paths = [...new Set([...seedHtml.matchAll(/href="(\/documentation(?:\/[^"?# ]*)?)"/g)]
    .map(match => match[1]).filter(path => path !== '/documentation').map(canonicalPath))]
    .sort((left, right) => left.localeCompare(right));
  assert.equal(paths.length, 418);
  const rows = await parallel(paths, 12, async requestedPath => {
    const response = await fetch(`${ORIGIN}${requestedPath}`, { redirect: 'follow' });
    assert.equal(response.status, 200, `${requestedPath}: HTTP ${response.status}`);
    const raw = Buffer.from(await response.arrayBuffer());
    const html = raw.toString('utf8');
    assert.ok(articleSlice(html), `${requestedPath}: article absent`);
    return extract(canonicalPath(response.url), html, sha256(raw));
  });
  rows.sort((left, right) => left.canonical_path.localeCompare(right.canonical_path));
  const jsonl = rows.map(row => `${JSON.stringify(row)}\n`).join('');
  const rawSet = rows.map(row => `${row.canonical_path}\t${row.raw_sha256}\n`).join('');
  const counts = {
    parameters: { present: rows.filter(row => row.parameters === 'present').length, absent: rows.filter(row => row.parameters === 'absent').length },
    returns: { present: rows.filter(row => row.returns === 'present').length, absent: rows.filter(row => row.returns === 'absent').length },
    related_topics: { present: rows.filter(row => row.related_topics.disposition === 'present').length, absent: rows.filter(row => row.related_topics.disposition === 'absent').length },
    examples: { 'present-source-only': rows.filter(row => row.examples === 'present-source-only').length, absent: rows.filter(row => row.examples === 'absent').length },
    version_notes: { present: rows.filter(row => row.version_notes.disposition === 'present').length, absent: rows.filter(row => row.version_notes.disposition === 'absent').length },
  };
  mkdirSync(SOURCES, { recursive: true });
  writeFileSync(resolve(SOURCES, 'documentation.jsonl'), jsonl);
  writeFileSync(resolve(SOURCES, 'documentation-manifest.json'), `${JSON.stringify({
    schema_version: 'animejs.agent-knowledge-vault.documentation-manifest.v2', source: `${ORIGIN}/documentation/`, row_count: 418,
    successful_rows: 418, failed_rows: 0, dispositions: counts, semantic_jsonl_sha256: sha256(jsonl), raw_page_set_sha256: sha256(rawSet),
    expected_semantic_jsonl_sha256: EXPECTED_SEMANTIC, expected_raw_page_set_sha256: EXPECTED_RAW_SET,
    semantic_match: sha256(jsonl) === EXPECTED_SEMANTIC, raw_set_match: sha256(rawSet) === EXPECTED_RAW_SET,
    materialization_status: 'reproduced-and-validated-candidate-local', authority_effect: 'none',
  }, null, 2)}\n`);
  console.log(JSON.stringify({ semantic: sha256(jsonl), raw: sha256(rawSet), counts }, null, 2));
}

function check() {
  const bytes = readFileSync(resolve(SOURCES, 'documentation.jsonl'));
  const rows = bytes.toString().trimEnd().split('\n').map(JSON.parse);
  const manifest = JSON.parse(readFileSync(resolve(SOURCES, 'documentation-manifest.json')));
  assert.equal(rows.length, 418); assert.equal(new Set(rows.map(row => row.canonical_path)).size, 418);
  assert.equal(sha256(bytes), manifest.semantic_jsonl_sha256);
  const rawSet = rows.map(row => `${row.canonical_path}\t${row.raw_sha256}\n`).join('');
  assert.equal(sha256(rawSet), manifest.raw_page_set_sha256);
  assert.equal(manifest.semantic_jsonl_sha256, EXPECTED_SEMANTIC);
  assert.equal(manifest.raw_page_set_sha256, EXPECTED_RAW_SET);
  assert.equal(manifest.semantic_match, true);
  assert.equal(manifest.raw_set_match, true);
  assert.deepEqual(manifest.dispositions, {
    parameters: { present: 260, absent: 158 }, returns: { present: 123, absent: 295 },
    related_topics: { present: 418, absent: 0 }, examples: { 'present-source-only': 353, absent: 65 },
    version_notes: { present: 388, absent: 30 },
  });
  console.log(`PASS documentation ingest v2: 418/418 routes, semantic-match=${manifest.semantic_match}, raw-set-match=${manifest.raw_set_match}`);
}

try {
  if (process.argv.includes('--build')) await build(); else if (process.argv.includes('--check')) check(); else throw new Error('usage: --build | --check');
} catch (error) { console.error(error.stack ?? error.message); process.exitCode = 2; }

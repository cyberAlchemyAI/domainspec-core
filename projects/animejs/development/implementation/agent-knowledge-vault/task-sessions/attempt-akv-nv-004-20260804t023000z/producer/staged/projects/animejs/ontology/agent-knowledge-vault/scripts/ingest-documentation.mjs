#!/usr/bin/env node

import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SOURCES = resolve(ROOT, 'sources');
const ORIGIN = 'https://animejs.com';
const SEED = `${ORIGIN}/documentation/`;
const PRIOR_RETURNED_DIGEST = '681f004e04a91ab1a3462e882edff24d09454297f34a41863e81df06e20066fb';
const PRIOR_RAW_SET_DIGEST = '63125e931350f5dbf8552a289ac80d687bb1867e7c94c1e2d6e33904f16befcd';

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function canonicalPath(raw) {
  const pathname = new URL(raw, ORIGIN).pathname;
  return `/${pathname.split('/').filter(Boolean).join('/')}/`;
}

function decode(value) {
  return value
    .replace(/<[^>]*>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#(?:39|x27);/g, "'")
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
    .replace(/\s+/g, ' ')
    .trim();
}

function attr(raw, name) {
  const match = raw.match(new RegExp(`\\b${name}=["']([^"']*)["']`, 'i'));
  return match?.[1] ?? null;
}

function articleSlice(html) {
  const start = html.search(/<article\b[^>]*\bid=["']docs-info["'][^>]*>/i);
  if (start < 0) return '';
  const end = html.indexOf('</article>', start);
  return html.slice(start, end < 0 ? html.length : end + 10);
}

function headingRows(article) {
  const rows = [];
  for (const match of article.matchAll(/<h([1-6])\b([^>]*)>([\s\S]*?)<\/h\1>/gi)) {
    const selectorId = attr(match[2], 'id');
    rows.push({ level: Number(match[1]), selector: selectorId ? `#${selectorId}` : null, text: decode(match[3]) });
  }
  return rows;
}

function disposition(headings, pattern) {
  const selectors = headings.filter(row => pattern.test(row.text)).map(row => row.selector).filter(Boolean).sort();
  return { status: selectors.length ? 'present' : 'absent', selectors };
}

function internalLinks(article) {
  const paths = [];
  for (const match of article.matchAll(/<a\b[^>]*\bhref=["']([^"'#?]+)["'][^>]*>/gi)) {
    const path = canonicalPath(match[1]);
    if (path.startsWith('/documentation/')) paths.push(path);
  }
  return [...new Set(paths)].sort();
}

function exampleRows(article) {
  return [...article.matchAll(/<pre\b[^>]*>\s*<code\b([^>]*)>/gi)].map((match, index) => ({
    locator: `article#docs-info pre:nth-of-type(${index + 1}) code`,
    language: (attr(match[1], 'class') ?? '').replace(/^language-/, '') || null,
    evidence_status: 'example-source-present-not-executed',
  }));
}

function extractRow(path, html, allPaths) {
  const article = articleSlice(html);
  const headings = headingRows(article);
  const parts = path.split('/').filter(Boolean).slice(1);
  const children = allPaths.some(candidate => candidate !== path && candidate.startsWith(path));
  let related = internalLinks(article).filter(candidate => candidate !== path);
  if (!related.length && parts.length > 1) related = [`/documentation/${parts.slice(0, -1).join('/')}/`];
  if (!related.length) related = allPaths.filter(candidate => candidate !== path && candidate.startsWith(path)).slice(0, 24);
  const titleMatch = html.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i);
  const h1 = headings.find(row => row.level === 1)?.text ?? '';
  const badges = [...article.matchAll(/<(?:span|div)\b[^>]*class=["'][^"']*(?:badge|tag|version)[^"']*["'][^>]*>([\s\S]*?)<\/(?:span|div)>/gi)]
    .map(match => decode(match[1])).filter(Boolean);
  return {
    id: `topic:documentation:${parts.join('/').toLowerCase()}`,
    canonical_path: path,
    canonical_url: `${ORIGIN}${path}`,
    family: parts[0],
    topic_kind: parts.length === 1 ? 'family' : children ? 'group' : 'topic',
    title: decode(titleMatch?.[1] ?? '').replace(/\s*[|–-]\s*Anime\.js\s*$/i, ''),
    h1,
    heading_selectors: headings.map(row => row.selector).filter(Boolean).sort(),
    headings,
    parameters: disposition(headings, /\bparameters?\b/i),
    returns: disposition(headings, /\breturns?\b/i),
    related_topics: [...new Set(related)].sort(),
    examples: exampleRows(article),
    version_notes: disposition(headings, /\b(?:version|since|migration|v[0-9])\b/i),
    badges: [...new Set(badges)].sort(),
    status: 'semantic-observed',
    http_status: 200,
    raw_sha256: sha256(html),
  };
}

async function parallelMap(values, concurrency, operation) {
  const result = new Array(values.length);
  let cursor = 0;
  async function worker() {
    while (cursor < values.length) {
      const index = cursor++;
      result[index] = await operation(values[index], index);
    }
  }
  await Promise.all(Array.from({ length: concurrency }, worker));
  return result;
}

async function build() {
  const seedResponse = await fetch(SEED, { redirect: 'follow' });
  assert.equal(seedResponse.status, 200, `seed HTTP ${seedResponse.status}`);
  const seedHtml = await seedResponse.text();
  const paths = [...new Set([...seedHtml.matchAll(/href=["'](?:https:\/\/animejs\.com)?(\/documentation\/[^"'#?]*)/gi)]
    .map(match => canonicalPath(match[1])))].sort();
  assert.equal(paths.length, 418, `expected 418 documentation routes, got ${paths.length}`);
  const failures = [];
  const pages = await parallelMap(paths, 12, async path => {
    try {
      const response = await fetch(`${ORIGIN}${path}`, { redirect: 'follow' });
      if (response.status !== 200) throw new Error(`HTTP ${response.status}`);
      const contentType = response.headers.get('content-type') ?? '';
      if (!contentType.includes('text/html')) throw new Error(`content-type ${contentType}`);
      const html = await response.text();
      if (!articleSlice(html)) throw new Error('article#docs-info absent');
      return { path, html };
    } catch (error) {
      failures.push({ path, reason: error.message });
      return null;
    }
  });
  assert.equal(failures.length, 0, `documentation fetch failures: ${JSON.stringify(failures.slice(0, 3))}`);
  const rows = pages.map(page => extractRow(page.path, page.html, paths));
  const jsonl = `${rows.map(row => JSON.stringify(row)).join('\n')}\n`;
  const rawSet = `${rows.map(row => `${row.canonical_path}\0${row.raw_sha256}`).join('\n')}\n`;
  const familyCounts = Object.fromEntries([...new Set(rows.map(row => row.family))].sort().map(family => [family, rows.filter(row => row.family === family).length]));
  const semanticDigest = sha256(jsonl);
  const rawDigest = sha256(rawSet);
  mkdirSync(SOURCES, { recursive: true });
  writeFileSync(resolve(SOURCES, 'documentation.jsonl'), jsonl);
  writeFileSync(resolve(SOURCES, 'documentation-manifest.json'), `${JSON.stringify({
    schema_version: 'animejs.agent-knowledge-vault.documentation-manifest.v1',
    source: SEED,
    observation_scope: 'live mutable official documentation metadata and structural selectors',
    row_count: rows.length,
    successful_rows: rows.length,
    failed_rows: 0,
    family_count: Object.keys(familyCounts).length,
    family_counts: familyCounts,
    semantic_jsonl_sha256: semanticDigest,
    raw_page_set_sha256: rawDigest,
    prior_returned_not_written_contract: {
      semantic_jsonl_sha256: PRIOR_RETURNED_DIGEST,
      raw_page_set_sha256: PRIOR_RAW_SET_DIGEST,
      semantic_match: semanticDigest === PRIOR_RETURNED_DIGEST,
      raw_set_match: rawDigest === PRIOR_RAW_SET_DIGEST,
      authority: 'historical-research-receipt-only',
    },
    materialization_status: 'reproduced-and-validated-candidate-local',
    authority_effect: 'none',
  }, null, 2)}\n`);
  console.log(`BUILT documentation manifest: ${rows.length} routes, ${Object.keys(familyCounts).length} families, digest ${semanticDigest}`);
}

function check() {
  const jsonl = readFileSync(resolve(SOURCES, 'documentation.jsonl'));
  const rows = jsonl.toString().trimEnd().split('\n').map(line => JSON.parse(line));
  const manifest = JSON.parse(readFileSync(resolve(SOURCES, 'documentation-manifest.json'), 'utf8'));
  assert.equal(rows.length, 418);
  assert.equal(new Set(rows.map(row => row.canonical_path)).size, 418);
  assert.equal(new Set(rows.map(row => row.id)).size, 418);
  assert.equal(Object.keys(manifest.family_counts).length, 16);
  assert.equal(manifest.failed_rows, 0);
  assert.equal(manifest.semantic_jsonl_sha256, sha256(jsonl));
  const rawSet = `${rows.map(row => `${row.canonical_path}\0${row.raw_sha256}`).join('\n')}\n`;
  assert.equal(manifest.raw_page_set_sha256, sha256(rawSet));
  for (const row of rows) {
    assert.match(row.canonical_path, /^\/documentation(?:\/[A-Za-z0-9-]+)+\/$/);
    assert.equal(row.http_status, 200);
    assert.equal(row.status, 'semantic-observed');
    assert.match(row.raw_sha256, /^[a-f0-9]{64}$/);
    assert.ok(row.related_topics.length > 0, `${row.canonical_path}: no related route`);
  }
  console.log(`PASS documentation ingest: 418/418 routes, 16 families, digest ${manifest.semantic_jsonl_sha256}, prior-contract-match=${manifest.prior_returned_not_written_contract.semantic_match}`);
}

try {
  if (process.argv.includes('--build')) await build();
  else if (process.argv.includes('--check')) check();
  else throw new Error('usage: ingest-documentation.mjs --build | --check');
} catch (error) {
  console.error(error.stack ?? error.message);
  process.exitCode = 2;
}

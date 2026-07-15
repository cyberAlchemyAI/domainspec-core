import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { parse } from 'parse5';
import {
  HTML_TRANSFORM_ENGINE,
  HtmlTransformEngine,
  htmlTransformEngine
} from '../src/kernel/html-transform.mjs';

const projectRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const golden = JSON.parse(await readFile(
  path.join(projectRoot, 'tests/fixtures/operations-transform/golden.json'),
  'utf8'
));

function bodyFrom(html) {
  const document = parse(html);
  const htmlElement = document.childNodes.find((node) => node.tagName === 'html');
  return htmlElement?.childNodes.find((node) => node.tagName === 'body') || null;
}

function assertGoldenResult(result, expected, id) {
  assert.equal(result.html, expected.html, `${id}: serialized HTML`);
  assert.equal(result.byte_length, expected.byte_length, `${id}: byte length`);
  assert.equal(result.sha256, expected.sha256, `${id}: SHA-256`);
  assert.equal(Buffer.isBuffer(result.bytes), true, `${id}: UTF-8 bytes`);
  assert.deepEqual(result.bytes, Buffer.from(expected.html, 'utf8'), `${id}: exact bytes`);
  assert.equal(
    createHash('sha256').update(result.bytes).digest('hex'),
    expected.sha256,
    `${id}: bytes bind digest`
  );
  assert.ok(bodyFrom(result.html), `${id}: complete document has a body`);
}

test('pins the selected parse5 engine and compatible Node floor', async () => {
  const packageJson = JSON.parse(await readFile(path.join(projectRoot, 'package.json'), 'utf8'));
  const packageLock = JSON.parse(await readFile(path.join(projectRoot, 'package-lock.json'), 'utf8'));

  assert.deepEqual(HTML_TRANSFORM_ENGINE, { name: 'parse5', version: '8.0.1' });
  assert.equal(packageJson.dependencies.parse5, '8.0.1');
  assert.equal(packageJson.engines.node, '>=20.19.0');
  assert.equal(packageLock.packages[''].dependencies.parse5, '8.0.1');
  assert.equal(packageLock.packages[''].engines.node, '>=20.19.0');
  assert.equal(packageLock.packages['node_modules/parse5'].version, '8.0.1');
});

test('freezes complete-document serialization and digest bytes', () => {
  for (const entry of golden.documents) {
    const first = htmlTransformEngine.replace(entry.input);
    const second = htmlTransformEngine.replace(entry.input);
    assertGoldenResult(first, entry.expected, entry.id);
    assert.deepEqual(second, first, `${entry.id}: repeated replacement is deterministic`);
    assert.equal(
      htmlTransformEngine.replace(first.html).html,
      first.html,
      `${entry.id}: serialized document is stable`
    );
  }
});

test('freezes body-context fragment append in input order', () => {
  for (const entry of golden.appends) {
    const first = htmlTransformEngine.append(entry.current_html, entry.fragment_html);
    const second = htmlTransformEngine.append(entry.current_html, entry.fragment_html);
    assertGoldenResult(first, entry.expected, entry.id);
    assert.deepEqual(second, first, `${entry.id}: repeated append is deterministic`);
  }

  const ordered = htmlTransformEngine.append(
    '<!doctype html><body><p id="existing">E</p></body>',
    '<section id="first"></section>tail<strong id="last">L</strong>'
  );
  const childNames = bodyFrom(ordered.html).childNodes.map((node) => node.tagName || node.nodeName);
  assert.deepEqual(childNames, ['p', 'section', '#text', 'strong']);
});

test('repairs ordinary malformed HTML instead of claiming syntax rejection', () => {
  const documentCase = golden.documents.find((entry) => entry.id === 'malformed-nesting');
  const fragmentCase = golden.appends.find((entry) => entry.id === 'malformed-fragment');
  assertGoldenResult(htmlTransformEngine.replace(documentCase.input), documentCase.expected, documentCase.id);
  assertGoldenResult(
    htmlTransformEngine.append(fragmentCase.current_html, fragmentCase.fragment_html),
    fragmentCase.expected,
    fragmentCase.id
  );
});

test('parses scripts and resources without executing or loading them', () => {
  delete globalThis.__transformExecuted;
  const originalFetch = globalThis.fetch;
  let fetchCount = 0;
  globalThis.fetch = () => {
    fetchCount += 1;
    throw new Error('transformer attempted a resource fetch');
  };

  try {
    const result = htmlTransformEngine.append(
      '<!doctype html><body><p>Existing</p></body>',
      '<script>globalThis.__transformExecuted = true</script><img src="https://invalid.local/x.png">'
    );
    assert.match(result.html, /<script>globalThis\.__transformExecuted = true<\/script>/);
    assert.match(result.html, /<img src="https:\/\/invalid\.local\/x\.png">/);
    assert.equal(globalThis.__transformExecuted, undefined);
    assert.equal(fetchCount, 0);
  } finally {
    globalThis.fetch = originalFetch;
    delete globalThis.__transformExecuted;
  }
});

test('rejects non-string inputs with stable typed errors', () => {
  const engine = new HtmlTransformEngine();
  assert.throws(
    () => engine.replace(Buffer.from('<html></html>')),
    (error) => error.code === 'operations_transform_invalid_input' && error.field === 'html'
  );
  assert.throws(
    () => engine.append(null, '<p>x</p>'),
    (error) => error.code === 'operations_transform_invalid_input'
      && error.field === 'current_html'
  );
  assert.throws(
    () => engine.append('<html></html>', undefined),
    (error) => error.code === 'operations_transform_invalid_input'
      && error.field === 'fragment_html'
  );
});

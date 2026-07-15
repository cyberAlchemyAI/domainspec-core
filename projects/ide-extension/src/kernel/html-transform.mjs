import { createHash } from 'node:crypto';
import { parse, parseFragment, serialize } from 'parse5';

const HTML_NAMESPACE = 'http://www.w3.org/1999/xhtml';

export const HTML_TRANSFORM_ENGINE = Object.freeze({
  name: 'parse5',
  version: '8.0.1'
});

function transformError(code, message, details = {}) {
  const error = new Error(message);
  error.code = code;
  Object.assign(error, details);
  return error;
}

function requireHtmlString(value, field) {
  if (typeof value !== 'string') {
    throw transformError(
      'operations_transform_invalid_input',
      `${field} must be a string`,
      { field }
    );
  }
}

function findSingleBody(document) {
  const htmlElements = document.childNodes.filter(
    (node) => node.tagName === 'html' && node.namespaceURI === HTML_NAMESPACE
  );
  const bodies = htmlElements.flatMap((htmlElement) => htmlElement.childNodes.filter(
    (node) => node.tagName === 'body' && node.namespaceURI === HTML_NAMESPACE
  ));

  if (htmlElements.length !== 1 || bodies.length !== 1) {
    throw transformError(
      'operations_transform_invalid_document',
      'parsed document must contain exactly one HTML body',
      {
        html_element_count: htmlElements.length,
        body_count: bodies.length
      }
    );
  }
  return bodies[0];
}

function resultFromDocument(document) {
  const html = serialize(document);
  const bytes = Buffer.from(html, 'utf8');
  return Object.freeze({
    html,
    bytes,
    byte_length: bytes.length,
    sha256: createHash('sha256').update(bytes).digest('hex')
  });
}

export class HtmlTransformEngine {
  replace(html) {
    requireHtmlString(html, 'html');
    const document = parse(html);
    findSingleBody(document);
    return resultFromDocument(document);
  }

  append(currentHtml, fragmentHtml) {
    requireHtmlString(currentHtml, 'current_html');
    requireHtmlString(fragmentHtml, 'fragment_html');

    const document = parse(currentHtml);
    const body = findSingleBody(document);
    const fragment = parseFragment(body, fragmentHtml);
    const nodes = [...fragment.childNodes];

    for (const node of nodes) {
      node.parentNode = body;
      body.childNodes.push(node);
    }
    fragment.childNodes.length = 0;

    return resultFromDocument(document);
  }
}

export const htmlTransformEngine = Object.freeze(new HtmlTransformEngine());

import {canonicalizeJson, deepFreeze, digestValue, fail, isRecord, nonEmptyString, uniqueStrings} from "./canonical.mjs";

const SCHEMA_VERSION = "are.request-context-selection/v1";
const STOP_WORDS = new Set([
  "about", "after", "again", "also", "build", "could", "from", "have", "into", "make", "more", "need",
  "project", "should", "that", "their", "there", "these", "they", "this", "using", "want", "what", "when",
  "where", "which", "with", "would", "your",
]);

function words(value) {
  return String(value ?? "")
    .replace(/([a-z0-9])([A-Z])/g, "$1 $2")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .match(/[a-z0-9]+/g) ?? [];
}

function searchableTerms(values) {
  const terms = [];
  for (const value of values) {
    const tokens = words(value).filter((token) => token.length >= 3 && !STOP_WORDS.has(token));
    if (tokens.length === 0) continue;
    terms.push(tokens.join(" "), ...tokens.filter((token) => token.length >= 4));
  }
  return uniqueStrings(terms);
}

function scoreTerms(requestText, requestWords, terms) {
  let score = 0;
  const matched = [];
  for (const term of terms) {
    const tokens = words(term);
    if (tokens.length === 0) continue;
    if (tokens.length === 1 && (tokens[0].length < 4 || STOP_WORDS.has(tokens[0]))) continue;
    const phrase = tokens.join(" ");
    const matches = tokens.length > 1
      ? requestText.includes(phrase)
      : requestWords.has(tokens[0]);
    if (!matches) continue;
    matched.push(phrase);
    score = Math.max(score, tokens.length * 100 + phrase.length);
  }
  return {score, matched_terms: uniqueStrings(matched)};
}

function includesExactPhrase(requestText, phrase) {
  return phrase.length > 0 && ` ${requestText} `.includes(` ${phrase} `);
}

function bounded(value, fallback, maximum = 64) {
  return Number.isSafeInteger(value) && value >= 0 ? Math.min(value, maximum) : fallback;
}

export function selectRequestContext(input) {
  if (!isRecord(input) || !nonEmptyString(input.raw_request) || !isRecord(input.catalog) || !isRecord(input.snapshot)) {
    return fail("request-context-selection", ["selection.input-incomplete"]);
  }
  const requestTokens = words(input.raw_request);
  const requestText = requestTokens.join(" ");
  const requestWordSet = new Set(requestTokens);
  const maxDefinitions = bounded(input.policy?.max_definition_matches, 8);
  const maxNodes = bounded(input.policy?.max_ontology_node_matches, 12);
  const maxEdges = bounded(input.policy?.max_ontology_edge_matches, 16);

  const definitionCandidates = (input.catalog.definitions ?? []).flatMap((definition) => {
    if (!isRecord(definition) || !nonEmptyString(definition.definition_id)) return [];
    const terms = Array.isArray(definition.lookup_terms) ? definition.lookup_terms : searchableTerms(definition.aliases ?? []);
    const match = scoreTerms(requestText, requestWordSet, terms);
    const primaryTokens = words(definition.primary_term ?? definition.aliases?.[0]);
    const primaryPhrase = primaryTokens.join(" ");
    const primaryExact = includesExactPhrase(requestText, primaryPhrase) ? 1000 + primaryTokens.length * 100 + primaryPhrase.length : 0;
    return match.score > 0 || primaryExact > 0 ? [{definition_id: definition.definition_id, ...match, score: Math.max(match.score, primaryExact), primary_exact: primaryExact > 0, primary_phrase: primaryPhrase}] : [];
  });
  const exactPrimaryCandidates = definitionCandidates.filter((candidate) => candidate.primary_exact);
  const dominantCandidates = exactPrimaryCandidates.length > 0
    ? exactPrimaryCandidates.filter((candidate) => !exactPrimaryCandidates.some((other) => (
      other.definition_id !== candidate.definition_id
      && other.score > candidate.score
      && includesExactPhrase(other.primary_phrase, candidate.primary_phrase)
    )))
    : definitionCandidates;
  const definitionMatches = dominantCandidates
    .sort((a, b) => b.score - a.score || a.definition_id.localeCompare(b.definition_id))
    .slice(0, maxDefinitions)
    .map(({primary_exact: _primaryExact, primary_phrase: _primaryPhrase, ...match}) => match);

  const nodeMatches = (input.snapshot.nodes ?? []).flatMap((node) => {
    if (!isRecord(node) || !nonEmptyString(node.node_id)) return [];
    const terms = Array.isArray(node.lookup_terms) ? node.lookup_terms : searchableTerms([node.node_id, ...(node.search_terms ?? [])]);
    const match = scoreTerms(requestText, requestWordSet, terms);
    return match.score > 0 ? [{node_id: node.node_id, ...match}] : [];
  }).sort((a, b) => b.score - a.score || a.node_id.localeCompare(b.node_id)).slice(0, maxNodes);

  const selectedNodes = new Set(nodeMatches.map((match) => match.node_id));
  const edgeMatches = (input.snapshot.edges ?? []).flatMap((edge) => {
    if (!isRecord(edge) || !nonEmptyString(edge.edge_id)) return [];
    const endpointCount = Number(selectedNodes.has(edge.from_node_id)) + Number(selectedNodes.has(edge.to_node_id));
    if (endpointCount === 0) return [];
    return [{edge_id: edge.edge_id, endpoint_count: endpointCount}];
  }).sort((a, b) => b.endpoint_count - a.endpoint_count || a.edge_id.localeCompare(b.edge_id)).slice(0, maxEdges);
  const contextItemMatches = (input.context_items ?? []).flatMap((item) => {
    if (!isRecord(item) || !nonEmptyString(item.context_item_id)) return [];
    const match = scoreTerms(requestText, requestWordSet, searchableTerms(item.match_terms ?? []));
    return match.score > 0 ? [{context_item_id: item.context_item_id, ...match}] : [];
  }).sort((a, b) => b.score - a.score || a.context_item_id.localeCompare(b.context_item_id));

  const value = canonicalizeJson({
    schema_version: SCHEMA_VERSION,
    request_digest: digestValue(input.raw_request),
    definition_matches: definitionMatches,
    ontology_node_matches: nodeMatches,
    ontology_edge_matches: edgeMatches,
    context_item_matches: contextItemMatches,
    policy: {max_definition_matches: maxDefinitions, max_ontology_node_matches: maxNodes, max_ontology_edge_matches: maxEdges},
    model_calls: 0,
    filesystem_calls: 0,
    ontology_runtime_calls: 0,
    authority_effect: "none",
  });
  return deepFreeze({schema_version: SCHEMA_VERSION, ok: true, value, digest: digestValue(value), authority_effect: "none"});
}

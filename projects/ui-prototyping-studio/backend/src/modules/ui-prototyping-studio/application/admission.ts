import {
  parseHtml,
  type CanonElement,
  type CanonNode,
} from "../domain/canonicalize.js";

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.ScopeAdmission
 *     type: Service
 *
 * M1 — the whole-tree od-id-attributed scope validator (the V3 fence, SWU-M1).
 * TypeScript port of the C-1 spike (DEC-C1-SPIKE-SURVIVED-016) over the M0c
 * canonicalizer. Pure, clock-free. Given the baseline (head) HTML and a candidate,
 * REJECTs any change attributed to an out-of-scope od-id, any forge/re-tag of a
 * baseline od-id, and any unattributable change (⊥); else NOT_REJECT.
 *
 * Carries GAP-V3-NODE-IDENTITY-008: the alignment key (tag + same-tag-sibling index
 * path) is brittle to legitimate structural reordering; production needs a more
 * robust node identity + real CSS cascade. Sufficient for the L0→L2 floor.
 */
export type ScopeVerdict = "REJECT" | "NOT_REJECT";

interface Entry {
  node: CanonElement;
  key: string;
  /** nearest-ancestor-first od-id chain (includes self) */
  scopeChain: string[];
}

function odIdOf(el: CanonElement): string | null {
  return el.attrs.get("data-od-id") ?? null;
}

/** Walk producing a stable alignment key + the od-id scope chain for each element. */
function walk(nodes: readonly CanonNode[]): Entry[] {
  const out: Entry[] = [];
  const rec = (ns: readonly CanonNode[], path: string, chain: string[]): void => {
    const counts = new Map<string, number>();
    for (const n of ns) {
      if (n.type !== "element") continue;
      const idx = counts.get(n.tag) ?? 0;
      counts.set(n.tag, idx + 1);
      const key = `${path}/${n.tag}[${idx}]`;
      const oid = odIdOf(n);
      const nextChain = oid ? [oid, ...chain] : chain;
      out.push({ node: n, key, scopeChain: nextChain });
      rec(n.children, key, nextChain);
    }
  };
  rec(nodes, "", []);
  return out;
}

/** Shallow content signature: identity-bearing structure of a single node. */
function shallowSig(el: CanonElement): string {
  const attrs = [...el.attrs.keys()].sort().map((k) => `${k}=${el.attrs.get(k)}`).join("|");
  const directText = el.children
    .filter((c): c is Extract<CanonNode, { type: "text" }> => c.type === "text")
    .map((c) => c.text)
    .join("");
  return `${el.tag}#${attrs}#${directText}#${el.rawText ?? ""}`;
}

function selectorResolves(el: CanonElement, selector: string): boolean {
  const s = selector.trim();
  if (s.startsWith(".")) return (el.attrs.get("class") ?? "").split(/\s+/).includes(s.slice(1));
  if (s.startsWith("#")) return el.attrs.get("id") === s.slice(1);
  const attr = /^\[([\w-]+)=["']?([^\]"']+)["']?\]$/.exec(s);
  if (attr) return el.attrs.get(attr[1]!) === attr[2];
  return el.tag === s.toLowerCase();
}

interface CssRule {
  selector: string;
  /** normalized "selector{decl}" — identity of the rule (catches declaration changes) */
  text: string;
}
function parseRules(rawStyle: string): CssRule[] {
  const out: CssRule[] = [];
  const re = /([^{}]+)\{([^{}]*)\}/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(rawStyle)) !== null) {
    const decl = m[2]!.replace(/\s+/g, " ").trim();
    for (const sel of m[1]!.split(",")) {
      const s = sel.trim();
      if (s) out.push({ selector: s, text: `${s}{${decl}}` });
    }
  }
  return out;
}

/**
 * The V3 fence. `baselineHtml` = current head; `candidateHtml` = proposed.
 * `taskScopeOdIds` = the in-scope od-id set (TaskScope).
 */
export function admitScope(
  baselineHtml: string,
  candidateHtml: string,
  taskScopeOdIds: readonly string[],
): ScopeVerdict {
  const scope = new Set(taskScopeOdIds);
  const baseEntries = walk(parseHtml(baselineHtml));
  const candEntries = walk(parseHtml(candidateHtml));
  if (candEntries.length === 0) return "REJECT"; // ⊥ collapse

  const baseByKey = new Map(baseEntries.map((e) => [e.key, e]));
  const candByKey = new Map(candEntries.map((e) => [e.key, e]));

  // baseline binding: od-id -> alignment key (trusted oracle)
  const binding = new Map<string, string>();
  for (const e of baseEntries) {
    const oid = odIdOf(e.node);
    if (oid && !binding.has(oid)) binding.set(oid, e.key);
  }

  // integrity: a candidate node asserting a baseline od-id must sit on its bound node
  for (const e of candEntries) {
    const oid = odIdOf(e.node);
    if (oid && binding.has(oid) && binding.get(oid) !== e.key) return "REJECT"; // forge / re-tag
  }

  // attribute each structural change to its nearest od-id; out-of-scope or ⊥ => REJECT
  const verdictForChange = (e: Entry): ScopeVerdict => {
    const oid = e.scopeChain[0];
    if (oid === undefined) return "REJECT"; // unattributable change (⊥)
    if (!scope.has(oid)) return "REJECT"; // out-of-scope
    return "NOT_REJECT";
  };

  for (const [key, ce] of candByKey) {
    if (ce.node.tag === "style") continue; // <style> handled by the CSS block below
    const be = baseByKey.get(key);
    if (!be) {
      if (verdictForChange(ce) === "REJECT") return "REJECT"; // added
    } else if (shallowSig(be.node) !== shallowSig(ce.node)) {
      if (verdictForChange(ce) === "REJECT") return "REJECT"; // changed
    }
  }
  for (const [key, be] of baseByKey) {
    if (be.node.tag === "style") continue; // handled by the CSS block
    if (!candByKey.has(key) && verdictForChange(be) === "REJECT") return "REJECT"; // removed
  }

  // CSS: a changed/added <style> rule must resolve only to in-scope od-id nodes
  const baseStyle = baseEntries.filter((e) => e.node.tag === "style").map((e) => e.node.rawText ?? "").join("\n");
  const candStyleEntries = candEntries.filter((e) => e.node.tag === "style");
  const candStyle = candStyleEntries.map((e) => e.node.rawText ?? "").join("\n");
  if (candStyle !== baseStyle) {
    const baseRuleTexts = new Set(parseRules(baseStyle).map((r) => r.text));
    for (const rule of parseRules(candStyle)) {
      if (baseRuleTexts.has(rule.text)) continue; // rule (selector+decl) unchanged
      for (const e of candEntries) {
        if (selectorResolves(e.node, rule.selector)) {
          const oid = e.scopeChain[0];
          if (oid === undefined || !scope.has(oid)) return "REJECT";
        }
      }
    }
  }

  return "NOT_REJECT";
}

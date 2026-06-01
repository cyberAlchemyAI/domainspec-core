import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { join, dirname } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const registerPath = join(here, "banned-terms.json");

let cachedRegister = null;

export async function loadRegister() {
  if (cachedRegister) return cachedRegister;
  const text = await readFile(registerPath, "utf8");
  const parsed = JSON.parse(text);
  for (const [name, group] of Object.entries(parsed.registers)) {
    if (group.match === "regex") {
      group._compiled = group.entries.map((entry) => ({
        ...entry,
        re: new RegExp(entry.pattern, entry.flags || ""),
      }));
    }
  }
  cachedRegister = parsed;
  return parsed;
}

export function getRegisterPath() {
  return registerPath;
}

function dirMatchesAny(dir, terms) {
  if (!terms || terms.length === 0) return false;
  return terms.some((term) => dir.includes(term));
}

function bodyContainsAll(body, strings) {
  return strings.every((s) => body.includes(s));
}

export function findForbiddenSubstrings(register, content, scope = "html") {
  const findings = [];
  for (const [groupName, group] of Object.entries(register.registers)) {
    if (group.match !== "case_insensitive_substring") continue;
    if (!group.scope.includes(scope)) continue;
    const lowered = content.toLowerCase();
    for (const entry of group.entries) {
      if (lowered.includes(entry.term.toLowerCase())) {
        findings.push({
          fail_code: group.fail_code,
          severity: group.severity,
          register: groupName,
          term: entry.term,
          reason: entry.reason,
          source: entry.source,
        });
      }
    }
  }
  return findings;
}

export function findForbiddenPatterns(register, content, scope = "html") {
  const findings = [];
  for (const [groupName, group] of Object.entries(register.registers)) {
    if (group.match !== "regex") continue;
    if (!group.scope.includes(scope)) continue;
    for (const entry of group._compiled) {
      if (entry.re.test(content)) {
        findings.push({
          fail_code: group.fail_code,
          severity: group.severity,
          register: groupName,
          pattern: entry.pattern,
          reason: entry.reason,
        });
      }
    }
  }
  return findings;
}

export function findMissingBlockerCopy(register, body, dirLabel) {
  const findings = [];
  const group = register.registers.required_blocker_copy;
  if (!group) return findings;
  for (const entry of group.entries) {
    if (!dirMatchesAny(dirLabel, entry.route_match_any)) continue;
    const inState = dirMatchesAny(dirLabel, entry.state_match_any);
    const excluded = dirMatchesAny(dirLabel, entry.state_exclude_any);
    if (!inState || excluded) continue;

    if (entry.required_strings && !bodyContainsAll(body, entry.required_strings)) {
      const missing = entry.required_strings.filter((s) => !body.includes(s));
      findings.push({
        fail_code: group.fail_code,
        severity: group.severity,
        register: "required_blocker_copy",
        rule_id: entry.id,
        route_dir: dirLabel,
        missing_strings: missing,
        source: entry.source,
      });
    }

    if (Array.isArray(entry.required_strings_any_of)) {
      for (const altGroup of entry.required_strings_any_of) {
        const oneMatched = altGroup.some((s) => body.includes(s));
        if (!oneMatched) {
          findings.push({
            fail_code: group.fail_code,
            severity: group.severity,
            register: "required_blocker_copy",
            rule_id: entry.id,
            route_dir: dirLabel,
            missing_any_of: altGroup,
            source: entry.source,
          });
        }
      }
    }
  }
  return findings;
}

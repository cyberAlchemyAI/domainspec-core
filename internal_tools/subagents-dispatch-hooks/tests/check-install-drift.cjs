#!/usr/bin/env node
'use strict';
/*
 * check-install-drift — the source-vs-installed diff.
 *
 *   node tests/check-install-drift.cjs [extra-repo-root ...]
 *
 * WHY THIS EXISTS (constitution §14 / RV-9, and the incident that produced it):
 *
 *   On 2026-06-16 an owner decision ("review goes inline") landed in THIS bundle.
 *   `install.cjs` was never re-run. For a month the *executing* appender
 *   (~/.claude/skills/register-dispatch/append-dispatch.cjs) still enforced the old
 *   rule, and a project copy of review/SKILL.md had been overwritten out-of-band from
 *   a sibling repo, restoring a mandate the decision had removed. Three copies, three
 *   different laws, and NOTHING FAILED — because nothing compared them.
 *
 *   No reviewer of any angle would have caught that. It is not a reasoning defect; it
 *   is a deployment-drift defect, and the only instrument that catches deployment drift
 *   is a diff. This is that diff. It is the primary defence; the governance around it
 *   (schema keys, amendments, red-team reviews) is secondary and does not substitute.
 *
 * WHAT IT CHECKS — the bundle is the SOURCE; every installed copy must MATCH IN CONTENT (EOL-normalized: the repos run autocrlf=true and commit .claude/skills, so git rewrites installs with CRLF).
 *
 *   GLOBAL (~/.claude, per user):
 *     hooks/{remind-register-dispatch,block-workflow,enforce-append-only-dispatch}.cjs
 *     skills/register-dispatch/{SKILL.md,append-dispatch.cjs}
 *   PROJECT (<repo>/.claude/skills/, per target repo):
 *     domainspec-subagents-strategy, research, review, experiment, check-tension, robot-talks
 *
 * WHICH REPOS — read from the install manifest that `install.cjs` writes
 * (~/.claude/subagents-dispatch-targets.json), plus any roots passed as arguments.
 * A repo that carries the chain skills but is NOT in the manifest is itself reported:
 * an un-manifested install is an install nobody will ever refresh.
 *
 * EXIT: 0 clean · 1 drift found (the report names every drifted file) · 2 usage/IO error.
 * Run it in CI, and after any edit to this bundle. A green battery over a stale install
 * proves nothing.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');

const here = path.resolve(__dirname, '..');           // the bundle root
const claudeDir = path.join(os.homedir(), '.claude');
const manifestPath = path.join(claudeDir, 'subagents-dispatch-targets.json');

// Keep in lockstep with install.cjs — if that file's tables change, these must too.
const HOOKS = ['remind-register-dispatch.cjs', 'block-workflow.cjs', 'enforce-append-only-dispatch.cjs'];
const GLOBAL_SKILL = 'register-dispatch';
const GLOBAL_SKILL_FILES = ['SKILL.md', 'append-dispatch.cjs'];
const CHAIN_SKILLS = ['domainspec-subagents-strategy', 'research', 'review', 'experiment', 'check-tension', 'robot-talks'];

const drift = [];    // { kind, file, why }
const fwd = (p) => p.split(path.sep).join('/');

// Compare CONTENT, not bytes. Every target repo runs `core.autocrlf=true` and commits
// `.claude/skills/**`, so git rewrites the installed files with CRLF while install.cjs
// writes LF. A byte compare would therefore report drift on every file whose content is
// identical — and a check that cries wolf is a check everyone learns to ignore, which is
// the exact failure mode this file exists to prevent. Normalize EOL and a trailing
// newline; compare what the file SAYS.
const norm = (buf) => buf.toString('utf8').replace(/^﻿/, '').replace(/\r\n/g, '\n').replace(/\s*$/, '\n');

function sameContent(a, b) {
  if (!fs.existsSync(a)) { return { ok: false, why: `MISSING IN BUNDLE: ${fwd(a)}` }; }
  if (!fs.existsSync(b)) { return { ok: false, why: 'NOT INSTALLED' }; }
  const A = fs.readFileSync(a), B = fs.readFileSync(b);
  if (norm(A) === norm(B)) return { ok: true };
  // Content really differs. Say which way, so the reader knows whether git reverted the
  // install (the common case: the repo's committed copy won) or someone edited in place.
  return { ok: false, why: `CONTENT DIFFERS (bundle ${A.length}B / installed ${B.length}B)` };
}

// --- GLOBAL surface -------------------------------------------------------
for (const h of HOOKS) {
  const r = sameContent(path.join(here, 'hooks', h), path.join(claudeDir, 'hooks', h));
  if (!r.ok) drift.push({ kind: 'global/hook', file: `~/.claude/hooks/${h}`, why: r.why });
}
for (const f of GLOBAL_SKILL_FILES) {
  const r = sameContent(path.join(here, 'skills', GLOBAL_SKILL, f), path.join(claudeDir, 'skills', GLOBAL_SKILL, f));
  // This one is the incident's ground zero: append-dispatch.cjs here is the file the
  // register-dispatch SKILL tells the model to EXECUTE. If it drifts, the running law
  // is not the written law.
  if (!r.ok) drift.push({ kind: 'global/skill', file: `~/.claude/skills/${GLOBAL_SKILL}/${f}`, why: r.why });
}

// --- PROJECT surface ------------------------------------------------------
let manifest = [];
try {
  if (fs.existsSync(manifestPath)) manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8')).targets || [];
} catch (e) {
  console.error(`cannot parse install manifest ${fwd(manifestPath)}: ${e.message}`);
  process.exit(2);
}
const extra = process.argv.slice(2).map((p) => path.resolve(p));
const targets = [...new Set([...manifest, ...extra])];

if (targets.length === 0) {
  console.error('no install targets known: the manifest is absent/empty and no roots were passed.');
  console.error(`run \`node install.cjs\` (it writes ${fwd(manifestPath)}), or pass repo roots as arguments.`);
  process.exit(2);
}

for (const repo of targets) {
  const skillsDir = path.join(repo, '.claude', 'skills');
  if (!fs.existsSync(skillsDir)) {
    drift.push({ kind: 'project', file: fwd(repo), why: 'TARGET HAS NO .claude/skills — stale manifest entry, or the repo moved' });
    continue;
  }
  for (const name of CHAIN_SKILLS) {
    const srcDir = path.join(here, 'skills', name);
    if (!fs.existsSync(srcDir)) continue;                    // not in the bundle; install.cjs skips it too
    for (const f of fs.readdirSync(srcDir)) {
      if (!fs.statSync(path.join(srcDir, f)).isFile()) continue;
      const r = sameContent(path.join(srcDir, f), path.join(skillsDir, name, f));
      if (!r.ok) drift.push({ kind: 'project', file: `${fwd(repo)}/.claude/skills/${name}/${f}`, why: r.why });
    }
  }
}

// --- Un-manifested installs ----------------------------------------------
// A repo carrying the chain skills but absent from the manifest will never be
// refreshed by a re-install, so it silently rots. Surface it. (Scan is shallow and
// cheap: the siblings of each known target.)
const parents = new Set(targets.map((t) => path.dirname(t)));
for (const parent of parents) {
  let entries = [];
  try { entries = fs.readdirSync(parent, { withFileTypes: true }); } catch (_) { continue; }
  for (const e of entries) {
    if (!e.isDirectory()) continue;
    const repo = path.join(parent, e.name);
    if (targets.includes(repo)) continue;
    if (fs.existsSync(path.join(repo, '.claude', 'skills', 'domainspec-subagents-strategy'))) {
      drift.push({ kind: 'unmanifested', file: fwd(repo), why: 'CARRIES THE CHAIN SKILLS BUT IS NOT AN INSTALL TARGET — it will never be refreshed; run install.cjs against it or remove its .claude/skills copies' });
    }
  }
}

// --- Report ---------------------------------------------------------------
console.log(`source: ${fwd(here)}`);
console.log(`targets: ${targets.length} repo${targets.length === 1 ? '' : 's'} (manifest: ${fwd(manifestPath)})`);
for (const t of targets) console.log(`  · ${fwd(t)}`);

if (drift.length === 0) {
  console.log('\n✓ no drift — every installed copy matches the bundle (EOL-normalized).');
  process.exit(0);
}

console.error(`\n✗ INSTALL DRIFT — ${drift.length} file${drift.length === 1 ? '' : 's'} out of sync with the bundle:\n`);
for (const d of drift) console.error(`  [${d.kind}] ${d.file}\n      ${d.why}`);
console.error('\nThe bundle is the source; the installed copies are what actually runs.');
console.error('Fix: re-run `node install.cjs` for each target repo (CLAUDE_PROJECT_DIR=<repo> node install.cjs).');
console.error('If a copy was edited in place, that edit is LOST on re-install — port it into the bundle first.');
process.exit(1);

import { readdir, readFile, mkdir, writeFile, stat } from "node:fs/promises";
import { join, dirname, relative } from "node:path";
import { fileURLToPath } from "node:url";
import {
  loadRegister,
  findForbiddenSubstrings,
  findForbiddenPatterns,
  findMissingBlockerCopy,
} from "../src/doctrine/banned-terms.mjs";

const appRoot = fileURLToPath(new URL("..", import.meta.url));
const stitchDir = join(appRoot, "stitch_tilth_os_institutional_shell 3");
const assetsDir = join(appRoot, "assets");
const reportsDir = join(appRoot, "reports", "doctrine-lint");

async function exists(path) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

async function scanDirectory(dir, suffix) {
  if (!(await exists(dir))) return [];
  let results = [];
  const entries = await readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      results = results.concat(await scanDirectory(fullPath, suffix));
    } else if (fullPath.endsWith(suffix)) {
      results.push(fullPath);
    }
  }
  return results;
}

function formatFinding(file, finding) {
  const rel = relative(appRoot, file);
  if (finding.term) {
    return `[${finding.severity}] ${finding.fail_code} — "${finding.term}" in ${rel} (${finding.reason})`;
  }
  if (finding.pattern) {
    return `[${finding.severity}] ${finding.fail_code} — pattern /${finding.pattern}/ matched in ${rel} (${finding.reason})`;
  }
  if (finding.missing_strings) {
    return `[${finding.severity}] ${finding.fail_code} — ${rel} missing required strings: ${finding.missing_strings.map((s) => JSON.stringify(s)).join(", ")} (rule ${finding.rule_id})`;
  }
  if (finding.missing_any_of) {
    return `[${finding.severity}] ${finding.fail_code} — ${rel} missing at least one of: ${finding.missing_any_of.map((s) => JSON.stringify(s)).join(", ")} (rule ${finding.rule_id})`;
  }
  return `[${finding.severity}] ${finding.fail_code} — ${rel}`;
}

async function runLint() {
  console.log("Doctrine lint starting — register: src/doctrine/banned-terms.json");
  const register = await loadRegister();
  const findings = [];

  const htmlFiles = await scanDirectory(stitchDir, ".html");
  for (const file of htmlFiles) {
    const content = await readFile(file, "utf8");
    const dirLabel = dirname(relative(appRoot, file));
    findings.push(
      ...findForbiddenSubstrings(register, content, "html").map((f) => ({ file, ...f })),
      ...findForbiddenPatterns(register, content, "html").map((f) => ({ file, ...f })),
      ...findMissingBlockerCopy(register, content, dirLabel).map((f) => ({ file, ...f })),
    );
  }

  const jsFiles = await scanDirectory(assetsDir, ".js");
  for (const file of jsFiles) {
    const content = await readFile(file, "utf8");
    findings.push(
      ...findForbiddenSubstrings(register, content, "extracted_js").map((f) => ({ file, ...f })),
    );
  }

  const totalScanned = htmlFiles.length + jsFiles.length;
  await mkdir(reportsDir, { recursive: true });
  const reportPath = join(reportsDir, "latest.md");

  let report = `# Doctrine Lint Report\n\n`;
  report += `- Register: \`src/doctrine/banned-terms.json\` (v${register.register_version})\n`;
  report += `- Files scanned: ${totalScanned} (${htmlFiles.length} html, ${jsFiles.length} js)\n`;
  report += `- Timestamp: ${new Date().toISOString()}\n\n`;

  if (findings.length === 0) {
    console.log(`Doctrine lint PASSED — ${totalScanned} files scanned, 0 findings.`);
    report += `## PASSED\n\nNo doctrine drift or governance violations detected.\n`;
    await writeFile(reportPath, report);
    process.exit(0);
  }

  console.error(`Doctrine lint FAILED — ${findings.length} findings across ${totalScanned} files.`);
  report += `## FAILED — ${findings.length} findings\n\n`;
  const byCode = new Map();
  for (const finding of findings) {
    const code = finding.fail_code;
    if (!byCode.has(code)) byCode.set(code, []);
    byCode.get(code).push(finding);
  }
  for (const [code, items] of byCode) {
    report += `### ${code} (${items.length})\n\n`;
    for (const item of items) {
      const line = formatFinding(item.file, item);
      console.error(line);
      report += `- ${line}\n`;
    }
    report += `\n`;
  }
  await writeFile(reportPath, report);
  process.exit(1);
}

runLint().catch((err) => {
  console.error("Doctrine lint crashed:", err);
  process.exit(1);
});

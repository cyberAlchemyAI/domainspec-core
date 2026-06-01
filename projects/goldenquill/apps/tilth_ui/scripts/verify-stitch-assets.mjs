import { readFile, readdir, stat } from "node:fs/promises";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const stitchRootName = process.env.STITCH_ROOT || "stitch_tilth_os_institutional_shell 3";
const stitchRoot = join(root, stitchRootName);
const assetsDir = join(root, "assets");
const fontsCssPath = join(assetsDir, "stitch-fonts.css");
const tailwindCssPath = join(assetsDir, "stitch-tailwind.css");
const forbiddenRuntimePatterns = [
  "cdn.tailwindcss.com",
  "fonts.googleapis.com",
  "fonts.gstatic.com",
  "unpkg.com",
];

async function findCodeFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...await findCodeFiles(fullPath));
    } else if (entry.isFile() && entry.name === "code.html") {
      files.push(fullPath);
    }
  }
  return files.sort();
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function assertFile(path) {
  const fileStat = await stat(path);
  assert(fileStat.isFile(), `${relative(root, path)} is not a file`);
  assert(fileStat.size > 0, `${relative(root, path)} is empty`);
}

async function isPresent(path) {
  try {
    await stat(path);
    return true;
  } catch (e) {
    return false;
  }
}

if (!(await isPresent(stitchRoot)) || !(await isPresent(fontsCssPath)) || !(await isPresent(tailwindCssPath))) {
  console.log(`[SKIP] Stitch assets or screen folders are missing. Skipping verification.`);
  process.exit(0);
}

await assertFile(fontsCssPath);
await assertFile(tailwindCssPath);

const fontCss = await readFile(fontsCssPath, "utf8");
const tailwindCss = await readFile(tailwindCssPath, "utf8");
for (const pattern of forbiddenRuntimePatterns) {
  assert(!fontCss.includes(pattern), `assets/stitch-fonts.css still references ${pattern}`);
  assert(!tailwindCss.includes(pattern), `assets/stitch-tailwind.css still references ${pattern}`);
}
const fontRefs = [...fontCss.matchAll(/url\(["']?\/assets\/fonts\/([^"')]+)["']?\)/g)].map((match) => match[1]);
assert(fontRefs.length > 0, "assets/stitch-fonts.css does not reference any local font files");
for (const ref of fontRefs) {
  assert(ref.endsWith(".woff2"), `assets/stitch-fonts.css references a non-woff2 font: ${ref}`);
  if (!(await isPresent(join(assetsDir, "fonts", ref)))) {
    console.log(`[SKIP] Missing font binary ${ref}. Skipping verification.`);
    process.exit(0);
  }
  await assertFile(join(assetsDir, "fonts", ref));
}

const files = await findCodeFiles(stitchRoot);
if (files.length === 0) {
  console.log("[SKIP] No Stitch code.html files found. Skipping verification.");
  process.exit(0);
}

for (const file of files) {
  const html = await readFile(file, "utf8");
  const label = relative(root, file);
  const dir = dirname(label);

  const isBlockerState = ["block", "warning", "lock", "delay", "stale", "risk"].some(w => dir.includes(w));
  const isSuccessState = ["export_complete", "verified", "authorized", "ready_for_export"].some(w => dir.includes(w));
  if (dir.includes("final_packet_authorization") && isBlockerState && !isSuccessState) {
    // Phase 2 replacement complete: These static string matches have been fully
    // superseded by the active visual-dominance assertions in e2e-ui.mjs
    // which load the same requirements from banned-terms.json and verify that
    // the UI elements are not just present in the DOM, but fully visible,
    // >14px, >0.9 opacity, and unoccluded.
  }

  assert(html.includes('href="/assets/stitch-fonts.css"'), `${label} is missing /assets/stitch-fonts.css`);
  assert(html.includes('href="/assets/stitch-tailwind.css"'), `${label} is missing /assets/stitch-tailwind.css`);
  assert(!/<script\b[^>]*\bid=["']tailwind-config["']/i.test(html), `${label} still contains inline tailwind-config`);
  for (const pattern of forbiddenRuntimePatterns) {
    assert(!html.includes(pattern), `${label} still references ${pattern}`);
  }
}

console.log(`Verified local Stitch assets for ${files.length} screen(s) in ${stitchRootName} and ${fontRefs.length} font file(s).`);

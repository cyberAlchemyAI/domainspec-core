import { spawn } from "node:child_process";
import { mkdir, readFile, readdir, rm, stat, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const stitchRootName = process.env.STITCH_ROOT || "stitch_tilth_os_institutional_shell 3";
const stitchRoot = join(root, stitchRootName);
const assetsDir = join(root, "assets");
const fontsDir = join(assetsDir, "fonts");
const tailwindCssPath = join(assetsDir, "stitch-tailwind.css");
const fontsCssPath = join(assetsDir, "stitch-fonts.css");
const configCachePath = join(assetsDir, "stitch-tailwind.config-cache.json");
const tempConfigPath = join(root, ".stitch-tailwind.config.cjs");
const tempInputPath = join(root, ".stitch-tailwind.input.css");
const refreshFonts = process.argv.includes("--refresh-fonts");

const localAssetLinks = [
  '<link rel="stylesheet" href="/assets/stitch-fonts.css">',
  '<link rel="stylesheet" href="/assets/stitch-tailwind.css">',
].join("\n");

const fontCssRequests = [
  "https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&display=swap",
  "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap",
  "https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap",
  "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap",
];

const modernBrowserUserAgent = [
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
  "AppleWebKit/537.36 (KHTML, like Gecko)",
  "Chrome/125.0.0.0 Safari/537.36",
].join(" ");

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

function extractTailwindConfig(html, filePath) {
  const match = html.match(/<script\b[^>]*\bid=["']tailwind-config["'][^>]*>([\s\S]*?)<\/script>/i);
  if (!match) return null;
  const sandbox = { tailwind: {} };
  try {
    vm.runInNewContext(match[1], sandbox, { filename: filePath, timeout: 1000 });
    return sandbox.tailwind.config || null;
  } catch (err) {
    console.warn(`Skipping malformed inline Tailwind config in ${relative(root, filePath)}: ${err.message}`);
    return null;
  }
}

function isPlainObject(value) {
  return value && typeof value === "object" && !Array.isArray(value);
}

function mergeDeep(target, source) {
  for (const [key, value] of Object.entries(source || {})) {
    if (isPlainObject(value) && isPlainObject(target[key])) {
      mergeDeep(target[key], value);
    } else if (isPlainObject(value)) {
      target[key] = mergeDeep({}, value);
    } else if (Array.isArray(value)) {
      target[key] = [...value];
    } else {
      target[key] = value;
    }
  }
  return target;
}

async function readCachedConfig() {
  try {
    return JSON.parse(await readFile(configCachePath, "utf8"));
  } catch {
    return null;
  }
}

function buildMergedConfig(configs, cachedConfig) {
  const merged = cachedConfig || { darkMode: "class", theme: { extend: {} } };
  for (const config of configs) {
    if (!config) continue;
    if (config.darkMode) merged.darkMode = config.darkMode;
    if (config.theme?.extend) {
      merged.theme ||= {};
      merged.theme.extend ||= {};
      mergeDeep(merged.theme.extend, config.theme.extend);
    }
  }
  return merged;
}

function stripRemoteAssets(html) {
  let next = html;
  next = next.replace(/<script\b[^>]*src=["'][^"']*cdn\.tailwindcss\.com[^"']*["'][^>]*>\s*<\/script>\s*/gi, "");
  next = next.replace(/<script\b[^>]*src=["'][^"']*unpkg\.com[^"']*["'][^>]*>\s*<\/script>\s*/gi, "");
  next = next.replace(/<script\b[^>]*\bid=["']tailwind-config["'][^>]*>[\s\S]*?<\/script>\s*/gi, "");
  next = next.replace(/<link\b[^>]*href=["'][^"']*fonts\.googleapis\.com[^"']*["'][^>]*>\s*/gi, "");
  next = next.replace(/<link\b[^>]*href=["'][^"']*fonts\.gstatic\.com[^"']*["'][^>]*>\s*/gi, "");
  next = next.replace(/<link\b[^>]*href=["']\/assets\/stitch-(?:fonts|tailwind)\.css["'][^>]*>\s*/gi, "");
  next = next.replace(/<!--\s*Google Fonts\s*-->\s*/gi, "");
  next = next.replace(/<!--\s*Tailwind CSS\s*-->\s*/gi, "");
  next = next.replace(/<!--\s*Tailwind Config\s*-->\s*/gi, "");
  return next;
}

function insertLocalAssets(html) {
  if (html.includes("</title>")) {
    return html.replace(/<\/title>/i, `</title>\n${localAssetLinks}`);
  }
  return html.replace(/<head>/i, `<head>\n${localAssetLinks}`);
}

async function rewriteStitchHtml(files) {
  for (const file of files) {
    const html = await readFile(file, "utf8");
    const rewritten = insertLocalAssets(stripRemoteAssets(html));
    if (rewritten !== html) {
      await writeFile(file, rewritten, "utf8");
    }
  }
}

function jsString(value) {
  return JSON.stringify(value, null, 2);
}

async function buildTailwindCss(files, mergedConfig) {
  const contentPaths = files.map((file) => `./${relative(root, file).replaceAll("\\", "/")}`);
  const configSource = `const forms = require("@tailwindcss/forms");
const containerQueries = require("@tailwindcss/container-queries");

module.exports = {
  darkMode: ${jsString(mergedConfig.darkMode || "class")},
  content: ${jsString(contentPaths)},
  theme: ${jsString(mergedConfig.theme || { extend: {} })},
  plugins: [forms, containerQueries],
};
`;
  await writeFile(tempConfigPath, configSource, "utf8");
  await writeFile(tempInputPath, "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n", "utf8");
  await runTailwind();
  await rm(tempConfigPath, { force: true });
  await rm(tempInputPath, { force: true });
}

function runTailwind() {
  return new Promise((resolve, reject) => {
    const bin = process.env.TAILWIND_BIN
      || join(root, "node_modules", ".bin", process.platform === "win32" ? "tailwindcss.cmd" : "tailwindcss");
    const child = spawn(bin, [
      "-c", tempConfigPath,
      "-i", tempInputPath,
      "-o", tailwindCssPath,
      "--minify",
    ], { cwd: root, stdio: "inherit" });
    child.on("exit", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`tailwindcss exited with code ${code}`));
    });
    child.on("error", reject);
  });
}

async function downloadFontCss() {
  await mkdir(fontsDir, { recursive: true });
  const cssChunks = [];
  for (const request of fontCssRequests) {
    const response = await fetch(request, {
      headers: {
        "User-Agent": modernBrowserUserAgent,
      },
    });
    if (!response.ok) throw new Error(`Font CSS fetch failed ${response.status}: ${request}`);
    let css = await response.text();
    const urls = [...css.matchAll(/url\((https:\/\/fonts\.gstatic\.com\/[^)]+?\.woff2)\)/g)].map((match) => match[1]);
    if (!urls.length) throw new Error(`Font CSS did not include woff2 assets: ${request}`);
    for (const url of urls) {
      const filename = fontFilename(url);
      const localPath = join(fontsDir, filename);
      const fontResponse = await fetch(url);
      if (!fontResponse.ok) throw new Error(`Font fetch failed ${fontResponse.status}: ${url}`);
      const buffer = Buffer.from(await fontResponse.arrayBuffer());
      await writeFile(localPath, buffer);
      css = css.replaceAll(url, `/assets/fonts/${filename}`);
    }
    cssChunks.push(css.trim());
  }
  await writeFile(fontsCssPath, `${cssChunks.join("\n\n")}\n`, "utf8");
}

function fontFilename(url) {
  const parsed = new URL(url);
  const basename = parsed.pathname.split("/").pop() || "font.woff2";
  const hash = createHash("sha256").update(url).digest("hex").slice(0, 10);
  return `${basename.replace(/[^a-zA-Z0-9_.-]/g, "_").replace(/\.woff2$/i, "")}-${hash}.woff2`;
}

async function ensureFontsPresent() {
  try {
    await stat(fontsCssPath);
  } catch {
    throw new Error("assets/stitch-fonts.css is missing. Run npm run build:stitch-assets -- --refresh-fonts once.");
  }
}

await mkdir(assetsDir, { recursive: true });
const files = await findCodeFiles(stitchRoot);
if (!files.length) throw new Error("No Stitch code.html files found.");

const htmlByFile = new Map(await Promise.all(files.map(async (file) => [file, await readFile(file, "utf8")])));
const inlineConfigs = [...htmlByFile].map(([file, html]) => extractTailwindConfig(html, file)).filter(Boolean);
const mergedConfig = buildMergedConfig(inlineConfigs, await readCachedConfig());
if (!inlineConfigs.length && !(await readCachedConfig())) {
  throw new Error("No inline Tailwind config found and no cached config exists.");
}

await writeFile(configCachePath, `${JSON.stringify(mergedConfig, null, 2)}\n`, "utf8");

if (refreshFonts) {
  await downloadFontCss();
} else {
  await ensureFontsPresent();
}

await rewriteStitchHtml(files);
await buildTailwindCss(files, mergedConfig);

console.log(`Built ${relative(root, tailwindCssPath)} for ${files.length} Stitch screen(s) in ${stitchRootName}.`);

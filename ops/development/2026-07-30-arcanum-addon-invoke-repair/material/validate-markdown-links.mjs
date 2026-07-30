import fs from "node:fs";
import path from "node:path";

const root = process.argv[2];
const files = process.argv.slice(3);
if (!root || files.length === 0) {
  throw new Error("usage: validate-markdown-links.mjs <root> <file...>");
}

const failures = [];
const linkPattern = /(?<!!)\[[^\]]*]\(([^)]+)\)/g;

for (const relativeFile of files) {
  const absoluteFile = path.resolve(root, relativeFile);
  const markdown = fs.readFileSync(absoluteFile, "utf8");
  for (const match of markdown.matchAll(linkPattern)) {
    let ref = match[1].trim();
    if (ref.startsWith("<") && ref.endsWith(">")) {
      ref = ref.slice(1, -1);
    }
    if (
      !ref ||
      ref.startsWith("#") ||
      /^[a-z][a-z0-9+.-]*:/i.test(ref)
    ) {
      continue;
    }
    const targetRef = decodeURIComponent(ref.split("#", 1)[0]);
    const target = path.resolve(path.dirname(absoluteFile), targetRef);
    if (!fs.existsSync(target)) {
      failures.push(`${relativeFile}: missing local target ${ref}`);
    }
  }
}

if (failures.length) {
  for (const failure of failures) {
    process.stderr.write(`FAIL: ${failure}\n`);
  }
  process.exit(1);
}

process.stdout.write(`PASS: local Markdown targets in ${files.length} changed files\n`);

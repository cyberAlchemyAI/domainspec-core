import assert from "node:assert/strict"
import { createHash } from "node:crypto"
import { execFileSync } from "node:child_process"
import { readFile, readdir } from "node:fs/promises"
import test from "node:test"
import { dirname, join, resolve } from "node:path"
import { fileURLToPath } from "node:url"

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../../../../")
const PACKAGE = resolve(ROOT, "projects/body-war/ontology/whole-system")
const FRONTEND = resolve(PACKAGE, "frontend")
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex")

async function treeDigest(root) {
  const rows = []
  async function walk(directory) {
    for (const entry of (await readdir(directory, { withFileTypes: true })).sort((left, right) => left.name.localeCompare(right.name))) {
      const path = join(directory, entry.name)
      if (entry.isDirectory()) await walk(path)
      else {
        const bytes = await readFile(path)
        rows.push(`${sha(bytes)} ${bytes.length} ${path.slice(root.length + 1)}`)
      }
    }
  }
  await walk(root)
  return sha(`${rows.join("\n")}\n`)
}

test("whole-system OEW projection is deterministic and strictly valid", async () => {
  const before = await treeDigest(FRONTEND)
  execFileSync(process.execPath, [resolve(PACKAGE, "scripts/generate-oew-frontend.mjs")], { cwd: ROOT, stdio: "pipe" })
  const after = await treeDigest(FRONTEND)
  assert.equal(after, before)
  const output = execFileSync(process.execPath, [resolve(PACKAGE, "scripts/validate-oew-frontend.mjs")], { cwd: ROOT, encoding: "utf8" })
  assert.match(output, /^PASS:/)
})

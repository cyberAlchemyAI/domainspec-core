import assert from "node:assert/strict"
import { createHash } from "node:crypto"
import { execFileSync } from "node:child_process"
import { readdir, readFile } from "node:fs/promises"
import test from "node:test"
import { dirname, resolve } from "node:path"
import { fileURLToPath } from "node:url"

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../../../../")
const PACKAGE_ROOT = resolve(ROOT, "projects/body-war/ontology/whole-system")
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex")

async function generatedTreeDigest() {
  const roots = ["profile.json", "source-universe.json", "residue.json", "architecture-map.json", "NODE-INDEX.md", "nodes", "relations", "views", "context"]
  const files = []
  async function walk(path) {
    const entries = await readdir(resolve(PACKAGE_ROOT, path), { withFileTypes: true })
    for (const entry of entries) {
      const child = `${path}/${entry.name}`
      if (entry.isDirectory()) await walk(child)
      else files.push(child)
    }
  }
  for (const root of roots) {
    if (root.includes(".")) files.push(root)
    else await walk(root)
  }
  files.sort()
  let joined = ""
  for (const path of files) joined += `${digest(await readFile(resolve(PACKAGE_ROOT, path)))}  ${path}\n`
  return digest(joined)
}

test("generation is deterministic and validation passes", async () => {
  const before = await generatedTreeDigest()
  execFileSync(process.execPath, [resolve(PACKAGE_ROOT, "scripts/generate.mjs")], { cwd: ROOT, stdio: "pipe" })
  const after = await generatedTreeDigest()
  assert.equal(after, before)
  const output = execFileSync(process.execPath, [resolve(PACKAGE_ROOT, "scripts/validate.mjs")], { cwd: ROOT, encoding: "utf8" })
  assert.match(output, /^PASS:/)
})

test("existing business ontology remains independently valid", () => {
  const output = execFileSync("env", ["-u", "NODE_TEST_CONTEXT", process.execPath, "--test", resolve(ROOT, "projects/body-war/ontology/business/tests/business-ontology.test.mjs")], { cwd: ROOT, encoding: "utf8" })
  assert.match(output, /pass [1-9]/i)
  assert.match(output, /fail 0/i)
})

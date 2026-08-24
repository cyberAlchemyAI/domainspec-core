#!/usr/bin/env node
import { createServer } from "node:http"
import { readFile, realpath, stat } from "node:fs/promises"
import { extname, relative, resolve, sep } from "node:path"

const root = await realpath(new URL("../frontend/", import.meta.url).pathname)
const host = "127.0.0.1"
const requestedPort = Number.parseInt(process.env.BODY_WAR_OEW_PORT ?? "4178", 10)
const mime = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".ico": "image/x-icon",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml; charset=utf-8",
}

function contained(path) {
  const logical = relative(root, path)
  return logical === "" || (logical !== ".." && !logical.startsWith(`..${sep}`))
}

const server = createServer(async (request, response) => {
  try {
    if (!request.url || !["GET", "HEAD"].includes(request.method ?? "")) {
      response.writeHead(405, { Allow: "GET, HEAD" }).end()
      return
    }
    const url = new URL(request.url, `http://${host}`)
    const requested = decodeURIComponent(url.pathname)
    const logical = requested === "/" ? "index.html" : requested.replace(/^\/+/, "")
    const lexical = resolve(root, logical)
    if (!contained(lexical)) {
      response.writeHead(403).end()
      return
    }
    const path = await realpath(lexical)
    if (!contained(path) || !(await stat(path)).isFile()) {
      response.writeHead(404).end()
      return
    }
    const bytes = await readFile(path)
    response.writeHead(200, {
      "Cache-Control": "no-store",
      "Content-Length": bytes.length,
      "Content-Security-Policy": "default-src 'self'; connect-src 'self'; font-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; worker-src 'self' blob:; script-src 'self'; object-src 'none'",
      "Content-Type": mime[extname(path)] ?? "application/octet-stream",
      "X-Content-Type-Options": "nosniff",
    })
    response.end(request.method === "HEAD" ? undefined : bytes)
  } catch {
    response.writeHead(404).end()
  }
})

server.listen(requestedPort, host, () => {
  const address = server.address()
  process.stdout.write(`Body War OEW frontend: http://${host}:${address.port}/?oew=1\n`)
})

for (const signal of ["SIGINT", "SIGTERM"]) process.on(signal, () => server.close(() => process.exit(0)))

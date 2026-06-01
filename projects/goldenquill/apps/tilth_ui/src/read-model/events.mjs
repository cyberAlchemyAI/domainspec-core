import { mkdir, readFile, appendFile } from "node:fs/promises";
import { dirname } from "node:path";
import { createHash } from "node:crypto";

export function stableJson(value) {
  if (Array.isArray(value)) return `[${value.map(stableJson).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableJson(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

export function sha256Json(value) {
  return `sha256-${createHash("sha256").update(stableJson(value)).digest("hex")}`;
}

export async function readJsonl(filePath) {
  if (!filePath) return [];
  try {
    const text = await readFile(filePath, "utf8");
    return text
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => JSON.parse(line));
  } catch (err) {
    if (err && err.code === "ENOENT") return [];
    throw err;
  }
}

export async function appendJsonl(filePath, event) {
  await mkdir(dirname(filePath), { recursive: true });
  await appendFile(filePath, `${JSON.stringify(event)}\n`, "utf8");
}

export function eventAuditRow(event) {
  return {
    event_id: event.event_id,
    event_type: event.event_type.toUpperCase().replace(/\./g, "_"),
    actor: event.actor || "LOCAL_COMMAND_HANDLER",
    timestamp: event.timestamp,
    artifact_hash: event.artifact_hash || sha256Json(event.payload || {}),
    signature_status: event.signature_status || "VERIFIED",
    posture: event.posture || event.payload?.posture || "SPLIT_CONTEXT_HYBRID",
    rationale: event.payload?.rationale || event.payload?.reason || event.event_type,
  };
}

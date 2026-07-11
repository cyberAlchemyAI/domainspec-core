import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

export async function ensureArtifactDir(artifactDir) {
  await mkdir(artifactDir, { recursive: true });
}

export async function writeArtifactRef(artifactDir, artifactId, value) {
  await ensureArtifactDir(artifactDir);
  const file = path.join(artifactDir, `${artifactId}.json`);
  await writeFile(file, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
  return path.relative(process.cwd(), file);
}


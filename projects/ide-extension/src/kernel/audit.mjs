import { appendFile, mkdir, readFile } from 'node:fs/promises';
import path from 'node:path';

export async function appendEvent(eventsFile, event) {
  await mkdir(path.dirname(eventsFile), { recursive: true });
  await appendFile(eventsFile, `${JSON.stringify(event)}\n`, 'utf8');
}

export async function readEvents(eventsFile) {
  try {
    const raw = await readFile(eventsFile, 'utf8');
    return raw
      .split('\n')
      .filter((line) => line.trim() !== '')
      .map((line) => JSON.parse(line));
  } catch (error) {
    if (error.code === 'ENOENT') return [];
    throw error;
  }
}


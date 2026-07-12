import { mkdir, open, readFile } from 'node:fs/promises';
import path from 'node:path';

export async function appendEvent(eventsFile, event) {
  await mkdir(path.dirname(eventsFile), { recursive: true });
  const handle = await open(eventsFile, 'a');
  try {
    await handle.writeFile(`${JSON.stringify(event)}\n`, 'utf8');
    await handle.sync();
  } finally {
    await handle.close();
  }
}

export async function readEvents(eventsFile) {
  try {
    const raw = await readFile(eventsFile, 'utf8');
    if (raw === '') return [];
    if (!raw.endsWith('\n')) {
      const error = new Error('authoritative event history has a truncated final line');
      error.code = 'invalid_event_history';
      error.reason = 'truncated_final_line';
      throw error;
    }

    return raw.slice(0, -1).split('\n').map((line, index) => {
      if (line.trim() === '') {
        const error = new Error(`authoritative event history has a blank line at ${index + 1}`);
        error.code = 'invalid_event_history';
        error.reason = 'blank_line';
        error.line_number = index + 1;
        throw error;
      }

      try {
        return JSON.parse(line);
      } catch {
        const error = new Error(`authoritative event history has invalid JSON at line ${index + 1}`);
        error.code = 'invalid_event_history';
        error.reason = 'invalid_json';
        error.line_number = index + 1;
        throw error;
      }
    });
  } catch (error) {
    if (error.code === 'ENOENT') return [];
    throw error;
  }
}

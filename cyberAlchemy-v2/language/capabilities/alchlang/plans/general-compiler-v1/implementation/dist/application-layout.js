import { mkdirSync, renameSync, readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { digest } from './domainspec-profile.js';
export function writeApplicationFile(root, name, bytes) {
    if (path.isAbsolute(name) || name.includes('\\') || name.split('/').some(p => !p || p === '.' || p === '..'))
        throw Error('APPLICATION_OUTPUT_PATH');
    const target = path.join(root, name);
    mkdirSync(path.dirname(target), { recursive: true });
    writeFileSync(target, bytes, { flag: 'wx' });
}
/** Move compiler output once; retain exact inputs and compiler evidence, not stale inventories. */
export function collectApplicationDomain(intermediate, root, paths) {
    const moved = {};
    const move = (from, to) => { const target = path.join(root, to); mkdirSync(path.dirname(target), { recursive: true }); if (existsSync(target))
        throw Error('APPLICATION_OUTPUT_COLLISION:' + to); renameSync(path.join(intermediate, from), target); moved[from] = to; };
    const generated = (from, to) => { for (const entry of readdirSync(path.join(intermediate, from), { withFileTypes: true })) {
        const next = to ? to + '/' + entry.name : entry.name;
        if (entry.isDirectory())
            generated(from + '/' + entry.name, next);
        else
            move(from + '/' + entry.name, next);
    } };
    generated('generated', '');
    if (existsSync(path.join(intermediate, 'domain.ts')))
        move('domain.ts', paths.apiSource);
    move('project', 'provenance/lowering/project');
    for (const name of ['source.alch', 'bindings.json'])
        move(name, 'provenance/lowering/' + name);
    for (const name of ['certificate.json', 'compiler-files.json', 'trace.json'])
        move(name, 'evidence/lowering/' + name);
    // The original manifest describes staging paths; the final application manifest owns final paths.
    writeApplicationFile(root, 'evidence/lowering/projection.json', JSON.stringify({
        schema_version: 'alchlang.application-projection/v1',
        input_manifest_sha256: digest(readFileSync(path.join(intermediate, 'manifest.json'))),
        moved, authority_effect: 'none'
    }, null, 2) + '\n');
}

import { assertRecord } from './validation.js';
import { normalizeRequest, ApplicationDomainError } from './normalization.js';
const contracts = {
    "CreateTrack": {
        "record": "CreateTrackRequest",
        "maxbytes": 16384,
        "error": "invalid_suggested_track"
    },
    "AttachEvidence": {
        "record": "AttachEvidenceRequest",
        "maxbytes": 16384,
        "error": "invalid_evidence_request"
    }
};
export class ApplicationRequestError extends Error {
    code;
    status;
    constructor(code, status) {
        super(code);
        this.code = code;
        this.status = status;
    }
}
const cache = new WeakMap();
export function readRequest(request, operation) { const prior = cache.get(request); if (prior) {
    if (prior.operation !== operation)
        throw Error('REQUEST_BINDING_MISMATCH');
    return prior.value;
} const c = contracts[operation]; if (!c)
    throw Error('UNKNOWN_REQUEST_CONTRACT'); const value = new Promise((resolve, reject) => { const chunks = []; let size = 0, overflow = false; request.on('data', (chunk) => { size += chunk.length; if (size > c.maxbytes) {
    if (!overflow) {
        overflow = true;
        chunks.length = 0;
        reject(new ApplicationRequestError('request_too_large', 413));
    }
    return;
} chunks.push(Buffer.from(chunk)); }); request.once('aborted', () => reject(new ApplicationRequestError(c.error, 400))); request.once('error', () => reject(new ApplicationRequestError(c.error, 400))); request.once('end', () => { if (overflow)
    return; try {
    const text = Buffer.concat(chunks).toString('utf8');
    const parsed = text ? JSON.parse(text) : {};
    assertRecord(c.record, parsed);
    resolve(normalizeRequest(operation, parsed));
}
catch (error) {
    reject(new ApplicationRequestError(error instanceof ApplicationDomainError ? error.code : c.error, 400));
} }); }); cache.set(request, { operation, value }); return value; }
//# sourceMappingURL=request.js.map
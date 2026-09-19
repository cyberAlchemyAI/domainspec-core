// Generated typed input normalization; no IO or arbitrary expressions.
const contracts = {
    "CreateTrack": {
        "fields": {
            "name": {
                "kind": "text",
                "min": 1,
                "max": 255
            },
            "place_label": {
                "kind": "text",
                "min": 1,
                "max": 255
            },
            "city": {
                "kind": "text",
                "min": 1,
                "max": 120
            },
            "public_note": {
                "kind": "text",
                "min": 0,
                "max": 500
            },
            "distance_hint_meters": {
                "kind": "positive-integer"
            }
        },
        "error": "invalid_suggested_track"
    },
    "AttachEvidence": {
        "fields": {
            "activity_id": {
                "kind": "text",
                "min": 0,
                "max": 255
            },
            "consent_text": {
                "kind": "text",
                "min": 0,
                "max": 500
            }
        },
        "error": "invalid_evidence_request"
    }
};
export class ApplicationDomainError extends Error {
    code;
    constructor(code) {
        super(code);
        this.code = code;
    }
}
export function normalizeRequest(operation, input) { const contract = contracts[operation]; if (!contract)
    return input; const result = { ...input }; for (const [field, rule] of Object.entries(contract.fields)) {
    const value = input[field];
    if (rule.kind === 'text') {
        const text = (typeof value === 'string' ? value : '');
        if (text.length < rule.min)
            throw new ApplicationDomainError(contract.error);
        result[field] = text;
    }
    else {
        if (value === undefined || value === null)
            result[field] = null;
        else if (typeof value === 'number' && Number.isInteger(value) && value > 0)
            result[field] = value;
        else
            throw new ApplicationDomainError(contract.error);
    }
} return result; }
//# sourceMappingURL=normalization.js.map
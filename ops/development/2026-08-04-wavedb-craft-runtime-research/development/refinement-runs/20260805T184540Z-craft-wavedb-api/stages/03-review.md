# Stage 03 — Interrogation Refine Review

## Review question

Does the definition promise useful consultation without smuggling in source
authority, row semantics, privacy disclosure, refresh effects, or durability
claims that the evidence does not support?

## Critique

1. `Space` must not be derived from a path and then exposed as though it were a
   stable global identity. Use an opaque snapshot-local identifier; provenance
   may carry a path only after authorization.
2. Exact raw retrieval is useful and proven, but a general row/query API is not
   yet proven. Row routes must be capability-advertised per space, not globally
   implied by `/v1`.
3. Freshness cannot be computed from import time alone. Without authorized live
   source stat/hash comparison, the only honest value is `unknown`.
4. A collection endpoint can leak private project existence even without raw
   content. Authorization must filter before enumeration and before not-found
   versus forbidden differentiation.
5. The snapshot manifest and individual records must be mutually bound. A store
   that reopens without its manifest is unavailable, not partially serviceable.
6. The failed atomic batch and mixed return types are contract constraints, not
   incidental diagnostic details.
7. `0.1` compatibility is an intent, not local proof. It must remain
   `unsupported` until an exact fixture and adapter exist.

## Parent synthesis

- Adopt opaque `space_id` and per-space capability discovery.
- Define freshness as a three-state comparison result; default to `unknown`.
- Return a uniform concealment-safe `404` for unauthorized/unavailable spaces
  at the external boundary; log internal reason without revealing it.
- Require manifest presence and record digest closure before `ready=true`.
- Keep raw-snapshot retrieval as L0; normalized rows/search are later layers.
- Mark `0.1` planned-but-unproven, not supported.

## Verdict

`pass-with-flags`. No authority or privacy contradiction remains in the revised
direction. The seven findings are mandatory inputs to Distill and Design.

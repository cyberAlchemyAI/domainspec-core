# Mappings

## Host evidence to neutral capacity record

| Host input | Neutral field | Rule |
| --- | --- | --- |
| authoritative scope identifier | `capacity_scope_id` | preserve exact opaque identity |
| authoritative current limit and occupancy | `spawnable_units` | calculate only under host-declared semantics |
| inventory status | occupancy categories | preserve observed status; do not infer limit or release |
| reservation receipt | `reservation_ref` | require exact run/wave/units/expiry binding |
| unsupported field | `authority: unknown` plus residue | never fill from history or error text |
| private diagnostic | opaque diagnostic handle | do not publish raw provider/account detail |

## Admission decision to consumer route projection

| Decision | Neutral consumer message | Authority effect |
| --- | --- | --- |
| admitted | The complete approved wave is ready under the named evidence policy. | none; execution remains separate |
| blocked-missing/stale | Capacity needs a current host check before starting. | none |
| blocked-insufficient | The approved wave does not fit current authoritative capacity. | none |
| blocked-unknown | The host cannot safely prove that this wave fits. | none |
| blocked-unreserved | A snapshot exists, but the host cannot guarantee all slots for the wave. | none |

Consumer labels may be plain language, but must preserve the exact verdict and
must not expose provider-private numbers unless the provider permits it.

## Spawn error to failure receipt

- Recognized host capacity error strings may set a safe cause class such as
  `capacity_exhausted`, but cannot establish the numeric limit or release rule.
- Unknown errors map to `host_spawn_failed_unknown`.
- Both branches keep `agent_id: null`, block dependents, and retain an opaque
  diagnostic handle.


# Local Glossary

Status: linked-local candidate vocabulary. These terms explain this package and
do not modify canonical Arcanum definitions.

| Term | Beginner explanation | Precise contract | Not the same as |
| --- | --- | --- | --- |
| capacity evidence | A dated note from the host saying what it can accept now. | Immutable record scoped to host, session/tree, run, wave, and observation time, with exact/advisory/unknown authority. | agent inventory, a guessed limit, or an old successful run |
| whole-wave admission | Check that the complete approved group fits before starting anyone. | Deterministic all-or-zero decision over requested units and current capacity evidence. | spawning until one call fails |
| requested width | How many fresh native workers this wave asks for. | Count of coordinator-emitted spawn actions before host execution. | number of roles only |
| retained thread | A finished thread still present in host inventory. | Terminal logical agent whose physical-capacity effect is host-defined and unproved. | released slot or reusable clean context |
| logical close | Orchestrate has finished tracking the agent result. | One terminal lifecycle event in the run evidence. | physical host release |
| physical release | The host proves the slot no longer consumes the relevant capacity scope. | Host-owned observation or release receipt. | `agent_closed` |
| reservation | The host atomically holds enough slots for the whole wave. | Lease bound to host, scope, run, wave, units, expiry, and consume/release rules. | a capacity snapshot |
| topology revision | A proposed change from parallel to smaller, serial, inline, queued, or fresh-session execution. | New route bytes requiring revalidation and, when material, renewed user approval. | automatic fallback |
| pre-agent failure receipt | An honest record that a spawn action failed before an agent existed. | Block receipt with `agent_id: null`, host failure cause class, residue, and reroute. | a timed-out or completed agent receipt |

## Glossary linking

- `Dispatch`, `Run`, `Gate`, and `Receipt` link to existing Arcanum vocabulary.
- Capacity-specific terms are local candidates because no canonical definition
  change is required to plan the runtime contract.
- Link status: partial. The existing lifecycle terms are linked; the new host
  scheduling terms remain package-local until a Definitions Governance owner
  explicitly accepts a broader need.


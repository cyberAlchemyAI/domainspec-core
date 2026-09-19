Archive migration and legacy API contracts are removed from the active application.
Current removal decisions are in ../REMOVAL-PLAN.md.

# Candidate pilot definitions

Source: [original project decisions](../../body-war/docs/PROJECT-DECISIONS.md),
[current suggested-track specification](../../body-war/docs/features/parque-taquaral-online-mvp/SPEC.md),
and [current pilot adapters](../provenance/imports.json). User scope: existing pilot first.

- **Runner**: the principal linked through the Strava adapter, with a safe profile.
- **Suggested track**: a route suggestion awaiting evidence; it is not verified geometry.
- **Activity evidence candidate**: the runner's consented, redacted activity summary.
- **Explicit consent**: boolean acknowledgement and nonempty consent text accompanying
  an activity identifier. These are necessary application inputs, not proof of legal consent.
- **Evidence request**: the typed facts consumed by the compiled consent predicate.
- **Pilot readiness**: a separate operational/product decision; a submitted activity
  does not establish source-backed geometry, verified score or territory control.

The complete pilot composition is authored in the root application, eight imported application modules and the consent submodel. The consent submodel retains DomainSpec's typed entity/rule
semantics. Other declarations use the candidate DomainSpec application ontology profile:
AlchLang syntax lowering, shared checked composition, generated consumers and
source-bound external adapters.
Adapter effects are declared behavior, not formal verification of adapter code.

Request contracts bind an operation's declared input record, maximum JSON body
size and rejection code to a generated parser. Critical requirements bind an
exact authored requirement to one retained integration case; they do not imply
formal or production qualification.

Normalization declarations bind typed input fields to a closed set of rules:
text is trimmed and truncated by UTF-16 code units, then checked for minimum
length; optional positive integers default to null. The pilot retains its existing
bounds and consent predicate. No arbitrary expressions or provider effects run
inside normalization. Public track/evidence and import receipt records are closed
recursively; identity views also use closed named records. Private persistence
metadata retains its explicitly declared open content.

Activity queries declare numeric conversion, integer bounds and absent-value
defaults. Duplicate and unknown query parameters are rejected. The provider
adapter independently limits direct callers. Scalar unions preserve numeric or
string identifiers. Archive migration contracts are removed. The provider adapter
retains generic bounded detail retrieval, while ordinary evidence submission
selects an activity from the connected runner’s summaries.

## Open Questions

Owned by [README](../README.md#open-questions).

## Runner withdrawal

Withdrawal deletes the owner's candidate row, including stored redacted summary and
consent. It resets a track only when its last evidence disappears. Foreign and absent
IDs return the same success response without modifying another runner's data. A valid
app session suffices; provider connection is not required. Re-submission is a new
consented candidate, not restoration of the deleted row. Backup erasure is not implied.

Open questions for recorded data and route matching remain in ../NEXT-STEPS.md.

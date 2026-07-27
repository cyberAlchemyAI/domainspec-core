# Glossary

These terms are local explanatory vocabulary for this Invoke run. They do not
promote new Arcanum or DomainSpec definitions.

| Term | Meaning |
| --- | --- |
| Governed workbench | The local browser surface that projects Studio state and routes reversible operator actions through application gates. |
| Stable shell | A page document whose identity and local interaction state survive unchanged polls and keyed projection updates. |
| Canonical update identity | Opaque server-computed value representing the exact governed projection version relevant to the workbench. |
| Unchanged poll | A `/state` observation whose canonical update identity equals the shell’s current identity. |
| Intended update | The single selected UI update caused by one genuine governed-state transition; main-document and child-frame navigation are counted separately. |
| Local task context | Browser-local target selection, drafts, focus, scroll, open inspector, and current task orientation. |
| Explicit invalidation | A visible, reasoned reset of local task context because its bound server identity became stale. |
| Lifecycle spine | Persistent state, progress, current identity, and next-valid-action context. |
| Active canvas | The primary current-head preview that is also the subject of annotation or review. |
| Contextual inspector | State-specific annotation, batch, review, or revision controls adjacent to the active canvas. |
| Staged review | Before/After/Diff evidence plus candidate identity, target state, acknowledgment, Accept, and Discard. |
| Historical lineage | Original variants and prior revisions retained as secondary, explicitly non-current reference evidence. |
| Bounded live region | An announced feedback node tied to one named event scope and calibrated with positive and negative fixtures. |
| Acceptance obligation | A future implementation evidence requirement; not a present-interface UX outcome classification. |
| Human-study residue | Comprehension, confidence, trust/safety, workload, delight, and real-task success that automated evidence cannot establish. |

## Consistency Rules

- “Stable” means zero unchanged navigation plus preserved named context.
- “Update” never silently means whole-document reload.
- “Current” names the application-owned head, never a historical variant.
- “Staged” never implies accepted, current, approved for release, or ready.
- “Acknowledged” does not imply actor identity or external authorization.
- “Accessible” is not claimed from a bounded set of frame, status, contrast,
  target-size, keyboard, or viewport checks.
- “Ready” must name its exact predicate and owner.


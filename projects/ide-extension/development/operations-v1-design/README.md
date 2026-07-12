# Operations V1 Design

Invoke design package for evolving the session content workbench from
complete-file V0 publication into a separate incremental HTML construction
surface.

The design preserves `/api/canvas/publish` and every existing V0 surface. A
selected V0 revision may be copied into a new `operations_v1` surface whose
immutable revision bodies are owned by the local kernel.

Start with:

- [Architecture bundle](ARCHITECTURE-BUNDLE.md)
- [Decision ledger](DECISIONS.md)
- [UX plan](UX-PLAN.md)
- [Distill validation](DISTILL-VALIDATION.md)
- [Invoke result](INVOKE-RESULT.md)

This package is design authority only. It does not implement routes, schemas,
storage, parsing, navigation, or browser behavior.

# Traceability

| Source obligation | Design control | SWU evidence |
|---|---|---|
| Exact 237-word whole request | FrozenExcerpt + ManifestToSpeechRequest | 001, 002, 003 |
| No render while `not_ready` | State/admission enforcement before credential/network | 002 negative fixtures; 003 live gate |
| One exact stock voice and two repetitions | Manifest identity + attempt join | 003, 004 |
| No unsupported controls or pronunciation repair | Request allowlist + Body War rejection | 002, 006 |
| Immutable raw bytes and metadata | Append-only run store | 004 |
| Separate alignment and fidelity | Verification architecture | 005, 006 |
| Blind fixed rubric and three listeners | UX plan | 007 |
| Scores do not decide | Authority split | 008 |
| AI-voice disclosure | Provider contract and production handoff gate | 008 |
| No production claim | L3 boundary and separate next route | 008 closeout |

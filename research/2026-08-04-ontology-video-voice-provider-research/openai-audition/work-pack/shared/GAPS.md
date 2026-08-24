# Cross-task Gaps

| Gap | Earliest affected SWU | Owner route | Fail behavior |
|---|---|---|---|
| Accent/locale unset | 003 | audition owner decision | Keep `not_ready`. |
| Exact stock voice unset | 003 | audition owner decision after official demos | Keep `not_ready`. |
| Named production operator absent | 003 | video owner decision | Keep `not_ready`. |
| Actual-account legal/data gates open | 003 | account/legal/data owners | Keep `not_ready`; no upload. |
| Exact token count/provider availability unverified | 003 | provider interface preflight | Keep `not_ready`. |
| Audio/align/fidelity tools absent | 005 | verification tool decision and authorized setup | Stop after raw evidence. |
| Listener operations unset | 007 | production operator | Stop after verification. |

No gap may be converted into a default by an implementation worker.

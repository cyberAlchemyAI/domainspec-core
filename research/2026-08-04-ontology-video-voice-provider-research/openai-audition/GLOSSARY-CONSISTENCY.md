# Glossary Consistency Review

Verdict: pass.

| Check | Result |
|---|---|
| `admission` versus provider availability | Separate throughout SPEC, state, interface, and source contracts. |
| `raw response` versus derivative | Separate in operations, mappings, persistence, and data lifecycle. |
| technical validity versus fidelity versus voice fit | Separate verdicts and owners. |
| score versus terminal decision | Scores are advisory; production operator remains owner. |
| audition approval versus release | Release and full narration remain outside the module. |
| unsupported control versus default | Unsupported fields are omitted; no generic defaults invented. |
| receipt versus authority | Receipts evidence one transition and cannot authorize successors. |

No synonym in the authored package changes the controlled meanings in [GLOSSARY.md](GLOSSARY.md).

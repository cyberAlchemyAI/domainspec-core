# Traceability

| Design requirement | Repair | SWUs | Scenarios |
| --- | --- | --- | --- |
| Stable acceptance gate | final-review validator finding | 000 | repeated ontology validation |
| Closed model-visible query | H1, H6 | 001, 007 | QS-07, QS-08, QS-14 |
| Status-tagged response and precedence | H2, H5 | 002, 005 | QS-03-QS-10 |
| Atomic provenance and freshness | H3, H9 | 002-004 | QS-01, QS-04-QS-06 |
| Relevance/confidence separation | H4 | 002, 006 | QS-13 |
| Early caps and cancellation | H7 | 005, 013 | QS-09, QS-10 |
| Cache isolation | H8 | 010 | QS-12 |
| Untrusted evidence | H10 | 008, 011 | QS-11 |
| Answering-agent ownership | H5 | 008-009 | QS-02-QS-06 |
| No writes or protected capabilities | boundary | 001-012 | QS-14 |

Recomposition path:

```text
000 deterministic ontology validation
  -> 001-002 contracts
  -> 003-004 neutral projection
  -> 005-006 fixture service
  -> 007-009 host and answer integration
  -> 010-011 hardening
  -> 012 optional evidence-selected extension
```

The approved one-go frontier terminates after 006. The remaining recomposition
path is planning context only and cannot be selected by that chain.

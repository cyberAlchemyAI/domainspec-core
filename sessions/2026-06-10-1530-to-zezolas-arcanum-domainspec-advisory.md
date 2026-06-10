---
tags: [compliance, anvisa, food-service, external-advisory, multi-agent-dispatch, arcanum, domainspec]
node_type: audit
is_session: true
layer: domain, application
nature: technical, explanatory
status: active
created: 2026-06-10
timestamp: 2026-06-10T15:30:00-03:00
expires: 2026-08-09
conversation_id: to-zezolas-arcanum-domainspec-2026-06-10
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "First documented external application of the Arcanum/DomainSpec advisory methodology (TO-VLAD format on a third-party codebase), producing two-pass audit memos and a distilled refs/ corpus."
---

# TO-ZEZOLAS — Arcanum/DomainSpec advisory on an external food-service SaaS

## Summary

Used parallel subagents to analyze Zezolas's external "nutridev-manager" (Next.js + Supabase ANVISA-compliance ERP) and distill the fundamental ideas of Arcanum and DomainSpec into business-language advisory memos modeled on Arcanum's TO-VLAD format. Produced TO-ZEZOLAS.md (first pass — "arrumação": hidden ANVISA rules, undeclared residue, mocked dashboard, missing forbidden transitions) and TO-ZEZOLAS2.md (second pass — "risco": cross-tenant RLS leak, cosmetic PNG e-signature, zero-tested menu solver returning invalid menus silently, plus an honest revision of pass 1). Added a refs/ folder of distilled mental-model docs (concreto-abstrato, meta-camadas, regra-para-teste, pass-flag-block-e-gate, glossario-do-dominio, estressores-e-residuo). All deliverables committed and pushed to the external Zezolas GitHub repo; the first memo was also committed here (40ced3d).

## Files touched

- TO-ZEZOLAS/README.md
- TO-ZEZOLAS/TO-ZEZOLAS.md
- refs/meta-camadas.md

model.run via gateway
provider: groq
model: openai/gpt-oss-120b
outputs: 1
**PREMISES**  
- **RT‑NEW‑01 (HIGH)** – external side‑effects (ChromaDB, vault, lessons.md writes) were not covered in the original rollback.  
- **RT‑NEW‑02 (MED)** – no detection for silent SDK breaking changes.  
- **RT‑NEW‑03 (MED)** – “LOCK” status ambiguous in queue pre‑conditions.  
- **RT‑NEW‑04 (MED)** – mapping table could drift vocabularly into production code.  
- **RT‑NEW‑05 (LOW)** – sovereignty asserted but never exercised under error states.  
- **RT‑NEW‑06 (MED)** – L‑003 precedent may let a successful Scribe spike legitimize SDK adoption for other seats.  

**Cycle‑2 fixes referenced**:  
- **F‑1** – rollback concreteness (branch isolation, external‑state inventory, transactional sandbox, `spike_rollback.sh` with dry‑run/apply/verify, operator ledger, ≤ 1 h timeline, escalation).  
- **F‑2** – silent SDK change detection (`sdk_contract_check.sh` snapshot + diff + outbound‑HTTP monitor; runs at spike‑open, version bumps, quarterly).  
- **F‑3** – “LOCK landed” mechanical definition (artifact at canonical path, signed ledger entry, SHA‑3‑512 hash match).  
- **F‑4** – L‑003 precedent bounded (each SDK adoption requires its own spike + audit + sign‑off).  
- **F‑5** – vocabulary‑drift lint (`lint_sdk_vocabulary_drift.sh` blocks SDK lifecycle identifiers; exceptions need `# SDK interop:` comment).  
- **F‑6** – sovereignty verification (four forced error states; outbound‑traffic allow‑list limited to Anthropic endpoints; fail on any other destination).  

---

**EXECUTION TRACE (closure assessment & new risks)**  

| Finding | Closure Status | Evidence‑based Reasoning |
|--------|----------------|--------------------------|
| **RT‑NEW‑01 (HIGH)** | **PARTIAL** | F‑1’s *external‑state inventory* lists ChromaDB collections, vault paths, and a “lessons.md non‑write rule”, which directly addresses the cited side‑effects. However, the fix text does **not** prove that every possible external write (e.g., hidden temporary files, OS‑level caches) is captured, nor does it verify that the `spike_rollback.sh` script actually implements the listed steps. Without concrete proof of full coverage, the high‑risk side‑effect remains only partially mitigated. |
| **RT‑NEW‑02 (MED)** | **PARTIAL** | F‑2 introduces `sdk_contract_check.sh` that snapshots the SDK public interface and monitors outbound HTTP. This catches interface‑level breaking changes and network‑level regressions. The fix **does not** address silent logical regressions that leave the interface unchanged (e.g., altered default parameters, internal algorithmic shifts). Hence the detection is incomplete. |
| **RT‑NEW‑03 (MED)** | **CLOSED** | F‑3 defines a deterministic “LOCK landed” state: an artifact at a canonical path, a signed ledger entry, and a SHA‑3‑512 hash match. These three mechanical checks resolve the ambiguity of the prior “LOCK” description and provide a verifiable condition before proceeding. |
| **RT‑NEW‑04 (MED)** | **PARTIAL** | F‑5’s lint rule blocks direct references to SDK lifecycle identifiers in production code and requires an explicit comment for exceptions. The rule’s effectiveness depends on exhaustive pattern matching. The fix text gives no evidence that the lint handles case‑variations, concatenated identifiers, or dynamically generated strings, leaving a window for covert vocabulary drift. |
| **RT‑NEW‑05 (LOW)** | **PARTIAL** | F‑6 forces four error states and validates outbound traffic against an Anthropic‑only allow‑list. While this demonstrates a concrete sovereignty test, the test set is limited. It omits other plausible error conditions (quota exhaustion, streaming interruptions, tool‑loop failures) and does not confirm that non‑HTTP channels (e.g., raw sockets, gRPC) are blocked. Hence sovereignty verification is only partially satisfied. |
| **RT‑NEW‑06 (MED)** | **PARTIAL** | F‑4 states that each seat must run its own spike, audit, and sign‑off. The wording is an *expectation*; there is no fail‑closed enforcement mechanism or automated gate that would prevent a seat from implicitly reusing the Scribe spike precedent. Without a hard enforcement rule, the precedent risk remains. |

**New weaknesses introduced by the fixes**  
1. **Rollback‑script attack surface** – Introducing `spike_rollback.sh` and a JSONL ledger creates a new code path that, if compromised, could trigger unauthorized rollbacks or hide malicious state changes. The fix text does not specify integrity‑verification (e.g., signature checks) for the script itself.  
2. **Sandbox scope ambiguity** – The “transactional sandbox” at `spike‑scratch/<id>/` is claimed to hold pre/post snapshots, yet the description does not confirm that *all* external writes (including indirect writes via libraries or OS‑level temp files) are redirected, leaving a potential leakage path.  
3. **Escalation path unspecified** – F‑1 mentions an “escalation path” but provides no concrete mechanism (e.g., alerting, automatic abort) and thus could be a dead‑end during a failed rollback.  
4. **Lint‑exception abuse** – Allowing comments `# SDK interop:` to bypass the lint opens a social engineering vector; a malicious contributor could insert the comment without genuine justification.  
5. **Outbound‑HTTP monitor bypass** – F‑2 monitors outbound HTTP only. An SDK could switch to HTTPS with custom certificates, raw TCP, or IPC mechanisms, evading detection.  

---

**CONCLUSION**  
- **Findings still open:** 1 HIGH (partial), 4 MED (partial), 1 LOW (partial).  
- **Blocking:** **true** – the unresolved HIGH‑severity side‑effect (RT‑NEW‑01) leaves a material risk that could compromise rollback safety.  
- **Verdict:** **REQUIRES_MINOR_FIXES** – additional evidence and hardening are needed to fully close the high‑severity issue and to eliminate the residual MED‑level gaps.

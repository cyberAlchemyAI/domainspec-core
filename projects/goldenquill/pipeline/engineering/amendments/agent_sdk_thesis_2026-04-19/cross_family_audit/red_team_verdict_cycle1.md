model.run via gateway
provider: groq
model: openai/gpt-oss-120b
outputs: 1
PREMISES:
P1: EN-001 states “Rollback: Dedicated branch. No state in SDK-only format. Baseline preserved verbatim. Abandonment = branch revert + zero-state migration.”
P2: EN-001 lists spike measures including “zero cross‑org file access (Cedar‑enforced).”
P3: EN-001 declares “Controlled dependency: SDK version pinned at spike‑open. Quarterly audit. Exit criterion: breaking change → halt and re‑scope.”
P4: EN-001 notes the spike is “Queued behind §6 Operating Envelope blueprint LOCK, §4 Logician v2.2 LOCK, §0.5 v4 refresh, real‑engineer validator gate per Da Vinci §13.”
P5: EN-002 creates a “SDK Lifecycle Vocabulary Reference Table” that maps ten SDK event names to Tilth lifecycle moments and is “not a substitution.”
P6: EN-001 claims “sovereignty preserved (BYOK, no phone‑home, all data local).”

EXECUTION TRACE:
- Finding RT‑NEW‑01 [HIGH]: The rollback claim (P1) assumes no external side‑effects, yet the amendment never addresses writes to mutable external stores (e.g., ChromaDB, the vault, lessons.md). If the spike writes any of these, a branch revert will not undo those changes. Mitigation: enumerate all external resources the spike may touch and require a transactional sandbox or explicit cleanup script.
- Finding RT‑NEW‑02 [MED]: The “controlled dependency” clause (P3) names a quarterly audit and an exit criterion but provides no concrete detection mechanism for silent SDK breaking changes (e.g., hidden telemetry activation, API signature removal). Mitigation: implement an automated integration test that validates the SDK’s public interface and monitors outbound network traffic on each audit.
- Finding RT‑NEW‑03 [MED]: The queue positioning (P4) references “LOCK” statuses without defining what constitutes a “landed” lock (e.g., is a merged PR sufficient, or must CI pass?). This ambiguity could allow the spike to start before all preconditions are truly satisfied. Mitigation: require explicit lock‑status flags in a shared state file that must be set to `complete` before the spike is triggered.
- Finding RT‑NEW‑04 [MED]: EN‑002’s mapping table (P5) introduces a shared taxonomy. Future contributors might import the table and begin using SDK event names directly in Tilth code, silently merging the vocabularies and causing drift. The amendment does not enforce a policy preventing such reuse. Mitigation: add a lint rule that forbids referencing SDK lifecycle identifiers in production code and require a review checkpoint before any code adopts them.
- Finding RT‑NEW‑05 [LOW]: Sovereignty preservation (P6) relies on “no phone‑home,” but the amendment does not verify the SDK’s default error‑reporting or diagnostic telemetry settings, which could transmit data under certain error conditions. Mitigation: include a test that forces an SDK error and inspects outbound traffic to confirm no external calls are made.
- Finding RT‑NEW‑06 [MED]: The spike focuses exclusively on the Anthropic‑family Scribe seat. While the amendment notes “no LiteLLM translation required,” it does not address the broader cross‑family rigor rule (L‑003) that future SDK adoptions for other seats could violate the rule that Judge must not share the provider family with Scribe. Mitigation: codify a policy that any future SDK adoption for a non‑Anthropic seat must include a cross‑family compatibility check and explicit approval.

CONCLUSION:
- Findings count: HIGH 1, MED 4, LOW 1
- Verdict: REQUIRES_MINOR_FIXES

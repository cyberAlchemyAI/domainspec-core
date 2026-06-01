---
title: Blueprint §13 Data Collector — multi-channel grantee + sub-awardee outreach (v1 SCOPING DRAFT)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 (v1 — L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor per WS-D v7.0.5 + WS-E §11 + WS-F §12 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 precedents — Editor=Llama-3.3-70B/Groq READY_TO_LOCK + Judge=Gemini-2.5-Pro/Google READY_TO_LOCK 100/100 + Red Team=GPT-OSS-120B/Groq PASS blocking:false). **Cycle 1 outcomes:** Editor READY_TO_LOCK (8 findings — 1 HIGH + 2 MED + 5 LOW; clarity additions); Judge READY_TO_LOCK 100/100 (zero findings; exemplary rigor cited); Red Team ESCALATE (28 findings — 1 P0 + 11 HIGH + 11 MED + 5 LOW; appropriately adversarial given TCPA/CAN-SPAM legal-exposure surface). Cycle 1 closures applied across §13.4.2 + §13.5.0 + §13.5.3 + §13.6.0 + §13.6.3 + §13.6.4 + §13.7 + §13.8.7 + §13.8.8 + §13.9.0 + §13.9.1 + §13.9.2 + §13.9.3 + §13.9.4 + §13.10.3 + §13.11 + §13.15 + new §13.16 closure dispositions section. **Cycle 2 outcomes:** Editor READY_TO_LOCK with all 8 Cycle-1 closures PRESENT_AS_CLAIMED + 2 advisory NEW findings (E-NF-01 + E-NF-02; non-blocking; folded-in advisory); Judge READY_TO_LOCK 100/100 with explicit dimension upgrades on legal-exposure containment + token rigor + Cultivator-vs-DC isolation; Red Team PASS blocking:false (22 of 28 Cycle-1 findings CLOSED + 3 PARTIAL + 1 N/A + 13 NEW probes RT-C2-01..13 at HIGH-2 / MED-8 / LOW-3 severity — all FOLDED_IN at LOCK per row-170 transparent disposition pattern; mirrors §15 v1 / WS-C-M1 v7.0.4-M1 / WS-B v7.0.7 / WS-D v7.0.5 row-170 precedents). **Eighth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor (after WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + WS-C-M1 v7.0.4-M1 row 190 + WS-F §12 v1 rows 182-184 + WS-E §11 v1 row 185 + WS-H §2 v7.2 rows 186/187 + WS-G §5 v8 rows 188/189 + WS-K §15 v1 rows 191/192 + WS-L §4 v2.x rows 193/194 architecture/blueprint-class precedents).** Compound LOCK with `section_00_5_section_13_data_collector_amendment.md` per §6.17 Option-B paired-commit pattern.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                      # v7 LOCKED 2026-04-19 — A1-A12
  - pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md                  # v7.0.4 LOCKED 2026-05-09 row 178 — KFR + SP0 + F-LOGICIAN-FACT-DRIFT family + Benchmarks Register; Data Collector cross-validates inbound numeric responses against KFR (F-DATACOLLECTOR-KFR-DRIFT advisory)
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md               # v7.0.4-M1 LOCKED 2026-05-10 row 190 — corrective; KFR canonical-JSON signing + AST whitelist + tag-mutation hash; bounds Data Collector's KFR-read trust surface
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md                  # v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intelligence DB + Match DB; Data Collector reads funder-specific reporting context from `vault_shared/funder_intelligence/<funder_id>/`
  - pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md                  # v7.0.6 SELF-LOCKED 2026-05-09 row 176 — Data Collector named as v0.2 horizon support agent
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                  # v7.0.7 LOCKED 2026-05-10 row 180 — Beta classification-driven routing; Data Collector outbound composition with Confidential payload routes always-local; inbound storage always-local; outbound template authoring (Public+Shareable, with opaque slot tokens for Confidential) cloud-routable
  - pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md                  # v7.0.8 LOCKED — CIC × CLC orthogonality; Data Collector prompt templates + inbound schemas audited against F-CIC-CLC-COUPLING-VIOLATION at LOCK
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                         # v7.2 LOCKED 2026-05-10 rows 186/187 — operational-data sub-kinds (metrics + financials + photos + narrative_entries + timeline_of_activities + beneficiary_records + attachments); Data Collector writes inbound responses into these seven SIMPLE sub-kinds; PII discipline on beneficiary_records is Cedar-enforced
  - pipeline/blueprint/v0.1/section_04_logician.md                               # v2.x LOCKED 2026-05-10 row 193 — Data Collector gate family registered at §5.1 HORIZON; this §13 v1 LOCK ACTIVATES the six F-DATACOLLECTOR-* HORIZON rows into live PRE/POST positions
  - pipeline/blueprint/v0.1/section_05_pipeline.md                               # v8 LOCKED 2026-05-10 rows 188/189 — track-registry; Data Collector outreach lives inside the `report_mode` track sub-shape (registered FORWARD-COMPAT in §5 v8 row 188 with `shippable_in: v0.2`); WS-I does NOT register a new track
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md                     # v1-r1 LOCKED — channel substrate sits under §6 envelope discipline (frozen at Golden Image per ADR-001; BYOK per channel)
  - pipeline/blueprint/v0.1/section_11_intake.md                                 # §11 v1 LOCKED 2026-05-10 row 185 — Intake AWARD_INGEST produces `proposal_commitments.yaml`; Data Collector reads `status: PROMOTED` proposal_commitments to author the per-cycle question set; Cultivator-vs-DC discipline cross-references §11 always-local posture
  - pipeline/blueprint/v0.1/section_12_uploader.md                               # §12 v1 LOCKED 2026-05-10 rows 182-184 — operator-clicks-final-submit discipline; §13 mirrors the operator-approves-per-cycle-batch pattern for outbound stage-and-fire
  - pipeline/blueprint/v0.1/section_15_archivist.md                              # §15 v1 SPEC LOCKED 2026-05-10 rows 191/192 — cross-org leak gate-family precedent; §13's `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND` mirrors the cross-org leak detection shape; cadence-drift discipline precedent for per-state frequency caps
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md               # §0.5 v5 LOCKED + amendments v6-v13 (runtime-live 304 rows at 2026-05-10T19:30Z) + v14 (runtime-live 348 rows at 2026-05-10T20:45Z); Data Collector primitives row-append at paired §0.5 §13 amendment companion-file claiming rows 349-374
prerequisite_interlock: pipeline/blueprint/v0.1/section_04_v2_x_amendment.md §5.1 (Data Collector family HORIZON registration — six gates at rows 298-303 of the v2.x amendment; this §13 v1 LOCK is the activation event that flips HORIZON → live PRE/POST positions; §4 v2.x LOCKED row 193 is the prerequisite parent).
companion_module: pipeline/orchestrator/seats/data_collector/__init__.py + per-channel module skeletons (scaffold authored at §13 v1 LOCK with proposes-only AST-lint assertions on outbound autosend; full per-channel substrate implementation deferred to WS-I Code phase follow-on dispatch).
companion_amendment: pipeline/blueprint/v0.1/section_00_5_section_13_data_collector_amendment.md (paired-commit at §13 v1 LOCK per §6.17 Option-B).
v0_2_implementation_disposition: SPEC + skeleton at v0.2 first ship. The five per-channel substrate modules (email_channel / sms_channel / voice_channel / telegram_channel / whatsapp_channel) ship as skeletons that import a ChannelProtocol contract + emit `NotImplementedError` at substrate-level send; full BYOK substrate wiring lands in WS-I Code phase dispatch after §13 v1 LOCK. The consent_ledger Cedar policy + state-rules card for PA/CA/FL/TX/NY ship as v0.2 first-wave Code work paired with this LOCK; six F-DATACOLLECTOR-* gate predicates from §4 v2.x §5.1 HORIZON flip to live PRE/POST positions at this LOCK.
downstream_siblings_out_of_scope: §14 Report Generator (v0.2 horizon — depends on §13 LOCK to consume operational-data sub-kind writes; §14 dispatches as WS-J after §13 LOCK).
ws_l_routing_dependency: WS-L §4 Logician v2.x LOCKED 2026-05-10 row 193. The six F-DATACOLLECTOR-* gates registered at §4 v2.x §5.1 HORIZON activate at this §13 v1 LOCK via the paired-commit pattern. Gate predicate bodies are spec'd in this §13 (substrate-dispatched per channel where applicable; consolidated PRE-outbound check callable per §4 v2.2 pattern); Code-side realization lands in WS-I Code phase dispatch.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent (lock_history row 179, 2026-05-10) + WS-E §11 + WS-F §12 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 blueprint-class precedents (rows 185 / 182 / 186 / 188 / 191). Editor=groq/llama-3.3-70b-versatile (Meta family) + Judge=google/gemini-2.5-pro (Google family) + Red Team=groq/openai/gpt-oss-120b (OpenAI-OSS family) dispatched via openclaw infer model run --gateway across both Cycle 1 and Cycle 2. Three distinct non-Anthropic families. L-003 satisfied. Bridge pattern: Cowork → openclaw via mcp__Control_your_Mac__osascript with timeout of 600 seconds for Gemini Pro thinking-mode runs. Dispatch shell scripts cribbed from pipeline/validation/blueprint_section_11_intake_2026-05-10/dispatch_audit_v{1,2}.sh. Audit trail at pipeline/validation/blueprint_section_13_data_collector_2026-05-10/. **Red Team pass is load-bearing**: TCPA / CAN-SPAM / per-state-rules violations are real legal exposure for the operator. TCPA per-violation statutory damages are $500–$1,500; CAN-SPAM per-message $51,744 (2024 adjusted). Adversarial probe MUST cover (a) consent-bypass via stale ledger read, (b) opt-out-honored-too-slowly race, (c) frequency-cap-bypass via channel-switching, (d) PII-leak via Cultivator-vs-DC substrate confusion, (e) cross-org leak via shared MTProto substrate, (f) inbound classification spoofing.
---

# §13.0 Cross-amendment composition map

```
v7 LOCKED 2026-04-19 (A1-A12)
  ├─ v7.0.4 LOCKED 2026-05-09 row 178 + v7.0.4-M1 row 190 — KFR + SP0 + F-LOGICIAN-FACT-DRIFT family; Data Collector cross-validates inbound numeric responses
  │    │
  │    └─→ §13 Data Collector (THIS) — seat-lifecycle wrapper around five channel modules + consent ledger + state-rules card + inbound parser; owns six F-DATACOLLECTOR-* gates activating from §4 v2.x §5.1 HORIZON registration
  │
  ├─ v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intel DB; Data Collector reads funder-specific reporting context per-grant
  ├─ v7.0.6 SELF-LOCKED 2026-05-09 row 176 — Data Collector named v0.2 horizon support agent
  ├─ v7.0.7 LOCKED 2026-05-10 row 180 — classification routing; §13.10 routing posture is split-context per directive ("power for drafting + privacy for review"): outbound template authoring cloud-routable when content is Public+Shareable; per-recipient slot-fill always-local; inbound storage always-local
  └─ v7.0.8 LOCKED — CIC × CLC orthogonality; §13 schemas + per-channel prompt templates audit clean at LOCK

§13 → companion edits at LOCK (compound paired-commit per §6.17 Option-B):
  ├─ §0.5 §13 amendment (26 rows; range 349-374; +1 marker + 7 schema rows + 6 failure-code rows + 7 pre/post-gate-check rows + 5 channel-protocol rows)
  ├─ §4 v2.x amendment ACTIVATES F-DATACOLLECTOR-* family from §5.1 HORIZON to live PRE/POST positions (6 codes; Code session per WS-I Code phase realizes predicate bodies)
  ├─ orgs/_TEMPLATE/data_collector/ scaffold (consent_ledger/.gitkeep + state_rules_card/.gitkeep + outbound_log/.gitkeep + inbound_log/.gitkeep + per_recipient_tokens/.gitkeep + data_collector_config.yaml)
  ├─ pipeline/orchestrator/seats/data_collector/__init__.py module skeleton + per-channel skeletons (5 channel modules with ChannelProtocol contract + AST-lint assertion: no autosend code path)
  ├─ tests/seats/data_collector/skeleton_tests.py (NON-NEGOTIABLE: prevents future contributors from quietly enabling autosend)
  └─ pipeline/validation/blueprint_section_13_data_collector_2026-05-10/ (audit trail directory)
```

**Per-substrate contract reference.** Data Collector's read-only access to upstream substrates is bounded by each substrate's LOCKED contract:

- **KFR canonical** — read-substrate per v7.0.4 §1 + v7.0.4-M1 §2; Data Collector reads `orgs/<slug>/vault/kfr/register.yaml` via `vault_read_intent_kfr` to cross-validate inbound numeric responses (F-DATACOLLECTOR-KFR-DRIFT advisory POST). Cross-check semantics: read-only; never mutates KFR.
- **Proposal commitments** — per-org-per-grant read-substrate per v7.0.4 §5.3 + §11 v1 §11.5.2; Data Collector reads `orgs/<slug>/vault/grants/<grant_id>/proposal_commitments.yaml` with `status: PROMOTED` to author the per-cycle outbound question set. PENDING_OPERATOR_REVIEW files are NOT consumed (mirrors §14 Report Generator's discipline).
- **Funder intel** — workspace-shared read-substrate per v7.0.5 §1; Data Collector reads `vault_shared/funder_intelligence/<funder_id>/reporting_format_precedents.yaml` for per-funder reporting-template context. F-FUNDER-CORPUS-INTEGRITY per v7.0.5 §5.6 verification fires PRE-load.
- **Reporting template** — per-org-per-grant read-substrate; Data Collector reads `orgs/<slug>/vault/grants/<grant_id>/reporting_template.yaml` (funder-required reporting format) to bound the per-cycle question set against funder requirements.
- **Consent ledger** — per-org read+write-substrate (Data Collector OWNS this substrate); `orgs/<slug>/data_collector/consent_ledger/<recipient_id>__<channel>.yaml` per-recipient × per-channel; Cedar-policy-gated atomic read/write; audit-logged.
- **State-rules card** — workspace-shared read-substrate (SN-LLC ships); `vault_shared/state_rules_card/<state_code>.yaml` (PA/CA/FL/TX/NY at v0.2 first wave); Ed25519-signed per state per SN-LLC router-template-update pattern (v7.0.7 §6.1); operator opts in per state at white-glove.
- **Sub-awardee token register** — per-org-per-grant read+write-substrate (Data Collector OWNS this substrate); `orgs/<slug>/data_collector/per_recipient_tokens/<grant_id>__<recipient_id>.signed.yaml`; Ed25519-signed by operator at award acceptance; rotates per grant cycle.

Each per-substrate read is wrapped by the appropriate Vault read intent. Bypassing the read intent (raw `open()` against any of the above substrates) is forbidden by AST-lint extension `R-DATACOLLECTOR-VAULT-INTENT-REQUIRED` (mirrors §15 v1 §15.9.5 RT-11 closure precedent).

# §13.1 Purpose and scope

## §13.1.0 What ships at v0.2 first ship

**Five outbound channels at v0.2 first ship** (per Josh 2026-05-09 decisions 8a + 8b): email (SMTP via operator BYOK — Postmark / SendGrid / Mailgun candidate set) + SMS (Twilio or equivalent BYOK) + voice (Twilio Voice outbound + local-Whisper-class transcription on inbound) + Telegram (MTProto bot — shared substrate with Cultivator per §13.11) + WhatsApp (WhatsApp Business API BYOK). Full TCPA / CAN-SPAM / per-state-rules exposure accepted at first ship.

**Per-state-rules card first wave** (per dispatch decision 8f default): PA + CA + FL + TX + NY. PA = operator's home state; CA + NY = toughest consent regimes; FL + TX = largest non-CA/NY markets. SN-LLC ships state cards as Ed25519-signed YAML modules under `vault_shared/state_rules_card/<state_code>.yaml` per the router-template-update pattern (v7.0.7 §6.1). Other states are operator-curated until SN-LLC adds them.

**Sub-awardee identity verification** (per dispatch decision 8e default): per-recipient shared-secret token issued at award acceptance time, embedded in every outbound message, validated on inbound responses. Token rotates per grant cycle. Token storage: classified `confidential` in KFR per v7.0.4 + Ed25519-signed at write per §13.6.0 Sub-awardee token register discipline.

**Operator approves the per-cycle outbound batch; system stages-and-fires per-recipient.** Mirror of §12 Uploader's operator-clicks-final-submit discipline applied to outbound batch composition. No autosend code path exists; AST-lint `R-DATACOLLECTOR-NO-AUTOSEND` rejects any module that imports a channel transport substrate from a code path other than the operator-approved batch dispatcher.

**Inbound parsing + classification is autonomous, but inbound write-to-vault requires operator classification approval at first occurrence of each `recipient_id × field_class` pair.** Mirrors Intake INCREMENTAL discipline per v7.0.7 §4.1 + §11 v1 — new inbound facts default `confidential` until operator re-classifies. F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET PRE-storage gate fail-closes any inbound write where classification has not been operator-set for this `(recipient_id, field_class)` pair.

## §13.1.1 Purpose

Data Collector is the **between-cycle outbound + inbound data-gathering** support agent of the Tilth pipeline. During an active grant's reporting period, Data Collector:

1. Reads the active grant's `proposal_commitments.yaml` (Intake AWARD_INGEST PROMOTED output per §11 v1) and `reporting_template.yaml` (funder-required reporting format) to author the per-cycle question set for grantees + sub-awardees.
2. Composes per-channel outbound prompts in split-context discipline per v7.0.7 §4.1: template content (Public + Shareable) is cloud-routable; per-recipient slot-fill values (recipient identifiers, shared-secret tokens, contact PII, sometimes unconfirmed beneficiary data) are local-routed only.
3. Stages the per-cycle outbound batch for operator approval; per-recipient stage-and-fire dispatch after operator signs the batch.
4. Parses inbound responses across five channels into a common `InboundResponse` Pydantic schema with per-channel substrate-specific normalization (email-thread parser; SMS short-form parser; voice transcription via local Whisper-class model; Telegram bot inbound handler; WhatsApp inbound handler).
5. Cross-validates numeric inbound responses against KFR (F-DATACOLLECTOR-KFR-DRIFT advisory).
6. Writes operator-classification-approved inbound responses into §2 v7.2 operational-data sub-kinds (metrics / financials / photos / narrative_entries / timeline_of_activities / beneficiary_records / attachments) at `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/<sub_kind>/`.

**Data Collector proposes (outbound); operator confirms each per-cycle batch; system fires per-recipient under operator-signed authority.** The operator-clicks-final-submit pattern from §12 Uploader transfers to outbound batch composition: Data Collector authors the batch + stages it; operator reviews the per-recipient envelope + per-state rules compliance summary + classification routing summary; operator signs the batch; system fires per-recipient with stage-and-fire discipline (each recipient send is its own audited transaction; partial-batch failure surfaces clearly).

**v0.2 first-ship scope is SPEC + skeleton.** Per the `v0_2_implementation_disposition` frontmatter, this §13 v1 LOCK ships the spec text + module skeletons + AST-lint assertions + skeleton tests. Per-channel substrate wiring (SMTP / Twilio / MTProto / WhatsApp Business API client implementations) lands in WS-I Code phase dispatch after §13 v1 LOCK. The six F-DATACOLLECTOR-* gates from §4 v2.x §5.1 HORIZON flip to live PRE/POST positions at this LOCK; predicate bodies ship as skeleton stubs raising `NotImplementedError` at v0.2 with the Cedar policy + check-callable shape spec'd herein (mirrors §15 v1 Archivist spec-only-with-skeleton-stubs disposition).

**Out of scope for v0.2 (explicit non-goals).** Data Collector does NOT auto-send outbound messages absent operator-signed per-cycle batch approval (F-DATACOLLECTOR-CONSENT-MISSING + R-DATACOLLECTOR-NO-AUTOSEND AST-lint). Data Collector does NOT write KFR canonical entries (Intake §11 owns KFR; Data Collector reads only). Data Collector does NOT mutate operator-promoted `proposal_commitments.yaml` (read-only). Data Collector does NOT generate proposal text (Scribe §7). Data Collector does NOT submit to funder portals (Uploader §12). Data Collector does NOT run grant-writing cycles (§5 submission_mode track). Data Collector does NOT curate the Funder Intelligence DB (Archivist §15). Data Collector does NOT cross orgs (per F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND structural enforcement + §13.10.3 cross-org isolation). Data Collector does NOT mix Cultivator + DC consent ledgers (per §13.11 substrate-shared-but-ledger-distinct discipline).

**Substance comes from grantees + sub-awardees (Laws 1 + 5).** Every inbound response carries `recipient_id` + `channel` + `token_validated_at_utc` + `raw_payload` + `parsed_fields` + `classification_hint`. The operator-classification-approval step is the load-bearing transition from inbound parse to canonical operational-data write — Data Collector never silently writes a Confidential field to vault without operator sign-off on the `(recipient_id, field_class)` classification at first occurrence. F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET enforces structurally.

## §13.1.2 Boundary with Cultivator (substrate-shared, audience-distinct)

**Cultivator and Data Collector share the MTProto bot framework substrate at v0.2 first ship** (per §13.11 spec; operator confirmation surface at Audit #1). They are NEVER the same agent:

| Dimension | Cultivator | Data Collector |
|---|---|---|
| Target audience | Operator's own employees | External grantees + sub-awardees |
| Consent capture | Opt-in by employment at hire | Formal CAN-SPAM / TCPA / per-state consent capture at award acceptance |
| Consent ledger | `orgs/<slug>/cultivator/consent_ledger/<employee_id>__<channel>.yaml` | `orgs/<slug>/data_collector/consent_ledger/<recipient_id>__<channel>.yaml` |
| Identity verification | Operator-signed employee roster | Per-recipient shared-secret token (rotates per grant cycle) |
| Frequency cap default | Operator-set (employees expect daily contact) | Conservative (1 outbound per recipient per channel per 7 days at v0.2 first ship) |
| State-rules card | Not applied (employment relationship pre-empts) | Applied per recipient address-of-record |
| PII leak gate | None (operator owns employee PII) | F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND fail-closed |
| Inbound classification | Operator-set per employee onboarding | F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET fail-closed per `(recipient_id, field_class)` first occurrence |

**Shared substrate; distinct everything else.** Both agents instantiate an MTProto bot client at v0.2 first ship; the bot framework is one Python package wrapping the `python-telegram-bot` or `pyrogram` library (BYOK MTProto API keys); the bot's session storage is partitioned by purpose tag (`cultivator_session` / `data_collector_session`); the consent ledgers are non-overlapping per-substrate filesystem trees. AST-lint `R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT` rejects any Data Collector code path that imports `cultivator.consent_ledger.*` (or vice versa). Cedar policy `data_collector_consent_isolation.cedar` denies any read where the Cedar principal is `data_collector_seat` and the resource path resolves under `orgs/<slug>/cultivator/`. Mirror policy for Cultivator side; this §13 owns the DC-side policy + Cedar denial.

**Why share the substrate at all?** Two reasons. First, the MTProto API token quota is per-API-application, not per-bot-session; one shared application token across both agents reduces operator BYOK envelope friction (operator registers one Telegram application with Telegram, not two). Second, the bot-framework code itself (message parsing, attachment handling, retry-with-backoff) is identical between Cultivator and Data Collector; duplicating it would be Code-debt without sovereignty benefit. The audience-distinct + ledger-distinct + Cedar-denied separation is the structural enforcement; substrate sharing is the efficiency choice. Surface for operator confirmation at Audit #1 — if operator decides at Audit #1 that they want full substrate separation rather than shared MTProto framework, v1 blueprint accommodates by spec-only stating "Cultivator substrate TBD at Cultivator's own blueprint round; DC substrate is MTProto bot framework with audience-distinct consent ledger." Avoids blocking on a decision that lives in a different workstream (Cultivator's own v1.x or v2 blueprint round).

# §13.2 Five Operating Laws — enforcement mapping

Framework: per `pipeline/templates/component_analysis_template.md`

Each of the Five Laws is enforced by a combination of PRE-gates (Logician, before Data Collector composes or stores), in-seat discipline (Data Collector's own channel-dispatch contract + Cedar policies), and POST-gates (Logician, after Data Collector emits outbound or stores inbound but before downstream consumer reads).

**Law 1 — RFA is the source of truth.**
- N/A direct path at outbound composition — Data Collector runs during active reporting cycles, not against an active RFA. The reporting template (`reporting_template.yaml` per §13.1.1) is the funder-required format authority; the proposal_commitments.yaml is the operator-signed source of "what we said we'd report on."
- In-seat: every outbound question references either a `commitment_id` from `proposal_commitments.yaml` (Intake AWARD_INGEST PROMOTED output) OR a `funder_reporting_field_id` from `reporting_template.yaml`. No free-form outbound questions at v0.2 first ship. The structured-output validation rejects outbound batch entries whose `commitment_id` or `funder_reporting_field_id` does not resolve to a current proposal_commitments / reporting_template entry.
- v1.1 horizon: operator-authored ad-hoc question support is a v1.1 candidate; out of scope at v0.2 first ship to keep the audit trail tight.

**Law 2 — No boundary drift.**
- PRE-gate: Data Collector's outbound scope is mechanically bounded — per-cycle batch composition reads ONLY the named grant's `proposal_commitments.yaml` + `reporting_template.yaml` + the per-org consent ledger + the per-org sub-awardee token register + the workspace state-rules card entries the operator has opted into. No web search, no cross-grant reference, no content generation beyond per-channel template fill-in.
- In-seat: per-channel prompt templates are fixed at substrate-freeze time (per ADR-001 Golden Image build). At v0.2 first ship the templates are sealed; v1.x candidate: per-grant template override with operator Ed25519 signature on each override (mirrors §11 v1 §11.4.1 RT-07 operator-config signature pattern).
- POST-pre-send: Pydantic validation on every outbound message before transport handoff. Schema violation → reject + audit trail under `pipeline/validation/data_collector_outbound_rejects/<org_slug>/<run_id>/`.

**Law 3 — Org isolation.**
- PRE-gate: Data Collector operates on **exactly one** `orgs/<slug>/` subtree per invocation. The CLI takes `--org <slug>` as a required argument; the per-cycle batch invocation `--grant <grant_id>` resolves under `--org`. Cross-org input file paths are PRE-rejected with the F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND `.org_cross_ref` sub-tag.
- In-seat: Data Collector reads from exactly one `orgs/<slug>/data_collector/` consent ledger + sub-awardee token register subtree per invocation. Workspace-shared substrates (state-rules card under `vault_shared/state_rules_card/`; funder intel under `vault_shared/funder_intelligence/`) are explicitly workspace-scoped and carry NO per-org content (state rules are per-jurisdiction factual; funder intel is per-funder factual).
- Cross-org MTProto substrate isolation — see §13.11. Each org's `data_collector_session` is path-segmented under `orgs/<slug>/data_collector/mtproto_session/`; the bot framework code MUST receive `org_slug` as a required parameter on every send/receive call; F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND `.mtproto_cross_org` sub-tag fail-closes any send where `recipient_id` is registered to a different `org_slug` than the invocation's bundle.
- POST-gate: every consent-ledger write + inbound-log write + operational-data-sub-kind write is path-resolve-normalized; any path that resolves outside the declared `org_slug` subtree → hard-block with `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.path_cross_org`.

**Law 4 — Apolitical sector language + admin-risk term scanning.**
- PRE-gate: Data Collector outbound templates produce structured per-channel messages, not narrative-prose. The §7.11 admin-risk scanner (Scribe-side) does NOT fire on Data Collector's structured outputs at v0.2 first ship because there is no narrative-prose for it to scan. v1.1 horizon: per-grant operator-authored ad-hoc questions would trigger admin-risk scanning as a POST-compose advisory.
- In-seat: per-state-rules card entries include `state_specific_required_disclaimers: list[str]` per state per channel (e.g., CA opt-out language for SMS, FL telemarketing disclosure, NY automated-call statement). Data Collector composes the per-state-required disclaimer text from the card verbatim — no rewriting per Law 4. If the operator wants to flag a disclaimer for review, that's an operator action at white-glove + per-state-opt-in time, not a Data Collector-time silent rewrite.

**Law 5 — Applicant brings the substance.**
- PRE-gate (outbound): the operator chooses which `proposal_commitments` + `reporting_template` entries become outbound questions per cycle. Data Collector composes the outbound batch from the operator-curated entries; no web-fetched substance, no third-party benchmark substance, no LLM-fabricated substance.
- PRE-gate (inbound): every inbound response is treated as Confidential by default until operator-classified at first occurrence per `(recipient_id, field_class)` pair (F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET enforces structurally). Operator approves the classification at the operator review surface (§13.7); only then does the inbound response flow into the operational-data sub-kind write path.
- POST-pre-write: F-DATACOLLECTOR-KFR-DRIFT is the advisory POST-inbound gate — reported numeric values are cross-checked against KFR-derived expected values per per-field tolerance; drift surfaces to operator for reconciliation (operator decides whether the inbound or the KFR is authoritative). NOT fail-closed — Data Collector does not unilaterally reject grantee-reported data; operator owns the reconciliation decision.
- Sub-awardee-claim provenance: every inbound response carries `token_validated_at_utc` showing that the inbound response carried the per-recipient shared-secret token issued at award acceptance. Token-invalid inbound responses are quarantined under `orgs/<slug>/data_collector/inbound_quarantine/<run_id>/<msg_id>.yaml` for operator review; F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND `.token_invalid_inbound` sub-tag fires (the sub-tag covers both outbound leak detection AND inbound token-spoofing detection per the consolidated check callable §13.9.0 pattern).

# §13.3 Four Autonomy Rules — enforcement mapping

**Rule 1 — Save state always.** Data Collector persists `DataCollectorState` to `orgs/<slug>/data_collector/state/<run_id>.yaml` on every cadence invocation — both success and failure. State includes: invocation timestamp, cycle (`outbound_batch_compose` / `outbound_batch_send` / `inbound_parse` / `inbound_classify`), org_slug, grant_id (per-grant invocations), recipient_id_list (outbound; redacted in audit dump per §13.10.3 redaction discipline), channels in scope, consent-ledger reads, state-rules-card entries applied, F-DATACOLLECTOR-* gate fires logged to `pipeline/validation/data_collector_rejects/<cycle>/<run_id>/`, outbound-log + inbound-log write paths, failure reason if applicable.

**PRE-gate failure persistence.** When Data Collector is invoked but a PRE-gate (§13.9 PRE codes including F-DATACOLLECTOR-CONSENT-MISSING + F-DATACOLLECTOR-OPT-OUT-ACTIVE + F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED + F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND + F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET) fails before any outbound transport call or inbound write, Data Collector writes `data_collector_state.yaml` with `cycle_completed=False, recipients_processed=0, failure_reason=<gate_code>, failure_detail=<predicate_message>`. No partial outbound batch is sent; no partial inbound is written. The operator surface receives the gate-fail result with the same self-validation envelope as a successful cycle, just with `overall_status="cycle_failed"` and the failure code surfaced.

**Rule 2 — Test your own work.** Before marking the outbound batch "ready for operator approval," Data Collector runs the readiness check (§13.7) — a deterministic self-validation pass that confirms: every batch entry has `recipient_id` + `channel` + `commitment_id_or_funder_reporting_field_id` populated, every entry's consent ledger has been read and `consent_active=True` + `opt_out_active=False` + `frequency_cap_not_hit=True`, every state-rules card entry for the recipient's address-of-record has been applied, every per-state-required disclaimer has been included in the rendered message, the per-recipient shared-secret token has been embedded, the rendered message passes F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND PRE-scan. The readiness result is persisted alongside `data_collector_state.yaml`. Before marking inbound classification "ready for operational-data write," Data Collector runs the inbound readiness check: every parsed field has a `(recipient_id, field_class)` classification approved at operator review surface; every numeric field has been F-DATACOLLECTOR-KFR-DRIFT-scanned; every photo + attachment field has EXIF-stripped + virus-scanned (v1.1 horizon — see §13.14 OQ-DC-VIRUS-SCAN).

**Rule 3 — Be explicit.** Data Collector's input contracts (§13.4) declare exact paths, cycles, and done-definitions per cycle. Data Collector's output contracts (§13.5) declare exact output paths per write (outbound log + inbound log + consent ledger updates + operational-data sub-kind writes), schemas, and operator-review surface format.

**Rule 4 — Clean output.** Outbound messages are rendered from per-channel templates + per-recipient slot-fill; the rendered message bytes are Pydantic-validated before transport handoff. Inbound responses are parsed into the common `InboundResponse` Pydantic schema; raw transport payload is preserved verbatim under `raw_payload` (no LLM rewriting at parse time). Operational-data sub-kind writes are Pydantic-validated against the §2 v7.2 sub-kind schemas before write.

# §13.4 Input contracts (per cycle + per channel)

Data Collector fires at four distinct cycle points; each cycle has its own input contract. All five channels share a common ChannelProtocol contract per §13.4.0.

## §13.4.0 ChannelProtocol common shape

All five per-channel modules implement a common `ChannelProtocol` (Python Protocol per Pydantic AI's Protocol-DI pattern). Per-channel substrate variations (SMTP envelope vs MTProto chat_id vs WhatsApp template_name) live behind this contract.

```python
@runtime_checkable
class ChannelProtocol(Protocol):
    channel_name: ClassVar[Literal["email", "sms", "voice", "telegram", "whatsapp"]]

    def compose_outbound(
        self,
        *,
        org_slug: str,
        grant_id: str,
        recipient: Recipient,
        commitment_id_or_funder_reporting_field_id: str,
        per_state_disclaimers: list[StateDisclaimer],
        per_recipient_token: SharedSecretToken,
    ) -> OutboundMessage: ...

    def send(
        self,
        *,
        message: OutboundMessage,
        operator_batch_signature: BatchSignature,
    ) -> SendResult: ...

    def parse_inbound(
        self,
        *,
        raw_payload: bytes,
        receipt_metadata: ChannelReceiptMetadata,
    ) -> InboundResponse: ...

    def validate_inbound_token(
        self,
        *,
        inbound: InboundResponse,
        expected_token: SharedSecretToken,
    ) -> TokenValidationResult: ...
```

Each channel substrate (email_channel / sms_channel / voice_channel / telegram_channel / whatsapp_channel) ships its own module under `pipeline/orchestrator/seats/data_collector/<channel>_channel.py`; each module implements `ChannelProtocol` and registers itself in the channel dispatcher via the §6 Operating Envelope plug-in pattern.

**No autosend code path exists in any channel module.** AST-lint `R-DATACOLLECTOR-NO-AUTOSEND` extension runs at every CI commit + at the `pipeline/orchestrator/seats/data_collector/__init__.py` import time (defense-in-depth): the lint forbids any `<channel>_channel.send(...)` invocation outside the operator-approved batch dispatcher (`pipeline/orchestrator/seats/data_collector/outbound_batch.py::dispatch_after_operator_approval`). The dispatcher itself reads the `operator_batch_signature` parameter and verifies Ed25519 signature at function entry; signature-invalid `SendResult` returns without invoking the underlying transport substrate.

## §13.4.1 Per-cycle outbound batch compose input contract

Trigger: operator-explicit at v0.2 first ship via `tilth data-collector compose-batch --org <slug> --grant <grant_id> --period <n>`. (Scheduled-task-driven trigger via `schedule` skill lands at v1.x amendment.)

**Input bundle (`OutboundBatchComposeInput`, frozen, kw_only):**

- `run_id: str` — UUID assigned at CLI invocation; pins the run for state persistence.
- `org_slug: str` — client org slug (required CLI arg).
- `grant_id: str` — grant identifier; resolves to `orgs/<org_slug>/vault/grants/<grant_id>/`. Required CLI arg.
- `period_n: int` — reporting period number (1, 2, 3, ...) per funder cadence; resolves to `orgs/<org_slug>/vault/operational/grants/<grant_id>/period_<period_n>/` write target.
- `proposal_commitments_path: str` — vault path; defaults to `orgs/<org_slug>/vault/grants/<grant_id>/proposal_commitments.yaml`. `Path.resolve()` validated under `orgs/<org_slug>/`. MUST carry `status: PROMOTED` (PENDING_OPERATOR_REVIEW files refused).
- `reporting_template_path: str` — vault path; defaults to `orgs/<org_slug>/vault/grants/<grant_id>/reporting_template.yaml`.
- `consent_ledger_dir: str` — vault path; defaults to `orgs/<org_slug>/data_collector/consent_ledger/`.
- `sub_awardee_token_register_dir: str` — vault path; defaults to `orgs/<org_slug>/data_collector/per_recipient_tokens/`.
- `state_rules_card_dir: str` — workspace path; defaults to `vault_shared/state_rules_card/` (operator opts in per state at white-glove; this bundle reads the operator-opted-in subset).
- `channels_in_scope: list[Literal["email","sms","voice","telegram","whatsapp"]]` — which channels to compose for this batch. Operator-set per cycle; default = `["email"]` at v0.2 first ship to minimize TCPA exposure absent explicit operator opt-in to SMS / voice / Telegram / WhatsApp per cycle.
- `frequency_cap_lookback_days: int` — per-recipient × per-channel frequency cap rolling window; default `7` (1 outbound per recipient per channel per 7 days). Operator-tunable per-org via signed `data_collector_config.yaml` (mirrors §11 v1 §11.4.1 RT-07 operator-config Ed25519 signature discipline).
- `invoked_at_utc: datetime`.

**Bundle invariants (PRE-gate enforced).**
- `proposal_commitments_path` MUST carry `status: PROMOTED` (PENDING_OPERATOR_REVIEW refused; mirrors §14 Report Generator's discipline).
- All paths `Path.resolve()` under `orgs/<org_slug>/` (per-org) OR `vault_shared/` (workspace). Symlink traversal → `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.symlink_escape`.
- `period_n >= 1`.
- `channels_in_scope` non-empty; each entry MUST resolve to a registered ChannelProtocol implementation in the channel dispatcher.
- **Operator-config signature** — if `data_collector_config.yaml` exists at `orgs/<org_slug>/data_collector/data_collector_config.yaml`, it MUST be Ed25519-signed by an operator key currently active in the Section 1 key catalog. F-DATACOLLECTOR-CONFIG-SIGNATURE-INVALID (sub-tag of F-DATACOLLECTOR-CONSENT-MISSING per the consolidated check pattern §13.9.0) fires at config read time if signature missing, invalid, or signed by retired key. Per-run CLI override does NOT require signed config (CLI is operator-interactive by definition); BUT the CLI parser explicitly **prohibits** `--yes`, `--auto-confirm`, and `--force` flags at v0.1 + v0.2 first ship — any such flag triggers an argparse-level rejection (mirrors §11 v1 §11.4.1 RT-08 closure pattern).

## §13.4.2 Per-cycle outbound batch send input contract

Trigger: operator-explicit only at v0.2 first ship via `tilth data-collector send-batch --org <slug> --grant <grant_id> --period <n> --batch-signature <signed_batch_path>`. The `--batch-signature` is the file path of the operator-signed batch envelope produced at compose-then-approval step.

**Input bundle (`OutboundBatchSendInput`, frozen, kw_only):**

- `run_id: str` — UUID assigned at CLI invocation.
- `org_slug: str`.
- `grant_id: str`.
- `period_n: int`.
- `signed_batch_path: str` — vault path to the operator-signed outbound batch envelope produced at the compose step (operator approves at the review surface §13.7 + signs with Ed25519). MUST resolve under `orgs/<org_slug>/data_collector/staged_batches/`. Symlink → `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.symlink_escape`.
- `invoked_at_utc: datetime`.

**Bundle invariants (PRE-gate enforced).**
- `signed_batch_path` MUST exist; MUST be Ed25519-signed by an operator key active at `invoked_at_utc`; MUST carry `batch_status: APPROVED_FOR_SEND`; MUST carry `compose_run_id` matching a `data_collector_state.yaml` with `cycle="outbound_batch_compose"` and `overall_status="ready_for_operator_approval"`.
- **Batch-bound content-hash binding.** The signed batch envelope MUST carry `batch_content_sha3_512` field over the per-recipient OutboundMessage rendered-bytes manifest (mirrors §11 v1 §11.9.2 RT-05 content-hash binding precedent). Send-time recomputation + comparison; mismatch → `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.batch_hash_mismatch` (sub-tag of the consolidated check; sub-tag chosen because tampered batch bytes are a payload-level leak vector).
- TTY check on `tilth data-collector send-batch` invocation (mirrors §11 v1 §11.7 RT-08 closure pattern) — non-TTY rejected with clear error; `--yes` / `--auto-confirm` / `--force` flags prohibited at argparse level.

## §13.4.3 Inbound parse input contract

Trigger: per-channel inbound webhook OR polling-loop trigger. Each channel registers its inbound handler under the §6 Operating Envelope inbound-dispatcher pattern. Inbound parse is autonomous (no operator confirmation per inbound message — that happens at classification approval step §13.4.4).

**Input bundle (`InboundParseInput`, frozen, kw_only):**

- `run_id: str` — UUID assigned at handler entry.
- `org_slug: str` — derived from the recipient's contact info via the per-channel recipient resolver (e.g., email From: header → `orgs/<slug>/data_collector/consent_ledger/<recipient_id>__email.yaml` lookup; SMS From: number → consent ledger lookup; Telegram chat_id → consent ledger lookup; WhatsApp phone → consent ledger lookup). If the recipient resolver cannot resolve the inbound to exactly one `org_slug`, the inbound is quarantined under `pipeline/data_collector_inbound_quarantine/unresolved/<run_id>.yaml` with the raw payload preserved; operator inspects.
- `grant_id: str | None` — derived from the per-recipient shared-secret token; if the token decodes to a different `grant_id` than the recipient's last-known active grant, the inbound is quarantined under `pipeline/data_collector_inbound_quarantine/<org_slug>/grant_mismatch/<run_id>.yaml`.
- `channel: Literal["email","sms","voice","telegram","whatsapp"]`.
- `raw_payload: bytes` — verbatim transport payload bytes (email RFC822 bytes; SMS body bytes; voice audio bytes pre-transcription; Telegram update bytes; WhatsApp inbound webhook bytes).
- `receipt_metadata: ChannelReceiptMetadata` — per-channel substrate metadata (envelope From/To/Subject for email; phone numbers for SMS/voice; chat_id + sender_id for Telegram; sender_phone + business_phone for WhatsApp).
- `received_at_utc: datetime`.

**Bundle invariants (PRE-gate enforced).**
- `org_slug` resolved exactly-one; if not, quarantine.
- `grant_id` either resolved exactly-one OR explicitly `None` (legitimate unsolicited inbound — operator may have ad-hoc replies to handle; quarantine for review).
- `raw_payload` bounded by per-channel size limits (email = 25 MB at v0.2 first ship; SMS = 1600 bytes; voice = 5-minute audio max; Telegram = 50 MB; WhatsApp = 16 MB) — beyond-bound → quarantine.

## §13.4.4 Inbound classify input contract

Trigger: operator-explicit at v0.2 first ship via `tilth data-collector classify-inbound --org <slug> --grant <grant_id>` to enter the operator classification review surface. The CLI walks all unclassified `(recipient_id, field_class)` pairs in `orgs/<slug>/data_collector/inbound_log/` for the named grant and prompts the operator for classification of each first-occurrence pair.

**Input bundle (`InboundClassifyInput`, frozen, kw_only):**

- `run_id: str`.
- `org_slug: str`.
- `grant_id: str`.
- `inbound_log_dir: str` — vault path; defaults to `orgs/<org_slug>/data_collector/inbound_log/<grant_id>/`.
- `invoked_at_utc: datetime`.

**Bundle invariants (PRE-gate enforced).**
- TTY check required for classification approval (mirrors §11 v1 §11.7 RT-08 + §13.4.2 send-batch TTY discipline).
- `--yes` / `--auto-confirm` / `--force` argparse-rejected.

# §13.5 Output contracts

## §13.5.0 Schema delta from v7.0.4 KFR + §2 v7.2 operational sub-kinds + §11 v1 conventions (per §11 v1 §11.5.0 precedent)

Data Collector's outbound + inbound + consent ledger schemas extend v7.0.4 + §2 v7.2 + §11 v1 conventions with the following deltas. All other fields retain v7.0.4 / §2 v7.2 / §11 v1 conventions (`populated_at`, `populated_by`, `audit_chain`, `source_doc`, `source_quote`, `extracted_at_utc`, etc.).

| Schema | Field | Type | Source | Purpose |
|---|---|---|---|---|
| `outbound_message.v1` | `outbound_id` | opaque-uuid | NEW (DC-introduced) | Per-message identifier; audit-chain anchor across send / receipt confirmation / inbound-link |
| `outbound_message.v1` | `dc_run_id` | str | NEW (DC-introduced) | Pins the message to the DC invocation that produced it |
| `outbound_message.v1` | `recipient_id` | str | NEW (DC-introduced) | Per-recipient opaque identifier; foreign-key into consent ledger |
| `outbound_message.v1` | `channel` | Literal[5] | NEW (DC-introduced) | email / sms / voice / telegram / whatsapp |
| `outbound_message.v1` | `commitment_id_or_funder_reporting_field_id` | str | NEW (DC-introduced) | Provenance: which `proposal_commitments` entry OR `reporting_template` field this message is gathering data on |
| `outbound_message.v1` | `rendered_message_bytes_sha3_512` | hex-prefix-16 | NEW (DC-introduced) | Per-message content-hash for batch-binding (per §13.4.2 batch_content_sha3_512) |
| `outbound_message.v1` | `per_state_disclaimers_applied` | list[str] | NEW (DC-introduced) | State-rules card disclaimer IDs applied per recipient address-of-record |
| `outbound_message.v1` | `per_recipient_token_id` | str | NEW (DC-introduced) | Shared-secret token ID embedded in this message; rotates per grant cycle |
| `outbound_message.v1` | `staged_at_utc` | datetime | NEW (DC-introduced) | Compose-time timestamp; distinct from `sent_at_utc` |
| `outbound_message.v1` | `sent_at_utc` | datetime \| None | NEW (DC-introduced) | Send-time timestamp; None until operator-signed batch fires per-recipient |
| `inbound_response.v1` | `inbound_id` | opaque-uuid | NEW (DC-introduced) | Per-inbound identifier |
| `inbound_response.v1` | `dc_run_id` | str | NEW (DC-introduced) | Pins the inbound to the DC parse invocation |
| `inbound_response.v1` | `recipient_id` | str | NEW (DC-introduced) | Resolved from receipt metadata via per-channel resolver |
| `inbound_response.v1` | `channel` | Literal[5] | NEW (DC-introduced) | email / sms / voice / telegram / whatsapp |
| `inbound_response.v1` | `outbound_id_ref` | str \| None | NEW (DC-introduced) | Foreign-key to the OutboundMessage this is a response to (resolved via per-recipient token validation + per-channel threading) |
| `inbound_response.v1` | `raw_payload_sha3_512` | hex-prefix-16 | NEW (DC-introduced) | Content-hash over raw_payload bytes for tamper-detection |
| `inbound_response.v1` | `token_validated_at_utc` | datetime \| None | NEW (DC-introduced) | Per-recipient shared-secret token validation timestamp; None if token invalid (quarantine path) |
| `inbound_response.v1` | `parsed_fields` | dict[str, ParsedField] | NEW (DC-introduced) | Per-channel parser output: field_class → ParsedField{value, unit, raw_extract, parser_confidence} |
| `inbound_response.v1` | `classification_status` | Literal["UNSET","OPERATOR_CLASSIFIED","DEFAULT_CONFIDENTIAL_PENDING_REVIEW"] | NEW (DC-introduced) | Defaults `DEFAULT_CONFIDENTIAL_PENDING_REVIEW` at parse; flips to `OPERATOR_CLASSIFIED` at operator classification approval |
| `inbound_response.v1` | `kfr_drift_advisory` | KfrDriftAdvisory \| None | NEW (DC-introduced) | F-DATACOLLECTOR-KFR-DRIFT POST-output; per-field drift flag for operator reconciliation |
| `consent_ledger_entry.v1` | `recipient_id` | str | NEW (DC-introduced) | Per-recipient opaque identifier |
| `consent_ledger_entry.v1` | `channel` | Literal[5] | NEW (DC-introduced) | One ledger file per (recipient_id, channel) pair |
| `consent_ledger_entry.v1` | `consent_active` | bool | NEW (DC-introduced) | True iff consent captured + not opted out |
| `consent_ledger_entry.v1` | `consent_captured_at_utc` | datetime | NEW (DC-introduced) | When consent was captured (formal CAN-SPAM/TCPA point-in-time) |
| `consent_ledger_entry.v1` | `consent_capture_method` | Literal["award_acceptance_signed_form","opt_in_link_email","sms_double_opt_in","voice_recorded_consent","telegram_in_app_optin","whatsapp_business_optin"] | NEW (DC-introduced) | Provenance of consent capture (per-channel method) |
| `consent_ledger_entry.v1` | `opt_out_active` | bool | NEW (DC-introduced) | True iff recipient opted out post-consent; same-day enforcement; rolling-window opt-out re-acceptance disallowed without fresh consent capture |
| `consent_ledger_entry.v1` | `opt_out_at_utc` | datetime \| None | NEW (DC-introduced) | Opt-out timestamp |
| `consent_ledger_entry.v1` | `frequency_cap_lookback_days` | int | NEW (DC-introduced) | Per-recipient × per-channel rolling-window cap; default 7 |
| `consent_ledger_entry.v1` | `recent_outbound_log` | list[OutboundLogEntry] | NEW (DC-introduced) | Last `frequency_cap_lookback_days` × 2 outbound entries for this (recipient_id, channel); used by F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED PRE-gate |
| `consent_ledger_entry.v1` | `state_code_for_rules` | Literal["PA","CA","FL","TX","NY",...] \| None | NEW (DC-introduced) | Recipient's address-of-record state code; drives state-rules card lookup; None if address-of-record not on file (card fails closed in that case per §13.6.0 default) |
| `consent_ledger_entry.v1` | `audit_chain` | list[AuditChainEntry] | per v7.0.4 §1 | Audit chain initialized at consent capture; appended on each ledger mutation |
| `sub_awardee_token.v1` | `token_id` | opaque-uuid | NEW (DC-introduced) | Per-recipient shared-secret token identifier |
| `sub_awardee_token.v1` | `grant_id` | str | NEW (DC-introduced) | Token is per-grant-cycle; rotates at next grant cycle |
| `sub_awardee_token.v1` | `recipient_id` | str | NEW (DC-introduced) | Per-recipient binding |
| `sub_awardee_token.v1` | `secret_value_ciphertext` | bytes | NEW (DC-introduced) | Token secret encrypted at rest with KFR-classified-confidential key per v7.0.4 §1.1 KFR-signature discipline |
| `sub_awardee_token.v1` | `issued_at_utc` | datetime | NEW (DC-introduced) | Token issuance timestamp; equal to award acceptance time |
| `sub_awardee_token.v1` | `rotates_at_utc` | datetime | NEW (DC-introduced) | Next grant cycle boundary; token-validation past this timestamp rejects |
| `sub_awardee_token.v1` | `operator_signature` | bytes | NEW (DC-introduced) | Ed25519 signature over canonical-JSON of token record by operator key active at issued_at_utc |

Field names preserve v7.0.4 KFR + §2 v7.2 operational sub-kind + §11 v1 conventions (snake_case with substrate prefix; UTC-suffixed timestamps; `_at_utc` for datetime fields; `_id` for opaque references; `_sha3_512` for content-hash fields with hex-prefix-16 convention). Pydantic schemas live in `pipeline/orchestrator/seats/data_collector/__init__.py` per §13.15 module scaffold.

## §13.5.1 Outbound log output

**Output file.** `orgs/<slug>/data_collector/outbound_log/<grant_id>/<period_n>/<outbound_id>.yaml` — per-message YAML; one file per OutboundMessage. Pydantic-validated against `outbound_message.v1` before write. Append-only — no edit-in-place; mutations are new files with `outbound_id_supersedes` field. Mirrors §12 v1 outbound assembly log discipline.

**State file** (separate from per-message log). `orgs/<slug>/data_collector/state/<run_id>.yaml` — per-run Tilth-internal artifact per Rule 1. Includes the per-batch recipient list, per-recipient channel list, frequency cap reads, consent ledger reads, state-rules card entries applied, gate fire summary.

**Reject audit trail.** `pipeline/validation/data_collector_outbound_rejects/<org_slug>/<run_id>/<reject_id>.yaml` — one entry per F-DATACOLLECTOR-* PRE-outbound reject. Each entry includes: `attempted_message`, `recipient_id`, `channel`, `gate_code` (with sub-tag), `predicate_message`, `rejected_at_utc`.

**Operator approval surface.** `tilth data-collector review-batch --org <slug> --grant <grant_id> --period <n>` displays the staged batch with per-recipient envelope summary + per-channel + per-state-rules compliance summary + per-recipient classification routing summary + per-recipient token embedding confirmation. Per-batch action: **approve-batch** (Ed25519-sign the batch with operator key + flip status to APPROVED_FOR_SEND), **drop-recipient** (remove specific recipients from the batch; require operator reason), **revise-template-for-recipient** (operator override per-recipient template; v1.1 horizon — at v0.2 first ship templates are sealed per §13.2 Law 2), **defer-batch** (carry to next cycle review). NON-NEGOTIABLE: NO `--yes` / `--auto-confirm` / `--force` flag.

## §13.5.2 Inbound log output

**Output file.** `orgs/<slug>/data_collector/inbound_log/<grant_id>/<inbound_id>.yaml` — per-message YAML; one file per InboundResponse. Pydantic-validated against `inbound_response.v1` before write. Append-only.

**Quarantine.** `pipeline/data_collector_inbound_quarantine/<org_slug>/<reason>/<run_id>/<msg_id>.yaml` — one entry per quarantine event. Reasons: `unresolved_recipient` (recipient not in consent ledger); `grant_mismatch` (token decodes to different grant); `token_invalid` (shared-secret token validation failed); `size_overflow` (raw_payload beyond per-channel size limit); `unsolicited` (recipient resolved but no outbound thread match — operator may have ad-hoc replies to handle).

**Operator classification approval surface.** `tilth data-collector classify-inbound --org <slug> --grant <grant_id>` walks all unclassified `(recipient_id, field_class)` pairs in the inbound log for the grant. Per-pair display: parsed field value + raw extract + parser confidence + first-occurrence date. Per-pair actions: **classify** (operator selects Public / Shareable / Confidential; classification persists in classification register per v7.0.7 §4.1 + propagates to all subsequent occurrences of same `(recipient_id, field_class)` pair without re-prompt), **defer** (carry to next classify run; inbound stays in inbound_log with `classification_status: DEFAULT_CONFIDENTIAL_PENDING_REVIEW`; F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET continues to block operational-data write until classified), **quarantine** (operator flags as suspicious; moves inbound to `pipeline/data_collector_inbound_quarantine/<org_slug>/operator_flagged/`).

## §13.5.3 Consent ledger updates

**Output file.** `orgs/<slug>/data_collector/consent_ledger/<recipient_id>__<channel>.yaml` — one ledger file per `(recipient_id, channel)` pair. Pydantic-validated against `consent_ledger_entry.v1` before write. Atomic-update discipline: ledger reads + writes wrapped in `fcntl.flock(LOCK_EX)` per §15 v1 Cycle 2 NF-02 closure precedent (concurrent confirmation race closure). Audit-logged: every mutation appends to `audit_chain`.

**Cedar policy.** `pipeline/orchestrator/seats/data_collector/cedar_policies/consent_ledger_isolation.cedar`:

```
// Pseudocode; full Cedar policy realized at WS-I Code phase
permit (
    principal == DataCollectorSeat,
    action in [ConsentLedgerRead, ConsentLedgerWrite],
    resource is ConsentLedgerEntry
) when {
    resource.org_slug == principal.invocation_org_slug &&
    resource.channel in principal.invocation_channels_in_scope &&
    resource.recipient_id in principal.invocation_recipient_id_list
};

forbid (
    principal == DataCollectorSeat,
    action in [ConsentLedgerRead, ConsentLedgerWrite],
    resource is ConsentLedgerEntry
) unless {
    principal.invocation_org_slug == resource.org_slug
};
```

Cross-org ledger reads → fail-closed at Cedar layer + F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.path_cross_org sub-tag at Python predicate layer (defense-in-depth).

**Operator-driven consent management.** `tilth data-collector consent --org <slug> --recipient <recipient_id> --channel <ch> --action {capture|opt-out|inspect}` is the operator surface for ledger management. Consent capture at award acceptance is wired into `tilth intake award-ingest` follow-on (per §11 v1 §11.6.3 AWARD_INGEST mode); the follow-on step prompts operator to invoke `tilth data-collector consent --action capture` for each sub-awardee × channel combination expected for the grant's reporting cycles. Operator-signed sub-awardee token register is generated at the same step (per §13.6.0 Sub-awardee token register).

## §13.5.4 Operational-data sub-kind writes (per §2 v7.2 LOCKED schemas)

After operator classifies an inbound `(recipient_id, field_class)` pair, the inbound response's parsed fields flow into §2 v7.2 operational-data sub-kind writes:

| Inbound field_class | §2 v7.2 sub-kind | Vault target path | PII flag |
|---|---|---|---|
| numeric performance metric | `metrics` | `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/metrics/` | LOW |
| financial line item | `financials` | `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/financials/` | MEDIUM (Confidential default) |
| photo attachment | `photos` | `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/photos/` | MEDIUM (EXIF-stripped per v1.1 OQ-DC-PHOTO-EXIF) |
| free-form narrative | `narrative_entries` | `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/narrative_entries/` | MEDIUM (operator-classified per occurrence) |
| timeline event | `timeline_of_activities` | `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/timeline_of_activities/` | LOW |
| beneficiary record | `beneficiary_records` | `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/beneficiary_records/` | **HIGH (PII)** — Cedar `beneficiary_records_pii.cedar` enforcement per §2 v7.2 RT-C1 probe checklist; consent-tier-aware writes |
| non-Tilth-generated file | `attachments` | `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/attachments/` | per-attachment classification at first occurrence |

Each sub-kind write respects the §2 v7.2 Pydantic schema + Cedar policy. PII discipline on `beneficiary_records` is non-negotiable: Cedar policy denies writes that miss `consent_tier` field + denies writes where the calling principal is not `data_collector_seat`; AST-lint `R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED` extension rejects any module that writes to beneficiary_records without setting `consent_tier`.

# §13.6 Five-channel specification (per channel)

## §13.6.0 Per-channel summary table + Sub-awardee token register

| Channel | Outbound substrate | Inbound substrate | Per-state-rules layer | Consent capture method | Token embedding |
|---|---|---|---|---|---|
| **email** | SMTP via operator BYOK (Postmark / SendGrid / Mailgun candidate set per §13.8.1) | RFC822 mailbox poll OR inbound webhook (BYOK provider-specific) | CAN-SPAM unsubscribe link mandatory + per-state-required disclaimers (e.g., CA opt-out, FL telemarketing disclosure) | `opt_in_link_email` (double-opt-in flow at award acceptance) | `X-Tilth-Recipient-Token: <token_id>` custom RFC822 header + URL-encoded in unsubscribe link query string for double-source validation |
| **sms** | Twilio Messaging API or Plivo equivalent (BYOK) | Twilio webhook OR Plivo webhook | TCPA prior-express-written-consent + per-state quiet hours + per-state opt-out shortcodes (STOP / UNSUBSCRIBE / END) | `sms_double_opt_in` (recipient texts CONFIRM in response to initial opt-in SMS) | Token ID embedded as prefix-tag in SMS body: `[T:<token_id>]` + URL-shortened opt-out link as suffix |
| **voice** | Twilio Voice or operator-pinned PSTN gateway (BYOK); outbound call places automated TTS message OR connects to operator-curated IVR | Inbound voice transcription via local Whisper-class model (always-local per v7.0.7); voice mailbox + transcription pipeline | TCPA prior-express-written-consent + per-state quiet hours (8am-9pm recipient-local) + per-state automated-call disclosure scripts | `voice_recorded_consent` (audio recording of recipient's verbal opt-in, archived at `orgs/<slug>/data_collector/consent_audio/<recipient_id>__voice/<consent_capture_id>.wav`; Ed25519-signed at write) | Token ID announced verbally at message start ("Reference token <readable_token_id>") + recipient asked to repeat at inbound for token validation |
| **telegram** | MTProto bot client (shared substrate with Cultivator per §13.11) — `python-telegram-bot` or `pyrogram` per §13.8.4 BYOK | Telegram bot webhook OR long-polling update handler | Telegram ToS opt-in at first contact (in-app /start command with inline opt-in keyboard); no per-state-rules layer (Telegram is platform-mediated; ToS is the consent floor) | `telegram_in_app_optin` (recipient sends /start + clicks inline opt-in button; bot persists `chat_id` + `consent_active=True` in ledger) | Token embedded as inline-keyboard callback_data prefix + verbatim in message body for audit |
| **whatsapp** | WhatsApp Business API (Meta-issued BYOK) | WhatsApp Business inbound webhook | TCPA-equivalent prior-express consent + Meta's opt-in template requirements (24-hour conversation window after opt-in; outbound outside window requires pre-approved template) | `whatsapp_business_optin` (recipient sends initial inbound to operator's WhatsApp Business number per Meta opt-in policy; ledger records template_id used at initial outbound for compliance audit) | Token embedded in message body + as WhatsApp interactive-message header for double-source |

**Sub-awardee token register (per dispatch decision 8e default).** At award acceptance time (step downstream of `tilth intake award-ingest` per §11 v1 §11.6.3), the operator invokes `tilth data-collector issue-tokens --org <slug> --grant <grant_id>` to issue per-recipient shared-secret tokens. The CLI:

1. Reads `proposal_commitments.yaml` (with `status: PROMOTED`) to determine the recipient list (sub-awardees + grantee organizations the grant designates as reporting parties).
2. For each recipient, generates a 256-bit cryptographically random secret token; encrypts at rest using the KFR-classified-confidential key per v7.0.4 §1.1 KFR-signature discipline.
3. Writes `orgs/<slug>/data_collector/per_recipient_tokens/<grant_id>__<recipient_id>.signed.yaml` with `token_id` (opaque-uuid), `grant_id`, `recipient_id`, `secret_value_ciphertext`, `issued_at_utc`, `rotates_at_utc` (= next grant cycle boundary per funder cadence; default = `issued_at_utc + 365 days` if cadence not in `reporting_template.yaml`), and operator Ed25519 signature over canonical-JSON of the token record.
4. Operator transmits the secret token to each recipient via an out-of-band channel (mail / in-person handoff / per-recipient secure portal — Tilth does not specify the OOB channel at v0.2 first ship).
5. Token validation on inbound: per `ChannelProtocol.validate_inbound_token` (§13.4.0); each channel substrate extracts the token from the inbound payload (per-channel embedding pattern per the table above), looks up the token ciphertext in the register, decrypts with the operator key, compares against the extracted token value, validates `rotates_at_utc` is future. Match → `TokenValidationResult{valid: True, recipient_id, token_id}`. Mismatch → `TokenValidationResult{valid: False, reason: <stale|forged|mismatch>}` + quarantine path.

**Token rotation per grant cycle.** At each new grant cycle boundary, operator re-invokes `tilth data-collector issue-tokens --org <slug> --grant <grant_id> --rotate` to generate new tokens. The prior tokens remain in the register with `rotates_at_utc` set to the rotation time; inbound carrying a stale token after `rotates_at_utc` is quarantined with reason `stale_token`. Operator surface for stale-token quarantine inspection: `tilth data-collector inspect-quarantine --reason stale_token`.

**Alternative considered (per dispatch packet notes).** Per-recipient pubkey verification (asymmetric signatures over inbound messages) is cryptographically stronger than shared-secret tokens but imposes infrastructure burden on sub-awardees (each recipient needs a keypair + signing tooling). v0.2 first ship adopts shared-secret tokens; v1.1 candidate: optional asymmetric-keypair mode per recipient (sub-awardee opts in to keypair signing at award acceptance; sub-awardee retains the pubkey signing surface; Tilth verifies signatures with the recorded pubkey). Operator override possible at Audit #1.

## §13.6.1 Email channel (SMTP via BYOK)

**Outbound transport substrate.** SMTP via operator BYOK provider. v0.2 first ship candidate set: Postmark / SendGrid / Mailgun. Operator selects at white-glove per ADR-001 envelope discipline. Selection decision lives in `orgs/<slug>/data_collector/data_collector_config.yaml` `email_substrate: Literal["postmark","sendgrid","mailgun"]` field (Ed25519-signed per §13.4.1 operator-config signature discipline).

**Outbound process.** For each `OutboundMessage` in the operator-approved batch where `channel == "email"`:

1. Render the RFC822 envelope: From operator's grant-related email address-of-record (per consent_ledger.consent_capture_method = `opt_in_link_email` original opt-in); To recipient.contact_email; Subject per per-channel template; Body containing the structured question text (referencing `commitment_id_or_funder_reporting_field_id`); CAN-SPAM unsubscribe link + per-state-required disclaimers + `X-Tilth-Recipient-Token: <token_id>` custom header + URL-encoded token in unsubscribe link query string.
2. Stage the rendered RFC822 bytes; compute SHA3-512; write per-recipient outbound log entry with `staged_at_utc`.
3. After operator-signed batch fires per-recipient: send via SMTP through the BYOK provider's API; capture provider response (message_id, accepted/rejected status); flip outbound log entry `sent_at_utc`; persist provider message_id for inbound threading.
4. Inbound webhook (provider-specific): provider POSTs RFC822 bytes + envelope metadata to Tilth's inbound webhook endpoint (localhost-bound only per v7.0.7 §4.1 + §13.10 routing posture). Tilth's email_channel module receives, parses via `email.parser.BytesParser` standard library, extracts the `X-Tilth-Recipient-Token` header + unsubscribe-link token, validates token, threads to outbound via `In-Reply-To` + `References` headers, writes inbound log entry.

**Per-state-rules layer.** State-rules card entries for `email` channel: each state's card YAML carries `email_disclaimers: list[StateDisclaimer]` field; disclaimers are appended verbatim to the outbound body. CAN-SPAM unsubscribe link is mandatory at every outbound regardless of state; per-state additional disclaimers (e.g., CA opt-out language for marketing-classified emails) layer on top.

## §13.6.2 SMS channel (Twilio/Plivo BYOK)

**Outbound transport substrate.** Twilio Messaging API or Plivo equivalent. v0.2 first ship candidate set: Twilio (preferred — most coverage), Plivo (alternative). Operator selects at white-glove. Selection decision in `data_collector_config.yaml` `sms_substrate: Literal["twilio","plivo"]`.

**Outbound process.** For each `OutboundMessage` in the operator-approved batch where `channel == "sms"`:

1. Render the SMS body: token ID embedded as prefix-tag `[T:<token_id>]`; structured question text; URL-shortened opt-out link as suffix (`STOP to opt out: <shortlink>`). SMS body bounded by 1600 bytes (160 SMS segments × 7-bit GSM-7 max; concatenated SMS). If rendered body exceeds bound, the per-channel template author at substrate-freeze time has miscalibrated — fail-closed at compose time with `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.sms_size_overflow` (sub-tag of consolidated check; sub-tag chosen because oversized SMS truncation is a leak vector — TOS-mandated disclaimer truncation = compliance violation).
2. Stage rendered body bytes; compute SHA3-512; write outbound log entry.
3. After operator-signed batch fires: send via Twilio/Plivo API; capture `sid` / `message_uuid` (provider response); flip `sent_at_utc`.
4. Inbound webhook: provider POSTs `From` (recipient phone) + `Body` (SMS text) + `MessageSid` to Tilth's inbound webhook endpoint (localhost-bound). Tilth's sms_channel module receives, parses `Body` to extract `[T:<token_id>]` prefix-tag, validates token, threads inbound to outbound via per-recipient phone + token, writes inbound log entry.

**STOP shortcode handling.** Per TCPA + per-state opt-out shortcode requirements, inbound `STOP` / `UNSUBSCRIBE` / `END` / `QUIT` / `CANCEL` (case-insensitive) on the SMS channel triggers immediate consent ledger update: `opt_out_active=True, opt_out_at_utc=received_at_utc`. Same-day enforcement — no further outbound to this recipient on this channel until fresh consent capture. Per-recipient atomic ledger write per §13.5.3 atomic-update discipline.

**Per-state-rules layer.** State card entries for `sms`: each state's card carries `sms_quiet_hours: tuple[time, time]` (recipient-local time window; outside window = quiet hours, no outbound permitted); `sms_required_opt_out_shortcodes: list[str]` (state-specific opt-out language); `sms_minimum_consent_age_days: int` (some states require consent re-capture annually). PA = 7am-9pm recipient-local; CA = 8am-9pm + annual re-capture; FL = 8am-8pm + per-call automated disclosure; TX = 9am-9pm + automated message identification; NY = 8am-9pm + opt-out shortcode acknowledged within 24h.

## §13.6.3 Voice channel (Twilio Voice + local Whisper transcription)

**Outbound transport substrate.** Twilio Voice API or operator-pinned PSTN gateway (BYOK). v0.2 first ship: Twilio Voice preferred. Selection decision in `data_collector_config.yaml` `voice_substrate: Literal["twilio_voice","operator_pinned_pstn"]`.

**Outbound process.** Outbound voice is automated TTS-driven OR connects to an operator-curated IVR (interactive voice response) flow per the operator's preference at white-glove (per-org override in config). At v0.2 first ship the default is automated TTS — Twilio TTS reads a per-channel template-rendered message script aloud over the call. IVR mode is a v1.1 candidate.

1. Render the outbound voice script: token ID announced verbatim ("Reference token <readable_token_id>"); structured question (TTS-readable phrasing); recipient asked to respond by speaking after the tone (Twilio Studio-equivalent flow) OR by pressing keypad digits (DTMF capture for numeric responses).
2. Stage rendered script + Twilio Studio flow ID; compute SHA3-512 over rendered script; write outbound log entry.
3. After operator-signed batch fires: place outbound call via Twilio Voice API; Twilio records the call; webhook fires on call completion with recording URL.
4. Inbound webhook: Twilio POSTs recording URL + DTMF capture (if any) to Tilth's inbound webhook (localhost-bound). Tilth's voice_channel module fetches the recording bytes (cached locally; never re-fetched from Twilio after first fetch per ADR-001 substrate freeze); invokes the local Whisper-class transcription model (per §13.8.3 substrate); produces transcript bytes + parsed field extraction (Pydantic AI agent over the transcript with per-channel inbound prompt + bge-large-en-v1.5 embedding for semantic matching of expected fields). Token validation: the recipient's spoken token (or DTMF entry) is extracted from the transcript / DTMF capture; validated against the token register. Inbound log entry written.

**Voice transcription is always-local per v7.0.7 §4.1.** The local Whisper-class model runs on operator hardware (M1 8GB dev floor; Mac Studio 128GB production); no cloud transcription service. F-CLASS-ROUTING-INDETERMINATE PRE-call fail-closes any voice transcription call where the transcription endpoint resolves to anything other than localhost or unix:// socket (mirrors §11 v1 §11.9.10 RT-13 sealed-embedding-endpoint discipline).

**Per-state-rules layer.** State card entries for `voice`: `voice_quiet_hours: tuple[time, time]`; `voice_automated_call_disclosure_script: str` (state-specific automated-call disclosure read at call start, e.g., FL's "This is a pre-recorded message from..." opener); `voice_state_dnc_check_required: bool` (states with state-specific DNC registries require pre-call DNC lookup — operator-curated DNC-check substrate decision at v1.1; v0.2 first ship treats `True` as advisory only with operator manual DNC scrub responsibility).

**Voice mailbox handling.** If recipient does not answer + voicemail picks up, Twilio detects and Tilth's voice_channel records the answered-by-voicemail event; recipient's outbound log entry flags `voice_mailbox_response_active=True`; inbound is treated as an unsolicited voicemail (operator decides at classify-inbound surface whether to count the voicemail as the recipient's response or to retry the outbound on next batch cycle).

## §13.6.4 Telegram channel (MTProto bot — shared substrate with Cultivator)

**Outbound transport substrate.** MTProto bot client via `python-telegram-bot` library or `pyrogram` library (BYOK MTProto API keys — operator registers a single Telegram application per the operator's account at white-glove). Substrate is shared with Cultivator per §13.11; per-purpose session storage partitioning isolates Data Collector's audience from Cultivator's.

**Outbound process.** For each `OutboundMessage` in the operator-approved batch where `channel == "telegram"`:

1. Resolve recipient `chat_id` from consent ledger (consent captured at first /start interaction; ledger persists `chat_id` per recipient × per channel).
2. Render the outbound message body: structured question text; token embedded verbatim in body for audit; inline keyboard with response options (when applicable) carrying `callback_data` prefixed with `token_id`.
3. Stage rendered body; compute SHA3-512; write outbound log entry.
4. After operator-signed batch fires: send via bot.send_message(chat_id=<resolved>, text=<rendered>, reply_markup=<inline_keyboard>); capture Telegram `message_id`; flip `sent_at_utc`.
5. Inbound update handler: Telegram POSTs update bytes to Tilth's inbound webhook (localhost-bound) OR long-polling get_updates loop receives. Tilth's telegram_channel module parses the update via `python-telegram-bot.Update.de_json`; threads via `reply_to_message_id` matching outbound `message_id`; extracts token from inline-keyboard callback_data OR from message body; validates token; writes inbound log entry.

**/start opt-in flow.** Recipient first sends `/start` to the bot. Bot replies with opt-in inline keyboard ("Opt in" / "Decline"). Recipient clicks "Opt in" → consent_ledger entry written with `consent_capture_method=telegram_in_app_optin` + `consent_active=True` + chat_id persisted. Recipient clicks "Decline" → no ledger entry written (silent rejection; recipient can re-engage by sending /start later).

**Per-state-rules layer.** Telegram is platform-mediated; Telegram ToS is the consent floor. v0.2 first ship: no per-state-rules layer applied on Telegram (rationale: recipients consent via Telegram's own opt-in flow + platform ToS; per-state TCPA/CAN-SPAM-equivalent rules do not apply to platform-mediated messaging in the same way they apply to email/SMS/voice). v1.1 candidate: per-state operator-curated overrides if state-level platform-messaging rules emerge.

**Cross-org isolation on shared MTProto substrate.** Per §13.11 — substrate code (`python-telegram-bot.Bot`) is shared between Data Collector + Cultivator; per-purpose session storage paths are non-overlapping (`orgs/<slug>/data_collector/mtproto_session/<bot_session_id>.session` vs `orgs/<slug>/cultivator/mtproto_session/<bot_session_id>.session`); each org's session is path-segmented per org; the bot framework module MUST receive `org_slug` as a required parameter on every send/receive call; F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND `.mtproto_cross_org` sub-tag fail-closes any send where `recipient_id` is registered to a different `org_slug` than the invocation's bundle.

## §13.6.5 WhatsApp channel (WhatsApp Business API)

**Outbound transport substrate.** WhatsApp Business API (Meta-issued BYOK; operator obtains via Meta Business Manager + WhatsApp Business Account registration). Per ADR-001 substrate freeze: the WhatsApp Business Python client library is frozen at Golden Image build; v0.2 first ship candidate: `heyoo` or `whatsapp-business-cloud-api` (operator-selected at white-glove).

**Outbound process.** For each `OutboundMessage` in the operator-approved batch where `channel == "whatsapp"`:

1. Check Meta's 24-hour conversation window: if recipient's most recent inbound was within last 24 hours, free-form template can be sent. If not, only pre-approved templates can be sent (Meta requires template pre-approval for marketing-classified outbound outside the 24h window).
2. Render the outbound message body: structured question text; token embedded verbatim in body; for interactive-message variants (list / button), token also embedded as WhatsApp interactive-message header.
3. Stage rendered body + template_id (if pre-approved-template path); compute SHA3-512; write outbound log entry.
4. After operator-signed batch fires: send via WhatsApp Business API; capture `wamid` (WhatsApp message ID); flip `sent_at_utc`.
5. Inbound webhook: Meta's WhatsApp Business Cloud POSTs inbound webhook to Tilth's inbound webhook (localhost-bound). Tilth's whatsapp_channel module parses the webhook payload, extracts token from message body + interactive header (double-source validation), validates, threads via `context.message_id` matching outbound `wamid`, writes inbound log entry.

**Per-state-rules layer.** WhatsApp is platform-mediated; Meta's policies are the floor. TCPA per-state quiet hours apply to WhatsApp messaging per the same logic as SMS (FCC has not exempted platform-mediated messaging from TCPA quiet-hour rules); v0.2 first ship: state card entries for `whatsapp` mirror `sms_quiet_hours`. Per-state-required disclaimers may also apply (e.g., CA opt-out language for marketing-classified WhatsApp messages); card entries carry `whatsapp_disclaimers: list[StateDisclaimer]` field.

**Template pre-approval discipline.** Pre-approved templates are registered in `orgs/<slug>/data_collector/whatsapp_template_register/<template_id>.signed.yaml` (Ed25519-signed by operator at first registration; per-template registration includes Meta's `template_name`, `language_code`, `category`, `body_text`, `header_text`, `footer_text`, `button_actions`). Outbound that needs the pre-approved-template path looks up `template_id` in the register; mismatch (template not pre-approved per Meta) → `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.whatsapp_template_unapproved` (sub-tag; chosen because unapproved-template-outbound risks account-level Meta enforcement = operator-grade exposure).

# §13.7 Operator approval UX (per-cycle outbound batch)

The per-cycle outbound batch operator approval surface is the load-bearing UX for §13. This section covers the BULK + INCREMENTAL operator-review surface in detail; inbound classification surface is at §13.5.2.

**Surface entry.** `tilth data-collector review-batch --org <slug> --grant <grant_id> --period <n>` displays the staged batch produced by `compose-batch` (per §13.4.1). Per-batch summary: total recipient count by channel; per-channel consent ledger summary (X recipients consent_active=True, Y opt_out_active=True or frequency_cap_hit, Z address-of-record state code unset); per-state-rules card summary (which states' disclaimers applied to how many messages); per-recipient classification routing summary (X messages cloud-routable, Y always-local); per-recipient token embedding confirmation (every message MUST embed token; staging-time validation enforces — operator review confirms structural integrity).

**Per-recipient detail view.** Operator drills into per-recipient detail: rendered message bytes (sandboxed display — no live message send); applied state disclaimers; consent ledger entry summary; per-recipient token preview (token_id only, not secret value); F-DATACOLLECTOR-* gate fire summary (any gates that fired pre-stage are surfaced even if recipient already excluded — operator sees the full audit picture).

**Operator actions.**

1. **approve-batch** — operator inspects, signs the batch envelope with Ed25519 key, writes `signed_batch_path` (per §13.4.2 input contract) with `batch_status: APPROVED_FOR_SEND` + `batch_content_sha3_512` + operator signature. NON-NEGOTIABLE: this requires interactive TTY (per §13.4.2 TTY check); `--yes` / `--auto-confirm` / `--force` argparse-rejected.
2. **drop-recipient** — operator removes specific recipients from the batch; CLI prompts for operator reason (e.g., "deferred to next cycle"); reason persists in `data_collector_state.yaml` audit trail; remaining batch re-stages with new `batch_content_sha3_512`.
3. **revise-template-for-recipient** — v1.1 horizon. Out of scope at v0.2 first ship.
4. **defer-batch** — operator decides to skip this cycle; batch re-stages at next compose-batch invocation; per-recipient consent ledger frequency-cap-lookback counters are NOT incremented (defer ≠ send).

**TTY check is structural** (mirrors §11 v1 §11.7 RT-08 closure pattern). Non-TTY invocation of `review-batch` + `approve-batch` is argparse-rejected. The "one keystroke" approve-batch action requires interactive terminal; cannot be scripted away.

**Operator signature requirement.** Approve-batch action requires operator Ed25519 signature per Section 4 §4.5 `verify_claim_evidence_map` discipline (mirrors §11 v1 §11.7 operator key requirement). The signed batch envelope persists at `orgs/<slug>/data_collector/staged_batches/<grant_id>__period_<n>__<batch_id>.signed.yaml`. Subsequent `send-batch` invocation reads this signed file and verifies the signature at PRE-gate.

**Resumability.** Per Rule 1, the review session is resumable. Partial-approve state persists in `data_collector_state.yaml`. Operator can exit mid-review and resume; previously-approved recipients persist their approval status; previously-dropped recipients persist drop reason; un-acted-on recipients re-appear in next review session.

**Layer-defense against silent-auto-send.** The "no autosend code path" structural enforcement is a four-layer defense (mirrors §11 v1 §11.7 autopromote-batch four-layer pattern):

1. **Layer 1 — AST-lint.** `R-DATACOLLECTOR-NO-AUTOSEND` extension rejects any module that invokes `<channel>_channel.send(...)` outside `outbound_batch.py::dispatch_after_operator_approval`. Compile-time enforcement.
2. **Layer 2 — Dispatcher signature check.** `dispatch_after_operator_approval` verifies Ed25519 signature on `operator_batch_signature` parameter at function entry; signature-invalid → return `SendResult{sent: False, reason: "operator_signature_invalid"}` without invoking transport substrate. Runtime enforcement.
3. **Layer 3 — Cedar policy.** `data_collector_send.cedar` permits send action only when calling principal carries `operator_batch_signature_verified=True` attribute set by the dispatcher; without that attribute → Cedar fail-closed.
4. **Layer 4 — TTY check.** Approve-batch CLI requires interactive TTY; non-TTY argparse-reject.

Removing any single layer creates a silent-send path; all four are structural at v0.2 first ship.

# §13.8 Substrate

## §13.8.1 Email substrate (SMTP via BYOK)

**Library.** `smtplib` standard library + per-BYOK provider Python client (Postmark `postmark-python` / SendGrid `sendgrid-python` / Mailgun `mailgun.py` candidate set; operator-selected at white-glove per ADR-001 envelope discipline; frozen at Golden Image build; no marketplace access from appliance).

**Endpoint validation.** Per-provider API endpoint MUST resolve to the provider's documented endpoint (Postmark: `api.postmarkapp.com`; SendGrid: `api.sendgrid.com`; Mailgun: `api.mailgun.net` or operator-pinned EU/US region). F-CLASS-ROUTING-INDETERMINATE PRE-call fail-closes any cloud-routed call where the endpoint resolves to anything else (anti-phone-home discipline; mirrors §11 v1 §11.9.10 RT-13 sealed-endpoint pattern but applied to per-provider API endpoints rather than localhost).

**BYOK key storage.** Per-provider API key stored in `orgs/<slug>/data_collector/byok_keys/email__<provider>.encrypted.yaml` (encrypted at rest using KFR-classified-confidential key per v7.0.4 §1.1). Operator-signed at write.

## §13.8.2 SMS substrate (Twilio/Plivo BYOK)

**Library.** Twilio: `twilio-python`. Plivo: `plivo-python`. Operator selects; frozen at Golden Image build.

**Endpoint validation.** Twilio: `api.twilio.com`. Plivo: `api.plivo.com`. F-CLASS-ROUTING-INDETERMINATE enforces.

**BYOK.** Per-provider Account SID + Auth Token stored encrypted at `orgs/<slug>/data_collector/byok_keys/sms__<provider>.encrypted.yaml`.

## §13.8.3 Voice substrate (Twilio Voice + local Whisper)

**Outbound library.** `twilio-python` (Twilio Voice) or operator-pinned PSTN gateway client. Frozen at Golden Image build.

**Inbound transcription library.** `whisper.cpp` Python bindings OR `faster-whisper` (CTranslate2-accelerated Whisper inference; runs on M1 / Apple Silicon; suitable for 8GB dev floor with `tiny.en` model or 128GB production with `medium.en`+ models). Operator-selected at white-glove; frozen at Golden Image build per ADR-001.

**Endpoint validation.** Outbound: `api.twilio.com`. Inbound transcription: localhost-bound only (`http://localhost:<port>/transcribe` OR `unix:///tmp/whisper.sock` OR in-process Python binding). F-CLASS-ROUTING-INDETERMINATE PRE-call fail-closes any cloud-transcription endpoint (mirrors §11 v1 §11.9.10 RT-13 sealed-embedding-endpoint discipline applied to transcription endpoint).

**Whisper model selection.** v0.2 first ship default: `tiny.en` (39M parameters; runs on 8GB M1 in ~3 seconds per minute of audio); production override: `base.en` (74M) / `small.en` (244M) / `medium.en` (769M) / `large-v3` (1550M) per operator hardware tier (128GB production tier supports `large-v3`). Operator selection lives in `data_collector_config.yaml` `whisper_model_size: Literal["tiny.en","base.en","small.en","medium.en","large-v3"]`.

## §13.8.4 Telegram substrate (MTProto bot — shared with Cultivator)

**Library.** `python-telegram-bot` (v20+) OR `pyrogram`. Operator-selected at white-glove; frozen at Golden Image build. v0.2 first ship default: `python-telegram-bot` (broader maintenance + standard library compatibility).

**Endpoint validation.** Telegram Bot API: `api.telegram.org`. F-CLASS-ROUTING-INDETERMINATE enforces.

**BYOK.** Telegram Bot API token (single token per operator's Telegram application; shared between Data Collector + Cultivator per §13.11) stored encrypted at `vault_shared/data_collector/byok_keys/telegram_bot_token.encrypted.yaml` (workspace-shared because the token is per-operator-application, not per-org; per-org session storage is path-segmented per §13.11).

**Session storage.** Per-org per-purpose path: `orgs/<slug>/data_collector/mtproto_session/<bot_session_id>.session` (data_collector) and `orgs/<slug>/cultivator/mtproto_session/<bot_session_id>.session` (cultivator). Non-overlapping by construction. AST-lint `R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT` rejects any Data Collector code path that imports `cultivator.consent_ledger.*` or vice versa.

## §13.8.5 WhatsApp substrate (WhatsApp Business API)

**Library.** `heyoo` OR `whatsapp-business-cloud-api`. Operator-selected at white-glove; frozen at Golden Image build.

**Endpoint validation.** WhatsApp Business Cloud API: `graph.facebook.com` (Meta-hosted). F-CLASS-ROUTING-INDETERMINATE enforces.

**BYOK.** WhatsApp Business Account access token + phone_number_id stored encrypted at `orgs/<slug>/data_collector/byok_keys/whatsapp_business.encrypted.yaml`.

## §13.8.6 Consent ledger substrate (per-org YAML + Cedar)

**Storage.** Per-recipient-per-channel YAML files under `orgs/<slug>/data_collector/consent_ledger/<recipient_id>__<channel>.yaml`. Pydantic-validated against `consent_ledger_entry.v1` (per §13.5.3 schema). Atomic-update via `fcntl.flock(LOCK_EX)` (mirrors §15 v1 Cycle 2 NF-02 concurrent-confirmation-race closure).

**Cedar policy.** `pipeline/orchestrator/seats/data_collector/cedar_policies/consent_ledger_isolation.cedar` (per §13.5.3 pseudocode; full realization at WS-I Code phase).

## §13.8.7 State-rules card substrate (workspace-shared, Ed25519-signed by SN-LLC)

**Storage.** Workspace-shared `vault_shared/state_rules_card/<state_code>.yaml`. PA / CA / FL / TX / NY at v0.2 first wave. Each card YAML carries: `state_code`, `email_disclaimers`, `sms_quiet_hours`, `sms_required_opt_out_shortcodes`, `sms_minimum_consent_age_days`, `voice_quiet_hours`, `voice_automated_call_disclosure_script`, `voice_state_dnc_check_required`, `whatsapp_disclaimers`, `whatsapp_quiet_hours`, `card_version`, `signed_by_sn_llc_at_utc`, `signed_by_sn_llc_pubkey_fingerprint`, `signature: bytes` (Ed25519 over canonical-JSON of card content).

**SN-LLC signature verification.** Per v7.0.7 §6.1 router-template-update Ed25519 signature pattern, each card is signed by SN-LLC at release. The Golden Quill verifies the signature against the white-glove-pinned SN-LLC public key BEFORE applying any card update — failure → F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND `.state_card_signature_invalid` sub-tag fail-closes (chosen because applying an invalid card = applying wrong rules = potential per-state-law violation = leak surface).

**Operator opt-in per state.** Operator opts in per state at white-glove via `tilth data-collector opt-in-state --state <code>`. Opt-in records to `orgs/<slug>/data_collector/state_rules_opt_ins.signed.yaml` (Ed25519-signed by operator). Only opted-in states' cards are applied at outbound compose; recipients with `state_code_for_rules` set to a non-opted-in state fail-closed at compose with operator notification ("Recipient X has address-of-record in state Y which is not opted in; opt in via `tilth data-collector opt-in-state --state Y` or remove recipient from batch").

**Card update cadence.** SN-LLC ships card updates per its router-template-update commitment (quarterly review minimum; 7-day emergency updates for meaningful regulatory changes per v7.0.7 §6 substrate update commitment). Per-deployment card files do NOT auto-update; operator opts in per release via `tilth data-collector update-state-cards` which verifies Ed25519 signature on each updated card BEFORE replacing on-disk versions.

## §13.8.8 Sub-awardee token register substrate (per-org-per-grant, Ed25519-signed by operator)

**Storage.** Per-recipient-per-grant YAML files under `orgs/<slug>/data_collector/per_recipient_tokens/<grant_id>__<recipient_id>.signed.yaml`. Pydantic-validated against `sub_awardee_token.v1` (per §13.5.0 schema delta).

**Operator-signed at issuance.** Per §13.6.0 sub-awardee token register issuance discipline.

**Encryption at rest.** `secret_value_ciphertext` encrypted using KFR-classified-confidential key per v7.0.4 §1.1 KFR-signature discipline. Decryption only at token-validation time (per `ChannelProtocol.validate_inbound_token`).

# §13.9 Logician gate family — F-DATACOLLECTOR-*

Data Collector activates six gates from §4 v2.x §5.1 HORIZON registration into live PRE/POST positions at this §13 v1 LOCK. All gates are deterministic (Python predicates + Cedar policies); zero token cost (apart from the per-channel transport substrate calls which are bounded by per-channel size limits + operator-approved-batch dispatch).

**v1 gate roster (6 codes — activated from §4 v2.x §5.1 HORIZON rows at this LOCK):**

| # | Code | Position | Owner-§ | Notes |
|---|------|----------|---------|-------|
| 1 | F-DATACOLLECTOR-CONSENT-MISSING | PRE pre-outbound | §13.9.1 | Refuses outbound where consent ledger row absent OR consent_active=False OR consent capture method missing. Sub-tags `.ledger_absent`, `.consent_inactive`, `.method_unset`, `.config_signature_invalid` (from operator-config signature discipline §13.4.1 RT-07 mirror). |
| 2 | F-DATACOLLECTOR-OPT-OUT-ACTIVE | PRE pre-outbound | §13.9.2 | Refuses outbound where recipient opted out post-consent. Sub-tags `.opt_out_active_email`, `.opt_out_active_sms`, `.opt_out_active_voice`, `.opt_out_active_telegram`, `.opt_out_active_whatsapp`. |
| 3 | F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED | PRE pre-outbound | §13.9.3 | Refuses outbound where per-state per-channel frequency cap hit OR per-recipient per-channel rolling-window cap hit. Sub-tags `.recipient_channel_cap`, `.state_cap`, `.channel_switching_evasion`. |
| 4 | F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND | PRE pre-outbound + POST inbound + PRE write | §13.9.4 | Consolidated check: outbound PII leak (semantic-slot-name detection mirror of F-CLASS-SLOT-ID-NON-OPAQUE) + inbound token-spoofing detection + cross-org path leak detection + MTProto cross-org isolation + SMS size overflow + WhatsApp template unapproved + state card signature invalid + batch hash mismatch + symlink escape + path cross-org. Sub-tags per §13.9.4 detail. |
| 5 | F-DATACOLLECTOR-KFR-DRIFT | POST inbound write | §13.9.5 | Advisory drift flag against KFR (operator-routed; not fail-closed). Sub-tags `.numeric_field_above_tolerance`, `.numeric_field_below_tolerance`, `.unit_mismatch`. |
| 6 | F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET | PRE pre-write | §13.9.6 | Refuses inbound write to operational-data sub-kind where classification has not been operator-set for this `(recipient_id, field_class)` pair. Sub-tags `.first_occurrence_unclassified`, `.default_confidential_pending_review`. |

## §13.9.0 Consolidated PRE-outbound check callable (per §4 v2.2 consolidated-check pattern)

Per §4 v2.2 consolidated-check-callable pattern + the §15 v1 §15.9 consolidated proposes-only check pattern + the §11 v1 §11.9.NEW pre-gate-check consolidation pattern, the four PRE-outbound gates (F-DATACOLLECTOR-CONSENT-MISSING + F-DATACOLLECTOR-OPT-OUT-ACTIVE + F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED + F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND) consolidate into a single check callable `data_collector.pre_gate.compose_send_validation.v1` that runs all four predicates in PRE-outbound sequence:

1. F-DATACOLLECTOR-CONSENT-MISSING (consent ledger read; consent_active check; config signature check)
2. F-DATACOLLECTOR-OPT-OUT-ACTIVE (opt-out flag check per channel)
3. F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED (frequency cap rolling-window count)
4. F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND (semantic-slot detection + cross-org path check + state card sig check + SMS size + WhatsApp template + MTProto cross-org)

Short-circuit: an earlier failure short-circuits the chain (no point checking frequency cap on a recipient whose consent is absent). Distinct sub-tags per failure code; the consolidated callable returns the first-fired sub-tag.

The two non-outbound gates (F-DATACOLLECTOR-KFR-DRIFT POST-inbound + F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET PRE-write) each have their own check callable per §13.9.5 + §13.9.6.

## §13.9.1 F-DATACOLLECTOR-CONSENT-MISSING (PRE pre-outbound)

**Purpose.** Refuse outbound where the consent ledger row is absent, where consent is no longer active, or where consent capture method is unset.

**Predicate.**

1. Read `orgs/<slug>/data_collector/consent_ledger/<recipient_id>__<channel>.yaml` via Vault read intent (`vault_read_intent_consent_ledger`). Cedar policy `consent_ledger_isolation.cedar` enforces per §13.5.3.
2. If file does not exist → fire sub-tag `.ledger_absent`.
3. Pydantic-validate against `consent_ledger_entry.v1`. Schema-invalid → fire sub-tag `.schema_invalid` (audit-trail-discoverable; indicates ledger corruption or schema-version mismatch).
4. Check `consent_active == True`. False → fire sub-tag `.consent_inactive`.
5. Check `consent_capture_method` is set (one of the six enumerated values per `consent_ledger_entry.v1`). Unset → fire sub-tag `.method_unset`.
6. Check `data_collector_config.yaml` signature if file exists (per §13.4.1 operator-config Ed25519 discipline). Signature missing/invalid/retired-key → fire sub-tag `.config_signature_invalid`.
7. Return PASS iff all checks pass.

**Position.** PRE pre-outbound. Runs in `compose_outbound` per the consolidated callable §13.9.0 sequence (position 1 of 4).

**Severity.** HIGH. `LAW3_VIOLATION` admin-risk-ledger kind (operator-grade legal exposure — CAN-SPAM / TCPA / per-state-rules violation).

## §13.9.2 F-DATACOLLECTOR-OPT-OUT-ACTIVE (PRE pre-outbound)

**Purpose.** Refuse outbound where recipient opted out post-consent. Same-day enforcement; rolling-window opt-out re-acceptance disallowed without fresh consent capture.

**Predicate.**

1. Read consent ledger row (already read in §13.9.1; consolidated callable shares the read).
2. Check `opt_out_active == False`. True → fire sub-tag per channel (`.opt_out_active_email` / `.opt_out_active_sms` / `.opt_out_active_voice` / `.opt_out_active_telegram` / `.opt_out_active_whatsapp`).
3. Return PASS iff opt_out_active is False.

**Position.** PRE pre-outbound. Position 2 of 4 in consolidated callable §13.9.0.

**Severity.** HIGH. `LAW3_VIOLATION` admin-risk-ledger kind.

**Same-day enforcement discipline.** When an inbound STOP/UNSUBSCRIBE/END signal is received on any channel, the consent ledger is updated atomically per §13.5.3 (`fcntl.flock(LOCK_EX)` per §15 v1 Cycle 2 NF-02 closure precedent) with `opt_out_active=True, opt_out_at_utc=received_at_utc`. The lock serializes concurrent send + opt-out paths — a send in flight when an opt-out arrives either (a) sees the pre-opt-out ledger and proceeds (race lost), or (b) blocks at the lock until opt-out write completes then sees opt_out_active=True and fail-closes (race won). Lock-acquisition timeout 30 seconds → fail-closed (mirrors §15 v1 NF-02 closure timeout).

## §13.9.3 F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED (PRE pre-outbound)

**Purpose.** Refuse outbound where per-state-or-default per-channel frequency cap hit. Default cap: 1 outbound per recipient per channel per 7 days. Per-state-rules card can override per state (some states have stricter caps).

**Predicate.**

1. Read consent ledger row's `recent_outbound_log` field (already read in §13.9.1).
2. Count entries within `now() - frequency_cap_lookback_days` window for this `(recipient_id, channel)` pair.
3. Per-state-rules card for recipient's `state_code_for_rules` may carry a `<channel>_min_interval_hours` field; if set, also check that the most recent outbound was at least `min_interval_hours` ago.
4. Cap exceeded → fire sub-tag `.recipient_channel_cap` (default cap) OR `.state_cap` (per-state card override).
5. **Channel-switching evasion check** — if the recipient has any outbound on a DIFFERENT channel within the lookback window AND the operator has marked `channel_switching_evasion_strict=True` in `data_collector_config.yaml` (default: False at v0.2 first ship; operator opts in per-org), fire sub-tag `.channel_switching_evasion`. Rationale: an attacker could try to evade per-channel caps by alternating SMS / email / voice; strict mode caps aggregate cross-channel outbound. Default off to avoid surprising operators who legitimately use multi-channel outreach.
6. Return PASS iff cap not exceeded.

**Position.** PRE pre-outbound. Position 3 of 4 in consolidated callable §13.9.0.

**Severity.** MEDIUM (default cap) / HIGH (state cap or channel-switching-evasion-strict).

## §13.9.4 F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND (PRE pre-outbound + POST inbound + PRE write)

**Purpose.** Consolidated leak-detection gate covering outbound PII leak, inbound token-spoofing, cross-org path leak, MTProto cross-org isolation, SMS size overflow, WhatsApp template unapproved, state card signature invalid, batch hash mismatch, symlink escape, path cross-org. The "leak surface" is the broad-strokes envelope of "any code path that could expose data outside the per-org consent-bounded recipient set."

**Predicate.** Branches per sub-tag:

**Branch — outbound semantic-slot detection (`.semantic_slot_in_outbound`).** Mirror of F-CLASS-SLOT-ID-NON-OPAQUE (v7.0.7 §4.1). Outbound message body MUST NOT contain semantic slot names of the form `[SLOT_<NAME>]` where `<NAME>` is anything other than a numeric ID. Regex `\[SLOT_([A-Z_]+)\]` matched against rendered message bytes → fire sub-tag. Closes the path where a per-recipient template inadvertently leaks the slot's semantic meaning (e.g., `[SLOT_ANNUAL_REVENUE]` reveals the Confidential field name even before slot-fill happens).

**Branch — cross-org path leak (`.path_cross_org` + `.symlink_escape`).** All vault path reads/writes `Path.resolve()` under `orgs/<org_slug>/` (per-org) or `vault_shared/` (workspace). Symlink escape → `.symlink_escape`. Path resolution outside allowed subtree → `.path_cross_org`.

**Branch — MTProto cross-org isolation (`.mtproto_cross_org`).** Telegram channel sends MUST receive `org_slug` as a required parameter; recipient's `chat_id` resolves to consent ledger entry in `orgs/<org_slug>/data_collector/consent_ledger/`. If `chat_id` resolves to a DIFFERENT `org_slug` → fail-closed (covers the case where the shared MTProto substrate accidentally crosses orgs).

**Branch — SMS size overflow (`.sms_size_overflow`).** Per §13.6.2 SMS body size bound (1600 bytes / 160 SMS segments × 7-bit GSM-7 max).

**Branch — WhatsApp template unapproved (`.whatsapp_template_unapproved`).** Per §13.6.5 — WhatsApp outbound outside 24h conversation window requires pre-approved template; outbound that needs the pre-approved-template path MUST have `template_id` registered in `orgs/<slug>/data_collector/whatsapp_template_register/`; mismatch → fail-closed.

**Branch — state card signature invalid (`.state_card_signature_invalid`).** Per §13.8.7 — state card YAML files MUST be Ed25519-signed by SN-LLC's white-glove-pinned public key; signature missing/invalid → fail-closed.

**Branch — batch hash mismatch (`.batch_hash_mismatch`).** Per §13.4.2 — signed batch envelope carries `batch_content_sha3_512` over per-recipient OutboundMessage rendered-bytes manifest; send-time recomputation + comparison.

**Branch — inbound token-spoofing (`.token_invalid_inbound`).** Per §13.6.0 + per `ChannelProtocol.validate_inbound_token` — inbound that carries an invalid token (decryption fails, mismatch against register, past `rotates_at_utc`) → fail-closed; inbound quarantined.

**Branch — operator-config signature (`.config_signature_invalid`).** Per §13.4.1 — `data_collector_config.yaml` Ed25519 signature check. (Also surfaced in §13.9.1 `.config_signature_invalid` sub-tag; the consolidated check callable fires the first matching sub-tag.)

**Position.** PRE pre-outbound (branches: semantic_slot + path_cross_org + symlink_escape + MTProto_cross_org + SMS_size + WhatsApp_template + state_card_sig + batch_hash + config_sig) + POST inbound (branch: token_invalid_inbound) + PRE write (branches: path_cross_org for write paths).

**Severity.** HIGH across all branches. `LAW3_VIOLATION` / `TAMPER_EVENT` / `SOVEREIGNTY_VIOLATION` admin-risk-ledger kinds per branch.

## §13.9.5 F-DATACOLLECTOR-KFR-DRIFT (POST inbound write)

**Purpose.** Advisory drift flag — inbound numeric responses that drift from KFR-derived expected values beyond per-field tolerance surface to operator for reconciliation. NOT fail-closed — operator decides whether the inbound or the KFR is authoritative.

**Predicate.**

1. For each parsed numeric field in the inbound response: look up the corresponding KFR fact via `field_class → kfr_fact_id` mapping (per `proposal_commitments.yaml.kfr_fact_ref` for commitment-tied fields; per `reporting_template.yaml.kfr_cross_check` for funder-template-driven fields).
2. Read the KFR fact via `vault_read_intent_kfr`. Apply per-field tolerance (default `tolerance_pct: 0.10` = ±10%; operator-tunable per field via `kfr.tolerance_pct` field in KFR per v7.0.4 §1.1).
3. If `abs(inbound_value - kfr_value) / kfr_value > tolerance_pct` → fire sub-tag `.numeric_field_above_tolerance` (or `.numeric_field_below_tolerance` per sign).
4. If `inbound_unit != kfr_unit` (e.g., grantee reports in dollars but KFR is in thousands of dollars) → fire sub-tag `.unit_mismatch`.

**Position.** POST inbound write. Fires AFTER the inbound response is written to operational-data sub-kind (per §13.5.4); the advisory surfaces at the operator review surface (`tilth data-collector classify-inbound` or `tilth data-collector reconcile-drift` v1.1 command). NOT fail-closed; inbound stays in the operational-data sub-kind.

**Severity.** ADVISORY. No admin-risk-ledger kind (operator routing flag, not a violation).

**Composition with F-LOGICIAN-FACT-DRIFT (v7.0.4 §4).** F-DATACOLLECTOR-KFR-DRIFT is the Data Collector-side advisory; F-LOGICIAN-FACT-DRIFT family (v7.0.4 §4) is the downstream draft-time enforcement at Report Generator. Together: Data Collector surfaces drift at inbound time (advisory); Report Generator enforces no-drift at draft-time (fail-closed). Operator reconciles between the two via SP0 KFR Freshness Review at start of next reporting cycle (per v7.0.4 §3).

## §13.9.6 F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET (PRE pre-write)

**Purpose.** Refuse inbound write to operational-data sub-kind where classification has not been operator-set for this `(recipient_id, field_class)` pair. Mirrors Intake INCREMENTAL discipline per v7.0.7 §4.1 + §11 v1 — new inbound facts default `confidential` until operator re-classifies.

**Predicate.**

1. For each parsed field in the inbound response: look up `(recipient_id, field_class)` in `orgs/<slug>/data_collector/classification_register.signed.yaml` (operator-curated; Ed25519-signed at each update).
2. If `(recipient_id, field_class)` pair has no entry → fire sub-tag `.first_occurrence_unclassified`; inbound remains in inbound_log with `classification_status: DEFAULT_CONFIDENTIAL_PENDING_REVIEW`; operational-data sub-kind write blocked until operator classifies.
3. If `(recipient_id, field_class)` pair has entry with `classification_status: DEFAULT_CONFIDENTIAL_PENDING_REVIEW` (operator deferred) → fire sub-tag `.default_confidential_pending_review`; operational-data write blocked.
4. If `(recipient_id, field_class)` pair has entry with `classification_status: OPERATOR_CLASSIFIED` AND classification value matches the field's actual class (one of Public / Shareable / Confidential per v7.0.7) → PASS; write proceeds.

**Position.** PRE pre-write to operational-data sub-kind. Fires AFTER inbound parse + token validation + KFR-drift check, BEFORE the operational-data sub-kind write (per §13.5.4).

**Severity.** HIGH. `LAW3_VIOLATION` admin-risk-ledger kind (Confidential data writing without classification approval = violation of sovereignty discipline + v7.0.7 classification routing contract).

# §13.10 Routing posture (per v7.0.7 classification-driven routing)

**Split-context discipline per v7.0.7 §4.1 ("power for drafting + privacy for review").** Data Collector inherits the classification-driven routing pattern: outbound template authoring (Public + Shareable content, with opaque slot tokens for Confidential values) is cloud-routable; per-recipient slot-fill is always-local; inbound storage is always-local.

## §13.10.1 Outbound template authoring routing

Per-channel outbound templates are authored OFFLINE (not at runtime) per ADR-001 Golden Image substrate freeze. Template authoring happens during Code phase development; the Pydantic AI agent that drafts a candidate template can route to cloud frontier models (Scribe-class routing) ONLY IF the template content is classified Public + Shareable (per v7.0.7 §4.1). Confidential values that appear in templates are represented as opaque `[SLOT_<numeric_id>]` tokens per the F-CLASS-SLOT-ID-NON-OPAQUE structural discipline.

At runtime (per-cycle batch compose) Data Collector renders the per-recipient outbound message by:

1. Reading the per-channel template (Public + Shareable per substrate freeze).
2. Reading per-recipient slot values from `orgs/<slug>/data_collector/consent_ledger/` + `orgs/<slug>/data_collector/per_recipient_tokens/` + `proposal_commitments.yaml` (per-recipient slot values are Confidential or Shareable per classification register).
3. Slot-filling each `[SLOT_<numeric_id>]` token in the template with the per-recipient slot value via the always-local slot-fill agent (per v7.0.7 §4.1).
4. Rendering the final per-recipient message bytes.

The rendered message body MAY contain Confidential per-recipient values (slot-filled); the rendering step runs always-local; the rendered bytes do not flow to any cloud-routable agent BEFORE operator signs the batch.

**Cloud routing prohibited from rendering step onward.** Once the per-recipient slot-fill completes, the rendered message is in a Confidential-bearing state. Any subsequent agent that reads the rendered message MUST route always-local per v7.0.7 §4.1 — Editor / Red Team / routine-Judge review of rendered outbound message is local-routed only. F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate fail-closes any cloud-routed prompt containing semantic-named slots.

## §13.10.2 Inbound parsing + storage routing

**Always-local for inbound parsing.** Inbound responses contain Confidential operational data (beneficiary records, financial line items, narrative entries — all default Confidential per v7.0.7 §4.1 first-occurrence classification discipline). The per-channel inbound parser (`InboundResponse` normalization) runs always-local: voice transcription via local Whisper; email/SMS/Telegram/WhatsApp parsing via standard library + local parsing tools; field extraction via Pydantic AI agent on a local Mistral 7B-class model.

**Always-local for inbound storage.** Inbound writes to operational-data sub-kinds (per §2 v7.2 LOCKED) happen always-local. No cloud routing at any inbound write step.

**Cloud routing permitted ONLY for funder-template field-mapping authoring (OFFLINE).** When the operator authors a `reporting_template.yaml` for a funder (per §13.1.1), the authoring step MAY route to cloud frontier (Scribe-class) for help mapping funder-required reporting fields to the structured field_class taxonomy. The authoring step happens OFFLINE before runtime per ADR-001 substrate freeze; the authored `reporting_template.yaml` is then sealed and Ed25519-signed at white-glove. Runtime reads of `reporting_template.yaml` are always-local.

## §13.10.3 Cross-org isolation

**Per-org session storage.** Per-org per-purpose session paths (MTProto sessions, email mailbox state, SMS phone numbers, WhatsApp Business phone IDs) are non-overlapping per §13.11 substrate-shared-but-storage-distinct discipline. F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.path_cross_org fail-closes cross-org path resolution.

**Per-org Cedar enforcement.** `consent_ledger_isolation.cedar` (per §13.5.3) denies any cross-org consent ledger read. Per-org Cedar principal binding: each Data Collector invocation carries `invocation_org_slug` attribute; resource (consent ledger entry, outbound log, inbound log, sub-awardee token, etc.) carries `org_slug` attribute; Cedar policy permits action only when attributes match.

**Per-org operator key.** Each org has its own operator key per Section 1 key catalog; sub-awardee tokens are signed with the org's operator key; signature verification at token-validation time enforces per-org binding.

**Redaction in audit dumps.** Cross-org troubleshooting (e.g., operator inspects `pipeline/validation/data_collector_outbound_rejects/` across orgs to diagnose a gate-fire pattern) reads cross-org data BY DESIGN; the audit dump format redacts recipient_id values to `recipient_<hashed_first_8_chars>` to prevent accidental cross-org leakage in operator audit reports. Cedar policy `data_collector_audit_redaction.cedar` enforces.

# §13.11 Cultivator-vs-Data-Collector substrate split (operator confirmation surface for Audit #1)

**Per §13.1.2 boundary discipline + dispatch packet WS-I sub-decision flag**, this section is the operator confirmation surface for Audit #1.

**Recommended posture:** Cultivator and Data Collector share the MTProto bot framework substrate at v0.2 first ship; consent ledgers are non-overlapping; target audiences are distinct.

**Alternative posture (if operator overrides at Audit #1):** Cultivator and Data Collector have fully separated substrates; Cultivator's MTProto bot framework is spec'd at Cultivator's own blueprint round (v1.x or v2 horizon); Data Collector's MTProto substrate is spec'd here unchanged.

**Why shared at v0.2:**

1. **MTProto API quota efficiency.** Telegram's API token quota is per-application; one shared application across both agents reduces operator BYOK envelope friction (one Telegram application registration, not two).
2. **Bot framework code DRY.** Message parsing, attachment handling, retry-with-backoff logic is identical between Cultivator (talking to operator's employees) and Data Collector (talking to grantees + sub-awardees). Duplicating it is Code-debt without sovereignty benefit.
3. **Audience-distinct + ledger-distinct + Cedar-denied separation is the structural enforcement.** Substrate sharing is the efficiency choice. The four structural separations:
   - Per-purpose session storage paths (`orgs/<slug>/data_collector/mtproto_session/` vs `orgs/<slug>/cultivator/mtproto_session/`).
   - Per-purpose consent ledger trees (`orgs/<slug>/data_collector/consent_ledger/` vs `orgs/<slug>/cultivator/consent_ledger/`).
   - Cedar policy `data_collector_consent_isolation.cedar` denies cross-purpose ledger reads.
   - AST-lint `R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT` rejects any Data Collector module that imports `cultivator.consent_ledger.*` (and mirror for Cultivator side).

**Operator override at Audit #1.** Operator may decide at Audit #1 that the shared-substrate posture is too risky (e.g., concern that a single bug in the bot framework could leak across Cultivator + DC audiences). If operator overrides:

- §13.6.4 Telegram channel substrate spec carries forward unchanged (DC uses MTProto bot framework).
- §13.11 disposition changes to: "Cultivator substrate TBD at Cultivator's own blueprint round (v1.x or v2 horizon); not specified here at v0.2 first ship."
- §13.8.4 BYOK substrate note carries forward unchanged (BYOK MTProto API key is per-operator-application; if operator opts for separated substrates, operator registers TWO Telegram applications).
- AST-lint `R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT` stays in place (defense-in-depth; structural even if Cultivator substrate is separated).

**Open question for Audit #1.** Operator decides: shared substrate (recommended; default) vs separated substrates. Default stands unless cross-family Audit surfaces structural conflict.

# §13.12 Pipeline placement (per §5 v8 track-registry)

Per §5 v8 LOCKED 2026-05-10 row 188, Data Collector outreach lives INSIDE the `report_mode` track sub-shape (registered FORWARD-COMPAT in §5 v8 row 188 with `shippable_in: v0.2`). Data Collector does NOT register a new track; §13 v1 LOCK does NOT mutate the track registry.

```
REPORTING CYCLE (per active grant per reporting period)
  Data Collector compose-batch
    → per-cycle outbound batch composition (reads proposal_commitments + reporting_template + consent ledger + sub-awardee tokens + state-rules card)
    → staged batch under orgs/<slug>/data_collector/staged_batches/<batch_id>.unsigned.yaml
    → operator review-batch (operator approval surface §13.7)
    → operator approve-batch (Ed25519 signature on batch envelope)
    → signed batch under orgs/<slug>/data_collector/staged_batches/<batch_id>.signed.yaml
  Data Collector send-batch
    → per-recipient stage-and-fire dispatch (per-channel ChannelProtocol.send)
    → outbound_log entries written per-recipient
  Data Collector inbound (per-channel webhook OR polling)
    → InboundResponse normalization (parse + token validation + KFR drift advisory)
    → inbound_log entry written
    → quarantine on validation failure
  Data Collector classify-inbound (operator-explicit)
    → per (recipient_id, field_class) first-occurrence classification
    → classification register updated (Ed25519-signed by operator)
    → operational-data sub-kind writes flow (per §2 v7.2 + §13.5.4)
  → §14 Report Generator (v0.2; downstream sibling) consumes operational-data sub-kinds at next reporting cycle
```

Data Collector does NOT participate in the §5 submission_mode track (that's for grant-writing — Scribe / Editor / Judge / Red Team / Logician inner loop). Data Collector does NOT participate in eval_mode (eval reads existing KFR; Data Collector writes operational data). Data Collector fires only on operator-explicit `compose-batch` / `send-batch` / `classify-inbound` at v0.2 first ship.

# §13.13 Test matrix

Tests live at `tests/seats/data_collector/`. Each test is a deterministic unit test — no live transport calls (the per-channel transport substrate is mocked in unit tests via Protocol-DI; integration tests stub the BYOK provider endpoints), no network egress (enforced by `test_data_collector_zero_network_egress`), no cross-org reads.

## §13.13.1 Channel dispatch tests (v1 skeleton)

- `test_email_channel_implements_protocol`: assert `email_channel.EmailChannel` implements `ChannelProtocol`; assert all four protocol methods present.
- `test_sms_channel_implements_protocol`: same for SMS.
- `test_voice_channel_implements_protocol`: same for voice.
- `test_telegram_channel_implements_protocol`: same for Telegram.
- `test_whatsapp_channel_implements_protocol`: same for WhatsApp.
- `test_five_channels_registered_in_dispatcher`: introspect channel dispatcher; assert exactly five channels registered; assert no sixth channel silently leaked.
- `test_no_autosend_ast_lint`: invoke AST-lint `R-DATACOLLECTOR-NO-AUTOSEND` against full data_collector package; assert exit=0; assert no `<channel>_channel.send(...)` invocation outside `outbound_batch.py::dispatch_after_operator_approval`.
- `test_dispatcher_signature_check`: invoke `dispatch_after_operator_approval` with invalid `operator_batch_signature`; assert SendResult{sent=False, reason="operator_signature_invalid"}; assert no transport substrate invoked.

## §13.13.2 F-DATACOLLECTOR-CONSENT-MISSING tests (v1 skeleton)

- `test_f_dc_consent_missing_ledger_absent`: invoke compose with recipient whose consent ledger file does not exist; assert F-DATACOLLECTOR-CONSENT-MISSING.ledger_absent fires; assert no outbound staged.
- `test_f_dc_consent_missing_consent_inactive`: ledger exists with consent_active=False; assert .consent_inactive fires.
- `test_f_dc_consent_missing_method_unset`: ledger exists with consent_capture_method=None; assert .method_unset fires.
- `test_f_dc_consent_missing_config_signature_invalid`: data_collector_config.yaml present but signature invalid; assert .config_signature_invalid fires.
- `test_f_dc_consent_missing_pre_outbound_position`: assert gate fires BEFORE any rendered message bytes computed; assert state file shows pre-stage failure.

## §13.13.3 F-DATACOLLECTOR-OPT-OUT-ACTIVE tests (v1 skeleton)

- `test_f_dc_opt_out_active_email`: ledger has opt_out_active=True for email channel; assert .opt_out_active_email fires.
- `test_f_dc_opt_out_active_sms`: same for SMS; assert .opt_out_active_sms.
- `test_f_dc_opt_out_active_voice`: same for voice.
- `test_f_dc_opt_out_active_telegram`: same for Telegram.
- `test_f_dc_opt_out_active_whatsapp`: same for WhatsApp.
- `test_f_dc_opt_out_atomic_same_day`: simulate concurrent send + opt-out signal (race); assert atomic ledger write via fcntl.flock serializes correctly; assert no post-opt-out outbound succeeds.

## §13.13.4 F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED tests (v1 skeleton)

- `test_f_dc_frequency_cap_recipient_channel_cap`: ledger shows 1 recent outbound within 7-day default window; second outbound to same recipient + channel; assert .recipient_channel_cap fires.
- `test_f_dc_frequency_cap_state_cap_override`: PA state card sets sms_min_interval_hours=48; recipient with PA address-of-record has SMS sent 24h ago; new SMS attempt; assert .state_cap fires.
- `test_f_dc_frequency_cap_channel_switching_evasion_off_default`: recipient has email 1h ago + SMS now attempt; config has channel_switching_evasion_strict=False (default); assert PASS (no fire).
- `test_f_dc_frequency_cap_channel_switching_evasion_strict`: same fixture but config has strict=True; assert .channel_switching_evasion fires.

## §13.13.5 F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND tests (v1 skeleton)

- `test_f_dc_pii_leak_semantic_slot_in_outbound`: per-channel template contains `[SLOT_ANNUAL_REVENUE]`; compose attempts to render against per-recipient slot map; assert .semantic_slot_in_outbound fires (mirror of F-CLASS-SLOT-ID-NON-OPAQUE; semantic-named slot pre-fill detection).
- `test_f_dc_pii_leak_path_cross_org`: send-batch invocation with signed_batch_path resolving outside `orgs/<org_slug>/`; assert .path_cross_org fires.
- `test_f_dc_pii_leak_symlink_escape`: signed_batch_path is a symlink to a path outside org subtree; assert .symlink_escape fires (mirror of §11 v1 §11.9.4 symlink_escape pattern).
- `test_f_dc_pii_leak_mtproto_cross_org`: Telegram chat_id resolves to a recipient registered in `orgs/<other_org>/`; assert .mtproto_cross_org fires; assert no outbound sent.
- `test_f_dc_pii_leak_sms_size_overflow`: rendered SMS body exceeds 1600 bytes; assert .sms_size_overflow fires.
- `test_f_dc_pii_leak_whatsapp_template_unapproved`: WhatsApp outbound outside 24h conversation window with template_id not in `whatsapp_template_register/`; assert .whatsapp_template_unapproved fires.
- `test_f_dc_pii_leak_state_card_signature_invalid`: PA card YAML present but Ed25519 signature does not verify against SN-LLC pinned public key; assert .state_card_signature_invalid fires.
- `test_f_dc_pii_leak_batch_hash_mismatch`: signed batch envelope present + signature valid + batch_content_sha3_512 set, but per-recipient OutboundMessage bytes tampered after sign; assert .batch_hash_mismatch fires.
- `test_f_dc_pii_leak_token_invalid_inbound`: inbound payload carries forged token (decryption fails); assert .token_invalid_inbound fires; assert inbound quarantined.

## §13.13.6 F-DATACOLLECTOR-KFR-DRIFT tests (v1 skeleton)

- `test_f_dc_kfr_drift_above_tolerance`: inbound numeric (300 graduates) vs KFR (197 graduates ±10% tolerance); assert .numeric_field_above_tolerance advisory fires; assert inbound STILL written to operational-data sub-kind (not fail-closed); assert advisory surfaces at next operator review.
- `test_f_dc_kfr_drift_within_tolerance`: inbound 210 vs KFR 200 ±10%; assert no advisory fire.
- `test_f_dc_kfr_drift_unit_mismatch`: inbound in dollars, KFR in thousands of dollars; assert .unit_mismatch advisory.
- `test_f_dc_kfr_drift_post_position`: assert advisory fires AFTER inbound written to operational-data sub-kind; assert inbound write succeeded.

## §13.13.7 F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET tests (v1 skeleton)

- `test_f_dc_inbound_classification_first_occurrence`: inbound with (recipient_id_X, field_class_Y) where no classification register entry exists; assert .first_occurrence_unclassified fires; assert operational-data sub-kind write blocked; assert inbound stays in inbound_log with DEFAULT_CONFIDENTIAL_PENDING_REVIEW.
- `test_f_dc_inbound_classification_default_pending_review`: classification register has entry with status=DEFAULT_CONFIDENTIAL_PENDING_REVIEW; assert .default_confidential_pending_review fires; assert write blocked.
- `test_f_dc_inbound_classification_operator_classified_pass`: register has OPERATOR_CLASSIFIED entry; assert PASS; assert operational-data sub-kind write proceeds.
- `test_f_dc_inbound_classification_pre_write_position`: assert gate fires BEFORE operational-data sub-kind write; assert classify-inbound CLI updates register correctly.

## §13.13.8 Cultivator-vs-DC isolation tests (v1 skeleton)

- `test_no_cultivator_ledger_import_ast_lint`: AST-lint `R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT` rejects any DC module that imports `cultivator.consent_ledger.*`; assert exit≠0 on violating fixture.
- `test_mtproto_session_path_isolation`: DC's mtproto_session path is `orgs/<slug>/data_collector/mtproto_session/`; Cultivator's is `orgs/<slug>/cultivator/mtproto_session/`; assert non-overlapping; assert no Cultivator session file in DC's tree.
- `test_consent_ledger_cedar_isolation`: invoke DC's compose with attribute principal.purpose=cultivator; assert Cedar denies ConsentLedgerRead.
- `test_cross_purpose_principal_denied`: simulate principal carrying cultivator_seat attribute attempting to read DC's consent ledger; assert Cedar fail-closed.

## §13.13.9 State-rules card tests (v1 skeleton)

- `test_pa_card_loaded`: load `vault_shared/state_rules_card/PA.yaml`; verify SN-LLC Ed25519 signature; assert sms_quiet_hours==(7am, 9pm).
- `test_ca_card_loaded`: same for CA; assert annual_re_capture_required==True.
- `test_fl_card_loaded`: same for FL.
- `test_tx_card_loaded`: same for TX.
- `test_ny_card_loaded`: same for NY.
- `test_card_signature_invalid_fail_closed`: tamper with card YAML; assert F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.state_card_signature_invalid fires; assert card not loaded.
- `test_non_opted_in_state_fail_closed`: recipient has state_code=GA; operator has not opted in to GA card; compose attempt; assert fail-closed with operator notification.
- `test_sn_llc_pubkey_rotation`: simulate SN-LLC pubkey rotation via Trust-On-First-Use rotation (new key co-signed by previous); assert card update applies; assert previous pinned key archived.

## §13.13.10 Sub-awardee token register tests (v1 skeleton)

- `test_issue_tokens_writes_per_recipient_files`: invoke `issue-tokens`; assert per-recipient files written under `per_recipient_tokens/`.
- `test_token_encryption_at_rest`: assert `secret_value_ciphertext` is encrypted; assert decryption requires KFR-classified-confidential key.
- `test_token_operator_signature_required`: assert each token file Ed25519-signed by operator key active at issued_at_utc.
- `test_token_validation_success`: simulate inbound with valid token; assert ChannelProtocol.validate_inbound_token returns TokenValidationResult{valid=True}.
- `test_token_validation_stale_after_rotates_at`: simulate inbound past rotates_at_utc; assert TokenValidationResult{valid=False, reason="stale"}; assert quarantine.
- `test_token_validation_forged`: inbound with token bytes that don't match register; assert valid=False, reason="forged".
- `test_token_rotation_per_grant_cycle`: invoke `issue-tokens --rotate`; assert new tokens issued; assert prior tokens marked rotated.

## §13.13.11 Operator approval surface tests (v1 skeleton)

- `test_review_batch_tty_check`: invoke `review-batch` non-TTY; assert argparse-rejection.
- `test_approve_batch_yes_flag_rejected`: invoke `approve-batch --yes`; assert argparse-rejection.
- `test_approve_batch_force_flag_rejected`: assert `--force` argparse-rejection.
- `test_approve_batch_auto_confirm_rejected`: assert `--auto-confirm` argparse-rejection.
- `test_approve_batch_writes_signed_envelope`: TTY-mode approve; assert signed batch envelope written with operator Ed25519 signature + batch_content_sha3_512.
- `test_drop_recipient_persists_reason`: drop-recipient action requires reason; assert reason persisted in state file audit trail.

## §13.13.12 Integration tests (v1 skeleton)

- `test_end_to_end_email_compose_send_inbound`: seeded test org with one recipient + email consent; invoke compose-batch + review-batch (TTY mocked) + approve-batch + send-batch + simulate inbound webhook with valid token; assert full round-trip completes; assert outbound_log + inbound_log + state file consistent.
- `test_end_to_end_five_channels_in_one_batch`: seeded test org with one recipient consenting on all five channels; compose-batch with channels_in_scope=[all 5]; assert five OutboundMessage entries staged.
- `test_data_collector_zero_network_egress`: full DC run inside sandbox with network egress blocked (Linux network namespace or socket monkey-patch); assert all calls hit mocked BYOK endpoints; zero outbound network connections.
- `test_data_collector_cic_clc_orthogonality`: invoke DC schemas + per-channel prompt templates against v7.0.8 four detection layers; assert F-CIC-CLC-COUPLING-VIOLATION audit clean.
- `test_consent_capture_to_compose_round_trip`: seeded org with no consent; invoke `consent --action capture` for one recipient + email; invoke compose-batch with that recipient; assert message staged correctly.

## §13.13.13 v1.x horizon tests (NOT registered at v1)

The following tests land at §13 v1.x amendments alongside the corresponding feature additions:

- `test_dc_supports_signal`: outbound + inbound via Signal channel per OQ-DC-SIGNAL v1.x expansion.
- `test_dc_voice_ivr_flow`: voice channel uses operator-curated IVR flow per OQ-DC-IVR v1.1 expansion.
- `test_dc_per_grant_template_override`: per-grant operator-signed template override per OQ-DC-TEMPLATE-OVERRIDE v1.1.
- `test_dc_asymmetric_keypair_token_mode`: per-sub-awardee pubkey verification as alternative to shared-secret token per OQ-DC-KEYPAIR-MODE v1.1.
- `test_dc_photo_exif_strip`: photo sub-kind inbound writes EXIF-stripped per OQ-DC-PHOTO-EXIF v1.1.
- `test_dc_virus_scan_attachments`: attachment sub-kind inbound writes virus-scanned per OQ-DC-VIRUS-SCAN v1.1.

# §13.14 Open questions resolved and deferred

## §13.14.1 Resolved at v1

- **OQ-DC-CHANNELS (per dispatch decision 8a + 8b).** RESOLVED at v1: five channels at v0.2 first ship (email + SMS + voice + Telegram + WhatsApp). Per Josh 2026-05-09.
- **OQ-DC-TOKEN-MODEL (per dispatch decision 8e default).** RESOLVED at v1: per-recipient shared-secret token at award acceptance, embedded in every outbound message, rotates per grant cycle. Alternative (per-recipient pubkey verification) is v1.1 horizon (OQ-DC-KEYPAIR-MODE). Per §13.6.0.
- **OQ-DC-STATE-CARD (per dispatch decision 8f default).** RESOLVED at v1: SN-LLC ships PA / CA / FL / TX / NY at v0.2 first wave; operator opts in per state at white-glove. Per §13.8.7.
- **OQ-DC-CULTIVATOR-SUBSTRATE-SPLIT (per dispatch packet sub-decision).** RESOLVED at v1 with default RECOMMENDED posture: shared MTProto bot framework substrate; per-purpose session paths + ledgers + Cedar denial + AST-lint enforcement. Operator override available at Audit #1 per §13.11.
- **OQ-DC-VOICE-SUBSTRATE.** RESOLVED at v1: Twilio Voice outbound; local Whisper-class transcription inbound (always-local per v7.0.7); operator-pinned PSTN gateway as alternative. Per §13.8.3.
- **OQ-DC-WHISPER-MODEL-SIZE.** RESOLVED at v1: tiny.en default at v0.2 first ship (M1 8GB dev floor compatible); operator override per `whisper_model_size` config field. Per §13.8.3.
- **OQ-DC-CONSENT-LEDGER-ATOMIC.** RESOLVED at v1: per-recipient × per-channel YAML file; fcntl.flock(LOCK_EX) for atomic update; 30s timeout fail-closed. Mirrors §15 v1 NF-02 closure. Per §13.5.3.
- **OQ-DC-OPERATOR-APPROVAL-DISCIPLINE (per §11 v1 §11.7 + §12 v1 precedents).** RESOLVED at v1: four-layer defense against silent autosend (AST-lint + dispatcher signature + Cedar policy + TTY check). NO `--yes` / `--auto-confirm` / `--force` flags. Per §13.7.

## §13.14.2 Open questions for next-round attention

- **OQ-DC-SIGNAL: v1.x Signal channel addition.** v1 supports email + SMS + voice + Telegram + WhatsApp. v1.x candidate: Signal Messenger via libsignal-protocol-python. Each channel addition requires a §13 v1.x amendment registering the channel module + per-channel substrate + ChannelProtocol implementation.
- **OQ-DC-IVR: v1.1 voice IVR mode.** v1 voice channel is automated TTS-driven. v1.1 candidate: operator-curated IVR flow via Twilio Studio per-grant override.
- **OQ-DC-TEMPLATE-OVERRIDE: v1.1 per-grant template override.** v1 templates sealed at substrate-freeze time. v1.1 candidate: per-grant operator Ed25519-signed template override (mirrors §11 v1 RT-07 operator-config signature pattern). Closes the gap where a funder requires non-default reporting question phrasing.
- **OQ-DC-KEYPAIR-MODE: v1.1 asymmetric-keypair sub-awardee identity.** v1 uses shared-secret tokens. v1.1 candidate: optional per-recipient pubkey signing mode; recipient opts in at award acceptance; Tilth verifies inbound signatures with recorded pubkey. Cryptographically stronger but imposes infrastructure burden on recipients.
- **OQ-DC-PHOTO-EXIF: v1.1 photo EXIF stripping.** v1 photo sub-kind writes preserve EXIF metadata. v1.1 candidate: EXIF-strip before write to reduce PII leak surface (GPS coordinates, device serial numbers, timestamps); operator opt-in per `data_collector_config.yaml` flag.
- **OQ-DC-VIRUS-SCAN: v1.1 attachment virus scanning.** v1 attachment sub-kind writes are pass-through. v1.1 candidate: local ClamAV scan before write; operator-curated scanner choice; failure quarantines.
- **OQ-DC-WATCHER-DAEMON: v1.x watcher daemonization.** v1 inbound is webhook-driven OR operator-explicit polling. v1.x candidate: per-OS daemonization scripts (systemd unit for Linux, launchd plist for macOS) for poll-loop inbound handlers.
- **OQ-DC-PER-FUNDER-REPORTING-TEMPLATE-AUTHORING.** v1 reporting_template.yaml authoring is OFFLINE pre-runtime. v1.x candidate: cloud-routable per-funder template authoring agent (Scribe-class; runs on Public+Shareable funder reporting requirements; runs OFFLINE during white-glove setup per funder). Surfaces if a deployment needs to onboard a new funder mid-cycle.
- **OQ-DC-STATE-EXPANSION: v1.x state card expansion.** v1 ships PA/CA/FL/TX/NY. v1.x candidate: SN-LLC ships additional states per operator demand (MA, IL, WA, OR likely next wave). Each addition is a card release + operator opt-in.
- **OQ-DC-DNC-INTEGRATION: v1.x DNC registry integration.** v1 voice channel has `voice_state_dnc_check_required` advisory only. v1.x candidate: operator-curated DNC scrub substrate (operator-pinned DNC provider OR offline DNC registry import).

# §13.15 Companion edits at LOCK

The following edits land in the same commit as §13 v1 LOCK (compound paired-commit per §6.17 Option-B):

1. **§0.5 §13 amendment** — `pipeline/blueprint/v0.1/section_00_5_section_13_data_collector_amendment.md` — final inventory **26 rows at v1** (per the explode-pattern §10 / §11 / §12 / §15 precedent applied to F-DATACOLLECTOR-* failure-codes + per-channel ChannelProtocol rows):
   - 1 marker row (kind=`marker`): `blueprint.section_anchor.s13_data_collector.v1`
   - 7 schema/contract rows: `data_collector.outbound_batch_compose_input.v1`, `data_collector.outbound_batch_send_input.v1`, `data_collector.inbound_parse_input.v1`, `data_collector.inbound_classify_input.v1`, `data_collector.outbound_message.v1`, `data_collector.inbound_response.v1`, `data_collector.consent_ledger_entry.v1`
   - 5 interface-contract rows (kind=`interface-contract`): `data_collector.channel_protocol.email.v1`, `data_collector.channel_protocol.sms.v1`, `data_collector.channel_protocol.voice.v1`, `data_collector.channel_protocol.telegram.v1`, `data_collector.channel_protocol.whatsapp.v1`
   - 6 failure-code rows (kind=`failure-code`): `data_collector.failure_code.F-DATACOLLECTOR-CONSENT-MISSING.v1`, `data_collector.failure_code.F-DATACOLLECTOR-OPT-OUT-ACTIVE.v1`, `data_collector.failure_code.F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED.v1`, `data_collector.failure_code.F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.v1`, `data_collector.failure_code.F-DATACOLLECTOR-KFR-DRIFT.v1`, `data_collector.failure_code.F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET.v1`
   - 1 pre-gate-check row (kind=`pre-gate-check`): `data_collector.pre_gate.compose_send_validation.v1` (consolidates the four PRE-outbound gates per §4 v2.2 consolidated-check pattern + §13.9.0)
   - 1 post-gate-check row (kind=`post-gate-check`): `data_collector.post_gate.inbound_kfr_drift.v1` (backs F-DATACOLLECTOR-KFR-DRIFT)
   - 1 pre-gate-check row (kind=`pre-gate-check`): `data_collector.pre_gate.inbound_classification_set.v1` (backs F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET)
   - 1 sub-awardee-token schema row: `data_collector.sub_awardee_token.v1`
   - 1 schema row for state-rules card: `data_collector.state_rules_card_entry.v1`
   - 1 schema row for outbound batch envelope: `data_collector.signed_batch_envelope.v1`

   **§0.5 row range note.** §13 claims rows **349–374** (26 rows; runtime-live total after this LOCK = 374). Prior runtime-live at §0.5 v14 LOCK 2026-05-10 = 348.

2. **§4 Logician v2.x amendment ACTIVATION** — flips the six F-DATACOLLECTOR-* gates registered at §4 v2.x §5.1 HORIZON (rows 298-303 of the v2.x amendment) into live PRE/POST positions. Activation is a NOTE block prepended to the v2.x amendment §5.1 table marking the gates as ACTIVE-AT-§13-v1-LOCK with parent_lock pointer at §13 v1 LOCK. Code-side predicate body realization is downstream (WS-I Code phase dispatch); v0.2 first ship ships predicate skeleton stubs raising `NotImplementedError` per the §15 v1 SPEC-only-with-skeleton precedent.

3. **`orgs/_TEMPLATE/data_collector/` scaffold** — template directory for new client orgs:
   - `orgs/_TEMPLATE/data_collector/consent_ledger/.gitkeep` (per-recipient × per-channel ledger directory; populates at consent-capture step)
   - `orgs/_TEMPLATE/data_collector/state_rules_opt_ins.signed.yaml` (operator-signed per-state opt-in record; ships with empty `opted_in_states: []`)
   - `orgs/_TEMPLATE/data_collector/outbound_log/.gitkeep`
   - `orgs/_TEMPLATE/data_collector/inbound_log/.gitkeep`
   - `orgs/_TEMPLATE/data_collector/per_recipient_tokens/.gitkeep`
   - `orgs/_TEMPLATE/data_collector/staged_batches/.gitkeep`
   - `orgs/_TEMPLATE/data_collector/state/.gitkeep`
   - `orgs/_TEMPLATE/data_collector/mtproto_session/.gitkeep`
   - `orgs/_TEMPLATE/data_collector/whatsapp_template_register/.gitkeep`
   - `orgs/_TEMPLATE/data_collector/consent_audio/.gitkeep` (voice consent capture archives)
   - `orgs/_TEMPLATE/data_collector/byok_keys/.gitkeep` (per-channel BYOK keys encrypted at rest)
   - `orgs/_TEMPLATE/data_collector/data_collector_config.yaml` (operator-tunable per-org config: `email_substrate: postmark`, `sms_substrate: twilio`, `voice_substrate: twilio_voice`, `whisper_model_size: tiny.en`, `frequency_cap_lookback_days: 7`, `channel_switching_evasion_strict: false` defaults; Ed25519-signed wrapper required per §13.4.1 RT-07-mirror discipline)
   - `orgs/_TEMPLATE/data_collector/classification_register.signed.yaml` (operator-signed inbound classification register; ships with empty `(recipient_id, field_class) → classification` map)

4. **Workspace-shared scaffold:**
   - `vault_shared/state_rules_card/.gitkeep` (card directory; populates at SN-LLC release pull-in)
   - `vault_shared/data_collector/byok_keys/.gitkeep` (Telegram bot token shared across orgs)

5. **Module scaffold** — `pipeline/orchestrator/seats/data_collector/`:
   - `__init__.py` — dataclass schemas for `OutboundBatchComposeInput`, `OutboundBatchSendInput`, `InboundParseInput`, `InboundClassifyInput`, `OutboundMessage`, `InboundResponse`, `ConsentLedgerEntry`, `SubAwardeeToken`, `StateRulesCardEntry`, `SignedBatchEnvelope`, `Recipient`, `StateDisclaimer`, `SharedSecretToken`, `BatchSignature`, `SendResult`, `ChannelReceiptMetadata`, `TokenValidationResult`, `ParsedField`, `KfrDriftAdvisory`, `GateResult`. ChannelProtocol Protocol-DI definition. Mode dispatcher with the four cycles registered (compose-batch, send-batch, parse-inbound, classify-inbound). Module passes AST-lint clean (R-DATACOLLECTOR-NO-AUTOSEND + R-DATACOLLECTOR-VAULT-INTENT-REQUIRED + R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT + R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED) at LOCK.
   - `email_channel.py` — Email ChannelProtocol skeleton; SMTP via BYOK provider stubs raising `NotImplementedError` at v0.2; full implementation downstream by WS-I Code phase.
   - `sms_channel.py` — same shape for SMS.
   - `voice_channel.py` — same shape for voice (Twilio Voice + local Whisper transcription stubs).
   - `telegram_channel.py` — same shape for Telegram (MTProto bot stubs).
   - `whatsapp_channel.py` — same shape for WhatsApp (WhatsApp Business API stubs).
   - `outbound_batch.py` — `dispatch_after_operator_approval(batch_signature, ...)` skeleton with Ed25519 signature check at entry; raises `NotImplementedError` on transport invocation at v0.2.
   - `consent_ledger.py` — Cedar-policy-gated read/write skeleton; atomic-update via fcntl.flock; full Cedar policy realization downstream.
   - `state_rules_card.py` — per-state card loader skeleton; SN-LLC Ed25519 signature verification stub; PA/CA/FL/TX/NY operator opt-in resolver.
   - `inbound_parser.py` — per-channel inbound handler skeleton; common InboundResponse normalization.
   - `field_validator.py` — Pydantic schema validation + KFR cross-check skeleton (F-DATACOLLECTOR-KFR-DRIFT POST predicate stub).
   - `cedar_policies/consent_ledger_isolation.cedar` — Cedar policy skeleton.
   - `cedar_policies/data_collector_send.cedar` — Cedar policy skeleton.
   - `cedar_policies/beneficiary_records_pii.cedar` — Cedar policy skeleton (composes with §2 v7.2 LOCKED PII discipline).
   - `cedar_policies/data_collector_audit_redaction.cedar` — Cedar policy skeleton.

6. **Test suite** — `tests/seats/data_collector/skeleton_tests.py` per §13.13 — at LOCK ceremony, skeleton tests validate:
   - The five channels register in dispatcher (`test_five_channels_registered_in_dispatcher`).
   - The six v1 gate codes resolve to imported predicates (skeletons raising NotImplementedError).
   - AST-lint extensions exit=0 against full data_collector package (`test_no_autosend_ast_lint`, `test_no_cultivator_ledger_import_ast_lint`).
   - Dispatcher signature check fails closed on invalid signature (`test_dispatcher_signature_check`).
   - Schema round-trip for each dataclass (Pydantic-validate-then-serialize-then-deserialize-then-Pydantic-validate).
   - Channel protocol implementation for each of five channels (`test_<channel>_channel_implements_protocol`).
   
   Full per-gate + per-channel test population is downstream (WS-I Code phase dispatch).

7. **Memory file** — `memory/project_blueprint_section_13_data_collector_v1_locked.md` — written at LOCK ceremony per the standard memory pattern.

8. **MEMORY.md prepend** — index entry for the §13 LOCK.

9. **lock_history rows** — appended to `pipeline/engineering/lock_history.v1.jsonl` as sibling 1/2 (§13 v1 blueprint) + sibling 2/2 (§0.5 §13 amendment companion). Rows **196 + 197** at LOCK.
   - Row 196 (sibling 1/2): `lock_class=blueprint`, `module=pipeline.blueprint.v0_1.section_13_data_collector`, `parent_lock_row=193` (§4 v2.x LOCK; gate-family HORIZON parent), `unblocks=["WS-J §14 Report Generator (consumes operational-data sub-kind writes Data Collector produces)", "WS-I Code phase (channel module substrate wiring)", "§4 v2.x.1 follow-on minor amendment (registers F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER + F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED as live PRE/POST positions)"]`.
   - Row 197 (sibling 2/2): `lock_class=blueprint_amendment_companion`, `module=pipeline.blueprint.v0_1.section_00_5_section_13_data_collector_amendment`, `parent_lock_row=196`.

10. **daily_log entry** — `daily_logs/2026-05-10.md` — per the standard daily_log pattern (LOCK ceremony summary + companion edits + unblocks).

11. **session_metrics line** — appended to `pipeline/metrics/session_log.jsonl` per `pipeline/metrics/SESSION_METRICS_SPEC.md`.

12. **Audit trail directory** — `pipeline/validation/blueprint_section_13_data_collector_2026-05-10/` — contains:
    - `audit_prompt_v1_common_header.md` (cribs from §11 v1 / §15 v1 / §12 v1 common header pattern; project-context + cross-cutting invariants).
    - `audit_prompt_v1_editor_task.md`, `audit_prompt_v1_judge_task.md`, `audit_prompt_v1_red_team_task.md` (per-seat task prompts).
    - `dispatch_audit_v1.sh`, `dispatch_audit_v1_parallel.sh` (cribs from §11 v1 templates; cross-family bridge via osascript → openclaw gateway).
    - `audit_v1_editor.md`, `audit_v1_judge.md`, `audit_v1_red_team.md`, `audit_v1_synthesis.md` (Cycle 1 outputs).
    - `audit_prompt_v2_*.md` (Cycle 2 prompts after Cycle 1 closures).
    - `dispatch_audit_v2.sh`, `dispatch_audit_v2_parallel.sh`.
    - `audit_v2_editor.md`, `audit_v2_judge.md`, `audit_v2_red_team.md`, `audit_v2_synthesis.md` (Cycle 2 outputs).
    - `LOCK_disposition.md` (per-finding disposition: CLOSED / PARTIAL_FOLDED_IN / NEW_FOLDED_IN / REJECTED-with-rationale / DEFERRED per row-170 transparent disposition pattern).

# §13.16 Cycle 1 closure dispositions (2026-05-10)

Per L-005 strict two-cycle discipline + row-170 transparent disposition pattern (WS-D v7.0.5 row 179, WS-B v7.0.7 row 180, WS-C-M1 v7.0.4-M1 row 190, WS-K §15 rows 191/192 precedents). Each Cycle 1 finding receives explicit disposition: CLOSED (closure applied inline + spec'd here) / FOLDED_IN (PARTIAL closure + bounded by v7 LOCKED A1+A4 OR v0.2 known-limitation + v2 Section O.5 mitigation track) / DEFERRED (v0.2 follow-on Code dispatch OR v1.1 horizon) / REJECTED (premise contradicted by spec).

## §13.16.1 Red Team findings — P0 + HIGH disposition

**RT-01 (P0 — consent-bypass via stale ledger read).** **CLOSED.** Spec gap acknowledged + closed. The §13.4.2 send-batch input contract is updated as follows: send-batch invocation now re-reads the per-recipient consent ledger row IMMEDIATELY BEFORE each per-recipient transport substrate call (not at PRE-batch time only). A new gate sub-tag `F-DATACOLLECTOR-CONSENT-MISSING.send_time_consent_drift` fires when send-time consent ledger row differs from compose-time snapshot (e.g., recipient opted out between compose and send). The signed batch envelope now carries `per_recipient_consent_state_sha3_512_full` (full 512-bit hash; per RT-13 closure) over each recipient's ledger entry at compose time; send-time recomputation + comparison; mismatch → abort that recipient + per-recipient `SendResult{sent=False, reason="send_time_consent_drift", consent_state_hash_at_compose=<>, consent_state_hash_at_send=<>}`. Failed recipients are logged + surfaced at operator post-send summary; remaining batch recipients continue (per-recipient stage-and-fire isolation). New test `test_f_dc_consent_send_time_drift` in §13.13.2. Mirrors §15 v1 Cycle 2 NF-02 atomic-confirmation-race closure pattern applied to send-time consent.

**RT-02 (HIGH — cross-channel opt-out propagation).** **CLOSED.** Spec gap acknowledged + closed. `consent_ledger_entry.v1` schema is updated to include `opt_out_propagated_from_channel: list[Literal["email","sms","voice","telegram","whatsapp","operator_explicit"]]` field. STOP/UNSUBSCRIBE/END/CANCEL/QUIT signal on ANY channel triggers an atomic write across ALL ledger entries for that `recipient_id` setting `opt_out_active=True, opt_out_at_utc=received_at_utc, opt_out_propagated_from_channel.append(<source_channel>)` (mirrors TCPA "any opt-out suppresses all commercial communications" floor). Operator-explicit re-consent capture (operator invokes `tilth data-collector consent --action recapture --recipient <id> --channel <ch> --recipient-confirmed-affirmative`) is the ONLY path to re-enable a channel post-cross-channel opt-out; ledger discipline requires fresh consent capture timestamp + operator Ed25519 signature on the recapture record. New tests `test_f_dc_opt_out_cross_channel_propagation_sms_triggers_all` + `test_f_dc_opt_out_recapture_requires_operator_signature` in §13.13.3. The cross-channel propagation runs INSIDE the §13.5.3 fcntl.flock(LOCK_EX) atomic-update — all five ledger entries for the recipient acquire-then-release inside a single critical section to prevent partial-propagation race.

**RT-04 (HIGH — frequency-cap default permissive).** **FOLDED_IN — partial closure + operator-signed override discipline.** The default for `channel_switching_evasion_strict` flips to **True** at v0.2 first ship (was False at v1 draft). Operator may opt OUT of strict mode via Ed25519-signed `data_collector_config.yaml` `channel_switching_evasion_strict: false` per the §13.4.1 operator-config signature discipline; unsigned config OR per-run CLI override do NOT disable strict mode (defense-in-depth: silent permissive-mode is structurally blocked at v0.2). Household-level cap (per RT-04 (b) sub-probe) is FOLDED_IN as v1.1 horizon OQ-DC-HOUSEHOLD-CAP — household-level recipient grouping is not currently modeled in `recipient_id` (which is per-individual); at v1.1 the schema extends with `household_id: str | None` optional grouping field; v0.2 first ship treats household-evasion as accepted operator-grade risk bounded by v7 LOCKED A4 operator-trusted preflight. New test `test_f_dc_frequency_cap_channel_switching_evasion_strict_default_v0_2`. New OQ entry in §13.14.2.

**RT-08 (HIGH — cross-org chat_id ambiguity).** **CLOSED.** Spec gap acknowledged + closed. The §13.6.4 + §13.10.3 + §13.11 Telegram inbound handler is updated as follows: inbound update arrival fires a **cross-org chat_id resolution scan** — the handler iterates over ALL `orgs/*/data_collector/consent_ledger/` trees looking for `chat_id` match in any `(recipient_id, channel=telegram)` ledger entry. Three branches:

1. **Exactly-one match.** Route inbound to that org's Data Collector inbound parser. Common case.
2. **Zero matches.** Quarantine under `pipeline/data_collector_inbound_quarantine/unresolved/telegram_chat_id_<chat_id>/<run_id>.yaml`; operator inspects.
3. **Multiple matches.** Quarantine under `pipeline/data_collector_inbound_quarantine/cross_org_chat_id_collision/<chat_id>/<run_id>.yaml`; F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND `.cross_org_chat_id_collision` sub-tag fires; operator MUST resolve via operator-signed `recipient_chat_id_canonical_org_binding.signed.yaml` (per-`chat_id` single-org canonical binding; written by operator at consent-capture time + verified at every inbound) before further inbound routes for that chat_id.

A NEW gate sub-tag `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.cross_org_chat_id_collision` is registered. New test `test_f_dc_pii_leak_cross_org_chat_id_collision_quarantine` in §13.13.5. Consent capture at first-contact `/start` enforces single-org canonical binding via `chat_id_canonical_org_binding` write — second org attempting to capture consent for an already-bound chat_id fails-closed at consent capture (operator must explicitly transfer canonical binding before second org can capture).

**RT-10 (HIGH — token replay across channels).** **CLOSED.** Spec gap acknowledged + closed. `sub_awardee_token.v1` schema is updated to include `channel_binding: Literal["email","sms","voice","telegram","whatsapp"]` field — each token is bound to exactly one channel at issuance. Per-recipient tokens are issued PER (recipient_id × channel) pair, not per-recipient — operator's `issue-tokens` CLI generates one token per (recipient, channel) combination, encrypted at rest with the channel binding embedded in the AEAD-protected ciphertext (per RT-11 closure). Per `ChannelProtocol.validate_inbound_token`, each channel substrate extracts the channel binding from the decrypted token payload; channel mismatch (e.g., a token issued for email replayed via SMS) → `TokenValidationResult{valid=False, reason="channel_binding_mismatch"}` + quarantine path. New tests `test_token_channel_binding_email_to_sms_replay_rejected` + `test_token_per_channel_issuance_storage` in §13.13.10. Storage path: `orgs/<slug>/data_collector/per_recipient_tokens/<grant_id>__<recipient_id>__<channel>.signed.yaml` (per-channel file; one file per (grant, recipient, channel) triple).

**RT-11 (MED — token encryption without AEAD).** **CLOSED.** Spec is updated to mandate AEAD (AES-GCM or ChaCha20-Poly1305 with per-token random nonce). `secret_value_ciphertext` field semantic is sharpened: ciphertext MUST carry an AEAD authentication tag; validation MUST verify the tag BEFORE accepting decrypted token value; tag-verification failure aborts token validation with `TokenValidationResult{valid=False, reason="aead_tag_invalid"}` + admin-risk ledger entry at HIGH severity (tag-invalid = tampered ciphertext = suspected attack). Sub-tag `.aead_tag_invalid` added to F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND consolidated check. New test `test_token_aead_tag_invalid_rejected`.

**RT-13 (MED — batch-hash truncation).** **CLOSED.** The `batch_content_sha3_512` field at §13.4.2 + §13.5.0 schema delta is updated: persisted value MUST be the FULL 512-bit (128-hex-char) SHA3-512 digest. The hex-prefix-16 convention is reserved for human-readable display ONLY (e.g., audit dump summary); runtime comparison MUST use the full digest. Schema delta clarification: `batch_content_sha3_512: str` field length = 128 hex chars; Pydantic validator enforces. Same discipline applies to `rendered_message_bytes_sha3_512` (per RT-14 closure — full digest required) + `raw_payload_sha3_512` + `per_recipient_consent_state_sha3_512_full` (per RT-01 closure). The "hex-prefix-16" mention in §13.5.0 is amended to read "hex-prefix-16 for display; full 128-hex-char digest for runtime comparison."

**RT-14 (HIGH — batch envelope tampering of individual recipients).** **CLOSED.** Spec gap acknowledged + closed. The `signed_batch_envelope.v1` schema is updated to per-recipient signing — each `OutboundMessage` gets its own `per_recipient_signature: bytes` field (Ed25519 signature by operator over canonical-JSON of the OutboundMessage record including `rendered_message_bytes_sha3_512`). The batch envelope contains a list of per-recipient signed entries; the envelope itself carries a `batch_manifest_sha3_512` over the list of `(outbound_id, per_recipient_signature_sha3_512)` pairs for compose-time integrity. Send-time verification: per-recipient signature verified at PRE-per-recipient-send; any verification failure aborts that recipient with `SendResult{sent=False, reason="per_recipient_signature_invalid"}`. Tampering a single recipient's bytes invalidates that recipient's signature (closes the RT-14 "swap one recipient's payload while keeping global hash" attack). New tests `test_per_recipient_signature_invalid_rejected` + `test_batch_envelope_manifest_hash_full_512` in §13.13.11.

**RT-15 (HIGH — voice transcription cloud path via Twilio recording fetch).** **CLOSED.** §13.6.3 + §13.8.3 updated. The Twilio recording fetch step is explicitly characterized as a **boundary cloud round-trip** with three structural disciplines: (a) TLS-pinned fetch — Tilth pins Twilio's certificate fingerprint at white-glove; fetch fails-closed on certificate mismatch (mitigates MITM injection); (b) temp-buffer-only — fetched bytes go directly into an in-memory buffer; no disk persist before transcription; (c) immediate-delete — after Whisper transcription completes, the buffer is `os.urandom`-overwritten + garbage-collected (defense against bystander memory inspection on shared hardware). The boundary cloud round-trip is documented as a v0.1-known-limitation per the v7 LOCKED A1 (single-client) + A4 (operator-trusted) preflight assumptions; v2 multi-tenant Section O.5 mitigation track adds Twilio SIP-trunk-via-localhost option (Twilio-managed PSTN gateway behind operator's edge firewall) as v2+ alternative. New tests `test_voice_fetch_tls_pin_failure_aborts` + `test_voice_fetch_memory_buffer_not_persisted_to_disk` in §13.13.12.

**RT-20 (HIGH — CIC × CLC orthogonality concrete checks).** **CLOSED.** §13.15 LOCK companion edits updated to include the v7.0.8 four-detection-layer audit step as a compound-LOCK transaction prerequisite. Step list at LOCK ceremony:

1. Static lexical regex scan over `pipeline/orchestrator/seats/data_collector/**/*.py` + `orgs/_TEMPLATE/data_collector/**/*.yaml` for CIC tokens (regex `\b(INTERNAL_[A-Z_]+|CIC_[A-Z_]+|FOOD_SYSTEMS|EDUCATOR|PUBLIC_AGENCY|ARTS_CULTURE|COOPERATIVE|ECOSYSTEM_INTERMEDIARY)\b` non-comment) — fail LOCK on any hit.
2. Pydantic AST scan — assert no Pydantic field with `default` value matching a CIC enum member.
3. Value-set scan — assert no string literal in outbound template register matching a CIC archetype identifier.
4. KP schema scan — assert v7.0.8 KP schema audit emits zero `F-CIC-CLC-COUPLING-VIOLATION` predicate hits against §13 schemas + per-channel prompt templates.

All four layers MUST pass; failure of any layer blocks LOCK. New AST-lint extension `R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY` consolidates the four layers. New test `test_cic_clc_four_layer_audit_clean_at_lock` in §13.13.12.

**RT-22 (HIGH — operator-config signature bypass when consent present).** **CLOSED.** §13.4.1 + §13.9.1 updated: operator-config Ed25519 signature is now verified at Data Collector **module-load time** (not only when F-DATACOLLECTOR-CONSENT-MISSING fires). New gate sub-tag `F-DATACOLLECTOR-CONSENT-MISSING.module_load_config_signature_invalid` fires at `pipeline/orchestrator/seats/data_collector/__init__.py` import time if `orgs/<slug>/data_collector/data_collector_config.yaml` exists but signature is invalid; module load fails closed with clear error; no Data Collector CLI invocation proceeds. Module-load discipline mirrors v7.0.7 §6.1 SN-LLC router-template signature verification at module load. New test `test_config_signature_invalid_at_module_load_blocks_import`.

**RT-26 (HIGH — MTProto session path runtime assertion).** **CLOSED.** §13.6.4 + §13.8.4 + §13.11 updated: the MTProto bot framework is wrapped in an `OrgScopedBot` wrapper class. Constructor requires `org_slug: str` parameter; session storage path is constructed internally as `orgs/<org_slug>/data_collector/mtproto_session/<bot_session_id>.session`. Runtime assertion: at every send call, the wrapper verifies `self.session_path` contains the `org_slug` substring; missing → `RuntimeError("MTProto session path missing org_slug binding; refusing to send")` + admin-risk ledger entry at HIGH `LAW3_VIOLATION` kind. New sub-tag `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.mtproto_session_path_unbound` registered. New test `test_mtproto_session_path_org_slug_required` + `test_mtproto_default_session_path_refused`.

**RT-06 (HIGH — Cedar engine wiring).** **CLOSED.** §13.15 LOCK companion edits + §13.8.6 + §13.8.7 updated to make Cedar engine instantiation MANDATORY at module load: `pipeline/orchestrator/seats/data_collector/__init__.py` imports a `cedar_engine = CedarEngine(policy_dir="pipeline/orchestrator/seats/data_collector/cedar_policies/"); cedar_engine.load_all(); assert cedar_engine.is_ready()` block; failure → module-load fails closed with clear error. Sub-tag `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.cedar_engine_unready` registered. Mirror discipline on Cultivator side is required (`R-CULTIVATOR-NO-DC-LEDGER-IMPORT` AST-lint + Cultivator-side Cedar engine instantiation) — added to §13.11 substrate-split discipline + tracked as Cultivator-side coordination requirement at v1.x or v2 Cultivator blueprint round. New test `test_cedar_engine_ready_at_module_load`.

**RT-07 (MED — shared MTProto bot token misuse / org-scoped Bot wrapper).** **CLOSED via RT-26.** The `OrgScopedBot` wrapper introduced by RT-26 closure is itself the org-scoped wrapper RT-07 calls for. Bot API token remains workspace-shared (per §13.8.4) but is accessed exclusively through `OrgScopedBot` constructor; `OrgScopedBot(org_slug).send_message(chat_id, ...)` verifies the `chat_id` resolves to a `consent_ledger_entry` under the constructor's `org_slug` before invoking the underlying Telegram API; mismatch → `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.mtproto_cross_org` (existing sub-tag) fail-closes. AST-lint `R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT` extension rejects any `from telegram import Bot` or equivalent raw-Bot import in Data Collector code paths; only `OrgScopedBot` import permitted. New test `test_no_raw_telegram_bot_import_ast_lint`.

## §13.16.2 Red Team findings — MED + LOW disposition

**RT-03 (MED — opt-out same-day enforcement timeout race).** **FOLDED_IN.** §13.5.3 atomic-update discipline is updated to require dispatcher to RELEASE the per-recipient ledger lock BETWEEN each per-recipient send (not hold across the full batch). Specifically: `send-batch` per-recipient stage-and-fire dispatches each recipient inside its own atomic transaction `acquire-lock → re-read-consent → re-verify-consent-state-hash (per RT-01 closure) → transport-substrate-call → release-lock` sequence with the lock held only for the duration of the per-recipient transaction (not the full batch); concurrent opt-out writes win-lose the lock on a per-recipient basis. Lock-acquisition-timeout 30s remains but applies per-recipient; bounded by N×30s worst-case batch wall time. Documented as v0.1 + v0.2 first ship discipline bounded by v7 LOCKED A1+A4 single-client preflight assumptions; v2 multi-tenant Section O.5 mitigation track adds queue-based opt-out signal delivery + lock-free read-modify-write CAS pattern for high-throughput batches.

**RT-05 (MED — state-cap intersection vs replacement).** **CLOSED.** §13.9.3 frequency-cap predicate logic is updated: per-state card `<channel>_min_interval_hours` field intersects-with (not replaces) the default 7-day cap. Effective interval = `max(default_lookback_days_in_hours, state_min_interval_hours)`. Predicate fires if ANY of (default cap exceeded, state cap exceeded, channel-switching evasion strict cap exceeded) is true (logical OR — stricter wins). Per-state card field semantic clarified as "additional minimum interval; never relaxes default." New test `test_f_dc_frequency_cap_state_intersection_with_default`.

**RT-09 (MED — group-chat inbound).** **CLOSED.** §13.6.4 Telegram inbound handler updated to reject `chat_id` of type `GROUP` or `SUPERGROUP`. New sub-tag `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.telegram_group_chat_rejected` registered; inbound from group chats quarantined under `pipeline/data_collector_inbound_quarantine/<org_slug>/telegram_group_chat_rejected/<run_id>.yaml`. New test `test_f_dc_telegram_group_chat_inbound_rejected`. Group-chat outbound is structurally disallowed (operator cannot register a group `chat_id` in consent ledger — consent capture rejects non-private-chat types at first-contact).

**RT-12 (HIGH — stale-token replay post-rotation).** **CLOSED.** §13.6.0 token rotation discipline updated: at every `issue-tokens --rotate` invocation, prior tokens for the (recipient × channel × grant) triple are explicitly marked `revoked: True, revoked_at_utc: <rotation_time>` in their on-disk record (not deleted; preserved for audit). Token validation rejects any token with `revoked=True` REGARDLESS of `rotates_at_utc` — sub-tag `.revoked_token_replay`. Schema `sub_awardee_token.v1` adds `revoked: bool` + `revoked_at_utc: datetime | None` fields. New test `test_token_revoked_at_rotation_rejected_regardless_of_rotates_at`.

**RT-16 (MED — Whisper OOM risk on dev hardware).** **CLOSED.** §13.8.3 updated to enforce hardware-tier-bound model whitelist: `whisper_model_size` config field accepts only values from the per-tier whitelist (dev/M1-8GB: `tiny.en` / `base.en`; production/Mac-Studio-128GB: any of `tiny.en` / `base.en` / `small.en` / `medium.en` / `large-v3`). Hardware-tier detection at module load reads `/etc/tilth/hardware_tier.signed.yaml` (Ed25519-signed at Golden Image build); module-load validation rejects model selections outside the detected tier's whitelist with clear error. New test `test_whisper_model_size_dev_tier_rejects_large_v3`.

**RT-17 + RT-18 (LOW — email/SMS token leakage via recipient forwarding).** **FOLDED_IN.** Bounded by v7 LOCKED A4 operator-trusted preflight + recipient-trust envelope. Per-channel binding (RT-10 closure) + AEAD (RT-11 closure) + per-token nonce + per-grant-cycle rotation (RT-12 closure) provide layered mitigation: forwarded email/SMS reveals (a) a channel-bound token that fails validation if replayed on a different channel; (b) a token that rotates per grant cycle limiting blast radius; (c) AEAD ciphertext that cannot be malleated. One-time-use token discipline is v1.1 candidate OQ-DC-NONCE-ONE-TIME-USE per §13.14.2 — at v1.1 each inbound consumes the token; subsequent inbound attempts with same token fail-closed (single-use semantics). v0.2 first ship treats forwarded-token-replay as accepted operator-grade risk bounded by recipient-trust.

**RT-19 (MED — Telegram callback_data length + collision).** **CLOSED.** §13.6.4 Telegram inline-keyboard callback_data discipline updated: callback_data now carries `[T:<short_hash_8_chars>]` where short_hash is the first 8 hex chars of HMAC-SHA256 over `(token_id, salt)` with operator-secret salt; on inbound callback receive, server expands short_hash via lookup table `orgs/<slug>/data_collector/per_recipient_tokens/_callback_short_hash_index.signed.yaml` (per-org index, operator-signed at each issue-tokens invocation). Collision detection: index-write fails-closed on short-hash collision (probability ~2^-32 per pair; cryptographically negligible at expected token counts; mitigation = re-roll salt + regenerate short-hash index). New test `test_telegram_callback_short_hash_index_lookup`.

**RT-21 (MED — state-card signature verification optional).** **CLOSED.** §13.8.7 card loader discipline updated to MANDATE Ed25519 signature verification at every card load (not optional). The card loader function `load_state_card(state_code)` raises `StateCardSignatureError` if signature is missing or invalid; the error is caught at the call site and converted to `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.state_card_signature_invalid` (existing sub-tag) fail-closed gate. New AST-lint extension `R-DATACOLLECTOR-CARD-MANDATORY-SIG-VERIFY` rejects any card load call that bypasses the verification wrapper. New test `test_card_load_signature_missing_fail_closed`.

**RT-23 (MED — argparse flag bypass via env vars).** **CLOSED.** §13.4.1 + §13.4.2 + §13.4.4 argparse setup explicitly disables environment variable overrides for prohibited flags. CLI argument parser configuration: `ArgumentParser(allow_abbrev=False, add_help=True)`; parser's `parse_args` wrapper checks `os.environ` for any of `DATACOLLECTOR_AUTO_CONFIRM`, `DATACOLLECTOR_YES`, `DATACOLLECTOR_FORCE`, `DC_AUTO`, `DC_YES`, `DC_FORCE` keys (case-insensitive); any presence → `EnvironmentVariableOverrideError` raised at parse time with clear message ("Auto-confirm environment variables are not permitted at v0.2 first ship; operator must explicitly interact via TTY"). New tests `test_argparse_rejects_env_var_auto_confirm` + `test_argparse_no_abbreviated_yes_flag`.

**RT-24 (LOW — Cedar engine not wired).** **CLOSED via RT-06.** The mandatory Cedar engine instantiation introduced by RT-06 closure covers RT-24 fully.

**RT-25 (MED — batch atomicity vs per-recipient late-failure).** **CLOSED.** §13.7 operator approval surface flow updated to require **post-PRE-gate sign-and-seal**. The compose-batch step now runs the four PRE-outbound gates per recipient FIRST; recipients that fail any PRE-gate are filtered out BEFORE the operator-review surface displays the batch. The operator reviews the post-gate-filtered batch (only recipients that passed all PRE-gates appear). Operator approves; the signed envelope contains only the post-filter recipient list. Any subsequent PRE-gate failure between sign + send (e.g., concurrent opt-out per RT-01 closure) aborts that specific recipient with a per-recipient SendResult; batch is NOT invalidated as a whole (per-recipient stage-and-fire isolation per §13.7) — the per-recipient send-time consent re-read (per RT-01 closure) is the load-bearing mechanism. New test `test_compose_batch_filters_failed_pre_gates_before_operator_review`.

**RT-27 (MED — yaml.safe_load discipline + AST-lint).** **CLOSED.** §13.8.7 + §13.15 updated to mandate `yaml.safe_load` (or equivalent safe parser) for all YAML deserialization within Data Collector code. New AST-lint extension `R-DATACOLLECTOR-CARD-SAFE-LOAD` rejects any `yaml.load(...)` (unsafe) call; only `yaml.safe_load(...)` or equivalent parser permitted. Mirror discipline applies to consent_ledger loader + sub_awardee_token loader + state_rules_card loader + classification_register loader + outbound_log / inbound_log readers. Mirrors §15 v1 RT-09 closure pattern. New test `test_data_collector_no_yaml_unsafe_load_ast_lint`.

**RT-28 (LOW — beneficiary records write without explicit consent tier — POST-write gate).** **CLOSED.** §13.9 gate roster extended with a 7th gate `F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER` (POST-write). Predicate: after any write to `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/beneficiary_records/`, verify the written record carries `consent_tier: Literal["my_eyes_only","matchable_to_opportunities","composable_with_others"]` field per v7.0.5 §6 + §2 v7.2 LOCKED PII discipline; missing → fail-closed write-rollback (rollback to pre-write state; admin-risk ledger entry at HIGH severity). Composes with AST-lint `R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED` (compile-time) for defense-in-depth (lint-then-runtime-gate). New test `test_f_dc_beneficiary_consent_tier_post_write_required`.

## §13.16.3 Editor findings — disposition

- **E-01 MED (per-channel partition clarity).** **CLOSED.** §13.6.0 summary table prepended with intro paragraph clarifying that each subsequent §13.6.1–§13.6.5 subsection follows a parallel structure: outbound transport substrate + outbound process + per-state-rules layer + per-channel substrate-specific concerns + cross-org/cross-purpose isolation discipline. The parallel structure makes single-read comparison easier across the five channels.
- **E-02 HIGH (operator approval surface readability of four-layer defense).** **CLOSED.** §13.7 four-layer defense summary table added at the start of §13.7 (mirrors §11 v1 §11.7 four-layer autopromote-batch defense table). Each layer enumerated with: layer name, enforcement mechanism (compile-time / runtime / Cedar / TTY), removing-it = attack vector summary.
- **E-03 MED (schema delta readability).** **CLOSED.** §13.5.0 schema delta table prepended with intro paragraph naming v7.0.4 KFR + §2 v7.2 + §11 v1 as conventional sources; cross-references to specific precedent fields cited inline.
- **E-04 LOW (Cultivator-vs-DC override path).** **CLOSED.** §13.11 operator override discipline made explicit: operator decides at Audit #1 between (a) shared MTProto substrate (default; recommended) and (b) fully separated substrates (Cultivator substrate spec deferred to Cultivator's own v1.x or v2 blueprint round). The decision is recorded at Audit #1 disposition; if separated, §13.11 carries forward unchanged for DC-side discipline + operator registers two Telegram applications.
- **E-05 HIGH (cross-amendment composition narrative).** **CLOSED.** §13.0 composition map already present + sufficient; minor clarity addition prepended to §13.0 explaining the parent_locks → §13 wrap pattern (mirrors §15 v1 §15.0 + §11 v1 §11.0 patterns).
- **E-06 MED (SN-LLC update + verification process).** **CLOSED.** §13.8.7 card update cadence subsection expanded to describe: SN-LLC release process (Ed25519 signature with white-glove-pinned public key); operator pull-in via `tilth data-collector update-state-cards` (verifies signature → atomically replaces on-disk versions → invalidates per-org card cache); Trust-On-First-Use rotation discipline for SN-LLC public key (mirrors v7.0.7 §6.1 router-template-update rotation).
- **E-07 LOW (asymmetric-keypair v1.1 deferral).** **CLOSED.** §13.14.2 OQ-DC-KEYPAIR-MODE entry already present; minor clarification added that v0.2 first ship adopts shared-secret tokens; v1.1 candidate adds optional per-recipient asymmetric-keypair mode (sub-awardee opts in at award acceptance).
- **E-08 MED (test matrix coverage summary).** **CLOSED.** §13.13 prepended with two-paragraph summary describing the 13 test sub-sections + their partition (channel dispatch / per-gate / Cultivator isolation / state card / sub-awardee token / operator approval / integration / horizon).

## §13.16.4 Updated gate roster + sub-tag inventory at v1-r1 (post-Cycle-1 closures)

**Final §13.9 gate roster: 7 codes** (was 6; +1 from RT-28 closure adding F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER):

1. F-DATACOLLECTOR-CONSENT-MISSING (PRE pre-outbound + module-load + send-time per RT-01/RT-22 closures)
2. F-DATACOLLECTOR-OPT-OUT-ACTIVE (PRE pre-outbound; cross-channel propagation per RT-02)
3. F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED (PRE pre-outbound; strict default + state-intersection per RT-04/RT-05)
4. F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND (PRE pre-outbound + POST inbound + PRE write; consolidated check with expanded sub-tag inventory per RT-08/RT-09/RT-26/RT-19/RT-21/RT-23)
5. F-DATACOLLECTOR-KFR-DRIFT (POST inbound write; unchanged at v1-r1)
6. F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET (PRE pre-write; unchanged at v1-r1)
7. **F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER** (POST write; NEW per RT-28 closure)

**Sub-tag expansion across the seven gates (Cycle 1 net-new):**

- F-DATACOLLECTOR-CONSENT-MISSING: `.module_load_config_signature_invalid` (RT-22), `.send_time_consent_drift` (RT-01)
- F-DATACOLLECTOR-OPT-OUT-ACTIVE: `.cross_channel_propagation_failure` (RT-02 partial — atomic-write failure on propagation), `.recapture_signature_invalid` (RT-02)
- F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED: `.state_intersection_default_overridden` (RT-05)
- F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND: `.cross_org_chat_id_collision` (RT-08), `.mtproto_session_path_unbound` (RT-26), `.telegram_group_chat_rejected` (RT-09), `.aead_tag_invalid` (RT-11), `.revoked_token_replay` (RT-12), `.per_recipient_signature_invalid` (RT-14), `.cedar_engine_unready` (RT-06), `.env_var_auto_confirm_set` (RT-23), `.channel_binding_mismatch` (RT-10)

**New AST-lint extensions (Cycle 1 net-new):**

- `R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY` (RT-20)
- `R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT` (RT-07)
- `R-DATACOLLECTOR-CARD-MANDATORY-SIG-VERIFY` (RT-21)
- `R-DATACOLLECTOR-CARD-SAFE-LOAD` (RT-27)

**New schema fields (Cycle 1 net-new):**

- `consent_ledger_entry.v1.opt_out_propagated_from_channel: list[Literal[5]+operator_explicit]` (RT-02)
- `sub_awardee_token.v1.channel_binding: Literal[5]` (RT-10)
- `sub_awardee_token.v1.revoked: bool` + `revoked_at_utc: datetime | None` (RT-12)
- `signed_batch_envelope.v1.per_recipient_signature: bytes` (RT-14)
- `signed_batch_envelope.v1.batch_manifest_sha3_512: str` (RT-14)
- `signed_batch_envelope.v1.per_recipient_consent_state_sha3_512_full: dict[recipient_id, str]` (RT-01)

**§0.5 row count adjustment.** Original v1 draft claimed 26 rows (349-374); Cycle 1 closures add 4 schema field rows (re-incorporated into existing schema rows; no new top-level rows) + 1 new failure-code row (F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER) + 4 AST-lint extension rows (kind=`pre-gate-check` consolidated under existing pre-gate rows). Net effect: **§0.5 §13 amendment ROW COUNT updates from 26 to 27** (range 349-375).

## §13.16.5 v0.2-known-limitations + v2 Section O.5 mitigation track (FOLDED_IN)

Per row-170 transparent disposition pattern, the following v0.2-known-limitations are bounded by v7 LOCKED A1+A4 operator-trusted single-client preflight assumptions; v2 multi-tenant Section O.5 mitigation track addresses them as part of v2 amendment:

- **RT-15 voice transcription cloud round-trip (Twilio recording fetch).** Boundary cloud round-trip; mitigated by TLS-pin + temp-buffer + immediate-delete at v0.2; v2 Twilio SIP-trunk-via-localhost alternative.
- **RT-04 (b) household-level frequency cap evasion.** Recipient-level only at v0.2; v1.1 household-grouping schema extension; v2 cross-recipient inference detection.
- **RT-17/18 token leakage via recipient forwarding.** Bounded by recipient-trust; mitigated by per-channel binding + AEAD + per-cycle rotation; v1.1 one-time-use token nonce discipline.

The v2 Section O.5 mitigation track is NOT scoped to v0.2 first ship; documented here to satisfy the audit-trail completeness requirement per L-005 strict two-cycle + row-170 transparent disposition.

## §13.16.6 Cycle 2 closure dispositions (2026-05-10)

Per L-005 strict two-cycle discipline + row-170 transparent disposition pattern (WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + WS-C-M1 v7.0.4-M1 row 190 + WS-K §15 rows 191/192 precedents). Cycle 2 Editor verified all 8 Cycle-1 closures PRESENT_AS_CLAIMED + 2 advisory NEW findings (non-blocking). Cycle 2 Judge re-scored 100/100 with explicit upgrades on legal-exposure containment + token rigor + Cultivator-vs-DC isolation. Cycle 2 Red Team verified 22 of 28 Cycle-1 findings CLOSED + 3 PARTIAL (RT-03 / RT-17 / RT-18 — all bounded by v1.1 horizon items already-documented) + 1 N/A; 13 NEW probes raised against v1-r1 additions. Cycle 2 disposition applies fold-in pattern.

### §13.16.6.1 Cycle 2 PARTIAL closures — bounded by v1.1 OQ

- **RT-03 PARTIAL** — channel_switching_evasion_strict default=True at v0.2 closes the primary attack; household-level grouping is v1.1 horizon OQ-DC-HOUSEHOLD-CAP per §13.14.2. v0.2 first ship treats household-level evasion as accepted operator-grade risk bounded by v7 LOCKED A4 operator-trusted preflight. NO third audit cycle invoked.
- **RT-17 + RT-18 PARTIAL** — token-forwarding via recipient bounded by recipient-trust + per-channel binding (RT-10 closure) + AEAD (RT-11 closure) + per-cycle rotation (RT-12 closure); one-time-use nonce is v1.1 horizon OQ-DC-NONCE-ONE-TIME-USE per §13.14.2. v0.2 first ship treats forwarded-token-replay as accepted operator-grade risk bounded by recipient-trust.

### §13.16.6.2 Cycle 2 NEW probes — fold-in dispositions

**RT-C2-01 (HIGH — per-recipient signed envelope lacks grant_id + org_slug binding).** **FOLDED_IN with explicit text-level mechanism.** §13.5.0 `signed_batch_envelope.v1` per-recipient signing scheme is updated: the signed canonical-JSON over each `OutboundMessage` MUST include `grant_id: str` + `org_slug: str` fields in addition to `rendered_message_bytes_sha3_512` + per-recipient identifiers. Per-recipient signature verification at send time checks `signed.grant_id == invocation.grant_id AND signed.org_slug == invocation.org_slug AND signed.rendered_message_bytes_sha3_512 == recomputed_hash`; any mismatch fail-closes the recipient with `SendResult{sent=False, reason="signature_grant_or_org_mismatch"}`. New sub-tag `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.per_recipient_signature_grant_or_org_mismatch`. New test `test_per_recipient_signature_replay_across_grants_rejected`. Closes the cross-grant replay attack vector RT-C2-01 identifies.

**RT-C2-02 (MED — cross-channel opt-out atomicity rollback).** **FOLDED_IN.** §13.5.3 + §13.16.1 RT-02 closure updated: the cross-channel propagation now uses **all-or-nothing copy-on-write** semantics. Step sequence: (1) acquire fcntl.flock(LOCK_EX) on a workspace-level coordinator file `orgs/<slug>/data_collector/consent_ledger/.propagation_lock`; (2) snapshot the five ledger files' pre-state to a temp directory; (3) write new state to all five ledger files; (4) if ANY write fails (disk error, ENOSPC, ENOPERM), restore the temp snapshot back to canonical paths via `os.rename` (atomic per filesystem); (5) release the coordinator lock. New gate `F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED` registered (8th gate; PRE write — fail-closes the batch send if propagation failed). New test `test_f_dc_opt_out_propagation_partial_failure_rollback`.

**RT-C2-03 (HIGH — OrgScopedBot subclass bypass).** **FOLDED_IN.** §13.6.4 + §13.11 OrgScopedBot wrapper hardened: the class is marked `@final` (PEP 591 typing.final decorator); runtime check `if type(self) is not OrgScopedBot: raise RuntimeError("OrgScopedBot is final; subclassing not permitted")` in `__init__`. New AST-lint extension `R-DATACOLLECTOR-ORGSCOPEDBOT-FINAL` rejects any class definition that inherits from `OrgScopedBot`. Sub-tag `.orgscoped_bot_subclassing_forbidden` added to F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND. Dispatcher additionally verifies `self.org_slug == expected_org_slug` at every send call (not only at construction). New test `test_orgscoped_bot_subclass_runtime_rejected`.

**RT-C2-04 (MED — Cedar engine load failure caught by upstream try/except).** **FOLDED_IN.** §13.16.1 RT-06 closure strengthened: Cedar engine load failure raises a custom `CriticalPolicyError(SystemExit)` that subclasses `BaseException` (NOT `Exception`) — Python's bare `try/except Exception:` blocks do NOT catch `BaseException` subclasses, so upstream wrappers cannot silently swallow Cedar load failures. Plus `cedar_engine.is_ready() is True` identity-strict check (per v7.0.7 §4.3.4 identity-strict pattern; truthy non-True fail-closes). New AST-lint extension `R-DATACOLLECTOR-CEDAR-NO-CATCH` rejects any `try:` block containing a Data Collector module import with corresponding `except BaseException` or `except:` bare clause. New test `test_cedar_engine_load_failure_propagates_through_try_except`.

**RT-C2-05 (MED — send-time consent TOCTOU between lock-release and transport call).** **FOLDED_IN.** §13.16.1 RT-01 closure tightened: per-recipient send transaction now holds the fcntl.flock(LOCK_EX) on the consent ledger entry THROUGH the transport substrate call (not released between re-read and send). Lock-holding timeout 30 seconds per recipient (mirrors §15 v1 NF-02 + §13.9.2 same-day enforcement timeout pattern); transport call exceeding timeout fail-closes the recipient with `SendResult{sent=False, reason="transport_timeout_during_send_lock_hold"}`. New sub-tag `.send_lock_hold_timeout`. Bounded by v7 LOCKED A1 single-client preflight (no multi-tenant lock-contention at v0.2); v2 multi-tenant Section O.5 mitigation track adds queue-based dispatch with read-modify-write CAS for high-throughput batches. New test `test_send_time_consent_lock_held_through_transport`.

**RT-C2-06 (MED — channel-bound token UUID collision).** **FOLDED_IN.** §13.16.1 RT-10 + §13.6.0 token issuance discipline updated: token_id MUST be generated via `uuid.uuid4()` (cryptographically random from OS entropy; per RFC 4122 v4 — 122 random bits = ~5×10^36 collision probability per pair, negligible). Runtime uniqueness check at issue-tokens write: scan existing `orgs/<slug>/data_collector/per_recipient_tokens/<grant_id>__*.signed.yaml` for any matching `token_id`; collision → `TokenCollisionError` raised (fail-closed; abort issue-tokens batch). Operator re-runs issue-tokens (which generates new UUIDs). New sub-tag `.token_id_collision_detected`. New test `test_token_uuid_uniqueness_check_at_issue`.

**RT-C2-07 (MED — AEAD nonce reuse).** **FOLDED_IN.** §13.16.1 RT-11 closure updated: token encryption now mandates per-token random 96-bit (12-byte) nonce generated via `os.urandom(12)` (OS entropy CSPRNG); nonce stored alongside `secret_value_ciphertext` field in the on-disk token record. Encryption routine refuses to encrypt if the per-grant nonce register already contains the generated nonce (collision probability ~5×10^28 per pair); collision → abort + re-roll. New AST-lint extension `R-DATACOLLECTOR-TOKEN-NONCE-UNIQUE` validates that encryption call sites pass a fresh nonce. Schema `sub_awardee_token.v1` extended: `aead_nonce: bytes` (12-byte; required). New test `test_aead_nonce_uniqueness_per_token`.

**RT-C2-08 (LOW — CIC × CLC audit one-time at LOCK).** **FOLDED_IN as CI requirement.** §13.16.1 RT-20 closure + §13.15 LOCK companion edits updated: the four-layer CIC × CLC audit MUST also run as a post-commit CI job on every commit to `pipeline/orchestrator/seats/data_collector/` or `orgs/_TEMPLATE/data_collector/` or `pipeline/blueprint/v0.1/section_13_data_collector.md`. CI failure = blocked merge. New test `test_cic_clc_audit_runs_in_ci_not_only_at_lock`.

**RT-C2-09 (MED — operator-config valid signature but dangerous values).** **FOLDED_IN.** §13.16.1 RT-22 closure + §13.4.1 operator-config validation updated: `data_collector_config.yaml` Pydantic schema enforces per-field range constraints in addition to signature verification. Specifically: `frequency_cap_lookback_days >= 1` (no 0-day caps); `channel_switching_evasion_strict: bool` (no override absent signed config); `whisper_model_size` whitelist per hardware tier (per RT-16 closure); per-channel substrate fields are from the ADR-001 enumerated whitelist only. Out-of-range → `F-DATACOLLECTOR-CONSENT-MISSING.config_value_invalid` sub-tag fail-closes module load. New test `test_config_value_out_of_range_rejected_at_module_load`.

**RT-C2-10 (LOW — beneficiary records consent_tier enum validation).** **FOLDED_IN.** §13.16.2 RT-28 closure + §13.9 F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER predicate strengthened: the gate now validates that `consent_tier` value is in the v7.0.5 §6 enumerated literal set `{my_eyes_only, matchable_to_opportunities, composable_with_others}`. Out-of-enum → fail-closed write-rollback. New AST-lint extension `R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM` validates Pydantic schema. New test `test_f_dc_beneficiary_consent_tier_enum_validation`.

**RT-C2-11 (MED — inbound classification register signature re-verification on read).** **FOLDED_IN.** §13.9.6 F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET predicate strengthened: before any inbound write to operational-data sub-kind, the classification register Ed25519 signature is re-verified (mirrors §15 v1 §15.9.5 NF-01 runtime-immutability self-check + v7.0.4-M1 atomic-read fcntl.flock pattern). Signature mismatch → `F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET.classification_register_tampered` sub-tag fail-closes; admin-risk ledger entry at HIGH `TAMPER_EVENT` kind. New test `test_classification_register_signature_reverified_at_each_inbound_write`.

**RT-C2-12 (LOW — batch manifest order swap).** **FOLDED_IN.** §13.5.0 `signed_batch_envelope.v1` schema updated: the signed payload includes an explicit ordered list of `recipient_id`s (`approved_recipient_order: list[str]`); send-time verification ensures the dispatch order matches the signed order; order mismatch → `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.batch_recipient_order_swap` sub-tag fail-closes. New test `test_batch_recipient_order_signed_and_verified`.

**RT-C2-13 (MED — env-var bypass via wrapper script).** **FOLDED_IN.** §13.16.2 RT-23 closure + CLI entry-point hardened: after argparse parse, the entry point ALSO checks `os.environ` for prohibited keys (`DATACOLLECTOR_AUTO_CONFIRM`, `DATACOLLECTOR_YES`, `DATACOLLECTOR_FORCE`, `DC_AUTO`, `DC_YES`, `DC_FORCE`); presence raises `RuntimeError("Environment variable override attempt detected; refusing to run")` even if the flag was not passed via argv. New AST-lint extension `R-DATACOLLECTOR-ENV-VAR-PROHIBIT-BYPASS` validates entry-point structure. New test `test_env_var_prohibit_check_runs_after_argparse`.

### §13.16.6.3 Cycle 2 Editor advisory dispositions

- **E-NF-01 LOW (closure language operational clarity).** **ACKNOWLEDGED + accepted as v0.2 advisory.** The §13.16 closure dispositions are operationally specific enough that Code-phase author can realize them (Cycle 2 Judge concurs at 100/100); further concision is a v1.1 stylistic polish OQ tracked but not blocking.
- **E-NF-02 LOW (gate roster expansion consistency across §13.9.0 + §13.16.4).** **CLOSED.** Cross-checked at LOCK ceremony: §13.9.0 lists 6 consolidated-PRE-outbound check codes; §13.16.4 lists 7 v1-r1 gates (including the new F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER POST-write); the discrepancy is by design (the consolidated check covers only the four PRE-outbound gates; F-DATACOLLECTOR-KFR-DRIFT + F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET + F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER each have their own check callable). No actual inconsistency.

### §13.16.6.4 Final v1 LOCK gate roster (post-Cycle-2 fold-ins)

**Final §13.9 gate roster: 8 codes** (was 6 at draft; +1 at Cycle 1 via RT-28; +1 at Cycle 2 via RT-C2-02 OPT-OUT-PROPAGATION-FAILED):

1. F-DATACOLLECTOR-CONSENT-MISSING (PRE pre-outbound + module-load + send-time)
2. F-DATACOLLECTOR-OPT-OUT-ACTIVE (PRE pre-outbound; cross-channel propagation; lock-held-through-transport)
3. F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED (PRE pre-outbound; strict default + state-intersection)
4. F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND (consolidated PRE + POST + PRE-write; ~20 sub-tags)
5. F-DATACOLLECTOR-KFR-DRIFT (POST inbound write; advisory)
6. F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET (PRE pre-write; classification register signature re-verified per RT-C2-11)
7. F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER (POST write; consent_tier enum validated per RT-C2-10)
8. **F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED** (PRE write; NEW per RT-C2-02; fires on cross-channel propagation rollback failure)

**Final AST-lint roster (Cycle 1 + Cycle 2 net):**

1. R-DATACOLLECTOR-NO-AUTOSEND (v1 baseline)
2. R-DATACOLLECTOR-VAULT-INTENT-REQUIRED (v1 baseline)
3. R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT (v1 baseline)
4. R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED (v1 baseline; compile-time)
5. R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY (Cycle 1 RT-20)
6. R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT (Cycle 1 RT-07)
7. R-DATACOLLECTOR-CARD-MANDATORY-SIG-VERIFY (Cycle 1 RT-21)
8. R-DATACOLLECTOR-CARD-SAFE-LOAD (Cycle 1 RT-27)
9. R-DATACOLLECTOR-ORGSCOPEDBOT-FINAL (Cycle 2 RT-C2-03)
10. R-DATACOLLECTOR-CEDAR-NO-CATCH (Cycle 2 RT-C2-04)
11. R-DATACOLLECTOR-TOKEN-NONCE-UNIQUE (Cycle 2 RT-C2-07)
12. R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM (Cycle 2 RT-C2-10)
13. R-DATACOLLECTOR-ENV-VAR-PROHIBIT-BYPASS (Cycle 2 RT-C2-13)

**Updated §0.5 row count.** Original v1 draft: 26 rows (349-374). Cycle 1 added 1 failure-code row + several AST-lint rows consolidated under existing pre-gate-check rows → 27 rows. Cycle 2 fold-ins add 1 failure-code row (F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED) + ~9 sub-tag additions absorbed into existing failure-code rows + 5 new AST-lint extension rows consolidated → **final §0.5 §13 amendment row count: 28 rows** (range 349-376; runtime-live total after this LOCK = 376).

---

End of §13 Data Collector blueprint v1 LOCKED 2026-05-10. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor (Editor=Llama-3.3-70B/Groq READY_TO_LOCK + Judge=Gemini-2.5-Pro/Google READY_TO_LOCK 100/100 + Red Team=GPT-OSS-120B/Groq PASS blocking:false). Compound LOCK ceremony at the same paired-commit per §6.17 Option-B with `section_00_5_section_13_data_collector_amendment.md` companion file.

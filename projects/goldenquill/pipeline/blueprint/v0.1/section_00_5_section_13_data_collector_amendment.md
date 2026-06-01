---
title: §0.5 Blueprint Interface Index — §13 Data Collector rows amendment (LOCKED 2026-05-10)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 — compound paired-commit with §13 v1 LOCK per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor (audit trail at pipeline/validation/blueprint_section_13_data_collector_2026-05-10/{audit_v1_*.md, audit_v2_*.md}). Cycle 2 PARTIAL closures (RT-03 / RT-17 / RT-18) + 13 NEW probes (RT-C2-01..13) folded-in at LOCK per row-170 transparent disposition pattern (mirrors WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + WS-C-M1 v7.0.4-M1 row 190 + WS-K §15 rows 191/192 precedents). Eighth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                                 # §0.5 v5 LOCKED 2026-04-19 — 101 master rows
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md                # §0.5 v6 LOCKED 2026-04-21 — rows 102-117
  - pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md                            # §0.5 v7 LOCKED 2026-04-21 — rows 118-158
  - pipeline/blueprint/v0.1/section_00_5_section_10_red_team_amendment.md                          # §0.5 v8 LOCKED 2026-05-02 — rows 159-211
  - pipeline/blueprint/v0.1/section_00_5_section_12_uploader_amendment.md                          # §0.5 v9 LOCKED 2026-05-10 — rows 212-232
  - pipeline/blueprint/v0.1/section_00_5_section_11_intake_amendment.md                            # §0.5 v10 LOCKED 2026-05-10 — rows 233-256
  - pipeline/blueprint/v0.1/section_00_5_section_02_v7_2_operational_amendment.md                  # §0.5 v11 LOCKED 2026-05-10 — rows 257-278
  - pipeline/blueprint/v0.1/section_00_5_section_05_v8_amendment.md                                # §0.5 v12 LOCKED 2026-05-10 — rows 279-290
  - pipeline/blueprint/v0.1/section_00_5_section_15_archivist_amendment.md                         # §0.5 v13 LOCKED 2026-05-10 — rows 291-304
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_amendment.md                              # §0.5 v14 LOCKED 2026-05-10 — rows 305-348
  - pipeline/blueprint/v0.1/section_13_data_collector.md                                           # §13 v1 LOCKED 2026-05-10
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_13_data_collector.md  # paired-commit at §13 v1 LOCK per §6.17 Option-B
compound_lock_with: section_13_data_collector.md v1
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §13 v1; resolves to actual commit hash at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v14 LOCK 2026-05-10 = 348 rows. **§13 amendment claims rows 349-376 (28 rows: 1 marker + 7 input-schema + 5 channel-protocol interface-contract + 1 outbound-message schema + 1 inbound-response schema + 1 consent-ledger-entry schema + 1 sub-awardee-token schema + 1 state-rules-card schema + 1 signed-batch-envelope schema + 8 failure-code rows + 1 consolidated pre-gate-check row).** New runtime-live total at this LOCK = 376.
kind_of_amendment: row-append. NO vocabulary extension — every row's `primitive_kind` resolves against the v5 + v6 closed vocabulary (marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check).
dependency_order: §13 v1 LOCK + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`. §4 v2.x amendment §5.1 HORIZON ACTIVATION (Data Collector family — six gates registered at HORIZON 2026-05-10T20:45:00Z; flip to ACTIVE at this LOCK) + the two NEW gates from Cycle 1/Cycle 2 (F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER + F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED) lands in a follow-on §4 v2.x.1 minor amendment per the §15 v1 v1.x-implementation-deferred precedent — the gate predicate bodies are skeleton stubs raising NotImplementedError at v0.2 first ship; Code-phase WS-I follow-on dispatch realizes the predicate bodies.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 28 new rows must be present in the index or the commit fails closed.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent (lock_history row 179, 2026-05-10). Eighth v0.1+v0.2 round to LOCK at this rigor level (after WS-D v7.0.5 architecture-class + WS-F §12 v1 + WS-E §11 v1 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 + WS-C-M1 v7.0.4-M1 + WS-L §4 v2.x blueprint/architecture-class precedents).
---

# Amendment intent

This amendment lands paired with §13 v1 LOCK per §6.17 Option-B compound-commit pattern. It registers §13-owned primitives (one section-anchor marker + seven input-schema rows + five channel-protocol interface-contract rows + ten data-schema rows + eight failure-code rows + one consolidated pre-gate-check row) into the Index. It does NOT reserve section anchors for any other downstream blueprint — §13 is the last v0.2-wave seat-spec section to LOCK (Intake = §11 LOCKED rows 233-256; Uploader = §12 LOCKED rows 212-232; Data Collector = §13 THIS; Report Generator = §14 v0.2 horizon pending WS-J dispatch; Archivist = §15 v1 SPEC LOCKED rows 291-304).

The §11 v1 amendment (§0.5 v10 LOCKED 2026-05-10 with rows 233-256 across 24 rows) and the §12 v1 amendment (§0.5 v9 LOCKED 2026-05-10 with rows 212-232 across 21 rows) and the §15 v1 amendment (§0.5 v13 LOCKED 2026-05-10 with rows 291-304 across 14 rows) are the load-bearing precedents for the explode-per-failure-code pattern. F-DATACOLLECTOR-* gate family at v1 contains 8 codes (was 6 at v1 draft; +1 at Cycle 1 via RT-28 BENEFICIARY-CONSENT-TIER; +1 at Cycle 2 via RT-C2-02 OPT-OUT-PROPAGATION-FAILED); this amendment registers one `failure-code` row per code (rows 365-372), one `pre-gate-check` row consolidating the four PRE-outbound gates per §4 v2.2 consolidated-check pattern (row 373), and additional dedicated check-callable rows for the non-consolidated gates (POST + PRE-write — rows 374-376).

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §13. Future master re-author folds all v6-v15 amendment files into the master.

# Amendment §A — row append (rows 349-376)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v1 LOCK (no PARENT_UNLOCKED transit since §13 LOCKs in the same compound transaction).

**Marker (row 349) — §13 section anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | stability_tier |
|---|---|---|---|---|---|---|
| 349 | `blueprint.section_anchor.s13_data_collector.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md` | §13 v1 | `<resolved_at_commit>` | marker | STABLE |

**Schemas — input contracts (rows 350-353):**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 350 | `data_collector.outbound_batch_compose_input.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.4.1` | schema | OutboundBatchComposeInput frozen kw_only |
| 351 | `data_collector.outbound_batch_send_input.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.4.2` | schema | OutboundBatchSendInput frozen kw_only |
| 352 | `data_collector.inbound_parse_input.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.4.3` | schema | InboundParseInput frozen kw_only |
| 353 | `data_collector.inbound_classify_input.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.4.4` | schema | InboundClassifyInput frozen kw_only |

**Interface contracts — per-channel ChannelProtocol (rows 354-358):**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 354 | `data_collector.channel_protocol.email.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.4.0+§13.6.1` | interface-contract | ChannelProtocol implementation for email channel (SMTP via BYOK provider) |
| 355 | `data_collector.channel_protocol.sms.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.4.0+§13.6.2` | interface-contract | ChannelProtocol implementation for SMS channel (Twilio/Plivo via BYOK) |
| 356 | `data_collector.channel_protocol.voice.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.4.0+§13.6.3` | interface-contract | ChannelProtocol implementation for voice channel (Twilio Voice outbound + local Whisper transcription always-local per v7.0.7) |
| 357 | `data_collector.channel_protocol.telegram.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.4.0+§13.6.4` | interface-contract | ChannelProtocol implementation for Telegram channel (MTProto bot via python-telegram-bot/pyrogram; shared substrate with Cultivator per §13.11; OrgScopedBot wrapper @final per Cycle 2 RT-C2-03 closure) |
| 358 | `data_collector.channel_protocol.whatsapp.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.4.0+§13.6.5` | interface-contract | ChannelProtocol implementation for WhatsApp channel (WhatsApp Business API via heyoo/whatsapp-business-cloud-api) |

**Schemas — data contracts (rows 359-364):**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 359 | `data_collector.outbound_message.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.5.0+§13.5.1` | schema | OutboundMessage frozen kw_only; rendered_message_bytes_sha3_512 (full 128-hex-char digest per Cycle 1 RT-13); per-recipient signed by operator including grant_id+org_slug per Cycle 2 RT-C2-01 closure |
| 360 | `data_collector.inbound_response.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.5.0+§13.5.2` | schema | InboundResponse frozen kw_only; classification_status defaults DEFAULT_CONFIDENTIAL_PENDING_REVIEW per v7.0.7 §4.1 |
| 361 | `data_collector.consent_ledger_entry.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.5.0+§13.5.3` | schema | ConsentLedgerEntry frozen kw_only; opt_out_propagated_from_channel field per Cycle 1 RT-02 cross-channel propagation closure; atomic fcntl.flock(LOCK_EX) with all-or-nothing copy-on-write rollback per Cycle 2 RT-C2-02 closure |
| 362 | `data_collector.sub_awardee_token.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.5.0+§13.6.0+§13.8.8` | schema | SubAwardeeToken frozen kw_only; channel_binding field per Cycle 1 RT-10; revoked field per Cycle 1 RT-12; AEAD-encrypted with per-token random 96-bit nonce per Cycle 2 RT-C2-07; UUID uniqueness check at issue per Cycle 2 RT-C2-06 |
| 363 | `data_collector.state_rules_card_entry.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.8.7` | schema | StateRulesCardEntry frozen kw_only; PA/CA/FL/TX/NY at v0.2 first wave; SN-LLC Ed25519-signed; mandatory signature verification per Cycle 1 RT-21 closure |
| 364 | `data_collector.signed_batch_envelope.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.4.2+§13.5.0` | schema | SignedBatchEnvelope frozen kw_only; batch_content_sha3_512 full 128-hex-char digest per Cycle 1 RT-13; per_recipient_signature including grant_id+org_slug per Cycle 2 RT-C2-01; approved_recipient_order list per Cycle 2 RT-C2-12; per_recipient_consent_state_sha3_512_full dict per Cycle 1 RT-01 send-time consent re-read |

**Failure codes (rows 365-372) — explode pattern per §10 / §11 / §12 / §15 precedent; one row per F-DATACOLLECTOR-* code at v1:**

| Row | primitive_id | defined_at | kind | Parent / sub-tags |
|---|---|---|---|---|
| 365 | `data_collector.failure_code.F-DATACOLLECTOR-CONSENT-MISSING.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.9.1` | failure-code | PRE pre-outbound + module-load + send-time. Sub-tags `.ledger_absent`, `.consent_inactive`, `.method_unset`, `.config_signature_invalid`, `.module_load_config_signature_invalid` (Cycle 1 RT-22), `.send_time_consent_drift` (Cycle 1 RT-01), `.config_value_invalid` (Cycle 2 RT-C2-09), `.env_var_auto_confirm_set` (Cycle 1 RT-23). |
| 366 | `data_collector.failure_code.F-DATACOLLECTOR-OPT-OUT-ACTIVE.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.9.2` | failure-code | PRE pre-outbound; cross-channel propagation per Cycle 1 RT-02; lock-held-through-transport per Cycle 2 RT-C2-05. Sub-tags `.opt_out_active_email`, `.opt_out_active_sms`, `.opt_out_active_voice`, `.opt_out_active_telegram`, `.opt_out_active_whatsapp`, `.cross_channel_propagation_failure`, `.recapture_signature_invalid`, `.send_lock_hold_timeout` (Cycle 2 RT-C2-05). |
| 367 | `data_collector.failure_code.F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.9.3` | failure-code | PRE pre-outbound; strict default per Cycle 1 RT-04; state intersection per Cycle 1 RT-05. Sub-tags `.recipient_channel_cap`, `.state_cap`, `.channel_switching_evasion`, `.state_intersection_default_overridden`. |
| 368 | `data_collector.failure_code.F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.9.4` | failure-code | PRE pre-outbound + POST inbound + PRE write. Sub-tags (~20+): `.semantic_slot_in_outbound`, `.path_cross_org`, `.symlink_escape`, `.mtproto_cross_org`, `.sms_size_overflow`, `.whatsapp_template_unapproved`, `.state_card_signature_invalid`, `.batch_hash_mismatch`, `.token_invalid_inbound`, `.cross_org_chat_id_collision` (Cycle 1 RT-08), `.mtproto_session_path_unbound` (Cycle 1 RT-26), `.telegram_group_chat_rejected` (Cycle 1 RT-09), `.aead_tag_invalid` (Cycle 1 RT-11), `.revoked_token_replay` (Cycle 1 RT-12), `.per_recipient_signature_invalid` (Cycle 1 RT-14), `.cedar_engine_unready` (Cycle 1 RT-06), `.channel_binding_mismatch` (Cycle 1 RT-10), `.orgscoped_bot_subclassing_forbidden` (Cycle 2 RT-C2-03), `.per_recipient_signature_grant_or_org_mismatch` (Cycle 2 RT-C2-01), `.batch_recipient_order_swap` (Cycle 2 RT-C2-12), `.token_id_collision_detected` (Cycle 2 RT-C2-06). |
| 369 | `data_collector.failure_code.F-DATACOLLECTOR-KFR-DRIFT.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.9.5` | failure-code | POST inbound write; ADVISORY (not fail-closed). Sub-tags `.numeric_field_above_tolerance`, `.numeric_field_below_tolerance`, `.unit_mismatch`. Composes with F-LOGICIAN-FACT-DRIFT family (v7.0.4 §4). |
| 370 | `data_collector.failure_code.F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.9.6` | failure-code | PRE pre-write to operational-data sub-kind; classification register signature re-verified per Cycle 2 RT-C2-11. Sub-tags `.first_occurrence_unclassified`, `.default_confidential_pending_review`, `.classification_register_tampered` (Cycle 2 RT-C2-11). |
| 371 | `data_collector.failure_code.F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.16.2+§13.16.6.4` | failure-code | POST write to beneficiary_records sub-kind (NEW per Cycle 1 RT-28). Composes with AST-lint R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED (compile-time) + R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM (Cycle 2 RT-C2-10). Sub-tags `.consent_tier_missing`, `.consent_tier_enum_invalid` (Cycle 2 RT-C2-10). |
| 372 | `data_collector.failure_code.F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.16.6.2` | failure-code | PRE write (NEW per Cycle 2 RT-C2-02). All-or-nothing copy-on-write rollback across five ledger files; lock acquisition via coordinator file `orgs/<slug>/data_collector/consent_ledger/.propagation_lock`. Sub-tag `.partial_propagation_rollback_required`. |

**PRE-gate-check (row 373) — consolidated per check callable per §4 v2.2 pattern:**

| Row | primitive_id | defined_at | kind | Parent / consolidated codes covered |
|---|---|---|---|---|
| 373 | `data_collector.pre_gate.compose_send_validation.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.9.0` | pre-gate-check | Consolidates the four PRE-outbound gates: F-DATACOLLECTOR-CONSENT-MISSING + F-DATACOLLECTOR-OPT-OUT-ACTIVE + F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED + F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND. Short-circuit ordered sequence per §13.9.0. Returns first-fired sub-tag. Per §4 v2.2 consolidated-check-callable pattern. |

**POST-gate-check (row 374) — KFR drift advisory:**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 374 | `data_collector.post_gate.inbound_kfr_drift.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.9.5` | post-gate-check | Backs F-DATACOLLECTOR-KFR-DRIFT advisory POST-inbound-write. Per-field tolerance + unit-mismatch detection. Composes with F-LOGICIAN-FACT-DRIFT family (v7.0.4 §4). |

**PRE-gate-check (row 375) — inbound classification:**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 375 | `data_collector.pre_gate.inbound_classification_set.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.9.6` | pre-gate-check | Backs F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET PRE-pre-write. Classification register Ed25519 signature re-verified per Cycle 2 RT-C2-11. |

**POST-gate-check (row 376) — beneficiary consent tier:**

| Row | primitive_id | defined_at | kind | Parent |
|---|---|---|---|---|
| 376 | `data_collector.post_gate.beneficiary_consent_tier.v1` | `pipeline/blueprint/v0.1/section_13_data_collector.md#§13.16.2+§13.16.6.2` | post-gate-check | Backs F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER POST-write (NEW per Cycle 1 RT-28). consent_tier enum validation per Cycle 2 RT-C2-10. Defense-in-depth with AST-lint compile-time R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED + R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM. |

# Amendment §B — row description block (per-row narrative)

- **349** `blueprint.section_anchor.s13_data_collector.v1` (kind=marker) — §13 Data Collector section anchor. v0.2 horizon support agent; spec + Phase-1 module skeleton at v1 LOCK; full per-channel substrate implementation via WS-I Code phase follow-on dispatch. Five outbound channels at v0.2 first ship (email + SMS + voice + Telegram + WhatsApp); operator approves per-cycle outbound batch via four-layer defense (AST-lint + dispatcher signature + Cedar policy + TTY check); inbound parsing always-local per v7.0.7 §4.1. Marker per `marker` precedent in v1 closed vocabulary (§0.5.3.1).
- **350** `data_collector.outbound_batch_compose_input.v1` (kind=schema) — `OutboundBatchComposeInput` frozen kw_only: run_id, org_slug, grant_id, period_n, proposal_commitments_path (PROMOTED status required), reporting_template_path, consent_ledger_dir, sub_awardee_token_register_dir, state_rules_card_dir, channels_in_scope (operator-set; default ["email"] at v0.2 first ship), frequency_cap_lookback_days, invoked_at_utc. Bundle invariants enforced PRE-gate by `data_collector.pre_gate.compose_send_validation.v1` + path-isolation per F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.
- **351** `data_collector.outbound_batch_send_input.v1` (kind=schema) — `OutboundBatchSendInput` frozen kw_only: run_id, org_slug, grant_id, period_n, signed_batch_path (Ed25519-signed envelope including grant_id + org_slug per Cycle 2 RT-C2-01; per-recipient signatures; batch_content_sha3_512 full digest), invoked_at_utc. Send-time consent re-read per Cycle 1 RT-01 closure; per-recipient signature verification with grant_id+org_slug binding per Cycle 2 RT-C2-01.
- **352** `data_collector.inbound_parse_input.v1` (kind=schema) — `InboundParseInput` frozen kw_only: run_id, org_slug (resolved via per-channel recipient resolver; cross-org chat_id collision quarantine per Cycle 1 RT-08), grant_id, channel, raw_payload (per-channel size-bounded), receipt_metadata, received_at_utc. Always-local per v7.0.7 routing posture.
- **353** `data_collector.inbound_classify_input.v1` (kind=schema) — `InboundClassifyInput` frozen kw_only: run_id, org_slug, grant_id, inbound_log_dir, invoked_at_utc. TTY required; argparse rejects `--yes`/`--auto-confirm`/`--force` + env-var bypass per Cycle 1 RT-23 + Cycle 2 RT-C2-13.
- **354** `data_collector.channel_protocol.email.v1` (kind=interface-contract) — Email ChannelProtocol implementation. SMTP via BYOK provider (Postmark/SendGrid/Mailgun candidate set per §13.8.1); endpoint validation per F-CLASS-ROUTING-INDETERMINATE PRE-call; token in `X-Tilth-Recipient-Token` custom header + URL-encoded in unsubscribe link (double-source validation); CAN-SPAM unsubscribe link mandatory + per-state-required disclaimers per card.
- **355** `data_collector.channel_protocol.sms.v1` (kind=interface-contract) — SMS ChannelProtocol implementation. Twilio Messaging API or Plivo (BYOK); token as `[T:<token_id>]` prefix-tag; STOP/UNSUBSCRIBE/END/CANCEL/QUIT cross-channel propagation per Cycle 1 RT-02; 1600-byte size bound per §13.6.2; TCPA prior-express-written-consent.
- **356** `data_collector.channel_protocol.voice.v1` (kind=interface-contract) — Voice ChannelProtocol implementation. Twilio Voice outbound + local Whisper-class transcription inbound (always-local per v7.0.7); TLS-pinned Twilio recording fetch + temp-buffer-only + immediate-delete per Cycle 1 RT-15; voice quiet hours per state card; token verbal announcement + DTMF capture.
- **357** `data_collector.channel_protocol.telegram.v1` (kind=interface-contract) — Telegram ChannelProtocol implementation. MTProto bot via python-telegram-bot/pyrogram; OrgScopedBot wrapper @final per Cycle 2 RT-C2-03 (`R-DATACOLLECTOR-ORGSCOPEDBOT-FINAL` AST-lint); shared substrate with Cultivator per §13.11 (four structural separations: per-purpose paths + ledgers + Cedar denial + AST-lint); cross-org chat_id quarantine per Cycle 1 RT-08; group-chat rejection per Cycle 1 RT-09; token as inline-keyboard callback_data short-hash + message body per Cycle 1 RT-19.
- **358** `data_collector.channel_protocol.whatsapp.v1` (kind=interface-contract) — WhatsApp ChannelProtocol implementation. WhatsApp Business API (Meta-issued BYOK); pre-approved template register; 24-hour conversation window discipline; token in message body + interactive-message header (double-source).
- **359-364** Data schemas — `OutboundMessage` / `InboundResponse` / `ConsentLedgerEntry` / `SubAwardeeToken` / `StateRulesCardEntry` / `SignedBatchEnvelope`. All frozen kw_only Pydantic dataclasses; field details per §13.5.0 schema delta table + Cycle 1 + Cycle 2 fold-in additions.
- **365-372** Failure codes — eight F-DATACOLLECTOR-* failure-code rows with explicit sub-tag enumerations. Per the explode-per-failure-code pattern from §10 / §11 / §12 / §15 precedents.
- **373** `data_collector.pre_gate.compose_send_validation.v1` (kind=pre-gate-check) — consolidates four PRE-outbound gates per §4 v2.2 consolidated-check-callable pattern.
- **374** `data_collector.post_gate.inbound_kfr_drift.v1` (kind=post-gate-check) — backs F-DATACOLLECTOR-KFR-DRIFT advisory.
- **375** `data_collector.pre_gate.inbound_classification_set.v1` (kind=pre-gate-check) — backs F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET.
- **376** `data_collector.post_gate.beneficiary_consent_tier.v1` (kind=post-gate-check) — backs F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER (NEW per Cycle 1 RT-28).

# Amendment §C — Vocabulary preservation

Every row in this amendment uses one of the 16-value closed `primitive_kind` vocabulary established at §0.5 v5 LOCK + extended at §0.5 v6 LOCK (`procedure`):

- `marker` (row 349)
- `schema` (rows 350-353 input contracts + 359-364 data contracts = 10 schema rows)
- `interface-contract` (rows 354-358 per-channel ChannelProtocol = 5 interface-contract rows)
- `failure-code` (rows 365-372 = 8 failure-code rows)
- `pre-gate-check` (rows 373 + 375 = 2 pre-gate-check rows)
- `post-gate-check` (rows 374 + 376 = 2 post-gate-check rows)

Total: 1 + 10 + 5 + 8 + 2 + 2 = 28 rows. No vocabulary extension.

# Amendment §D — F-INDEX-STALE PRE-gate preflight discipline

At commit time, F-INDEX-STALE PRE-gate fires. All 28 new rows (349-376) MUST be present in the runtime-live index (the union of master + v6 through v15 amendments) OR the commit fails closed. Compound LOCK semantics: §13 v1 blueprint LOCK + this §0.5 amendment LOCK + §4 v2.x §5.1 HORIZON-to-ACTIVE flip-flag (referenced; realized in §4 v2.x.1 follow-on Code dispatch) land in a single atomic transaction at `lock_timestamp_utc`.

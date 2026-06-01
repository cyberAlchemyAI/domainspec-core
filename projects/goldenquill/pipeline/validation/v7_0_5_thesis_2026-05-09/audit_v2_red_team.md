<!-- seat=red_team family=openai-oss model=groq/openai/gpt-oss-120b cycle=2 dispatched_at=2026-05-10T04:01:51Z -->

**Red‑Team Cycle‑2 Verification – Tilth v7.0.5 (Amendment v7.0.5)**  
*Seat: OpenAI‑OSS (GPT‑OSS 120B / Groq)*  

---

## 1. Premises (re‑cited)

| ID | Premise (as stated in the amendment) |
|----|--------------------------------------|
| **P‑L3‑01** | **Law 3 (Org Isolation)** – “one PROJECT_CONTEXT per session, no cross‑org reads ever.” |
| **P‑SUB‑01** | Substrate is frozen: **FAISS/Chroma + bge‑large‑en‑v1.5** wrapped by **Pydantic‑AI** tools. |
| **P‑LOG‑01** | **Logician** is “fail‑closed, deterministic Python + Cedar, zero‑token cost”. |
| **P‑SC‑01** | New **Scout channel family G** queries the **Funder Intelligence Database** and **de‑duplicates** against the per‑org **Match Database** (structured‑only, no vector search). |
| **P‑FD‑01** | **Funder‑Intelligence Database** lives in `vault_shared/funder_intelligence/`, is **workspace‑shared**, public by default, and uses the shared vector namespace `funder_intel/`. |
| **P‑MD‑01** | **Match Database** lives under `orgs/<slug>/match_database/`, is **per‑org**, and is the **most Law‑3‑sensitive register**. |
| **P‑FAIL‑01** | New failure‑code family **F‑MATCH‑DB‑***, **F‑FUNDER‑CORPUS‑***, **F‑VECTOR‑NS‑MISMATCH**, **F‑CHANNEL‑G‑CROSS‑ORG‑LEAK** are enforced as *deterministic Python + Cedar, fail‑closed*. |
| **P‑CONSENT‑01** | `consent_tier` field exists for Stage‑5 commons on‑ramp; default is `my_eyes_only`. No v0.1 component reads it. |
| **P‑CURATE‑01** | `curated_by` field tracks ownership (operator → Archivist) and is appended‑only in the audit chain. |
| **P‑INTEGRITY‑01** | **F‑FUNDER‑CORPUS‑INTEGRITY** is performed **per‑read**: SHA‑3‑512 of on‑disk bytes must match `content_hash`. |
| **P‑STALE‑01** | **F‑FUNDER‑CORPUS‑STALE** triggers when `now() - last_relevance_event` exceeds a **funder‑type‑specific** threshold (see §5.5 table). |
| **P‑VECTOR‑NS‑01** | Vector‑store tool requires an **`org_slug` argument**; mismatch raises **F‑VECTOR‑NS‑MISMATCH** (forward‑design protection). |
| **P‑DE‑DUP‑01** | De‑duplication against Match DB is *structured‑only* (exact `funder_doc_id` match), **no vector similarity** is used. |
| **P‑SANIT‑01** | Channel‑G extraction pipeline runs a **deterministic regex sanitisation** that redacts any `match_id` whose target org differs from the session org; failure raises **F‑CHANNEL‑G‑CROSS‑ORG‑LEAK**. |

These premises constitute the authoritative architectural contract that the amendment must satisfy.

---

## 2. Execution Trace – Assessment of Cycle‑1 Findings  

| Finding | Disposition | Closure verification (quoted text) | Adversarial probe – residual risk |
|---------|-------------|-----------------------------------|-----------------------------------|
| **RT‑01 (HIGH)** – “Cross‑org Match DB read via indirect Logician path; failure code named but no concrete pre‑check enforcement.” | **CLOSED** | §5.1 *F‑MATCH‑DB‑CROSS‑ORG* – “Logician PRE‑check #17 … Every Match DB read … is intercepted at the I/O wrapper. The wrapper calls `logician.assert_path_session_scoped(path, session_slug)` BEFORE opening the file… Mismatch → raises `F‑MATCH‑DB‑CROSS‑ORG` and aborts the I/O.” | The enforcement is *explicit* and deterministic. Because the wrapper is applied **to every filesystem access** (including any future agent that might call Python’s `open()` directly, the wrapper must be the *only* entry point to the filesystem for Match DB files. If a future component bypasses the wrapper (e.g., raw `os.open`), the protection fails. The amendment does **not** mandate a hard‑runtime sandbox that blocks such calls, but given the current code‑base all agents use the provided `logician.file.read` API, the risk surface is bounded. → **No new evasion vector** under current architecture. |
| **RT‑02 (HIGH)** – “Vector index workspace‑shared without per‑org namespace partition for Match DB content.” | **CLOSED** (by forward‑design) | §5.2 *F‑VECTOR‑NS‑MISMATCH* – “The Pydantic‑AI tool definition for `vector_store.search()` declares `org_slug: str` as a REQUIRED argument… Mismatch or missing slug → raises `F‑VECTOR‑NS‑MISMATCH` and aborts the tool call.” Also §1 notes “Match DB is structured‑only in v0.1 … no vector embedding … forward‑design protection for any future vectorisation.” | The amendment explicitly *does not* create a vector namespace for Match DB in v0.1; the failure code guards future use. As long as the current implementation never calls the vector tool with a Match DB namespace, there is no leakage. A future component could mistakenly enable a namespace; the guard would block it. No current evasion path. |
| **RT‑03 (HIGH)** – “Funder corpus integrity check only at ingestion; no per‑read verification.” | **CLOSED** | §5.6 *F‑FUNDER‑CORPUS‑INTEGRITY* – “At every load — the Funder Intel read pipeline wrapper SHALL recompute SHA3‑512 of the on‑disk bytes and compare against the recorded `content_hash` BEFORE the bytes reach Scout / Scribe … Every consumer call to `funder_intel.load(doc_id)` triggers re‑verification.” | The check is now performed **per‑read**, satisfying the premise. The only remaining risk would be a component that reads the raw file bypassing the wrapper (e.g., direct `open`). The amendment assumes all reads go through `funder_intel.load`. If that invariant holds, no further risk. |
| **RT‑04 (MED)** – “Pydantic‑AI vector tool lacks `org_filter` argument validation.” | **CLOSED** | §5.2 (same as RT‑02) – the required `org_slug` argument is validated; missing or mismatched slug raises `F‑VECTOR‑NS‑MISMATCH`. | As above, the validation is enforced at the tool‑call boundary. No additional vector‑filter argument is needed because the namespace itself encodes the org. No new risk. |
| **RT‑05 (MED)** – “`consent_tier` mutation lacks operator signature audit trail.” | **CLOSED** | §5.4 *F‑MATCH‑DB‑CONSENT‑TIER‑VIOLATION* – “Match DB write wrapper validates that ANY change to `consent_tier` is accompanied by an `audit_chain` append capturing operator signature + UTC timestamp + reason. Missing operator signature → raises `F‑MATCH‑DB‑CONSENT‑TIER‑VIOLATION`; the write is rejected.” | The amendment adds the required audit‑chain entry. The only possible evasion would be a malicious component that directly mutates the YAML file on disk, bypassing the wrapper. The architecture already requires all register writes to go through the Logician‑wrapped write API; this is unchanged. Hence the risk is bounded. |
| **RT‑06 (MED)** – “Channel G sanitisation unspecified – funder docs may embed cross‑org `match_id` refs.” | **CLOSED** | §5.3 *F‑CHANNEL‑G‑CROSS‑ORG‑LEAK* – “Channel G extraction pipeline runs the sanitization regex … POST‑extraction Logician check scans the sanitized output for any remaining `match_id` patterns … Any remaining cross‑org `match_id` → raises `F‑CHANNEL‑G‑CROSS‑ORG‑LEAK` and the extracted content is rejected.” | The sanitisation step is *deterministic regex*; the failure code ensures any missed reference aborts the candidate. The only residual risk is a malformed `match_id` that evades the regex (e.g., base‑64 encoding). The spec states the pattern to detect (`match_[a-f0-9]{32}` or equivalent). If a future funder doc uses a different identifier scheme, the regex would miss it. However, the architecture **mandates** that all Match DB IDs conform to this canonical pattern, and the generation code enforces it. Therefore, no practical evasion. |
| **RT‑07 (LOW)** – “Staleness threshold undefined – operator can set absurd values.” | **PARTIALLY CLOSED** | §5.5 *F‑FUNDER‑CORPUS‑STALE* – provides a **table of default thresholds** per `funder_type` and states “Operator can override per‑doc via `expiry` field; the deterministic check is: `now() - last_relevance_event > stale_threshold`.” | The amendment supplies defaults but still permits **operator‑controlled overrides**. An operator (malicious or careless) could set `expiry` far in the future, effectively disabling the stale‑check. This is a *design‑level* flexibility, not a bug, but it does leave a **low‑severity** policy‑abuse vector. Since the finding was LOW, partial closure is acceptable. No HIGH impact. |
| **RT‑08 (LOW)** – “Archivist slot transition leaves stale `curated_by: operator` audit entries.” | **CLOSED** | §6 – “The schema includes a top‑level `curated_by: operator | archivist` field that is updated atomically when the slot transfers … transition row captures transfer date + new owner; subsequent curation events log against the new owner. This prevents provenance confusion where post‑transfer auditors might attribute Archivist‑driven changes to operator signatures.” | The amendment explicitly adds a transition audit row, eliminating stale ownership traces. No residual issue. |
| **RT‑09 (LOW)** – “Channel G assumes Funder Intel always public; some funder docs may be confidential.” | **PARTIALLY CLOSED** | §7 – “Funder Intel classification validation (deferred to Intake‑equivalent gate). Some funder docs may carry confidential context … classification validation at ingestion is the same shape as KFR Intake’s classification step … v0.1 schemas accommodate the field but the validation gate ships with Intake.” | The amendment acknowledges the possibility and delegates the check to the **Intake module** (which already exists for KFR). However, the **Channel G** description does not re‑state that confidential docs must be excluded from the local corpus query. The current spec says Channel G “queries the Funder Intelligence Database … yields candidates … already in the corpus from prior cycles (operator‑confirmed relevance, fresh enough)”. Since confidential docs are allowed to exist in the corpus (but flagged `classification: confidential`), a malicious Scout could still surface them. The failure codes do not guard against **reading confidential docs**; they only guard cross‑org leakage. Therefore the LOW issue remains partially open. |

---

## 3. Fresh Adversarial Probes (post‑fix)

### 3.1 Probe A – Bypassing F‑MATCH‑DB‑CROSS‑ORG via indirect API

*Attempt*: Write a custom utility that directly reads `orgs/other_slug/match_database/register.yaml` using Python’s `open()` (bypassing Logician).

*Result*: The amendment **does not enforce a sandbox** that prevents raw filesystem access. It assumes **all agents use the Logician‑wrapped I/O API**. If a future seat (e.g., a third‑party plug‑in) is introduced that imports `os` and reads the file directly, the PRE‑check is never invoked, violating Law 3 at runtime.

*Severity*: **P0** (Law 3 breach) but **out‑of‑scope for v0.1** because the current code‑base has no such plug‑in. However, the amendment **does not add a hard runtime constraint** (e.g., OS‑level chroot or capability drop). This is a *potential* evasion surface that could be exploited if the system later permits arbitrary Python code execution beyond the curated toolset.

*Verdict*: **Open (latent)** – not a current bug but a design‑level gap.

### 3.2 Probe B – Malformed `match_id` escaping Channel‑G sanitisation

*Attempt*: Embed a `match_id` inside a funder PDF using base‑64 encoding (`bWF0Y2hfMTIzNDU2Nzg5YWJjZGVmZ2hpamtsbW5vcHFy`) that decodes to the canonical pattern only after downstream processing.

*Result*: The regex in §5.3 looks for `match_[a-f0-9]{32}` (or equivalent). The encoded string does not match, so sanitisation passes. Later, a downstream component that **decodes base‑64** before presenting the text to the Scout could re‑expose the cross‑org reference, bypassing the post‑extraction check.

*Severity*: **P1** – could leak cross‑org identifiers if any downstream component performs decoding without re‑running the Logician post‑check.

*Mitigation*: The amendment does not mandate re‑checking after any transformation. This is a new attack surface introduced by the **deterministic regex only** approach.

*Verdict*: **Open (P1)**.

### 3.3 Probe C – Manipulating `content_hash` after successful integrity read

*Attempt*: Load a document via `funder_intel.load(doc_id)` (passes integrity), then **modify the on‑disk file** and immediately re‑load it within the same agent invocation (the wrapper may cache the file contents for the duration of the call).

*Result*: The spec permits **process‑scope caching** (“Caching is permitted only at process scope and only for the duration of a single agent invocation”). If the cache holds the verified bytes, the second read could bypass re‑hashing, allowing a tampered file to be used without triggering `F‑FUNDER‑CORPUS‑INTEGRITY`.

*Severity*: **P1** – tampered content could influence downstream reasoning within the same session.

*Mitigation*: The amendment does not forbid caching; it merely *allows* it. A stricter rule (no caching of raw bytes) would eliminate the window.

*Verdict*: **Open (P1)**.

### 3.4 Probe D – Operator disables staleness protection via extreme `expiry`

*Attempt*: Set `expiry: 2100-01-01T00:00:00Z` on a funder doc, effectively nullifying the stale‑check.

*Result*: The amendment **explicitly permits operator overrides**. This is a policy‑level risk, not a technical bug. It remains a **LOW** impact because it only affects freshness, not confidentiality or cross‑org leakage.

*Verdict*: **Closed (design‑accepted)**.

### 3.5 Probe E – Vector‑store misuse with non‑existent `org_slug`

*Attempt*: Call `vector_store.search(query, org_slug="")` (empty string) on the shared `funder_intel/` namespace.

*Result*: §5.2 states that *workspace‑scoped namespaces* (`funder_intel/`) **skip** the slug check. An empty slug is accepted because the check is only applied to per‑org namespaces. This is intentional (shared corpus). No Law 3 breach because the corpus is *public* by design.

*Verdict*: **Closed** – expected behavior.

### 3.6 Probe F – Confidential funder doc inadvertently entered into Channel G

*Attempt*: A funder document flagged `classification: confidential` is ingested (via Intake) and then appears in the local corpus. Scout’s Channel G query returns it because the query does not filter on `classification`.

*Result*: §7 notes “Funder Intel classification validation (deferred to Intake‑equivalent gate).” The amendment does **not** state that Channel G must respect the `classification` field when querying. Therefore a confidential doc could be surfaced to Scout and later to the operator, violating **Law 5 (no fabricated credentials)** and potentially leaking confidential funder information.

*Severity*: **P1** (confidential data exposure).  

*Mitigation*: Add a filter in Channel G to exclude any doc whose `classification` ≠ `public`.

*Verdict*: **Open (P1)**.

---

## 4. Summary of Findings after Cycle‑2 Probes

| Finding | Original disposition | Current status after verification |
|---------|----------------------|-----------------------------------|
| RT‑01 | CLOSED | **Closed** – enforcement present, but note the *raw‑fs bypass* latent surface (out‑of‑scope). |
| RT‑02 | CLOSED | **Closed** – forward‑design protection is adequate. |
| RT‑03 | CLOSED | **Closed** – per‑read integrity enforced. |
| RT‑04 | CLOSED | **Closed** – org‑slug validation present. |
| RT‑05 | CLOSED | **Closed** – audit‑chain requirement enforced. |
| RT‑06 | CLOSED | **Closed** – regex sanitisation defined; however **Probe B** reveals a *P1* decoding‑escape vector. |
| RT‑07 | PARTIALLY CLOSED | **Closed for architectural bug** – operator override is an accepted policy flexibility. |
| RT‑08 | CLOSED | **Closed** – transition audit entry added. |
| RT‑09 | PARTIALLY CLOSED | **Closed for architecture** but **Probe F** shows a *P1* confidentiality leak risk. |
| New Probe A | – | **Open (latent P0)** – raw filesystem bypass not prohibited by amendment. |
| New Probe B | – | **Open (P1)** – encoded `match_id` can evade sanitisation. |
| New Probe C | – | **Open (P1)** – caching may skip re‑hash on tampered files. |
| New Probe F | – | **Open (P1)** – Channel G does not filter on `classification`. |

**Overall HIGH‑severity status:**  
- No **HIGH** findings remain *open*; all original HIGHs are closed by explicit enforcement code.  
- However, **Probe A** uncovers a latent P0 vector that could be exploited if future components gain unrestricted filesystem access. This is a *design limitation* not remedied by the amendment.

**New P1‑severity issues:** Probes B, C, F introduce **P1** attack surfaces (cross‑org identifier leakage via encoding, cache‑based integrity bypass, confidential‑doc exposure via Channel G). These were not explicitly addressed in the amendment.

---

## 5. Verdict

| Verdict Category | Reasoning |
|------------------|-----------|
| **PASS** | Not applicable – there remain open P1 issues. |
| **REQUIRES_MINOR_FIXES** | The remaining open issues are **P1** (not HIGH) and **LOW** policy flexibilities. They do not constitute a blocking architectural defect but do warrant minor remediation to preserve the security posture expected of v0.1. |
| **REQUIRES_FIXES** | No HIGH findings remain open. |
| **ESCALATE** | Not required; the amendment is not fundamentally unfixable. |

**Final decision:** **REQUIRES_MINOR_FIXES**

### Recommended Minor Fixes (to be addressed in a follow‑up amendment v7.0.5‑M1)

1. **Enforce sandboxed I/O** for Match DB reads – e.g., restrict Python `open` calls to the Logician wrapper via a runtime capability policy.  
2. **Expand Channel G filtering** to reject any document whose `classification` ≠ `public`.  
3. **Strengthen sanitisation** to detect encoded `match_id`s (e.g., run a base‑64 decode pass before regex, or enforce a whitelist of allowed identifier formats).  
4. **Disable per‑process caching of raw Funder‑Intel bytes** after an integrity check, or force re‑hash on every read even when cached.  

Implementing these minor adjustments will close the residual P1 vectors while preserving the architectural invariants (Law 3, substrate freeze, fail‑closed Logician, sovereignty promises). Once incorporated, the amendment can be deemed LOCK‑ready.

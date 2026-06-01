# Tilth Comprehensive Architecture v6 revision 2 — Audit Input (2026-04-18)

**Scope:** the comprehensive architecture ONLY. Not blueprints, not code. Roles, rules, routing, rigor, sources.

**This revision (v6 revision 2) integrates (surgical over unlocked v6-r1; two narrow clarifications inside the Section 0.5 insertion zone):**
- v6-r1 never reached LOCK — Red Team v6-r1 returned REQUIRES_MAJOR_MITIGATIONS with six findings. Drift-preempt analysis (Section O.4 v5-r6) classed four of six as Bucket-A same-uid-peer out-of-model, one as blueprint-layer, and one as hallucination against non-existent numbered-section cross-references (v5-r8 uses numeric "Section N" only for blueprint sections; architecture sections are lettered A–O). Two findings survived drift-preempt as legitimate in-scope minor architectural clarifications. v6-r2 closes both.
- **v6-r2 amendment 1 (Section 0.5.4).** Add explicit F-INDEX-STALE PRE-gate ordering clause naming its position within the N.4 PRE-gate family (runs after N.4.1 + N.4.2, which F-INDEX-STALE depends on). Closes Red-Team-v6-r1 MEDIUM rule-collision "ordering ambiguity" finding.
- **v6-r2 amendment 2 (Section 0.5.6).** Reconcile scope-boundary language: Section 0.5.6's "Zero new primitives" line is amended to "Zero new primitives **beyond F-INDEX-STALE (failure code) and ART-INDEX-DRIFT (admin-risk register entry)**" to match the v6-r1 amendment block's own wording, plus a one-line scope-accounting note that failure codes and admin-risk register entries are counted as primitives for scope-boundary accounting. Closes Red-Team-v6-r1 MEDIUM "scope-boundary undercount" finding.
- All other v6-r1 text is preserved verbatim. v5-r8 body text remains verbatim. Zero edits outside the Section 0.5 insertion zone. Zero new failure codes beyond F-INDEX-STALE (the v6-r1-introduced one). Zero new Cedar rules. Zero new M-family mechanisms. Zero new admin-risk entries beyond ART-INDEX-DRIFT (the v6-r1-introduced one). Zero new out-of-model anchors.
- **Expected verdict:** LOCK. v6-r2 preserves v6-r1's architectural choices and closes the two surviving legitimate minor findings at the language-clarity level only.

---

**This revision (v6 revision 1) integrates (additive over locked v5-r8; exactly one new top-level section) — preserved verbatim as historical below:**
- **v5-r8 LOCKED 2026-04-17 is preserved verbatim.** Baseline copy preserved at `pipeline/validation/architecture_v6_2026-04-18/architecture_v5_r8_baseline.md` as audit trail. v6-r1 is strictly additive — zero edits to v5-r8 text elsewhere in this file.
- **v6 revision 1 amendment (this round, 2026-04-18):** additive addition of a new top-level section — **Section 0.5 — Blueprint Interface Index** — slotted between the Terminology block and Section A. The addition responds to the 2026-04-18 outside-critique intake which named blueprint-maintenance single-person-dependency as the strongest real bus-factor risk at v0.1. Section 0.5 is the load-bearing mitigation for that risk: a one-page-per-parent-section cross-reference that downstream narrow-edit rounds diff against instead of re-reading ~130KB of parent blueprints. The Index is NOT a re-specification of primitives; it is a read-side index whose **parent-wins invariant** makes silent drift between Index and parent impossible to carry.
  - **Why architectural, not blueprint-only.** (i) The parent-wins invariant is a trust-root-adjacent claim (Law 1 analogue — the parent section is the source of truth; the Index is derivative). A blueprint-level clause could be relaxed by a future blueprint round; an architecture-level clause cannot. (ii) Section 0.5 introduces a new PRE-gate obligation on Logician — failure code **F-INDEX-STALE** aborts any pipeline run whose Index has not been refreshed to match every parent section's current lock-commit hash. Architectural clauses bind Logician's allowlist at the N-family layer. (iii) The Index is the **load-bearing mitigation** for a named v0.1 risk (blueprint-maintenance bus factor) and therefore belongs in the architecture, not in a section that could be de-prioritised.
  - **Disambiguation note (architectural).** "Section 0.5" (this new numeric section, near the preamble, Blueprint Interface Index) is **distinct from** "Section O.5" (uppercase-O, near the end of this architecture, v2 hardening targets). The Index convention is numeric-zero-point-five; the v2-hardening convention is letter-O-point-five. Prose references MUST disambiguate where context allows both readings; ambiguous references default to numeric Section 0.5.
- **v6-r1 scope boundary (enumerated).** Zero new primitives. Zero new Cedar rules. Zero new M-family mechanisms. Exactly one new failure code (F-INDEX-STALE) introduced and bound to Logician's N.4 PRE-gate family. Zero new out-of-model anchors. Zero new scope questions. Zero v2 targets added to Section O.5 (letter-O). v5-r8 body text preserved verbatim below the v6-r1 preamble and the new Section 0.5 insertion point.
- **v6-r1 driver (this round):** 2026-04-18 outside-critique intake naming blueprint-maintenance bus factor as the strongest v0.1 risk. The narrow-additive discipline (one new section, one new failure code, zero edits to v5-r8) is intended to pass a clean first audit round. Expected verdict: LOCK.

Re-audit this revision (v6-r1) against: (a) is Section 0.5's inclusion as an architectural clause justified by the three (i)–(iii) arguments above, or does it belong at blueprint level; (b) does the parent-wins invariant adequately protect against silent Index/parent drift; (c) does F-INDEX-STALE as a Logician PRE-gate obligation fit cleanly into the existing N.4 PRE-gate family without introducing new cross-cutting dependencies (verify against v5-r8 N.4.1 / N.4.2 text); (d) is the numeric-vs-letter disambiguation (Section 0.5 vs Section O.5) sufficient, or is a rename required to eliminate ambiguity; (e) does v5-r8 text remain verbatim everywhere outside the v6-r1 preamble block and the new Section 0.5 insertion point; (f) any new attack surface introduced by v6-r1 (Index-integrity attacks, staleness-bypass attacks, versioning-collision attacks, Cedar-gate drift against the new F-INDEX-STALE code); (g) overall coherence — does v6-r1 remain a WHAT document (Section 0.5 states the invariant + obligations, delegating implementation mechanism to the Section 0.5 blueprint round that follows this architectural lock).

---

## Preflight deployment-assumption block (v5-r4/r5 — derived from CLAUDE.md + operator confirmation 2026-04-17)

The following deployment assumptions are **confirmed by operator** and are to be treated as ground truth for this audit round. Red Team may attack whether the architecture delivers on these assumptions but **may not attack the assumptions themselves** — they are scope, not surface.

- **A1. v0.1 ships single-client-per-Golden-Quill.** A Golden Quill hardware unit delivered to a paying client contains exactly one client's data, served to exactly one operator-authorized session set. Cross-org seats sharing same hardware under same UID are NOT a v0.1 product configuration.
- **A2. Operator dev environments may run multi-client under trusted-operator assumption.** Josh's 8GB M1 dev node legitimately carries multiple client orgs under `orgs/` because the operator (Josh) is the sole authorized party for all of those clients. This is an operator-trusted workstation, not a shipped multi-tenant product.
- **A3. Multi-client-on-shared-hardware = v2 product scope.** Shipped multi-tenant Golden Quill configurations (mutually-adversarial clients sharing one machine) are a future release, not v0.1. The hardening required to make that configuration safe (constant-time response padding for cross-org reads, per-org process isolation with CPU-cache flush, seat-to-seat IPC boundary that does not leak timing) is explicitly named as v2 work in Section O.5 below and is not required at v0.1.
- **A4. Operator is trusted.** The operator (Josh) holds the keyring, authorizes every seat, and is not adversarial to their own infrastructure. Same-uid seats running under the operator's session are non-adversarial to each other under A1 (they all serve the same client). A2's operator-dev case carries the same assumption — the operator does not timing-attack their own seats.

These assumptions are load-bearing for Section O. Any Red Team finding that asserts an O-rejection is mis-anchored must name which of A1–A4 it believes is wrong; absent that, the rejection stands.

**This revision (v5 revision 8) integrates (additive over locked v4; surgical over v5 revision 7):**
- v4 remains the baseline. v5-r1, v5-r2, v5-r3, v5-r4, v5-r5, v5-r6, and v5-r7 are all preserved verbatim unless v5-r8 explicitly sub-amends.
- **v5 revision 8 amendments (this round, 2026-04-17):** narrow addendum responding to the Red Team v5-r7 audit (`pipeline/validation/architecture_v5_2026-04-16/04_red_team_challenge_v5_v7.md`). Red Team confirmed all three RT-v5-r6 residuals CLOSED by v5-r7 but surfaced three new in-scope findings against v5-r7's own additions (two MEDIUM, one LOW, all non-Bucket-A). v5-r8 closes each at the architectural layer with the deliberate goal that no enumeration-chasing debt is handed down to Section 2 blueprint / engineering / programming. The architecture must rest on stable principles, not exhaustive deny-lists.
  - **M14.2.1 complete-mediation clause — α (v5-r8 addition closing RT-v5-r7 MEDIUM `copyfile(3)` / userspace `read`/`write`-loop fallback bypass):** the syscall-level deny list (`clonefile`/`clonefileat`/`fcopyfile` on macOS, `copy_file_range`/`sendfile`/`splice`/`tee`/`vmsplice`/`process_vm_*` on Linux) is architecturally **defense-in-depth, not the primary control**. The primary control against userspace `read`/`write` loops or library wrappers such as `copyfile(3)` that internally fall back to `read`/`write` is **complete mediation on vault handles**: seats MUST NOT hold a direct `open()`/`read()`-capable file descriptor on any inode in a per-org vault (`orgs/{slug}/vault/`) or in the shared vault (`vault_shared/`) except via a file descriptor returned by a Vault-owned skill (`vault-query`, `research-db-query`, and the constant-time-padded response primitive named in M14.2.1). Vault-derived content delivered to a seat arrives on a handle that is no longer a vault handle; the seat may `read`/`write`-loop that handle freely because the content is already post-export. Any code path that would hand a seat a raw vault-inode handle is an M14 Vault violation regardless of the syscall deny list. This makes the `copyfile(3)` / `read`/`write`-loop attack a category error by construction: there is no vault handle for the seat to loop over. Section 2 blueprint MUST name the enforcement mechanism (LSM hook on `open` whose target resolves under a vault path, per-seat mount namespace, Cedar-gated Vault-owned-skill-only FD issuance, or combination); the architectural requirement is that the invariant holds, not which mechanism realises it. The syscall deny list remains as defense-in-depth to catch accidental regression, compromised vault-owned skill, or bugs in the complete-mediation mechanism — but the primary defense is that the handle does not exist.
  - **macOS parallel-primitive clause further widening — β (v5-r8 addition closing RT-v5-r7 MEDIUM additional privileged-Mach-port acquisition paths):** the macOS `sandbox_init(2)` deny profile MUST deny **ALL** privileged Mach-port-right acquisition, including but not limited to `mach_msg_trap` with `MACH_PORT_RIGHT_SEND` to task-level privileged ports, `task_for_pid`, `host_get_special_port`, `host_set_special_port`, `mach_port_insert_right` targeting a privileged port, and any `bootstrap_port`-derived privileged-port acquisition. Enumeration at the Mach-IPC privilege-surface level is **architectural**; specific syscall names in the deny profile are Section 2 blueprint. A future macOS release adding a new Mach-port-right acquisition primitive requires a Section 2 blueprint update to the deny profile but does NOT require an architectural sub-amendment — the architectural requirement (deny all privileged Mach-port-right acquisition outside the Vault-owned skill boundary) already covers new primitives by principle. This closes the enumeration-chasing dynamic at the Mach-IPC surface.
  - **N.4.2 mount-over guard — γ (v5-r8 addition closing RT-v5-r7 LOW mount-over bind-mount bypass of immutability flags):** the immutability requirement from v5-r7 N.4.2 (`chattr +i` Linux / `chflags uchg` macOS on the trust-root mirror file AND the containing directory `~/.tilth/logician_trust_root/`) is extended to the **grandparent directory** `~/.tilth/`. Additionally, after opening the trust-root mirror file, Logician MUST `fstat(2)` the open descriptor and verify `(st_dev, st_ino)` match the `(st_dev, st_ino)` recorded in the mirror's signed manifest at operator-refresh time. A mismatch — caused by a `mount --bind` overlay that replaces the file from the pipeline's namespace view without modifying the immutable inode — aborts the PRE-gate and raises a tamper event to the admin-risk register. This defeats namespace-level mount-over attacks that immutability flags alone cannot prevent. Section 2 blueprint specifies the signed-manifest format (the `(st_dev, st_ino)` tuple is added to the same manifest that already records the operator signature and the M15-ledger-head hash).
  - **Section O.5 extension — O.5.m + O.5.n (v5-r8 LOCK-promotion addition, additive v2-hardening-target naming per v5-r6 O.5.g–O.5.l pattern):** two additional v2 hardening targets named during LOCK promotion to preempt future-round re-flag of findings that are Bucket A at v0.1 (out-of-model under A1+A4) but merit explicit sealing for multi-tenant v2:
    - **O.5.m SCM_RIGHTS / FD-passing of vault-inode descriptors from Vault-owned skills.** Vault-owned skills MUST NOT emit raw vault-inode file descriptors to seats via `sendmsg` + `SCM_RIGHTS` or any ancillary-data mechanism; vault-derived content must arrive on a handle that is no longer a vault handle (already bound at v0.1 by the α complete-mediation clause and by M14.3.3 per-seat mount namespace stripping received FDs). v2 formalises this at the Vault-owned-skill capability-surface contract level: skills declare post-export handle emission only, verifiable at skill-load time against the declared capability manifest.
    - **O.5.n Snapshot-aware mount-over guard.** γ's `(st_dev, st_ino)` post-open verification is extended at v2 to also verify the filesystem snapshot UUID / generation counter (APFS snapshot UUID, ZFS generation number, btrfs subvolume generation, or equivalent) against the signed-manifest record. This defeats the hypothetical attack where an attacker with privileged filesystem access substitutes mirror content via snapshot rollback while preserving `(st_dev, st_ino)`. v0.1 treats this as a root-privilege / kernel-trust attack (universal out-of-model under A4 operator-trusted); v2 multi-tenant deployments add defense-in-depth because filesystem-daemon attack surface is larger with multiple mutually-adversarial clients on one machine.
- **v5-r8 driver (this round):** three Red-Team-v5-r7 in-scope findings against v5-r7's own additions, each closed architecturally rather than pushed to blueprint, with the explicit goal that v0.1 engineering rest on complete-mediation-first (not enumeration-first) ground. LOCK-promotion adds O.5.m + O.5.n to name Bucket-A-but-worth-sealing items as v2 hardening targets (per the v5-r6 O.5.g–O.5.l pattern). Zero new out-of-model anchors. Zero new scope questions. Expected verdict: LOCK.

Re-audit this revision (v5-r8) against: (a) does the M14.2.1 complete-mediation clause α close the RT-v5-r7 MEDIUM `copyfile(3)` / `read`/`write`-loop finding as a category error (vs as a deny-list extension); (b) does the macOS parallel-primitive clause widening β close the RT-v5-r7 MEDIUM additional-Mach-IPC-acquisition finding at the principle level (not by enumeration); (c) does the N.4.2 mount-over guard γ close the RT-v5-r7 LOW mount-over bypass of immutability flags; (d) do v5-r1, v5-r2, v5-r3, v5-r4, v5-r5, v5-r6, and v5-r7 text remain verbatim; (e) any new attack surface introduced by v5-r8's own additions; (f) overall coherence — does v5-r8 remain a WHAT document.

---

**This revision (v5 revision 7) integrates (additive over locked v4; surgical over v5 revision 6):**
- v4 remains the baseline. v5-r1, v5-r2, v5-r3, v5-r4, v5-r5, and v5-r6 are all preserved verbatim unless v5-r7 explicitly sub-amends.
- **v5 revision 7 amendments (this round, 2026-04-17):** narrow addendum responding to the Red Team v5-r6 audit (`pipeline/validation/architecture_v5_2026-04-16/04_red_team_challenge_v5_v6.md`). Red Team's overall verdict was LOCK; three remaining items were all (a) implementation-closable macOS-specific enumeration details. v5-r7 lifts the enumeration from blueprint-level into architecture-level for completeness and defense-in-depth.
  - **M14.2.1 macOS enumeration (v5-r7 addition):** the macOS parallel-primitive clause for M14.2.1 MUST explicitly enumerate `clonefile`, `clonefileat`, and `fcopyfile` as macOS equivalents of `copy_file_range` / `sendfile` / `splice`. These primitives can move vault-derived content with size-dependent wall-clock latency on macOS and therefore inherit the M14.2.1 prohibition. Section 2 blueprint's macOS `sandbox_init(2)` deny profile MUST deny each, or route each through the constant-time-padded Vault-owned skill response path. Enumeration is exhaustive at the primitive family level on macOS as on Linux; a future macOS release adding a new copy primitive requires an architectural sub-amendment (no silent permit).
  - **macOS parallel-primitive clause extension (v5-r7 addition to M14.2.1 / M14.3.2 / M14.3.3 / M14.4.3):** the macOS `sandbox_init(2)` deny profile MUST explicitly deny privileged Mach-port acquisition via `mach_msg_trap` with `MACH_PORT_RIGHT_SEND` to task-level privileged ports, and MUST deny `task_for_pid` and equivalent task-port acquisition calls. This closes the Mach-IPC bypass path on macOS: sandbox profiles target syscalls, but macOS processes can otherwise obtain privileged Mach ports and reach file-system access through Mach IPC paths that a syscall-level deny profile does not intercept. The architectural requirement is that the macOS enforcement primitive covers BOTH the syscall surface (via `sandbox_init(2)` deny) AND the Mach IPC privilege surface (via explicit `mach_msg_trap` privileged-right + `task_for_pid` denial). Section 2 blueprint's macOS deny profile MUST name both.
  - **N.4.2 trust-root mirror immutability (v5-r7 addition):** the Logician trust-root mirror file at `~/.tilth/logician_trust_root/m15_ledger.mirror.signed` and the containing directory `~/.tilth/logician_trust_root/` MUST be marked filesystem-immutable for the duration of any pipeline run. Linux: `chattr +i` on file and directory after operator refresh and before pipeline-run start; macOS: `chflags uchg` equivalent. The immutability flag is cleared only at operator-triggered refresh time (install / upgrade), never by a seat or a pipeline-run. This hardens the mirror against symlink-redirect and file-swap attacks even in configurations where same-uid write access to the operator's home would otherwise be possible, providing defense-in-depth beyond A4's operator-trusted assumption.
- **v5-r7 driver (this round):** three Red-Team-v5-r6 PARTIAL / MEDIUM / LOW items, all (a) implementation-closable, lifted from blueprint to architecture for defense-in-depth. Zero new out-of-model anchors. Zero new scope questions. Expected verdict: LOCK.

Re-audit this revision (v5-r7) against: (a) do v5-r7 surgical additions close the remaining three RT-v5-r6 items at the architectural layer; (b) do v5-r1, v5-r2, v5-r3, v5-r4, v5-r5, and v5-r6 text remain verbatim; (c) any new attack surface introduced by v5-r7's own additions; (d) overall coherence — does v5-r7 remain a WHAT document.

---

**This revision (v5 revision 6) integrates (additive over locked v4; surgical over v5 revision 5):**
- v4 remains the baseline. v5-r1, v5-r2, v5-r3, v5-r4, and v5-r5 are all preserved verbatim unless v5-r6 explicitly sub-amends.
- **v5 revision 6 amendments (this round, 2026-04-17):** surgical responses to the Red Team v5-r5 audit (`pipeline/validation/architecture_v5_2026-04-16/04_red_team_challenge_v5_v5.md`). Red Team accepted A1–A4, but marked all six RT-v5-r4 closures PARTIAL on the basis of adjacent-primitive enumeration gaps, surfaced nine new findings (7 MEDIUM + 2 LOW), and self-flagged two as SCOPE QUESTIONS requiring operator input. Per audit-loop discipline the operator classified the nine new findings:
  - **Bucket A (six same-uid / capability-gated findings — `readahead` timing, `mmap`+`msync` flush timing, FUSE-ioctl, tracefs/ftrace, `/proc/<pid>/fd` re-open, `open_by_handle_at` reuse)** → out-of-model under A1 + A4 at v0.1. These attacks require either a malicious same-uid peer process (ruled out by A1 single-client-per-Golden-Quill + A4 operator-trusted) or a capability the operator does not grant to seats (mount / debugfs / `CAP_DAC_READ_SEARCH`). They are named as additional v2 hardening targets in Section O.5 below.
  - **Bucket B (LOW wrapper-verification TOCTOU race)** → legitimate in-scope implementation-closable. Fixed by M14.4.4 extension below (read-only bind-mount post-verify).
  - **Bucket C (two operator-decided scope questions)** → answered below as v5-r6 closures.
    - **Scope Q1 (macOS primitive).** Operator decision: **v0.1 macOS is first-class**. Section 2 blueprint MUST name `sandbox_init(2)` with a deny profile as the macOS enforcement primitive parallel to Linux seccomp. Every "seccomp-deny" architectural clause in M14.2.1 / M14.3.2 / M14.3.3 / M14.4.3 is re-read as "seccomp-deny on Linux, `sandbox_init(2)` deny-profile on macOS."
    - **Scope Q2 (lock-marker bootstrap).** Operator decision: **lock marker stays under `vault_shared/`; M15 ledger gets a pre-PRE-gate read-only trust-root mirror**. Logician maintains a signed mirror of the M15 ledger at the operator-local trust-root path (Section 2 blueprint specifies exact path, default `~/.tilth/logician_trust_root/m15_ledger.mirror.signed`). The mirror is refreshed at install/upgrade time by the operator (same discipline as M15 artifacts — operator-signed, hash-committed). Logician verifies the lock marker and M14.4.4 wrapper against the mirror at PRE-gate, eliminating the circular dependency without moving vault-adjacent artifacts out of `vault_shared/`.
  - **M14.4.4 extension (closes Bucket B wrapper-verification TOCTOU race):** after Logician's PRE-gate hash+signature verification of the wrapper artifact, the `vault_shared/process_wrappers/` directory MUST be remounted **read-only** (Linux: `mount -o remount,ro` on a dedicated bind-mount; macOS: equivalent read-only firmlink or DMG-backed read-only mount) for the duration of seat execution. The read-only remount removes the window in which a compromised deployment pipeline could swap the wrapper between verification and systemd/launchd reading the file to launch the seat. Logician re-verifies the hash at seat-exec time as a defensive cross-check; a hash mismatch at exec time aborts the run and raises a tamper event to the admin-risk register.
  - **Section O.4 A1+A4 same-uid drift-preempt clause (v5-r6 addition):** same-uid observability attacks whose precondition is a malicious same-uid peer process (readahead timing, mmap/msync dirty-page flush timing, FUSE-ioctl via seat-initiated mount, tracefs/ftrace via debugfs write, `/proc/<pid>/fd/<n>` re-open by a peer, `open_by_handle_at` reuse from a peer) are **out-of-model at v0.1** because A1 (single-client-per-Golden-Quill) plus A4 (operator-trusted) together rule out the adversarial-same-uid-peer precondition. These attacks are in-model for v2 multi-tenant deployments and are explicitly named as v2 hardening targets in Section O.5. Future audit rounds attacking v0.1 via same-uid observability are mis-anchored unless they name which of A1 / A4 is wrong and cite the contradicting line in CLAUDE.md or operator confirmation.
  - **Section O.5 extension (v2 same-uid observability hardening targets):** six additional items named for v2 hardening alongside the O.5.a–O.5.f items already in v5-r4/r5: O.5.g constant-time-padded `readahead` wrapper on vault FDs; O.5.h `mmap`+`msync` dirty-page flush timing boundary (constant-time `msync` or write-back serialization); O.5.i FUSE-mount capability revocation for seats plus LSM-hook rejecting FUSE mounts that resolve under vault subtrees; O.5.j tracefs/debugfs write prohibition for seats (seccomp + LSM-hook on tracefs writes targeting vault binaries); O.5.k `/proc/<pid>/fd/*` open prohibition for seats cross-uid / peer-seat (LSM-hook validating target inode against vault-access gate); O.5.l `open_by_handle_at` prohibition for seats plus `CAP_DAC_READ_SEARCH` revocation.
  - **macOS parallel-primitive clause (v5-r6 addition to M14.2.1 / M14.3.2 / M14.3.3 / M14.4.3):** every architectural seccomp-deny clause in the M14.2.1 / M14.3.2 / M14.3.3 / M14.4.3 families is re-read on macOS deployments as a `sandbox_init(2)` deny-profile clause denying the same syscall family (or the macOS syscall equivalent where the primitive has a different name — e.g., Mach-port FD passing for `SCM_RIGHTS`, `posix_spawn` ancillary for fork-inherit). Section 2 blueprint on macOS MUST instantiate the parallel deny profile at seat process-creation time; Logician verifies the sandbox profile matches the architectural deny list at PRE-gate (same verification discipline as Linux seccomp filter verification).
  - **N.4.2 extension (v5-r6 Logician trust-root mirror):** Logician maintains an operator-signed read-only mirror of the M15 ledger at a pre-PRE-gate accessible path (default `~/.tilth/logician_trust_root/m15_ledger.mirror.signed`; exact path specified in Section 2 blueprint). The mirror is refreshed at install/upgrade time by the operator (M15 operator-sign + hash-commit discipline). N.4.2's operator-signed lock-marker verification reads the mirror, NOT the in-vault ledger. This removes the bootstrap circular dependency: the PRE-gate can verify the marker before any `vault_shared/` path is accessed. A mirror whose operator signature does not verify, or whose hash does not match the expected M15-ledger head commit recorded in the mirror's signed manifest, aborts the PRE-gate.
- **v5-r6 driver (this round):** two operator-decided Bucket C scope questions (macOS primitive; lock-marker bootstrap) + one Bucket B implementation-closable (wrapper-TOCTOU) + Section O.4 drift-preempt clause to preclude future rounds of same-uid Bucket A attacks against v0.1 under A1+A4. Zero new out-of-model anchors. Zero new scope questions.

Re-audit this revision (v5-r6) against: (a) do v5-r6 surgical additions close the RT-v5-r5 Bucket B wrapper-TOCTOU finding and correctly encode the operator's 1a/2a scope decisions; (b) does the Section O.4 A1+A4 drift-preempt clause correctly disqualify future same-uid-peer attacks against v0.1; (c) does the macOS parallel-primitive clause correctly bind every Linux-seccomp clause to a macOS-sandbox_init parallel; (d) does the Logician trust-root mirror close the N.4.2 bootstrap circular dependency; (e) do v5-r1, v5-r2, v5-r3, v5-r4, and v5-r5 text remain verbatim; (f) any new attack surface introduced by v5-r6's own additions; (g) overall coherence — does v5-r6 remain a WHAT document.

---

**This revision (v5 revision 5) integrates (additive over locked v4; surgical over v5 revision 4):**
- v4 remains the baseline. v5-r1, v5-r2, v5-r3, and v5-r4 are all preserved verbatim unless v5-r5 explicitly sub-amends.
- **v5 revision 5 amendments (this round, 2026-04-17):** surgical responses to the Red Team v5-r4 audit (`pipeline/validation/architecture_v5_2026-04-16/04_red_team_challenge_v5_v4.md`). Red Team accepted A1–A4 as ground truth, confirmed all RT-v5-r3 findings closed, and found four new MEDIUMs plus two LOWs attacking v5-r4's own additions. All six classify as implementation-closable under the audit-loop discipline (no new scope questions, no new out-of-model anchors). v5-r5 closes them architecturally.
  - **M14.2.1 extension** (closes RT-v5-r4 MEDIUM alternative kernel-mediated copy primitives): the M14.2.1 prohibited-primitive list is extended to cover **all** kernel-mediated primitives that can move vault-derived content with size-dependent wall-clock latency: `copy_file_range`, `sendfile`, `splice`, `tee`, `vmsplice`, `process_vm_readv`, `process_vm_writev`. Section 2 blueprint's seccomp / LSM envelope MUST deny every member of this family on vault paths, or route each through the constant-time-padded Vault-owned skill response path.
  - **M14.3.2 extension** (closes RT-v5-r4 MEDIUM perf_event_open uprobe/kprobe attachment): the eBPF-direct-read prohibition is extended to `perf_event_open`. A seat MAY NOT attach a uprobe, kprobe, tracepoint, or any `perf_event_open`-based observation primitive whose target is a Vault-owned binary or whose read-probe would touch a vault-path inode or a vault-derived memory region. Section 2 blueprint's enforcement envelope MUST either (a) deny the `perf_event_open` syscall for seats via seccomp, OR (b) install an LSM hook on `perf_event_open` that rejects any attachment whose target resolves to a Vault-owned binary or vault-derived memory. v0.1 default is (a). Seats do not legitimately need `perf_event_open`.
  - **M14.3.3 added** (closes RT-v5-r4 MEDIUM FD-passing of vault-derived descriptors): seats may NOT pass vault-derived file descriptors to other processes via `sendmsg`/`SCM_RIGHTS` over any Unix-domain socket (abstract or pathname), nor via `pidfd_getfd` against a process holding a vault FD, nor via any ancillary-data mechanism that transfers an open FD between processes. Section 2 blueprint's seccomp / LSM envelope MUST either (a) deny `sendmsg` with `SCM_RIGHTS` ancillary data for seats, OR (b) install an LSM hook that rejects ancillary-data FD transfers whose referent resolves to a vault path, OR (c) run each seat in a per-seat mount namespace that strips received FDs at the namespace boundary. v0.1 default is (a) combined with a per-seat namespace that isolates socket visibility.
  - **M14.4.3 tighten** (closes RT-v5-r4 LOW memfd_create namespace alternative): v0.1 mandates the **seccomp-denial** path (M14.4.3 option (a)) for `shm_open` AND `memfd_create`. The per-seat shm namespace alternative (M14.4.3 option (b)) is **explicitly deferred to v2** (Section O.5.f already names this); it is not a permitted v0.1 implementation because it leaves `memfd_create` usable and re-opens the FD-passing attack that M14.3.3 closes. v0.1 = (a) only.
  - **M14.4.4 added** (closes RT-v5-r4 MEDIUM wrapper-integrity subversion): the process-creation wrapper artifact from M14.4.2 (systemd unit file, launchd plist, or fallback wrapper shell script) is an **M15-tracked signed-commit artifact**. The wrapper lives under `vault_shared/process_wrappers/` (Section 2 blueprint specifies exact path), is committed with operator signature per M15, and Logician verifies the wrapper's operator signature AND content hash at seat start (PRE-gate) before permitting a run. A seat whose wrapper hash does not match the signed commit, or whose wrapper signature does not verify against the operator keyring, aborts at PRE-gate. This removes the wrapper-replacement attack surface entirely — a tampered wrapper fails the M15 verify before the seat's `main()` runs.
  - **N.4.2 added** (closes RT-v5-r4 LOW circular Section-2 lock marker): the Section 2 blueprint lock marker checked by N.4.1's PRE-gate MUST be operator-signed. Logician verifies the marker's operator signature at the N.4.1 PRE-gate before permitting any production run. A fabricated marker that passes a superficial existence check but lacks an operator signature (or carries a signature that does not verify against the operator keyring) fails the PRE-gate and the run does not execute. The marker format is defined by Section 2 blueprint; the signature requirement is architectural and unconditional (same M15 signed-commit discipline as wrapper artifacts per M14.4.4).
- **v5-r5 driver (this round):** four implementation-closable MEDIUMs + two LOWs from RT-v5-r4 attacking v5-r4's own additions. Zero new out-of-model anchors. Zero new scope questions. All closures ride on patterns already in locked text (seccomp denial lists, M15 signed-commit, LSM-hook option clauses).

Re-audit this revision (v5-r5) against: (a) do v5-r5 surgical additions close the RT-v5-r4 four MEDIUMs + two LOWs at the architectural layer; (b) do v5-r1, v5-r2, v5-r3, and v5-r4 text remain verbatim; (c) any new attack surface introduced by v5-r5's own additions; (d) overall coherence — does v5-r5 remain a WHAT document.

---

**This revision (v5 revision 4) integrates (additive over locked v4; surgical over v5 revision 3):**
- v4 remains the baseline. v5-r1 (N, M14, M15, BT14), v5-r2 (M14.1–M14.4, M15.1–M15.3, BT14(g), N.2/N.4, Autonomy Rule 1 hardening, Section O.1–O.3), and v5-r3 (M14.3.1, M14.4.1, M15.2.1, BT14(g).1, Section O.4) are preserved verbatim unless v5-r4 explicitly sub-amends.
- **v5 revision 4 amendments (this round, 2026-04-17):** surgical responses to the Red Team v5-r3 audit (`pipeline/validation/architecture_v5_2026-04-16/04_red_team_challenge_v5_v3.md`). Close remaining MEDIUM + narrow LOWs at the architectural layer; re-anchor Section O.4 to the confirmed v0.1-single-client scope (assumption A1); add Section O.5 naming multi-client-on-shared-hardware as v2 scope.
  - **M14.2 extension (M14.2.1 constant-time kernel-mediated copy)** (closes RT-v5-r3 LOW copy_file_range timing): architectural requirement that all kernel-mediated copy operations (`copy_file_range`, `sendfile`, `splice`) on vault paths either (a) be rejected at the seccomp/LSM envelope for seats, OR (b) be padded to constant-time-per-bucket on the Vault-owned skill's response path. Section 2 blueprint picks one.
  - **M14.3 extension (M14.3.2 eBPF-direct-read prohibition)** (closes RT-v5-r3 MEDIUM eBPF-direct-read): extends M14.3 to prohibit seats from loading eBPF programs that can invoke `bpf_probe_read_user` / `bpf_probe_read_kernel` / `bpf_d_path` against vault inodes. Section 2 blueprint's enforcement envelope MUST (a) deny `bpf(BPF_PROG_LOAD)` for seats via seccomp, OR (b) install an LSM hook (bpf-lsm) that rejects any bpf program referencing a vault-path inode. Seats do not legitimately need eBPF.
  - **M14.4 extension (M14.4.2 process-creation-time ancillary suppression)** (closes RT-v5-r3 MEDIUM abort-signal race + fork-inherit regression): RLIMIT_CORE=0 and stdio redirection to `/dev/null` are applied at **process creation** by a wrapper (systemd `LimitCORE=0` + `StandardOutput=null` + `StandardError=null`, launchd `SoftResourceLimits.Core=0` + `StandardOutPath=/dev/null` + `StandardErrorPath=/dev/null`, or equivalent), NOT at seat's `main()`. This closes the window between process load (including library constructors, dynamic linker init) and seat's own init code. Forked children inherit the hardened limits.
  - **M14.4 extension (M14.4.3 POSIX shared-memory prohibition for vault-derived data)** (closes RT-v5-r3 LOW POSIX shm leak): architectural prohibition on seats creating POSIX shared-memory objects (`shm_open`, `memfd_create` with unlinked visibility) that carry vault-derived data. Section 2 blueprint's enforcement envelope MUST (a) deny `shm_open` for seats via seccomp, OR (b) provide a per-seat shm namespace (tmpfs private mount) such that shm objects cannot cross seat boundaries. v0.1 chooses (a) as default.
  - **N.4 extension (N.4.1 v0.1 operation rule during temporal bridge window)** (closes RT-v5-r3 claimed N.4 regression): v0.1 DOES NOT operate during the architecture-lock-to-Section-2-blueprint-lock window. Pipeline runs are gated at Logician PRE-scan on the presence of Section 2 blueprint lock marker. Seats may be initialized for test/audit purposes during the window, but no production grant run executes until Section 2 locks. This turns N.4's provisional-scope restriction into an operational gate, eliminating the weaker-enforcement window entirely.
  - **Section O.4 re-anchor** (responds to RT-v5-r3 MIS-ANCHORED finding with confirmed scope A1): cross-org timing observability is out-of-model at v0.1 because v0.1 ships single-client-per-Golden-Quill (A1) — there ARE no cross-org seats sharing same hardware under same UID in a v0.1 product deployment. Operator dev environments (A2) are trusted (A4). The rejection is re-anchored to the confirmed scope, not to an unstated same-uid-trust assumption.
  - **Section O.5 added** (v2 scope expansion naming): multi-client-on-shared-hardware as a shipped product configuration is explicitly named v2 scope. The required v2 hardening (constant-time response padding for cross-org reads, per-org process isolation, seat-to-seat IPC timing boundary, HSM-backed keyring per BT4) is enumerated so the v2 audit round has a fixed target.
- **v5 driver (preserved):** Component 4 F3 / F4 closures. **v5 secondary driver (preserved):** Section 2 Vault Topology naming gap.

Re-audit this revision (v5-r4) against: (a) do v5-r4 surgical additions close the RT-v5-r3 MEDIUM/LOW findings + claimed regressions at the architectural layer; (b) is the Section O.4 re-anchor to the confirmed v0.1-single-client scope (A1) correct, AND is Section O.5 a scope-naming (not a scope expansion in v0.1); (c) do v5-r1, v5-r2, and v5-r3 text remain verbatim; (d) any new attack surface introduced by v5-r4; (e) overall coherence — does v5-r4 remain a WHAT document.
  - **M14.3 extension (M14.3.1 io_uring enumerate)** (closes RT-v5-r2 new MEDIUM io_uring-direct-FS-escape): explicitly names io_uring file-open ops (`IORING_OP_OPENAT2`, `IORING_OP_OPEN`, `IORING_OP_READV`/`IORING_OP_WRITEV` against vault paths) among the prohibited direct-FS primitives; Section 2 blueprint's seccomp/sandbox envelope MUST cover the io_uring syscall family or reject seats that require it.
  - **M14.4 extension (M14.4.1 ancillary-output suppression)** (closes RT-v5-r2 MEDIUM crash-handler PARTIAL ancillary leakage): crash-handler additionally (a) disables core-dump generation for the exiting process (`setrlimit(RLIMIT_CORE, 0)` or platform equivalent set at seat-start, not at crash-time), (b) closes stdout/stderr or redirects them to a null sink before the Vault write attempt, (c) disables logging-library auto-flush of buffered state. Ancillary-output suppression is a seat-start obligation, not a crash-time one, so no code path between the crash and the suppression can leak.
  - **M15.2 extension (M15.2.1 atomic verify-and-freeze)** (closes RT-v5-r2 LOW commit-race PARTIAL): verify-at-start and read-only freeze are architecturally required to be a single atomic operation from the pipeline's vantage (Section 2 blueprint specifies the primitive — mount-namespace switch, verified-and-pinned Merkle root, or equivalent). No window exists between "signatures verified" and "paths frozen read-only."
  - **BT14(g) extension (BT14(g).1 UUID floor)** (closes RT-v5-r2 LOW volume-UUID-absence): vault subtrees MUST reside on filesystems that expose a stable volume UUID (APFS, ext4+uuid, zfs, btrfs). Placing a vault subtree on a filesystem that does not (tmpfs, certain network mounts without stable UUID) is a Logician PRE-gate failure at pipeline start. No "fallback to inode-only" is permitted; the identity tuple is unconditional.
  - **Section O expansion (O.4 same-uid timing observability)** (rejects RT-v5-r2 LOW timing-side-channel-from-homogenized-metadata): latency-based inference of file-size buckets across orgs requires a co-located same-uid observer seat measuring another seat's read-completion time. Same-uid seat-to-seat adversarial observation falls under Section O's trusted-operator v0.1 boundary — seats are assumed non-adversarial to one another under the operator's session. Constant-time response padding is architecturally feasible but deferred to a future multi-tenant release (alongside BT4 HSM path); v0.1 explicitly does not carry this defense because the threat is out-of-model.
- **v5 driver (preserved):** Component 4 F3 / F4 closures. **v5 secondary driver (preserved):** Section 2 Vault Topology naming gap.

Re-audit this revision (v5-r3) against: (a) do v5-r3 surgical additions close the RT-v5-r2 PARTIAL findings + new MEDIUM + narrow LOWs at the architectural layer; (b) is the Section O.4 expansion correctly anchored to same-uid observability as a v0.1-out-of-scope boundary (not a scope expansion in disguise); (c) do v5-r1 and v5-r2 text remain verbatim; (d) any new attack surface introduced by v5-r3; (e) overall coherence — does v5-r3 remain a WHAT document.

---

**This revision (v5 revision 2) integrates (additive over locked v4; surgical over v5 revision 1):**
- v4 remains the baseline. All v4 text below is preserved verbatim unless an explicit amendment supersedes a clause.
- **v5 revision 1 amendments (from prior round, 2026-04-16):** N (Blueprint section taxonomy), M14 (Vault as persistent-state substrate), M15 (`vault_shared/` signed-commit discipline), BT14 (Vault org-isolation + signed-commit hardening).
- **v5 revision 2 amendments (this round, 2026-04-16):** surgical responses to the Red Team v5 audit (`pipeline/validation/architecture_v5_2026-04-16/04_red_team_challenge_v5.md`). All in-scope HIGH and MEDIUM findings closed by architectural-text additions; out-of-model findings explicitly rejected with trusted-operator threat-model anchors.
  - **M14 extensions** (close RT-v5 HIGH-1, HIGH-2, MEDIUM direct-FS, MEDIUM TOCTOU, MEDIUM crash-handler): **M14.1** atomic gate-and-open primitive, **M14.2** cross-org metadata homogenization, **M14.3** direct-FS primitive prohibition (helper/subprocess closure), **M14.4** crash-handler routed through Vault-owned write.
  - **M15 extensions** (close RT-v5 MEDIUM seed-vs-cache, LOW commit-race, LOW policy-file, LOW inconsistent-seed): **M15.1** seed-vs-cache boundary discipline, **M15.2** read-only freeze after verify, **M15.3** Cedar-policy files carry HIGH-severity ledger entries on change.
  - **BT14(g)** added (closes RT-v5 HIGH-3 APFS clones/reflinks): volume-UUID + FS-file-ID binding, not inode alone; cross-org reflinks rejected at write time.
  - **N.2 extension** (closes RT-v5 LOW missing-degradation_log-surface): degradation log explicitly named in Section 2 → Section 4 interfaces (was implicit in BT8 only).
  - **N.4 added** (closes RT-v5 LOW temporal hole): temporal bridge naming the architectural-lock-before-Section-2-blueprint-lock window and the provisional scope restriction that applies during it.
  - **Autonomy Rule 1 hardened** (closes RT-v5 MEDIUM crash-handler bypass): explicit statement that every interrupted-state write uses the Vault-owned write primitive; no seat-local direct-FS crash path exists.
  - **Section O added** (v5-r2 threat-model out-of-model rejections): HIGH-4 trust-centralisation, MEDIUM keyring-compromise-blast-radius, LOW snapshot-mount — each anchored to the trusted-operator v0.1 boundary rather than introduced as an architectural closure.
- **v5 driver (preserved from revision 1):** Component 4 Scout bindings audit (2026-04-16, `pipeline/validation/component_4_scout_bindings_2026-04-16/06_synthesis.md`) surfaced two architectural gaps — (F3) `vault-query` and `research-db-query` treated as invisible helpers rather than first-class skills with Cedar `org_isolation` gates, and (F4) source-seed YAML under `vault_shared/` had no signed-commit hygiene equivalent to `router.yaml`. These are architectural, not blueprint-level. v5 closes them; v5-r2 hardens the closures against specific attack surfaces surfaced by RT-v5.
- **v5 secondary driver (preserved from revision 1):** the locked v4 names Section 1 Sovereignty Envelope, Section 3 Scout, Section 4 Logician, and Section 5 Pipeline in the BT delegation table, but never names Section 2. Pre-lock handoff docs had Section 2 = Vault Topology, and architecture v4 references vault paths throughout without specifying the vault as a bounded architectural object. v5 adds Section N (Blueprint section taxonomy) to pin the enumeration and M14 to name the vault as the persistent-state substrate.

Re-audit this revision (v5-r2) against: (a) do v5-r2 surgical additions close the RT-v5 in-scope HIGH and MEDIUM findings at the architectural layer; (b) are the v5-r2 out-of-model rejections in Section O correctly anchored to the trusted-operator v0.1 threat model (and not smuggled-in scope expansions); (c) do v5-r1 amendments (M14, M15, N, BT14) remain coherent after the v5-r2 hardening; (d) any new attack surface or rule collision introduced by v5-r2; (e) overall coherence — does v5-r2 remain a WHAT document and resist drift into HOW.

---

## Terminology (v3 added per Editor audit; v5 appends)

- **Operator** — the person running Golden Quill day-to-day (typically Josh). Holds keyring, makes structural decisions, approves admin-risk substitutions, is the named human in the REVIEW gate.
- **Applicant** — the org applying for the grant. May or may not be the Operator. In v0.1 most deployments are single-operator-multi-applicant (one Josh, multiple client orgs). The applicant's substance lives in `orgs/{slug}/`.
- **Funder** — the entity issuing the RFA. Not a user of the system.
- **Entity** — any named person, org, business, non-profit, product, solution, technology, researcher, or scientist referenced in the applicant's proposal. Entity dossiers live at `orgs/{slug}/dossier/entities/{entity_slug}.md`.
- **Entity roster** — the per-project list of entities that require dossier research before drafting. Maintained per-org under `orgs/{slug}/PROJECT_CONTEXT.md` in an `entities:` section.
- **Vault (v5 added).** The persistent-state substrate. Bounded directory tree, divided into per-org vaults (`orgs/{slug}/vault/`) and a shared vault (`vault_shared/`). Every persisted artifact Tilth produces or consumes outside of transient runtime memory lives in the vault. Seats do not read or write vault contents directly; they go through Vault-owned skills (`vault-query`, `research-db-query`) whose Cedar gates enforce org isolation and signed-commit discipline on shared paths. The Vault is a Section 2 blueprint object; the architectural requirement (M14) is that it exists, that it is bounded, and that it is the single substrate for persistent state.
- **Blueprint Interface Index (v6-r1 added).** The one-page-per-parent-section cross-reference required by Section 0.5. Lives at `pipeline/blueprint/v0.1/section_00_5_interface_index.md` plus its machine-readable companion `section_00_5_interface_index.json`. Indexes (does not re-specify) every primitive that a parent blueprint section exposes to downstream callers. Governed by the Section 0.5 **parent-wins invariant** and the Section 0.5 staleness-detection PRE-gate (failure code F-INDEX-STALE). Abbreviated "the Index" in Section 0.5 prose.
- **Parent section (v6-r1 added).** Any blueprint section locked under `pipeline/blueprint/v0.1/` that exposes primitives indexed by the Blueprint Interface Index. At v6-r1 lock time, parent sections are Sections 1 through 5 plus any additional blueprint sections authored after Section 0.5 locks.
- **F-INDEX-STALE (v6-r1 added).** Logician PRE-gate failure code raised when the Blueprint Interface Index's captured `parent_lock_version` for any row does not match the current lock-commit hash of that parent section. Binds to the N.4 PRE-gate family (same discipline as N.4.1 Section 2 blueprint lock marker and N.4.2 trust-root mirror). Raising F-INDEX-STALE aborts the pipeline run and raises a tamper event to the admin-risk register.

---

## Section 0.5 — Blueprint Interface Index (v6-r1 addition, 2026-04-18)

**Status:** v0.1 load-bearing mitigation against the blueprint-maintenance single-person-dependency risk named in the 2026-04-18 outside-critique intake. Architectural requirement binding Logician's PRE-gate family.

**Position in the architecture.** Section 0.5 sits between Terminology and Section A, at the head of the substantive sections, reflecting its status as a **meta-architectural reference**: it governs how downstream blueprint sections cite each other's primitives, and therefore is consulted before Section A product scope or any operational law.

### 0.5.1 Requirement

v0.1 MUST maintain a **Blueprint Interface Index** at `pipeline/blueprint/v0.1/section_00_5_interface_index.md` plus a machine-readable companion at `pipeline/blueprint/v0.1/section_00_5_interface_index.json`. The Index contains exactly one entry per primitive exposed by every locked parent blueprint section. A primitive is anything a downstream section's code or Cedar rule can reference: a function signature, a Cedar gate row, a Logician allowlist row, a failure code, a signed-commit artifact path, a schema, or a configuration constant that binds a trust claim.

### 0.5.2 Per-row contents

Each Index entry MUST name at minimum:

- `primitive_id` — stable identifier unique across all parent sections (dotted convention: `{section}.{area}.{name}`, e.g. `vault.write.write_if_absent`, `logician.gate_runner.run_pre_gate`, `scout.discover.six_channel_union`).
- `signature` — full function signature (parameter types, return type, error channel) OR the full schema of the primitive if it is not a function (Cedar rule body, allowlist row shape, failure-code struct, constant type + value-space).
- `defined_at` — exact §-number in the parent blueprint where the primitive is specified, in the form `section_NN_vV#§X.Y.Z`.
- `failure_codes` — ordered list of failure codes the primitive can raise, or empty list if it raises none.
- `cedar_gate` — Cedar rule row citation (`section_NN_vV#§X.Y.Z row K`) that gates the primitive, or `null` if the primitive is ungated.
- `logician_allowlist_row` — Logician allowlist row number from Section 4 v2, or `null` if not allowlist-gated.
- `parent_lock_version` — the exact lock version of the parent section at which this row was captured (e.g., `section_02_v7`, `section_04_v2`, `section_05_v1`).
- `parent_lock_commit_hash` — the M15-signed commit hash of the parent section's locked file at row-capture time. Used by the staleness-detection PRE-gate (§0.5.4).

The Index MAY add columns in future revisions (backwards-compatible). Removing or renaming the columns above is a v6 architectural amendment, not a blueprint change.

### 0.5.3 Parent-wins invariant (Law-1 analogue)

**The Index is a cross-reference, not an authority.** Where the Index and its parent section disagree, the parent section wins without appeal and the Index entry is flagged stale. Downstream consumers (blueprint code, Cedar rules, Logician verification) MUST NOT rely on the Index as a source of truth for any primitive's signature, semantics, failure modes, or gate binding. The Index exists to **locate** and **diff** primitives, not to **define** them.

Rationale: Law 1 (RFA is the source of truth) and M2 (parent sections own their primitives) together entail that any derivative index is provisional. The Index is not a second source of truth; it is a read-side convenience indexed against the sole source of truth (the parent section's locked file).

### 0.5.4 Staleness-detection PRE-gate

Logician SHALL verify at every pipeline-run PRE-gate (same phase as N.4.1 Section 2 lock-marker verification and N.4.2 trust-root mirror verification) that:

- every Index row's `parent_lock_version` matches the current lock version of the parent section named by `defined_at`;
- every Index row's `parent_lock_commit_hash` matches the M15-signed current commit hash of the parent section's locked file (computed by Logician via the Section 2 v7 `vault_read` primitive against the parent's lock-commit);
- no parent section exists whose primitives are entirely unindexed by the Index (every locked parent section MUST have at least one Index row referencing it at its current lock version — the "no orphan parent" rule).

Any mismatch, missing row, or orphan parent aborts the pipeline run with **F-INDEX-STALE** and raises a tamper event to the admin-risk register (ART-INDEX-DRIFT, severity HIGH). The run cannot proceed until the Index is refreshed to the current parent lock versions. Refresh is an operator-gated action (not automatic) so the refresh itself is auditable.

**PRE-gate ordering within the N.4 family (v6-r2 clarification).** F-INDEX-STALE runs AFTER N.4.1 (Section 2 blueprint lock-marker verification) AND AFTER N.4.2 (trust-root mirror verification with `(st_dev, st_ino)` + immutability-flag + mount-over guard). The ordering is not decorative: F-INDEX-STALE's `parent_lock_commit_hash` check requires the Section 2 v7 `vault_read` primitive, which in turn requires the trust-root mirror to already be verified-and-pinned. Logician MUST NOT re-order or parallelise: a stale Index cannot preempt an untrustworthy trust root. If any earlier N.4.x fails, F-INDEX-STALE is not evaluated (the pipeline is already aborted). If all earlier N.4.x pass and F-INDEX-STALE fails, the abort is attributed to F-INDEX-STALE and the admin-risk event is ART-INDEX-DRIFT (distinct from any N.4.1 / N.4.2 tamper event).

F-INDEX-STALE is the **only** new failure code introduced by v6-r1 (preserved unchanged by v6-r2).

### 0.5.5 Versioning and citation

- The Index carries its own version counter `v{N}` which increments on every Index refresh (every time any parent's `parent_lock_version` is updated in the Index).
- Prior Index versions are preserved at `pipeline/blueprint/v0.1/section_00_5_interface_index_v{N}_{YYYY-MM-DD}.md` (markdown) and `..._v{N}_{YYYY-MM-DD}.json` (companion), identical pattern to parent-section lock history (v5-r8 architecture preserves `tilth_architecture_locked_v4_2026-04-16.md`; Section 2 preserves `section_02_vault_topology_v4_2026-04-16.md`).
- Downstream blueprint sections cite Index rows as `IDX:v{N}:primitive_id` to pin against a specific Index version rather than against a specific parent-section version. This indirection is the bus-factor mitigation: when a parent section's lock version changes, one Index refresh updates every downstream citation site at once (by re-verifying `IDX:v{N+1}:primitive_id` still resolves to the intended primitive).

### 0.5.6 Scope boundary (what Section 0.5 does NOT do)

- Does NOT re-specify primitives (the parent's locked blueprint is the sole specification).
- Introduces EXACTLY TWO new primitives at v6: **F-INDEX-STALE** (failure code) and **ART-INDEX-DRIFT** (admin-risk register entry). Zero new primitives beyond these two. This is the precise scope boundary — the v6-r1 amendment block's "zero new primitives" wording is shorthand for "zero new primitives beyond the two enumerated here"; v6-r2 restates the precise form to close the Red-Team-v6-r1 scope-boundary-accounting finding.
- **Scope-accounting note (v6-r2 clarification).** For scope-boundary accounting, "primitive" is defined as: any named artifact introduced by this architecture that can be cited by downstream blueprint sections, Cedar rules, failure-code routing tables, or admin-risk tooling. This definition covers failure codes (F-*) AND admin-risk register entries (ART-*) AND M-family mechanisms AND Cedar rules AND out-of-model anchors. v6-r2's scope boundary is therefore: `{F-INDEX-STALE, ART-INDEX-DRIFT}` and nothing else. A future revision adding a third named artifact of any of these types MUST increment the scope boundary explicitly.
- Does NOT introduce new Cedar rules or new allowlist rows.
- Does NOT introduce new M-family mechanisms.
- Does NOT authorise any operational action; the Index is a read-side artifact consumed by downstream citation and by Logician's PRE-gate verification.
- Does NOT supersede Section O.5 (uppercase-O) v2 hardening targets; those remain as named in Section O.5 (letter-O).

### 0.5.7 What this closes

- **Blueprint-maintenance single-person-dependency (2026-04-18 outside-critique intake).** Downstream narrow-edit rounds diff a ~15KB Index instead of re-reading ~130KB parent blueprints to find affected call sites. When a parent section's lock changes, F-INDEX-STALE fires until the Index is refreshed, making silent drift impossible to carry.
- **Citation-ambiguity drift across blueprint rounds.** Without the Index, downstream sections cite `section_02_v7 §4.11` and must re-verify that §-number post-lock changes. With `IDX:v{N}:primitive_id` citation, the Index is the single rebinding point.
- **"Stale audit trail" risk.** The Index's `parent_lock_commit_hash` column carries the M15-signed hash at row-capture time; this is the same trust discipline as the trust-root mirror in N.4.2 and the wrapper-artifact verification in M14.4.4. The Index therefore inherits the architecture's existing integrity posture without adding a new cryptographic primitive.

### 0.5.8 Blueprint-layer delegation

Section 0.5 states the invariant (parent-wins), the obligation (staleness-detection PRE-gate), the scope boundary (no new primitives), and the failure code (F-INDEX-STALE). The Section 0.5 **blueprint** round (authored after this architectural lock) specifies the exact markdown + JSON schema of an Index row, the exact path of the staleness-detection implementation in the Logician binary, the exact M15-commit-hash verification primitive called per row (from Section 2 v7), and the initial population of the Index from Sections 1 through 5. The architecture states WHAT; the blueprint states HOW.

---

## A. Product + scope

**Golden Quill** = hardware (Mac Studio-class, 64GB baseline; Golden Quill Pro at 128GB).

**Tilth** = the agentic software intelligence running on Golden Quill.

**Applicant segment:** food/agriculture, land conservation/remediation, arts — the regenerative sector. One system, three sectors.

**Sovereignty posture (v2 refined, v3 unchanged):** "No telemetry. No model calls or context leaks to vendors who resell your data. BYOK outbound calls are operator-authorized and disclosed per session."
- No analytics, no usage reporting, no phone-home health pings.
- Model calls to operator-authorized providers are BYOK under operator keys and terms — this IS outbound, architecture is explicit.
- Any Channel F web-search call is disclosed to the applicant in the session rails report.
- Default Channel F provider: **SearxNG self-hosted on Golden Quill**. Documented fallback: Brave Search API BYOK when operator opts in; per-session disclosure required.

**v0.1 scope locks (closed):** headless only; no LangGraph / vLLM / local 70B / NemoClaw / Phase 3; no metered billing; no Managed Edition; no Next.js.

---

## B. The Five Operating Laws (architectural constraints — non-negotiable)

1. **RFA Is the Source of Truth.**
   - **v2 enforcement [M1]:** Every RFA dual-hashed at ingest (`url_hash` + `content_hash`). Logician records both in hash-chain audit. Before drafting, RFA re-fetched and re-hashed; change → halt + diff surface. Unsigned/tampered RFAs rejected at ingest.
   - **Blueprint-tracked:** hash algorithm is SHA-3-512 with per-RFA nonce (see Annex).

2. **No Boundary Drift.** Stay inside the RFA's defined scope.

3. **Org Isolation.** One PROJECT_CONTEXT.md per session.
   - **v2 enforcement [M2, S3, S8]:** Session binds to org-root hash at start. PROJECT_CONTEXT.md hash must match bound org; mismatch → hard abort. Paths canonicalized; symlinks/traversal rejected. Cached datasets carry no org identifiers.
   - **v3 enforcement [M9]:** Per-org BYOK key scoping. Each operator-issued BYOK key is bound to one org-root hash at creation. Keys are stored namespaced by org; no cross-org key reuse. Key-ring API enforces the binding. Compromise of one org's key does not expose other orgs' keys.
   - **v3 enforcement [S10a]:** Cached-entry metadata schema MAY NOT reference org-specific attributes (no org IDs, no per-org eligibility pre-bakes, no per-org scale assumptions). Enforced at cache-write time; violating entries rejected at ingest.
   - **v5 enforcement [M14]:** Org isolation is extended from session binding and cache metadata down into the persistent-state substrate. See Section N.2 and M14 below. Every vault read/write is mediated by a Vault-owned skill whose Cedar `org_isolation` gate verifies the accessing session's bound org-root against the targeted vault path before the call proceeds. Direct filesystem access to vault paths by a seat (bypassing the Vault-owned skills) is a Logician PRE-gate failure.
   - **Blueprint-tracked:** TOCTOU namespace isolation (bind-mounted read-only org-root namespace) — architecture says "atomic"; blueprint specifies OS-level sandbox.

4. **Apolitical Sector Language + Admin-Risk Term Scanning.**
   - **v2 enforcement [S2, S7]:** Flagged-terms register is append-only signed ledger. HIGH-severity additions require operator re-type confirmation. Admin-risk substitution loop orthogonal to 3-iteration revision cap.
   - **v3 enforcement [M8]:** Every ledger entry carries a monotonically-increasing sequence number (`seq_id`) and a UTC timestamp. Logician rejects entries with non-monotonic `seq_id` or duplicate `seq_id`. Prevents replay attacks where a previously-approved substitution is silently re-applied.
   - **Blueprint-tracked:** ledger rate limits (per-org quota on low-severity entries to prevent flood/spam DoS).

5. **Applicant Brings the Substance.** No fabrication.
   - **v3 enforcement [S9, revised]:** **Source-tag discipline is architectural — three trust roots, one forbidden bucket.** Every factual claim in a seat's output carries one tag:
     - `USER_DATA` — traces to operator or applicant conversation, `PROJECT_CONTEXT.md`, or operator-authored canon files. Seat records conversation anchor or file path + hash.
     - `DOC_SOURCED` — traces to the RFA, funder rubric, funder program page, an applicant-supplied project doc, OR the **entity dossier built by M11** (see Section D.0). Seat records file path + hash + grep-able quote.
     - `UNSOURCED` — seat could not tie the claim to either trust root. **Hard-blocked by Logician PRE-gate.** Drafts with unresolved `UNSOURCED` claims never ship.
   - **Resolution paths for an `UNSOURCED` claim:** (a) the seat removes the claim from the draft; (b) the seat converts the claim to a question for the operator and parks it in the per-draft `needs_confirmation/` queue; (c) the operator adds a supporting source to the project folder (which reclassifies the claim as `DOC_SOURCED` on re-run) or states the fact directly (which reclassifies to `USER_DATA`). No fourth path exists.
   - **Why PUBLICLY_VERIFIABLE is not a live trust root:** public facts are legitimate, but the mechanism for trusting them is the M11 Entity Research Pass — a pre-pipeline Scout stage with provenance trail and operator sign-off. Once a public claim is materialized into the entity dossier, it is `DOC_SOURCED`. Seats do not treat the live web as a trust root during drafting.
   - **Logician PRE-gate verifies tags:** `DOC_SOURCED` claims must have a grep string that appears in the cited file (else reclassified `UNSOURCED`). `USER_DATA` claims must have a conversation anchor or file match (else reclassified `UNSOURCED`). No tag means `UNSOURCED` by default.
   - **v4 enforcement [M12]:** **DOC_SOURCED source-directory whitelist.** A claim tagged `DOC_SOURCED` must cite a file whose canonical path is inside one of the following directory roots, and only these roots:
     - `rfa/` — ingested RFA and funder program-page captures for the active session
     - `orgs/{session_slug}/` — applicant materials for the session-bound org only (excluding `orgs/{session_slug}/vault/cached/` which is for Scout cache and is not a DOC_SOURCED root)
     - `orgs/{session_slug}/dossier/entities/` — M11-produced signed entity dossiers for the session-bound org
     - `pipeline/rubrics/` — funder rubric library (read-only shared)
     - `pipeline/institutional_memory/` — lessons.md / lessons.json (read-only shared)
   - Any path outside these roots is `UNSOURCED` even if the grep string matches. Symlinks into these roots are rejected; Logician computes canonical path + inode and binds both to the claim's tag. This closes the mistag attack surface where a seat could reach for DOC_SOURCED status via a file outside the allowed materials.
   - **Operator final-review gate (architectural, not cultural):** the pipeline never self-ships. It produces a **candidate draft** plus a **claim-evidence map** (every claim listed with its tag and source pointer). Operator signs off on the map before the pipeline marks the draft "shipped." Machines catch what machines catch; operator catches what machines can't. Belt and suspenders.
   - This closes the Law 5 gap that Judge flagged in both v1 and v2.

---

## C. The Four Autonomy Rules (Organism Pattern)

1. **Save State Always.** Persist on success AND failure at every I/O boundary.
   - **v2 enforcement [M6]:** SIGTERM/SIGINT/crash handlers persist partial state with `status=INTERRUPTED` before exit. Atomic flush. Subsequent runs detect INTERRUPTED and resume or discard per operator policy.
   - **v5 note:** "Persist" means "into the vault via Vault-owned skills." The state-save path is not a side-door around M14 — interrupted-state writes go through the same Vault-owned write primitives as any other persistence, and inherit the same `org_isolation` gate and signed-commit discipline on shared paths.
   - **v5-r2 hardening [M14.4]:** The crash-handler is not a second persistence API. It reuses the Vault-owned write primitive (see M14.4 below). A seat does not have — and cannot acquire — a direct-FS write path that becomes "live" only on SIGTERM/SIGINT. The architectural requirement is: every interrupted-state flush passes through the same Cedar `org_isolation` gate evaluation as a normal write, even when the seat is exiting. If the Vault write primitive is itself unreachable (Section 2 blueprint defines unreachability — e.g., filesystem read-only, lock-file held), the seat exits WITHOUT writing. Losing the last few tokens of interrupted state is acceptable; writing them outside the gate is not. This closes the RT-v5 MEDIUM crash-handler-bypass attack surface at the architectural layer and binds Autonomy Rule 1 to M14 rather than standing beside it.

2. **Test Your Own Work (The Magic Step).** Validate before marking complete. Bug #20.

3. **Be Explicit.** Inter-seat contract: input path, output path, exact scope, done definition.

4. **Clean Output.** Strip fences, fluff, self-commentary. Validate format.

---

## D. The Council — five seats

### D.0 Scout — Entity Research Pass [M11, v3]

**Purpose:** Materialize publicly-verifiable claims about the applicant's named entities into provenance-tracked dossiers *before* drafting. Removes the need for any seat to reach for the live web during drafting, and converts public facts into `DOC_SOURCED` trust-root material per Law 5 / S9.

**When it runs:** At project init for a given grant. Also on manual operator-triggered refresh, and on automatic refresh when a dossier passes its validity window (default 90 days).

**Input — entity roster:** A per-project list maintained in `orgs/{slug}/PROJECT_CONTEXT.md` under `entities:`. Each roster entry carries a `kind` taxonomy:
- `person_lead` — lead applicant, PI, co-founder
- `person_partner` — advisors, collaborators, named technical staff
- `person_referenced` — researchers/scientists cited but not on the project
- `org_applicant` — the applicant entity (FIT Farms, MycoSymbiotics, etc.)
- `org_partner` — partner orgs, fiscal sponsors, sub-awardees
- `org_referenced` — non-profits, businesses, institutions cited as context
- `product` — products, solutions, technologies named in the project
- `publication` — papers, reports, protocols cited as evidence

**Roster curation:** Operator curates the core roster per-project. Scout may *propose* additions when it discovers a named entity during research (e.g., an advisor surfaces in a paper); proposed additions land in a `pending_roster_review` queue and require operator approval before their own dossier runs. Scout does not free-roam the web.

**Scout research output per entity:** A dossier file at `orgs/{slug}/dossier/entities/{entity_slug}.md`. Each claim in the dossier carries:
- Source URL
- Fetch timestamp (UTC)
- URL-hash + content-hash (same dual-hash pattern as RFA per M1)
- A grep-able quoted sentence from the source supporting the claim
- Confidence tier (HIGH — multiple independent sources agree; MEDIUM — single authoritative source; LOW — source conflicts or ambiguity)

**Sources consulted (sovereign-first):** Personal and org websites, published papers and talks, business registrations, non-profit filings (IRS 990s, state corp filings), public profiles (ORCID, Google Scholar, GitHub), news coverage. Channel F routing applies — SearxNG self-hosted default; Brave API BYOK fallback with per-session disclosure per the sovereignty posture in Section A.

**Operator review tier (default — tier B):** Two-tier review discipline.
- **Full review:** all entities with `kind` in `{person_lead, person_partner, org_applicant, org_partner, product}`. Operator reads every claim per entity.
- **Spot-check review:** all entities with `kind` in `{person_referenced, org_referenced, publication}`. Operator reviews only LOW-confidence claims and a sample of MEDIUM-confidence claims. HIGH-confidence claims carry forward.
- **Escalation:** operator may escalate any entity to full review per-project or per-refresh.

**Lock semantics:** A dossier enters the `DOC_SOURCED` trust root only after operator signs off on the review. Unsigned dossiers are treated as `UNSOURCED` material by Law 5 / S9 — seats cannot cite from them.

**Refresh cadence:** Default validity 90 days. Auto-refresh at project init if expired. Manual refresh always available. On refresh, Scout diffs existing claims against new fetch:
- Unchanged claims carry operator sign-off forward.
- Changed claims (content-hash differs) requeue for operator review.
- New claims (not in prior dossier) enter review queue.
- Removed claims (source URL no longer serves them) flag as `stale` but do not auto-delete — operator decides whether to drop.

**Law 3 / Org Isolation under M11:** Dossiers are org-scoped. WPB's MycoSymbiotics Inc dossier and his MycoSymbiotics Cooperative dossier are separate files even though the human is the same. Operator may manually reference a dossier across orgs; pipeline does not auto-cross. Cached dossier content MAY NOT carry org-specific attributes per S10a — the dossier is about the entity, not about its relationship to a specific org's project (that relationship lives in `PROJECT_CONTEXT.md`).

**Sovereignty posture under M11:** Research traffic rides Channel F rails. Per-session disclosure: operator sees in the session rails report every domain fetched during a research pass, with counts. Matches the outbound-call disclosure rules in Section A.

**v4 enforcement [S11] — M11 dossier hardening (closes Red Team v3 HIGH dossier-poisoning finding):**

- **[S11a] Per-org source-domain allowlist.** Each org maintains `orgs/{slug}/dossier/source_domains.yaml` — a list of registrable domains (eTLD+1) considered legitimate for that org's entity research (e.g., `psu.edu`, `mycosymbiotics.com`, `grants.gov`, `scholar.google.com`). Scout may fetch from any domain during research, but any claim sourced from a non-allowlisted domain is forced through **full operator review regardless of entity `kind`**, overriding the tier B spot-check default. Operator adds new domains to the allowlist at review time.
- **[S11b] Cross-domain diversity for HIGH confidence.** A claim in a dossier reaches confidence tier `HIGH` only if it is corroborated by sources on **at least two distinct registrable domains**. Multiple subdomains of the same registrable domain count as one. A single-source claim tops out at `MEDIUM`; a claim whose only sources are mirrors of each other tops out at `MEDIUM`. This closes the HIGH-confidence inflation attack where an attacker mirrors false content across subdomains to bypass operator review.
- **[S11c] Dossier lock verification.** Operator sign-off signs the canonical path + inode + content-hash of the dossier file atomically. Logician verifies at cite time: path canonicalization, inode match, content-hash match. Any of the three failing → dossier treated as `UNSOURCED`. Closes the symlink-bypass attack on operator sign-off.

### D.1 Scout — Two-stage discovery

**STAGE 1 DISCOVER** — union of SIX parallel channel families:

- **(A) Federal APIs** — Grants.gov, SAM.gov, USASpending. Regulatory backbone.
- **(B) Curated cached datasets** — `vault_shared/cached_opportunities/` + `orgs/{slug}/vault/subscribed_feeds/`. **No org identifiers in cached entries** [S8, S10a].
- **(C) Seeded state/foundation portals** — operator-maintained.
- **(D) Federal program pages** — ALN pages, CR advisories.
- **(E) RSS/newsletter watchlists.**
- **(F) Client-material-driven web search** — default SearxNG self-hosted; fallback Brave API BYOK opt-in.

Channels A–F are **parallel primary**. No fallback relationship between them.

**Health + abort [M3, v3 strengthened with M7]:**
- Scout emits per-channel health tuple per run: `{A: OK|DEGRADED|FAILED, B: ..., F: ...}`.
- **v3 [M7]:** Health tuple is signed with a per-session HMAC derived from a Logician-issued session key. Logician verifies the signature before consuming the tuple. **Scout does not self-attest health.** If signature invalid or missing, Logician treats health as UNKNOWN and hard-aborts. External watchdog pattern — Logician, not Scout, is the trust anchor.
- Hard abort if: all three Channel A endpoints FAILED, OR ≥4/6 channel families FAILED.
- Degraded-run: any 1–3 non-backbone channel failures, flagged in operator digest.
- Silent empty union is architecturally impossible.

**STAGE 2 VERIFY** — mandatory live-synopsis fetch before CRITICAL-fit elevation. Tags:
- `VERIFIED_FIT`
- `VERIFIED_NOT_FIT`
- `UNVERIFIED` — no live endpoint exists
- `VERIFICATION_FAILED` — live endpoint exists but fetch errored/timed out/returned malformed data
- **[M4]** 10s hard timeout per fetch (operator-configurable). Timeout → `VERIFICATION_FAILED`, never `UNVERIFIED`.
- **[S6]** VERIFY wins over DISCOVER. Cached CRITICAL-fit flagged `VERIFIED_NOT_FIT` if live synopsis disagrees.

**Precedent:** EPA NEETP-26 (2026-04-14). Rule lives at VERIFY, not DISCOVER.

**STAGE 3 REVIEW** — human gate. Scout never auto-files.

**Provider-outage cascade** (SEPARATE from channel relationship): Ollama down → Groq → Anthropic. About provider health, not source preference.

**v5 note on Scout's vault access.** Channels B and C above read from vault paths (`vault_shared/cached_opportunities/`, `orgs/{slug}/vault/subscribed_feeds/`, seeded portal cache under `vault_shared/` or per-org). Scout reads these via the Vault-owned `vault-query` skill (see M14 and N.2). Scout does not open vault files directly. Scout's entity research pass (D.0) writes dossier artifacts under `orgs/{slug}/dossier/entities/` via the Vault-owned write primitive; the shared research index under `vault_shared/research_db/` is accessed via the `research-db-query` skill.

### D.2 Scribe — Writing

Section-by-section drafting. KGIE preflight. SMART outcomes. Overlooked-expenses checklist. Funder dialect code-switching per Law 4.

**Funder dialect code-switching (v3 clarifying examples per Editor audit):** four dialects configured per funder — Conservative (e.g., USDA Farm Service Agency RFAs), Centrist (e.g., NSF standard program solicitations), Progressive (e.g., USDA SARE), and Soul-fire (e.g., Bread and Roses Community Fund). Scribe selects dialect by funder match; operator can override. Code-switching affects vocabulary and framing, NOT substance. Substance always comes from applicant (Law 5).

### D.3 Editor — Clarity review

Jargon flags with 2–3 replacement options. Goals/outputs/outcomes/objectives sorted.

### D.4 Judge — Scoring

Funder's rubric first, related rubrics next. Cross-family rigor with Scribe (Section E).

### D.5 Logician — Deterministic policy enforcement

Python + Cedar. Fail-closed. Enforces all Five Laws as PRE/POST gates. Zero token cost. Cannot be overridden.

**v3 role expansion:** Logician is the external trust anchor for:
- Source-tag verification (S9 — grep-check of DOC_SOURCED claims against cited file content; conversation-anchor match for USER_DATA claims; hard-block drafts with UNSOURCED claims)
- Health-tuple signature verification (M7)
- Sequence-ID monotonicity on admin-risk ledger (M8)
- Per-org key scoping enforcement (M9)
- Entity dossier lock verification (M11 — dossier must carry operator sign-off hash before seats can cite from it as DOC_SOURCED; unsigned dossiers treated as UNSOURCED)
- Operator final-review gate (S9 operator sign-off) — pipeline emits candidate draft + claim-evidence map; "shipped" status requires operator signature on the map

**v5 role expansion [M14, M15]:** Logician additionally anchors:
- Vault access gating — every seat call into `vault-query` or `research-db-query` passes through a Cedar `org_isolation` policy evaluation before the skill executes its read/write. Logician owns the policy file and the evaluation invocation.
- `vault_shared/` signed-commit verification — at pipeline start, Logician verifies git signatures on every tracked seed file under `vault_shared/` (see M15). Unsigned or tampered → hard abort. This is the same discipline S5 applies to `router.yaml`, widened to all shared-vault seed YAML.

### D.6 Operational gears (v3 with usage examples per Editor audit)

- **Sparring Partner** — seat generates options, human decides. Use when operator is still defining scope (new funder, new program type, ambiguous fit).
- **Co-Pilot** — human provides direction, seat executes and refines. **DEFAULT.** Use for standard drafting work where operator knows the substance and needs help shaping it.
- **Synthesizer** — full delegation, human reviews final output only. Use for well-understood repeatable grants (annual renewals, template-driven submissions where the only thing changing is the project details).

---

## E. Cross-family rigor

Review seats MUST NOT share provider family with author seat.

**v2 runtime invariant [M5]:** Cross-family rigor is an invariant on the **runtime seat pair**. Router re-checks family constraint on every fallback/escalation. If candidate fallback violates, router advances to next tier until compliant family found.

**v3 degradation policy [M10]:** Graceful-degradation is asymmetric by seat criticality:
- **Review seats (Judge, Red Team, Code Review, Reasoner Review):** NO graceful degradation by default. If no compliant family available, hard abort with operator alert. These seats exist specifically to guard against model-specific blind spots; running them on a same-family model defeats their purpose.
- **Author seats (Scout, Scribe, Editor):** graceful degradation allowed after `max_outage_minutes` (default 30) of full family-outage, with explicit operator alert + audit-log breach entry. Operator sees the rigor-breach flag in the rails report.
- **Channel F specifically:** graceful degradation is automatic (Channel F can run without cross-family rigor — it's a discovery channel, not a review gate).

**v4 enforcement [M13] — Review-seat outage escape valve (closes Red Team v3 HIGH review-seat DoS finding):**

Hard-abort on review-seat family outage is the default and correct stance — it preserves cross-family rigor. But a coordinated, prolonged outage of all compliant review-seat families (for example, Anthropic and Google both unavailable during a deadline crunch) turns that default into a denial-of-service on the operator. M13 names the escape valve so the architecture does not silently rely on ad-hoc operator improvisation.

- **Trigger condition:** All compliant review-seat families for a specific review seat have been `FAILED` for `max_review_outage_hours` (default **24 hours**, operator-configurable per-project up to a ceiling of 72 hours).
- **Escape mechanism:** Operator may issue a signed **review-seat bypass authorization** specifying (a) which review seat is bypassed, (b) the outage start timestamp, (c) the bypass expiry (max 24 hours from authorization; renewable with re-signing), (d) an operator attestation string acknowledging rigor breach. The authorization is written to the admin-risk ledger with a HIGH-severity entry requiring operator re-type confirmation (per S2).
- **Draft consequence:** Any draft produced while a bypass is active carries a mandatory **rigor-breach flag** in the rails report + in the claim-evidence map, visible to the operator at final-review time. The flag names the bypassed seat, the bypass authorization ID, and the active duration. Operator cannot ship the draft without explicitly acknowledging the flag at sign-off.
- **Default remains hard-abort.** Bypass is opt-in per-session by the operator with signed authorization; there is no automatic fallback to a weaker review. Operator must make a conscious, audited decision.
- **What the escape valve is NOT:** M13 is not a way to skip review seats for convenience, not a way to bypass Code Review for Opus-authored code without record, not a way to silently degrade Judge scoring. Every use leaves an auditable trail.

**v3 rule-collision resolution [S10b]:** **M5 wins over S5 at runtime.** If signed `router.yaml` points to a fallback that violates cross-family rigor, the runtime invariant blocks the call. This is treated as a routing-config bug that must be fixed in config, not bypassed at runtime. Logician logs the conflict to the audit chain; operator addresses at next maintenance window.

**router.yaml integrity [S5]:** Git-tracked with signed commits on operator's keyring. Logician verifies signature at pipeline start. Unsigned/tampered → hard abort.

**v5 extension [M15] — `vault_shared/` signed-commit discipline (closes Component 4 F4):**

S5's signed-commit requirement applies to `router.yaml` only in v4. Component 4's Scout bindings audit (2026-04-16) surfaced an equivalent supply-chain hole: seed YAML under `vault_shared/` (e.g., `vault_shared/sources/sources.yaml`, seeded foundation spreadsheets, the shared research-index seed set under `vault_shared/research_db/seeds/`) is consumed at pipeline start and drives Scout's fetch targets. An unsigned edit to a seed YAML can inject hostile endpoints, authenticated-with-attacker-token URLs, or malicious JSON-endpoint targets into Scout's discovery path.

M15 widens S5's discipline:

- **Covered paths.** Every tracked file under `vault_shared/` whose contents drive seat behavior at runtime — source-seed YAML, rubric-library entries, domain allowlists committed to shared vault, seed entries in `vault_shared/research_db/seeds/` — is git-tracked with signed commits on the operator's keyring.
- **Not covered.** Content written to `vault_shared/` at runtime by seats (e.g., `vault_shared/cached_opportunities/` entries) is NOT git-tracked seed content and is out of M15's scope. That content is covered by M14's vault-access gating and by the S10a no-org-attributes rule.
- **Verification.** Logician verifies signatures at pipeline start, alongside the existing S5 check on `router.yaml`. Unsigned or untrusted-signer → hard abort.
- **Key binding.** The signing keyring for `vault_shared/` seed files is the same operator keyring used for `router.yaml`. There is one trust root for vault-shared seed integrity, and it is the operator.
- **Why architectural and not blueprint-level.** Signed-commit discipline on runtime-consumed config is a trust-root policy. Hiding it inside a blueprint section would fragment the trust root across multiple blueprint artifacts. M15 states the rule once at architecture level; blueprint Section 2 specifies the verification mechanism (which paths are covered, how Logician walks them, how operator rotates the keyring).

**Current bindings (authoritative: `router.yaml`):**
- Scout: Ollama (local) / Groq / Anthropic
- Scribe: Anthropic / **[fixed in v2] OpenAI or Google** (previously Groq Qwen 3 32B — violated M5 runtime invariant)
- Editor: Groq Llama / OpenAI
- Judge: Groq Qwen / Google
- Red Team: Groq GPT-OSS / Anthropic
- Code Review (Codex): OpenAI / Anthropic
- Reasoner Review: Google / Anthropic
- Logician: none (deterministic)

---

## F. Review discipline — Thesis Team + Codex split

- **Opus-authored code → Codex** (OpenAI `code_review` seat).
- **Everything else → Thesis Team** (Editor Llama 3.3 70B + Judge Qwen 3 32B + Red Team GPT-OSS 120B).
- **Claude Code** MAY supplement; does NOT replace Thesis Team.

---

## G. Client org isolation

See Law 3 in Section B for v3 enforcement.

**v5 note:** Law 3's v5 extension (M14) adds vault-substrate enforcement. Section 2 Vault Topology is the blueprint section that implements this — see Section N.1 for the enumeration and N.2 for cross-section interfaces.

---

## H. Admin-risk register

See Law 4 in Section B for v3 enforcement.

---

## I. Institutional memory

- Tracked in `pipeline/institutional_memory/lessons.json` + `lessons.md`.
- **[S4] belief weight formula:** `belief_weight = severity × Σ(exp(-age_days / half_life))`, default `half_life = 365 days`.
- Retention cap: 1000 lessons active; oldest archived to `lessons/archive/YYYY-MM.json`.
- Before each run, load active lessons and pre-check.

---

## J. Pipeline and delivery

- **Revision loop cap:** 3 iterations.
- **Delivery:** three-tab — (1) draft, (2) rails report (scores, flags, per-channel health, sovereignty disclosures, source tags, rigor-breach flags, evidence trail), (3) lessons delta.
- **Cron:** Monday fund-radar at 08:30 local.

---

## K. Hardware and sovereignty

- Dev: M1 Mac Mini 8GB. Client: Golden Quill 64GB / Pro 128GB.
- Trust boundary = operator's keyring. Single-operator, single-machine v0.1 posture.

---

## L. What the architecture does NOT do

- Does NOT execute financial actions without per-action human approval.
- Does NOT maintain long-term cross-conversation state in LLM context.
- Does NOT silently rewrite flagged terms.
- Does NOT cross-reference org data.
- Does NOT absorb real collaborators into personas.
- Does NOT phone home for telemetry.
- Does NOT make outbound calls without operator-configured keys and per-session disclosure.

---

## M. Amendments added in v5

### M14 — Vault as the persistent-state substrate (closes Component 4 F3 at architectural layer)

**Statement.** Tilth's persistent state lives in a bounded substrate called the Vault. The Vault is divided into per-org vaults (`orgs/{slug}/vault/`) and a shared vault (`vault_shared/`). Every persisted artifact that Tilth produces or consumes outside of transient runtime memory — cached opportunities, subscribed-feed pulls, research briefs, entity dossiers, claim-evidence maps, rails reports, conversation logs, draft versions, revision-loop state, interrupted-state checkpoints, M10/M13 breach-flag history — lives in the Vault.

**Access discipline.**

- **Two Vault-owned first-class skills.** `vault-query` (read path, per-org vault + per-org views of shared vault) and `research-db-query` (read path, shared research index under `vault_shared/research_db/`). Skills are first-class council-accessible skills with declared Cedar gates and declared law bindings, not invisible internal helpers. Every seat that needs persistent state goes through one of these two skills.
- **Cedar `org_isolation` gate on both.** Each call carries the session-bound org-root hash (Law 3 / M2). The gate verifies that the targeted vault path resolves under that org's vault or under a permitted shared-vault read view before the read proceeds. Cross-org reads of `orgs/{other_slug}/vault/` paths are rejected by the gate. Shared-vault reads that would expose another org's attributes are rejected at cache-write time by S10a, and independently re-checked at read time by the gate.
- **Write path is narrower.** Writes to `orgs/{slug}/vault/` are routed through a Vault-owned write primitive that inherits the same `org_isolation` gate and the atomic-flush + canonical-path + inode-verified pattern from Section 1 Sovereignty Envelope. Writes to `vault_shared/` are further restricted: runtime-cached writes (e.g., `vault_shared/cached_opportunities/`) are allowed via the write primitive with S10a enforcement; writes to `vault_shared/` seed files are NOT a runtime operation — those are git commits and go through M15 signed-commit discipline.
- **Direct filesystem access by a seat bypassing the Vault-owned skills is a Logician PRE-gate failure.** Logician's rails check scans seat outputs and tool-call logs for vault-path reads that did not pass through `vault-query` or `research-db-query`. Any hit fails the pipeline.

**Why architectural.** The vault crosses every other architectural line. Scout (D.0, D.1), Logician (D.5), Pipeline (J), Law 3 (org isolation), Law 5 (DOC_SOURCED substrate including M11 dossiers), Autonomy Rule 1 (save state), and the admin-risk ledger all touch it. Naming the Vault as an architectural object with its own access discipline is what lets Section 2 specify the layout, Section 1 provide the primitives, and the other sections trust that the substrate enforces Law 3 below them. Without this naming, the Component 4 Scout audit's F3 gap ("`vault-query` and `research-db-query` should be first-class skills, not invisible deps") reappears every time a new section is blueprinted.

#### M14.1 — Atomic gate-and-open primitive (v5-r2, closes RT-v5 HIGH-1 gate-bypass TOCTOU)

**Statement.** The Cedar `org_isolation` policy evaluation and the corresponding filesystem open MUST be a single logically-atomic operation from the Vault-owned skill's point of view. No vault read or write may be composed as "evaluate Cedar → then later open(path)." The evaluated path and the opened file descriptor bind to the same inode/file-ID under a single resolution step.

**Why architectural.** RT-v5 HIGH-1 showed that a time-of-check-to-time-of-use gap between gate evaluation (at t0) and filesystem open (at t1) is exploitable by an attacker who mutates the path between t0 and t1 — a bind-mount flip, a rename, a symlink replanted after canonicalization, a snapshot swap. A non-atomic "evaluate-then-open" is always a TOCTOU hole, regardless of how careful the canonicalization logic is. The fix is not better canonicalization — it is removing the gap. Architecture states the requirement that the gap not exist. Blueprint Section 2 specifies the OS primitive that delivers it (e.g., Linux `openat2()` with `RESOLVE_NO_SYMLINKS | RESOLVE_NO_MAGICLINKS | RESOLVE_BENEATH`, or macOS equivalent using `O_NOFOLLOW` + post-open `fstat` inode-compare + fail-closed, or a privileged wrapper that performs gate+open in a single kernel-side call).

**Contract with Section 1.** Section 1's `safe_open_lock_file` helper (BT2 / Section 1 v5) already operates on the same "no-symlink + inode-compare after open" discipline. M14.1 requires that the Vault-owned skill's open path reuses that pattern (or an equivalent certified by Section 2 blueprint) for every read and every write. The Cedar evaluation sees the same inode the open sees. Blueprint implementers may not substitute a "canonicalize then open later" shortcut.

**What this closes.** Bind-mount flips, symlink-replant races, rename races, snapshot swaps against evaluated paths. What this does NOT close (by design): same-uid hostile code, compromised keyring, hostile OS — those are the trusted-operator threat-model's out-of-scope boundary (see Section O).

#### M14.2 — Cross-org metadata homogenization (v5-r2, closes RT-v5 HIGH-2 metadata-leak side-channel)

**Statement.** Any `vault-query` or `research-db-query` response whose content originates from a shared-vault read view (i.e., reads the same shared file from the vantage of multiple org sessions) MUST expose homogenized metadata: file size bucketed to a coarse class, mtime clamped to day-granularity, inode/file-ID not surfaced, cache-hit-rate not surfaced, per-path enumeration counts not surfaced. The byte content the requesting seat sees is the byte content it asked for; the shape of the surrounding metadata is not a side-channel that leaks which other orgs touched which shared entries.

**Why architectural.** RT-v5 HIGH-2 observed that a "permitted shared-vault read view" can LOOK correctly org-isolated at the content level yet leak cross-org attributes via derived keys — size deltas, mtime correlations, cache-hit-rate signals, inode-adjacency fingerprints. The fix is architectural because it is a requirement on the response shape of the Vault-owned skills, not on any particular file. Stating it once here prevents Section 2 blueprinters from re-inventing the metadata surface per-subtree.

**What this does NOT restrict.** Per-org metadata (an org reading its own `orgs/{slug}/vault/` subtree) is not homogenized — the org owns that metadata. The rule applies only to cross-org-visible shared views (`vault_shared/cached_opportunities/`, `vault_shared/research_db/`, Cedar policy files, shared rubrics, shared lessons). Homogenization does not apply to the claim-evidence map, rails report, conversation log, or any per-org path.

**Contract with S10a.** S10a prevents org-identifiable content from entering shared-vault cache at write time. M14.2 prevents org-identifiable metadata from leaking at read time. The two together close the symmetric content-and-shape attack surface.

##### M14.2.1 — Constant-time discipline extends to kernel-mediated copy (v5-r4, closes RT-v5-r3 LOW copy_file_range timing)

**Statement.** M14.2's metadata homogenization applies to the Vault-owned skill's response shape, but kernel-mediated copy primitives (`copy_file_range`, `sendfile`, `splice`) can move vault-path content between file descriptors with wall-clock durations that vary with source size below the bucket boundary, producing a timing side-channel that bucketed-size metadata does not cover. M14.2.1 requires that seats be denied these primitives entirely on vault paths: Section 2 blueprint's seccomp / LSM envelope MUST either (a) reject `copy_file_range` / `sendfile` / `splice` syscalls whose source or destination FD references a vault path, OR (b) route all kernel-mediated copy through a Vault-owned skill that pads the operation to constant-time-per-bucket on its response path. v0.1 default is (a).

**Why architectural.** RT-v5-r3 observed that M14.2's response-shape homogenization is evaluated at the Vault-owned skill's return boundary, but once a seat holds a vault-path FD (through a permitted gate call) it can issue a kernel-mediated copy that bypasses the response-shape gate and measures the kernel's own copy-loop duration. The architectural bar is that no observable signal varying with true file size escapes the gate; M14.2.1 names the kernel-copy primitive family explicitly so Section 2 blueprint cannot silently omit it.

**Scope.** Applies only to kernel-mediated copy operations that touch vault paths. Non-vault copies are unaffected.

**M14.2.1 extension (v5-r5, closes RT-v5-r4 MEDIUM alternative kernel-mediated copy primitives).** The prohibited-primitive list under M14.2.1 is not closed by `copy_file_range` / `sendfile` / `splice` alone. The architectural rule covers **all** kernel-mediated primitives that can move vault-derived content with size-dependent wall-clock latency. At v5-r5 the explicit list extends to: `copy_file_range`, `sendfile`, `splice`, `tee`, `vmsplice`, `process_vm_readv`, `process_vm_writev`. Section 2 blueprint's seccomp / LSM envelope MUST deny every member of this family when a vault-path FD or vault-derived memory region is the source or destination, or route each through the constant-time-padded Vault-owned skill response path. The architectural bar is "no kernel-mediated primitive with size-dependent latency escapes the gate"; enumeration is exhaustive at the primitive family level, and Section 2 blueprint MUST document its coverage of each named primitive. A future OS kernel that adds a new member of this family (e.g., a new pipe-splice variant) requires an architectural sub-amendment; Section 2 does not silently permit.

#### M14.3 — Direct-FS primitive prohibition (v5-r2, closes RT-v5 MEDIUM direct-FS-via-helper + MEDIUM TOCTOU)

**Statement.** Seats are architecturally prohibited from acquiring vault-path file descriptors via ANY path that does not resolve to a Vault-owned skill invocation. This includes (a) helper libraries that wrap `open()` on vault paths, (b) subprocess invocations where the child opens a vault path, (c) `sendfile()` / `splice()` / `mmap()` from a vault-path file descriptor obtained elsewhere, (d) POSIX message queues or shared memory segments that carry vault-path FDs, (e) FD-passing over unix domain sockets. Logician's PRE-gate scan (see D.5) covers the seat's own tool-call log; M14.3 extends the architectural requirement that Section 2 blueprint specifies the enforcement envelope (e.g., seccomp filter, sandbox policy, audit of linked libraries) such that no library or subprocess available to a seat can produce a vault-path FD outside the gate.

**Why architectural.** RT-v5 MEDIUM direct-FS-via-helper showed that a seat could route around `vault-query` by calling a helper that itself opens a vault path. The Logician PRE-gate scan as stated in M14 covers the seat's own code; M14.3 widens the requirement so that Section 2 blueprint is obligated to specify which OS primitives and which bundled libraries are allowed to hold vault-path FDs, and how the enforcement is audited. The architectural bar is "no off-ramp exists"; Section 2 specifies the exhaust.

**What this does NOT claim.** M14.3 does not pretend to stop same-uid hostile code from injecting a shared library and opening vault paths directly at the OS layer. Same-uid hostile code is the trusted-operator threat-model's out-of-scope boundary (see Section O). M14.3 closes off-the-shelf helpers and accidental composition; it does not pretend to sandbox against a compromised process.

##### M14.3.1 — io_uring file-open ops explicitly prohibited (v5-r3, closes RT-v5-r2 new MEDIUM io_uring-direct-FS-escape)

**Statement.** `io_uring` provides kernel-side file-open primitives (`IORING_OP_OPENAT2`, `IORING_OP_OPEN`) and kernel-side read/write primitives (`IORING_OP_READV`, `IORING_OP_WRITEV`, `IORING_OP_READ_FIXED`, `IORING_OP_WRITE_FIXED`) that bypass the conventional syscall path. A seat that submits an `io_uring` SQE targeting a vault path would bypass M14.1's atomic gate-and-open envelope. M14.3.1 names these explicitly among the prohibited direct-FS primitives: no seat may submit an `io_uring` SQE that touches a vault path, and Section 2 blueprint's seccomp / sandbox envelope MUST either (a) block the `io_uring_setup` / `io_uring_enter` syscalls entirely for seats, OR (b) enforce an eBPF / LSM filter on `io_uring` submission that rejects any SQE whose target path resolves under a vault subtree. A seat whose dependencies require `io_uring` is not a valid v0.1 seat; Section 2 blueprint documents the supported OS primitive list.

**Why architectural.** RT-v5-r2 observed that M14.3 enumerated "helper libraries, subprocesses, FD-passing, mmap/splice/sendfile" but not `io_uring`, leaving an enumerated-but-not-exhaustive list that invites the next attack. M14.3.1 closes that gap by naming `io_uring` specifically, and by stating that the seccomp/sandbox envelope is the required enforcement mechanism (not optional). The architectural bar is "no kernel-side file-open primitive reachable to a seat bypasses the gate"; M14.3.1 makes that bar explicit for the `io_uring` primitive that would otherwise be the leakiest off-ramp.

**Contract with Section 2.** Section 2 blueprint's "supported OS primitive list" is part of the Vault Topology spec. v5-r3 requires that list explicitly address `io_uring` (permit with filter, or reject wholesale); Section 2 cannot silently omit the question.

##### M14.3.2 — eBPF-direct-read prohibition (v5-r4, closes RT-v5-r3 MEDIUM eBPF-direct-read)

**Statement.** eBPF programs running in kernel context can invoke `bpf_probe_read_user`, `bpf_probe_read_kernel`, and `bpf_d_path` to read arbitrary memory and file-path contents, returning the result to user space via eBPF maps. A seat that is permitted to load eBPF programs (because `CAP_BPF` is granted to the operator uid, or because the kernel permits unprivileged eBPF) could use this to read vault-path content without invoking a Vault-owned skill, bypassing Cedar `org_isolation` entirely. M14.3.2 prohibits seats from loading eBPF programs that can touch vault inodes. Section 2 blueprint's enforcement envelope MUST deliver one of:
- **(a) Deny `bpf(BPF_PROG_LOAD)` syscall for seats via seccomp.** The full `bpf()` syscall family is rejected at the sandbox boundary. Seats do not legitimately need eBPF.
- **(b) Install an LSM hook (bpf-lsm or equivalent) that rejects any eBPF program whose verifier-visible read operations reference a vault-path inode or vault-path file descriptor.** This is the narrower permit-with-filter path for platforms or deployments where seccomp-level `bpf()` denial is too coarse.

v0.1 default is (a). A seat that requires eBPF is not a valid v0.1 seat.

**Why architectural.** RT-v5-r3 observed that M14.3 and M14.3.1 enumerated user-space helpers (libraries, subprocesses, FD-passing, mmap/splice/sendfile) and `io_uring` as kernel-side primitives but did NOT cover eBPF — the kernel-side primitive that can read vault content without ever invoking the conventional file-open path. M14.3.2 closes this by naming the eBPF read-probe family explicitly at the architectural layer.

**Contract with Section 2.** Section 2 blueprint's enforcement envelope documents the chosen mechanism (seccomp `bpf()` denial vs LSM-hook permit-with-filter) and verifies it is active at seat start.

**M14.3.2 extension (v5-r5, closes RT-v5-r4 MEDIUM perf_event_open uprobe/kprobe attachment).** On kernels where `perf_event_open` can attach a uprobe / kprobe / tracepoint to a user-space function WITHOUT re-invoking the `bpf()` syscall (the eBPF program is loaded once via `bpf()` but attachment is performed via `perf_event_open`), a seat could read vault memory via `bpf_probe_read_user` by attaching to a Vault-owned binary's code path and triggering the probe without triggering M14.3.2's `bpf()` seccomp denial. The architectural rule is extended: a seat MAY NOT invoke `perf_event_open` whose target is a Vault-owned binary, whose target process holds a vault-path FD, or whose read-probe would touch a vault-path inode or vault-derived memory. Section 2 blueprint's enforcement envelope MUST deliver one of:
- **(a) Deny `perf_event_open` syscall for seats via seccomp.** v0.1 default. Seats do not legitimately need `perf_event_open`; the loss of profiling/tracing capability is acceptable at the vault boundary.
- **(b) Install an LSM hook (perf-event-lsm or equivalent) that rejects any `perf_event_open` attachment whose target resolves to a Vault-owned binary OR whose uprobe/kprobe target is a function that reads vault memory.** This is the narrower permit-with-filter path for deployments where system-wide profiling is required outside the vault boundary.

v0.1 default is (a). The architectural bar is "no kernel-side memory-read primitive reachable to a seat bypasses the gate"; M14.3.2's extension makes the bar explicit for `perf_event_open` — otherwise the primitive is a silent off-ramp around the `bpf()` seccomp denial.

##### M14.3.3 — FD-passing of vault-derived descriptors prohibited (v5-r5, closes RT-v5-r4 MEDIUM FD-passing via abstract Unix-domain sockets)

**Statement.** A seat may NOT transfer an open vault-path file descriptor, or any FD whose referent is a vault inode or vault-derived memory region, to another process via any ancillary-data mechanism. The prohibited mechanisms include (non-exhaustive at the primitive level; exhaustive at the family level):
- `sendmsg(2)` with `SCM_RIGHTS` ancillary data carrying a vault-derived FD, over any Unix-domain socket (pathname OR abstract namespace).
- `pidfd_getfd(2)` against a process that holds a vault-derived FD.
- Any other OS primitive that duplicates an open FD from one process's FD table into another's (`CMSG_DATA`-equivalent mechanisms on BSDs, future kernel additions).

Section 2 blueprint's seccomp / LSM envelope MUST deliver one of:
- **(a) Deny `sendmsg`/`recvmsg` with `SCM_RIGHTS` ancillary data for seats via seccomp** (seats communicate via byte streams only; no FD-passing), combined with seccomp denial of `pidfd_getfd`. v0.1 default.
- **(b) Install an LSM hook that rejects ancillary-data FD transfers whose referent resolves to a vault path** (narrower permit-with-filter path for deployments where non-vault FD-passing is required).
- **(c) Run each seat in a per-seat mount + user namespace that strips received FDs at the namespace boundary** (defense-in-depth only; not a substitute for (a) or (b)).

v0.1 combines (a) with per-seat socket-namespace isolation so a seat cannot reach another seat's abstract-namespace socket even if `SCM_RIGHTS` were somehow permitted. Seats do not legitimately need FD-passing; the Vault-owned skill is the IPC.

**Why architectural.** RT-v5-r4 observed that with `shm_open`/`memfd_create` denied per M14.4.3 (tightened at v5-r5 to seccomp-only — see below), a seat could still open a vault FD via a permitted gate call and then hand it to another same-uid seat via `sendmsg`/`SCM_RIGHTS` over an abstract-namespace Unix socket, leaking vault data without invoking a Vault-owned skill on the receiver side. M14.3.3 closes the off-ramp at the architectural layer; the architectural bar is "a vault FD, once issued to a seat, does not leave that seat's process boundary."

**Contract with M14.3 / M14.3.2.** M14.3 already named FD-passing over unix domain sockets as prohibited in its (e) clause; M14.3.3 extends the requirement to explicitly name `SCM_RIGHTS` and `pidfd_getfd` as the specific primitives, and requires Section 2 blueprint's seccomp envelope to enforce the prohibition at the syscall layer (not merely at the Logician PRE-gate scan of the seat's own tool-call log). M14.3.2 covers kernel-side direct reads; M14.3.3 covers kernel-side FD duplication. The two together close the "seat can hand its FD to another seat" family.

**Contract with Section 2.** Section 2 blueprint's seccomp filter specifies the chosen enforcement mechanism (denial vs LSM-filter vs namespace-strip) and verifies at seat start that the expected behavior is active.

#### M14.4 — Crash-handler routed through Vault-owned write (v5-r2, closes RT-v5 MEDIUM crash-handler bypass)

**Statement.** The Autonomy Rule 1 crash-path (SIGTERM / SIGINT / uncaught exception / OOM handler) writes interrupted-state via the Vault-owned write primitive, not via a fallback direct-FS path. If the crash-handler cannot acquire the Vault-owned write primitive within a bounded timeout (Section 2 blueprint specifies the timeout; default 2 seconds), the seat exits WITHOUT writing interrupted-state. Lost interrupted-state is a recoverable degradation; a bypass-gated write is not. The crash-handler's Cedar `org_isolation` evaluation uses the same session-bound org-root hash as the seat's normal writes — the seat does not escalate privilege during exit.

**Why architectural.** RT-v5 MEDIUM crash-handler-bypass observed that Autonomy Rule 1's "save state on failure" creates architectural pressure to have a write path that ALWAYS works, even when the normal Vault-owned primitive is unreachable. M14.4 states the opposite: the Vault-owned primitive is the only persistence path, period. The cost of that discipline is paid in occasionally-lost interrupted-state; the benefit is that no off-ramp exists around M14. Stating this at the architectural layer prevents Section 2 or Section 5 blueprinters from silently reintroducing a "safe crash dump" that bypasses the gate.

**Contract with Section 5 Pipeline.** Section 5 owns orchestration; Section 5 blueprint specifies how a run that exited without writing interrupted-state is detected and recovered. The architectural requirement here is only that no such write exists outside the gate.

##### M14.4.1 — Ancillary-output suppression is a seat-start obligation (v5-r3, closes RT-v5-r2 MEDIUM crash-handler PARTIAL residual)

**Statement.** The crash-handler's write path is insufficient defense if the EXITING process emits state via ancillary channels — stderr, core dumps, logging-library buffered flushes, OS-level ptrace/crash-reporter integrations. M14.4.1 requires that:
- **(a) Core-dump generation is disabled at seat start**, not at crash time. Seats call `setrlimit(RLIMIT_CORE, 0)` (or macOS equivalent `ulimit -c 0` in the parent shell / `sysctl -w kern.coredump=0` scoped where supported) as part of seat initialization, BEFORE the seat executes any Vault-accessing code. A seat cannot legitimately produce a core file.
- **(b) stdout and stderr are closed or redirected to `/dev/null` before the seat performs any Vault read or write**. Seat initialization redirects both file descriptors to a null sink. A seat that genuinely needs diagnostic output emits it to the Vault-owned conversation log (per N.2 Section 2 → Section 4 interface), not to the inherited stdio.
- **(c) Logging libraries' auto-flush-on-exit hooks are disabled** at seat start. Seat initialization registers no `atexit()` handler that dumps buffered state anywhere other than the Vault-owned write primitive. Third-party logging frameworks that install such handlers implicitly MUST be configured to not do so (Section 2 blueprint documents the permitted logging library list).
- **(d) OS-level crash-reporter integrations (macOS CrashReporter, Linux abrt/systemd-coredump) are opt-out for seats**, not opt-in. Seat initialization signals the OS not to capture the exiting process; a seat whose crash would land in `/var/crash` or `/Users/.../Library/Logs/DiagnosticReports/` violates M14.4.1.

**Why seat-start not crash-time.** If ancillary-output suppression happens AT crash time, the code path between "crash occurs" and "suppression applied" is exploitable. Moving the suppression to seat-start removes that window entirely — the crash-handler inherits an already-suppressed process environment.

**Architectural bar.** The requirement is that no interrupted-state information reaches any persistence surface other than the Vault-owned write primitive. Section 2 blueprint specifies the OS primitives that deliver each of (a)–(d) on the supported platforms (macOS, Linux).

##### M14.4.2 — Ancillary suppression is applied at process creation, not at seat init (v5-r4, closes RT-v5-r3 MEDIUM abort-signal race + fork-inherit regression)

**Statement.** M14.4.1 required ancillary-output suppression at seat-start. RT-v5-r3 observed that library constructors and the dynamic linker's own init code run BEFORE the seat's `main()` / `__init__` block, so a seat whose third-party library calls `abort()` in its constructor would leak a core dump or stderr trace BEFORE M14.4.1's suppression code has a chance to run. M14.4.2 closes the window by pushing the suppression primitives to **process creation** via the process wrapper:
- **systemd-managed Linux seats:** `LimitCORE=0`, `StandardOutput=null`, `StandardError=null`, `SystemCallFilter=~bpf @debug` (covers M14.3.2), `NoNewPrivileges=yes`.
- **launchd-managed macOS seats:** `SoftResourceLimits.Core=0`, `HardResourceLimits.Core=0`, `StandardOutPath=/dev/null`, `StandardErrorPath=/dev/null`, `ProcessType=Interactive` off.
- **Fallback:** wrapper shell script that `ulimit -c 0` and `exec >/dev/null 2>/dev/null` before `exec`ing the seat binary. The wrapper MUST be signed per M15 if checked into `vault_shared/`.

**Why architectural.** The architectural bar moves from "seat must suppress at init" to "the process the seat runs inside was created with suppression already active." This removes the pre-seat-init window entirely and extends to forked children that inherit the hardened limits. M14.4.1 remains in force (seats also suppress at init as defense-in-depth), but the guarantee no longer depends on seat code running before library constructors.

**Contract with Section 2.** Section 2 blueprint specifies the per-platform wrapper (systemd unit / launchd plist / fallback script) and verifies at seat start that the inherited rlimits and stdio redirection are active. A seat whose inherited limits do not match expectations aborts at PRE-gate.

##### M14.4.3 — POSIX shared-memory prohibition for vault-derived data (v5-r4, closes RT-v5-r3 LOW POSIX shm leak)

**Statement.** POSIX shared-memory objects (`shm_open`, `memfd_create` with unlinked visibility via `/proc/self/fd`, named `/dev/shm/...` segments) can persist after a seat crashes and be read by another same-uid seat. A seat that writes vault-derived data to a named shm segment and crashes leaves that data accessible to any subsequent same-uid process that opens the same name. M14.4.3 prohibits this. Section 2 blueprint's enforcement envelope MUST deliver one of:
- **(a) Deny `shm_open` and `memfd_create` syscalls for seats via seccomp.** v0.1 default. Seats that need shared-memory communication use the Vault-owned skill IPC instead.
- **(b) Provide a per-seat shm namespace.** Each seat runs in a mount namespace where `/dev/shm` is a private tmpfs that is unmounted and discarded at seat exit. No named shm segment survives seat termination, and no two seats share a `/dev/shm` view.

**Why architectural.** RT-v5-r3 observed that M14.4.1's stdio / core-dump / atexit-flush suppression did not cover POSIX shm — a persistence surface outside the vault that same-uid seats can share. M14.4.3 names the primitive explicitly and states that Section 2 must deliver either denial or per-seat isolation.

**Contract with A1 (v5-r4 preflight).** M14.4.3 is a belt-and-suspenders guarantee. Under A1 (single-client-per-Golden-Quill at v0.1) the adversarial scenario — same-uid seats serving different clients sharing one shm object — does not arise in a shipped product. M14.4.3 closes the attack surface anyway because the operator dev environment (A2) still runs multi-client under operator trust, and because leaving the attack surface open would weaken the v2 hardening path (Section O.5).

**M14.4.3 tighten (v5-r5, closes RT-v5-r4 LOW memfd_create namespace alternative).** At v0.1, M14.4.3's permitted implementation is **option (a) seccomp-denial ONLY**. Option (b) per-seat shm namespace is **NOT a permitted v0.1 implementation** because it leaves `memfd_create` usable; a seat can still create an anonymous memfd, write vault-derived bytes to it, and pass the FD to another seat via a mechanism covered by M14.3.3 (which v5-r5 closes at the seccomp layer), but the architectural rule is belt-and-suspenders: `memfd_create` is itself denied at v0.1 so the attack never composes. Option (b) (per-seat shm namespace) is explicitly reserved for v2 and is named there under Section O.5.f as insufficient-alone-at-v2. At v0.1, Section 2 blueprint's seccomp filter MUST deny both `shm_open` AND `memfd_create` unconditionally for seats; a seat whose dependency requires either syscall is not a valid v0.1 seat.

##### M14.4.4 — Process-creation wrapper is an M15 signed-commit artifact (v5-r5, closes RT-v5-r4 MEDIUM wrapper-integrity subversion)

**Statement.** The per-platform process-creation wrapper from M14.4.2 (the systemd unit file, launchd plist, or fallback wrapper shell script) is NOT a free-form deployment artifact. It is an **M15-tracked signed-commit artifact**. The wrapper lives under `vault_shared/process_wrappers/` (Section 2 blueprint specifies the exact path layout, e.g., `vault_shared/process_wrappers/{platform}/{seat_family}.{unit|plist|sh}`), is committed to `vault_shared/` with operator signature per the M15 signed-commit discipline, and Logician verifies at seat start (PRE-gate):
- **(a)** The wrapper artifact's content hash matches the signed-commit hash recorded in the M15 ledger.
- **(b)** The operator signature on the M15 commit verifies against the operator keyring (same keyring used for `router.yaml` per S5 / M15).
- **(c)** The wrapper in use at seat launch — as inherited by the running process via the systemd `/proc/1/exe`-chain or launchd equivalent — is the same artifact referenced by the M15 signed commit.

If any of (a), (b), or (c) fails, the seat aborts at PRE-gate. A tampered wrapper (one whose content has been modified after the signed commit, or one replaced at deployment time by a compromised deployment pipeline) does not pass the verify and the seat does not run.

**Why architectural.** RT-v5-r4 observed that M14.4.2's security guarantee depends on the systemd unit / launchd plist / wrapper shell script being correctly deployed and unmodified. If the wrapper is replaced with one that omits `LimitCORE=0` or redirects stdout/stderr to a file instead of `/dev/null`, the ancillary suppression evaporates and the M14.4.1 window reopens. M14.4.4 closes this by binding the wrapper artifact to the same operator-signed integrity discipline that protects `router.yaml` and `vault_shared/` seed files (M15). The architectural bar is "the wrapper is as trustworthy as the keyring it is signed by"; a seat whose wrapper fails M15 verify is not a valid seat.

**Contract with M15.** M14.4.4 is a direct application of M15's signed-commit pattern to a new class of artifact (process-creation wrappers). No new keyring is introduced (O.2 rejection holds); the operator's keyring signs the wrapper commits the same way it signs `router.yaml` and `vault_shared/cedar/` policy files. M15.1's seed-vs-cache boundary applies: `vault_shared/process_wrappers/` is a seed path, not a cache path.

**Contract with Section 2.** Section 2 blueprint specifies the exact path layout under `vault_shared/process_wrappers/`, the Logician verification primitive (`/proc/self/status` inheritance check for Linux; `launchctl print` for macOS; wrapper-script hash compare for fallback), and the PRE-gate error message format for each failure mode. Section 2 blueprint also specifies how wrapper updates are rolled out (signed commit + seat restart — never hot-patch).

### M15 — `vault_shared/` signed-commit discipline (closes Component 4 F4 at architectural layer)

See Section E above. M15 widens S5's signed-commit requirement from `router.yaml` alone to all git-tracked seed files under `vault_shared/`.

#### M15.1 — Seed-vs-cache boundary discipline (v5-r2, closes RT-v5 MEDIUM scope-gap + LOW inconsistent-seed)

**Statement.** The seed / cache partition is defined by path, not by file content or intent. A path under `vault_shared/` is EITHER git-tracked seed (covered by M15 signed-commit) OR runtime cache (covered by M14 gate + S10a). No path is "sometimes seed, sometimes cache." A path cannot be reclassified at runtime. The canonical enumeration of seed vs cache subtrees lives in Section 2 Vault Topology blueprint; that enumeration is itself a seed file (Section 2's own path policy is signed at M15 keyring).

**Why architectural.** RT-v5 MEDIUM scope-gap showed that an attacker could reclassify a seed path as runtime cache to dodge signing. RT-v5 LOW inconsistent-seed observed that "seed" was referenced without a single enumeration. M15.1 states once at the architectural layer that the partition is path-keyed, that it is itself a seed, and that reclassification at runtime is not a supported operation. The attack surface closes because there is nowhere for a reclassification to land that does not itself require a signed commit.

**Operational note.** Moving a path from seed to cache (or vice versa) is a signed-commit operation that updates the Section 2 enumeration. It is not a runtime event.

#### M15.2 — Read-only freeze after verify (v5-r2, closes RT-v5 LOW commit-race)

**Statement.** After Logician verifies signatures on `vault_shared/` seed files at pipeline start (t=0), the seed-path set is frozen read-only for the duration of the pipeline run. A post-verify mutation of a seed file is detected by a repeat-verify at Logician's end-of-pipeline check, and if the verify-at-end differs from verify-at-start, the pipeline's output is flagged `seed_drift` in the rails report and the operator is prompted to re-run. The freeze is an architectural requirement; blueprint Section 1 or Section 2 specifies the OS mechanism (e.g., read-only bind-mount over seed paths for the pipeline's namespace, per-file lock with `O_EXCL` guard, Merkle root re-check at end).

**Why architectural.** RT-v5 LOW commit-race showed that verify-at-t0 + consume-at-t1 leaves a window for an unsigned push at t=0.5. The fix is to make t0 through end-of-pipeline a single frozen view, and to detect any drift across that window. Architecture states the freeze requirement; blueprint chooses the primitive.

**Relation to S5.** S5 already requires signed-commit on `router.yaml`; M15.2 extends that discipline with a freeze-after-verify requirement across BOTH `router.yaml` AND `vault_shared/` seed paths. `router.yaml` is now freeze-gated along with M15's paths — a small retroactive hardening of S5.

##### M15.2.1 — Atomic verify-and-freeze (v5-r3, closes RT-v5-r2 LOW commit-race PARTIAL)

**Statement.** The architectural requirement is that signature verification AND application of the read-only freeze are a single atomic operation from the pipeline's vantage. There is no addressable window between "verify succeeded at t=0" and "paths are read-only at t=0+ε" during which a concurrent writer could swap in mutated content that the pipeline would then consume before end-of-pipeline drift detection fires.

**Architectural mechanisms (Section 2 blueprint specifies; architecture requires one):**
- **(a) Mount-namespace switch.** The pipeline enters a new mount namespace at verification time; the read-only bind-mount is applied inside the namespace before any seat call returns. Seats operate inside the namespace for the pipeline lifetime. Outside mutations are invisible to the namespace.
- **(b) Verified-and-pinned Merkle root.** Verification computes a Merkle root over the seed set; the root is pinned in memory (not re-read from disk); every subsequent seed access is gated by a Merkle proof against the pinned root. Any on-disk mutation is invisible to seed reads because seed reads never re-hit disk after verification.
- **(c) Copy-on-verify to a per-pipeline snapshot.** Verified seed set is copied (via hardlink or content-addressable snapshot) to a per-pipeline read-only location; the pipeline reads from the snapshot for the run. Outside mutations do not affect the snapshot.

**Why architectural, not blueprint.** RT-v5-r2 observed that M15.2's "freeze after verify" language left a narrow window between t=0 verify and t=0+ε freeze-application during which a writer with in-scope write privileges could swap in mutated seed content. M15.2.1 closes the window architecturally by requiring that verify-and-freeze be a single operation, and by enumerating the OS primitive families that deliver it. Blueprint Section 2 picks one and specifies it.

**What remains out-of-scope.** A same-uid writer that mutates seed files BEFORE pipeline start (i.e., before verify-at-start runs at t=0) is covered by M15 signed-commit discipline: a mutated seed file fails the verification at t=0 and the pipeline aborts. A same-uid writer that mutates AFTER end-of-pipeline cannot affect the completed run. The only window M15.2.1 closes is the narrow verify-to-freeze gap.

#### M15.3 — Cedar-policy files carry HIGH-severity ledger entries on change (v5-r2, closes RT-v5 LOW policy-file social-engineering)

**Statement.** Cedar policy files under `vault_shared/cedar/` are M15-signed seed files, but additionally any change to a Cedar policy file is written to the admin-risk ledger with HIGH severity, requiring operator re-type confirmation (per S2) at sign time. This is architecturally distinct from generic seed signing: a compromised-or-coerced operator signing a benign-looking YAML seed is a less catastrophic failure than the same operator signing a Cedar policy that silently allows cross-org reads. The re-type confirmation forces the operator to pause, read the diff, and consciously acknowledge the change before the signature lands.

**Why architectural.** RT-v5 LOW policy-file observed that M15 signs Cedar policies the same way it signs source-seed YAML, which means a single key compromise or social-engineering success catastrophically unlocks the `org_isolation` enforcement. M15.3 does not prevent a determined attacker with keyring access from landing the policy — that is out-of-scope per the trusted-operator threat model (see Section O). It raises the friction so that an accidental or semi-coerced sign is intercepted by the operator's own re-type gate.

**Ledger entry content.** Each policy-change ledger entry names: (a) the policy file path, (b) the content-hash before and after, (c) a short operator-authored reason, (d) a cross-reference to the signed commit. Logician verifies the ledger entry exists and matches the commit at pipeline start.

---

## N. Blueprint section taxonomy (v5 added — closes the Section-2-is-unnamed gap)

### N.1 Section enumeration

The architecture delegates implementation to blueprint sections. Five blueprint sections cover v0.1:

| # | Name | Scope |
|---|---|---|
| **Section 1** | **Sovereignty Envelope** | Cryptographic primitives (BT1 SHA-3-512 + nonce), session lifecycle (BT6 HMAC key rotation), org-root containment (BT2 OS-level isolation), HMAC audit chains (ledger watermarks, boot-clock-history, init marker), filesystem isolation (`safe_open_lock_file` helper, canonical-path + inode binding), atomic flush (Autonomy Rule 1). **Status:** LOCKED 2026-04-16 (v5 of Section 1 blueprint, unanimous Thesis Team). |
| **Section 2** | **Vault Topology** | Persistent-state substrate — directory layout (per-org `orgs/{slug}/vault/`, shared `vault_shared/`, subtrees for cached opportunities / subscribed feeds / research briefs / dossiers / drafts / claim-evidence maps / rails reports / conversation logs / interrupted-state checkpoints / degradation-log), access-control via Vault-owned skills (`vault-query`, `research-db-query`), Cedar `org_isolation` policy file, signed-commit enforcement on `vault_shared/` seed paths (M15), TTL / staleness policy per subtree, per-org vault initialization and operator-sign-off on new-org provisioning. **Status:** next up for blueprint drafting once architecture v5 locks. |
| **Section 3** | **Scout** | Six-channel DISCOVER (A–F), VERIFY stage, REVIEW stage, entity research pass (D.0 / M11), health tuple HMAC (M7), S11a/b/c dossier hardening, Channel F pre-flight (BT12). Consumes Section 2 for cached opportunities, subscribed feeds, research briefs, dossier storage. |
| **Section 4** | **Logician** | Deterministic Python + Cedar fail-closed policy enforcement (D.5 role expansion). Owns claim-evidence map (BT7), USER_DATA conversation-anchor integrity (BT9), DOC_SOURCED grep windowing (BT10), cross-org dossier policy (BT11), rails report + breach-flag signing (BT13). Consumes Section 2 for claim-evidence map storage, rails-report storage, conversation-log storage, degradation-log storage. |
| **Section 5** | **Pipeline** | Orchestration + delivery (Section J). Owns provider-call rate limiting (BT5), revision loop cap, three-tab delivery, cron scheduling. Consumes Section 2 for draft version storage and revision-loop-state persistence. |

This enumeration is load-bearing: BT annex delegations in Section M reference blueprint-section ownership by number. v5 closes the prior gap where Section 2 was referenced implicitly (through vault paths) but never named as a first-class blueprint section.

### N.2 Cross-section interfaces

Blueprint sections do not re-implement each other. Each provides a narrow, named interface to the others. Section 2's vault is the only substrate all other sections touch, so Section 2 is the primary cross-section hub.

**Section 1 → Section 2 (primitives consumed by Vault).**
- `within_org_root(path, org_slug) → bool` — path-containment predicate.
- Canonical path resolver + inode snapshot — Vault writes bind both at write time.
- Reserved-slug guard — prevents a new-org provision from colliding with system slugs (e.g., `_TEMPLATE`, `vault_shared`).
- HMAC audit-chain writer — vault append-only logs (degradation-log, admin-risk-ledger, conversation-log) use the Section 1 chain pattern.
- Atomic flush (temp-file + rename) — vault writes use the same primitive.
- `safe_open_lock_file` — vault lock files (per-subtree write locks) route through this.
- Per-session HMAC key lifecycle (BT6) — vault claim-evidence map signing, rails-report signing, conversation-log signing all use Section 1's session key.

**Section 2 → Section 3 (Vault surfaces Scout consumes).**
- `vault-query` read view of `vault_shared/cached_opportunities/` — Scout Channel B source.
- `vault-query` read view of `orgs/{slug}/vault/subscribed_feeds/` — Scout Channel B per-org source.
- `vault-query` read view of `orgs/{slug}/vault/research/briefs/{claim_hash}/` — Scout research-brief cache (with brief_max_age_days gate referenced — blueprint-level, Component 4 F2 context).
- `vault-query` read/write view of `orgs/{slug}/dossier/entities/{entity_slug}.md` — Scout entity research pass output (reads carry S11c lock verification, writes carry operator-sign-off gating).
- `research-db-query` read view of `vault_shared/research_db/` — shared research index.
- Vault write primitive for Scout cache writes — Scout writes cached opportunities via this, S10a no-org-attributes enforced at write time.

**Section 2 → Section 4 (Vault surfaces Logician consumes).**
- `vault-query` write view for claim-evidence maps under `orgs/{slug}/vault/claim_evidence/` — atomic sign-overwrite per BT7.
- `vault-query` write view for rails reports under `orgs/{slug}/vault/rails/` — signed per BT13.
- `vault-query` write view for conversation logs under `orgs/{slug}/vault/conversations/` — append-only signed per BT9.
- `vault-query` write view for degradation log under `orgs/{slug}/vault/degradation_log/` — append-only hash-chained per BT8.
- `vault-query` read views of the above when Logician verifies sign-off at cite time.
- Cedar `org_isolation` policy file lives at `vault_shared/cedar/org_isolation.cedar` (M15 signed). Logician loads and evaluates; Vault skills invoke the evaluation before each call.

**Section 2 → Section 5 (Vault surfaces Pipeline consumes).**
- `vault-query` write view for draft versions under `orgs/{slug}/vault/drafts/{rfa_hash}/v{n}/`.
- `vault-query` write view for revision-loop state under `orgs/{slug}/vault/revision_state/{rfa_hash}/`.
- `vault-query` write view for interrupted-state checkpoints under `orgs/{slug}/vault/interrupted/` — Autonomy Rule 1 persistence target.

**Section 3/4/5 → Section 2 (no direct filesystem writes).** Each of Scout, Logician, and Pipeline writes persistent state exclusively through Vault-owned skills. A seat that attempts a direct `open()` on a vault path bypasses the org_isolation gate and fails the Logician PRE-gate (M14), closed further by M14.1–M14.3 (v5-r2).

**v5-r2 surface addition (closes RT-v5 LOW missing-degradation_log-in-N.2).** The Section 2 → Section 4 interface list above is explicit that the degradation log (`orgs/{slug}/vault/degradation_log/`) is a `vault-query` write view consumed by Logician, append-only hash-chained per BT8. This surface was implicit in BT8 in v5-r1; v5-r2 names it in N.2 so Section 2 blueprinters cannot silently omit the subtree when enumerating covered paths.

### N.3 Section-2 ownership of BT14

BT14 (see below) is delegated to Section 2 Vault Topology.

### N.4 Temporal bridge — architecture-lock-before-Section-2-blueprint-lock window (v5-r2, closes RT-v5 LOW temporal hole)

**Statement.** When architecture v5-r2 locks, Section 2 Vault Topology blueprint is not yet locked (it is next up for drafting per N.1). During this window, the architectural requirement that every persistent-state access routes through Vault-owned skills is binding on seats, but the blueprint-level implementation of those skills does not yet exist. Two architectural provisions cover the window:

- **(a) Seats that are already locked (Section 1 Sovereignty Envelope, and the council seats per D.1–D.5) operate only through the primitives their own locked blueprint provides.** Until Section 2 locks, no seat executes a vault read or write that depends on `vault-query` or `research-db-query` as a first-class skill. Pipeline operation during the window is restricted to v4's implicit vault access pattern (seats reading via Section 1 primitives directly, with the Section 1 canonical-path + inode + within_org_root envelope enforcing containment). This is a provisional regression — acceptable because v5-r2's architectural commitments bind the next blueprint-lock round, not the current window.
- **(b) The temporal bridge is a provisional scope restriction, not an escape hatch.** Seats may NOT land new persistent-state subtrees during the window that would need Section 2 to exist to be accessible safely. New persistent-state requirements surface in Section 2 blueprint drafting; they do not land in v4-implicit access patterns and then retroactively inherit M14 coverage when Section 2 locks.

**Why architectural.** RT-v5 LOW temporal-hole observed that v5-r1 silently depends on a not-yet-locked blueprint section for its enforcement teeth. N.4 names the dependency explicitly, limits operation during the window to the primitives that do exist, and forbids growing the covered surface during the window. The architectural bar is honest about the temporal gap rather than papering over it.

**Exit criterion.** N.4 expires when Section 2 Vault Topology blueprint locks unanimous. At that point the provisional-scope restriction in (b) lifts automatically.

#### N.4.1 v0.1 does not operate during the temporal bridge window (v5-r4, closes RT-v5-r3 claimed N.4 regression)

**Statement.** v0.1 production grant runs DO NOT execute during the architecture-lock-to-Section-2-blueprint-lock window. Pipeline `run` entrypoints are gated at Logician PRE-scan on the presence of a Section 2 blueprint lock marker; absence of the marker is a PRE-gate failure, not a degraded mode. Seats MAY be initialized during the window for test, audit, or development purposes (operator-authored under the operator's trusted environment per A2), but no seat-pipeline run that produces an operator-deliverable artifact (draft, rails report, claim-evidence map) executes until Section 2 locks.

**Why architectural.** RT-v5-r3 observed that N.4 named the temporal bridge as a provisional regression with a weaker enforcement window — seats using v4's implicit pattern without M14.1's atomic gate-and-open. N.4.1 closes that by stating v0.1 simply does not operate in that window. The weaker-enforcement window is not a degraded mode that ships; it is a not-running mode. Architecture does not need a defense for a mode that does not execute.

**Exit criterion.** N.4.1 lifts when Section 2 blueprint locks. At that point v0.1 production runs are enabled.

**Contract with Section 5 Pipeline.** Section 5 blueprint's `router.py` / `pipeline.py` entrypoints check the Section 2 lock marker at the first PRE-gate. The marker format, path, and signature requirement are specified by Section 2 blueprint itself (self-referential but resolves because Section 2 lock is the marker's ground truth).

#### N.4.2 Section-2 lock marker MUST be operator-signed (v5-r5, closes RT-v5-r4 LOW circular Section-2 lock marker)

**Statement.** The Section 2 blueprint lock marker checked by N.4.1's PRE-gate is NOT validated by a superficial existence check. The marker MUST be operator-signed, and Logician MUST verify the marker's operator signature at the N.4.1 PRE-gate before permitting any production run. Verification is a three-part check, same pattern as M14.4.4:
- **(a)** The marker file exists at the path specified by Section 2 blueprint.
- **(b)** The marker content is accompanied by an operator signature that verifies against the operator keyring (the same keyring used for M15 signed-commits — the operator's keyring is the single trust root per O.1).
- **(c)** The marker's content hash is committed to the M15 signed-commit ledger (a fabricated marker that has not been operator-committed fails the ledger check even if it carries a bit-pattern that resembles a signature).

A marker that fails any of (a), (b), or (c) is not a valid N.4.1 release-gate; the run is blocked.

**Why architectural.** RT-v5-r4 observed that N.4.1 checks for a lock-marker whose format is defined inside Section 2. A hostile seat, or a deployment pipeline that prematurely drops a marker-shaped file into the expected path, could pass a superficial existence check and cause N.4.1 to permit a production run before Section 2 blueprint is actually locked by the Thesis Team. The fix is to make the marker's authenticity — not merely its existence — the gate condition. Operator signature + M15 ledger entry together prove the marker was issued by the operator's trusted keyring AND recorded in the signed-commit chain, not merely written to disk.

**Contract with M15 / M14.4.4.** N.4.2 is the third artifact (after `router.yaml` and process-creation wrappers) bound to the M15 signed-commit discipline. No new keyring; no new trust root; the operator's keyring signs the marker the same way it signs every other integrity-critical artifact. Cedar policy files under `vault_shared/cedar/` and source-seed YAML under `vault_shared/` already share this pattern per M15.

**Contract with Section 2.** Section 2 blueprint specifies the marker's path and content format; N.4.2 specifies the architectural requirement that the marker MUST be operator-signed and M15-committed. Section 2 blueprint cannot silently omit the signature requirement.

---

## M-prime. Blueprint-tracked hardening requirements (v5 annex — BT1–BT14)

These are architectural requirements that delegate the HOW to blueprint layer. The architecture states the requirement; blueprint sections specify the implementation. Blueprint sections that omit any of these fail their own audit.

| ID | Requirement | Blueprint section that owns it |
|---|---|---|
| BT1 | Hash algorithm for RFA dual-hash and audit chain is SHA-3-512 with per-RFA random nonce. Must be collision-resistant against adversarial pre-image construction. | Section 1 — Sovereignty Envelope (`audit.py`, `keys.py` bind nonce generation) |
| BT2 | Org-root filesystem enforcement uses OS-level namespace isolation (macOS sandbox / Linux namespaces). Canonical path resolution is necessary but not sufficient. TOCTOU race must be closed with atomic bind-mount or equivalent. | Section 1 — Sovereignty Envelope (`isolation.py`, `topology.py`) |
| BT3 | Admin-risk ledger enforces per-org rate limits and size quotas. Low-severity flood attacks must be blocked at write time, not at read time. | Section 1 — Sovereignty Envelope (`admin_risk.py`) |
| BT4 | BYOK keys may optionally be stored in HSM / separate encrypted vault with distinct access controls. Default implementation uses OS keyring per org; HSM path is documented and switchable. | Section 1 — Sovereignty Envelope (`keys.py`) |
| BT5 | External provider calls (Brave, Anthropic, Groq, OpenAI, Google) enforce per-session and per-org quota limits with exponential back-off on repeated failures. Prevents quota exhaustion / cost attacks. | Section 5 — Pipeline (rate-limiter middleware in router) |
| BT6 | **M7 HMAC key lifecycle.** Per-session HMAC key (health-tuple signing) must support rotation on session start, revocation on session end or operator-triggered rotation, and optional HSM-backed storage via the BT4 switch. Key material MUST NOT persist past session termination. | Section 1 — Sovereignty Envelope (`keys.py`, `session.py`) |
| BT7 | **Atomic claim-evidence map sign-overwrite.** Map generation → content-hash computation → operator signature of hash → write of `(map, hash, signature)` triple must be atomic (temp-file + rename, or equivalent). Post-generation modification invalidates the signature. | Section 4 — Logician (`claim_evidence.py`) |
| BT8 | **M10 degraded-run flag integrity.** Author-seat `degraded_run` flag and review-seat `bypass_active` flag are stored in an append-only hash-chained log (same pattern as S2 admin-risk ledger). No in-place mutation; flag history auditable. | Section 1 — Sovereignty Envelope (`degradation_log.py`) |
| BT9 | **USER_DATA conversation-anchor integrity.** Conversation transcripts are written to an append-only signed log; Logician verifies log signature before accepting any `USER_DATA` anchor reference. Per-session log signed by Logician-issued session key. | Section 4 — Logician (`conversation_log.py`) |
| BT10 | **S9 grep verification windowing.** Logician grep-check for `DOC_SOURCED` claims is windowed (±N sentences or ±N lines of surrounding context, configurable; default ±2 sentences). Optional semantic similarity check between claim and surrounding paragraph when available. | Section 4 — Logician (`source_tag_verify.py`) |
| BT11 | **M11 cross-org dossier reference policy.** Manual operator cross-referencing of a dossier from a different org must log a per-reference audit entry and require a secondary operator confirmation at draft-time (not at reference-creation time). Default posture: cross-org references flagged as `cross_org_dossier` in the claim-evidence map. | Section 4 — Logician (`dossier_verify.py`) |
| BT12 | **M11 Channel F domain pre-flight.** Per-org research fetches consult the S11a allowlist *and* a per-org jurisdiction/sovereignty policy before dispatching. Fetches to disallowed jurisdictions are rejected pre-flight, not disclosed after-the-fact. Default policy: none; operator opts in. | Section 3 — Scout (`channel_f_preflight.py`) |
| BT13 | **Rails report + breach-flag integrity.** Final rails report (including rigor-breach flags, M13 bypass authorizations, session-fetch disclosures) is signed by Logician before delivery to operator. Operator-visible report carries signature; any post-delivery edit invalidates it. | Section 4 — Logician (`rails_report.py`) |
| **BT14** | **v5 — Vault org-isolation + `vault_shared/` signed-commit hardening.** (a) Per-org vault containment enforced by Section 1's `within_org_root` + canonical-path + inode primitives, bound at every vault read/write call. (b) Vault-owned skills `vault-query` (per-org + permitted shared-vault views) and `research-db-query` (shared research index) are first-class skills with declared Cedar `org_isolation` gates and declared law bindings. (c) Cedar `org_isolation` policy file lives under `vault_shared/cedar/` and is M15-signed. (d) `vault_shared/` seed YAML, rubric-library entries, Cedar policy files, and domain allowlists committed to shared vault are git-tracked with operator-signed commits; Logician verifies at pipeline start alongside the existing `router.yaml` check. (e) Seat-side direct filesystem access to vault paths is a Logician PRE-gate failure; every persistent-state read and write routes through `vault-query` or `research-db-query`. (f) Per-org vault initialization (new-org provisioning) is operator-gated and produces a per-org `vault/init.marker` equivalent so Section 1's first-boot-reset defense (Section 1 v5 init marker pattern) extends to each org's vault. **(g) v5-r2 — Volume-UUID + FS-file-ID containment, not inode alone (closes RT-v5 HIGH-3 APFS clones/reflinks).** Per-org containment binds (volume UUID, FS file ID) as the identity tuple, NOT inode alone. APFS clones, reflinks, snapshot-mount file IDs, and any OS primitive that can produce the same inode under two different volume / namespace vantages are rejected at the vault-write gate. A vault write that would produce a reflink or clone crossing org boundaries fails the gate. Section 2 blueprint specifies the OS primitive (e.g., macOS `statfs` volume UUID + `st_ino` + `getattrlist` file ID combination, Linux `statx` STATX_MNT_ID + file ID combination) that delivers the identity tuple. **(g.1) v5-r3 UUID floor (closes RT-v5-r2 LOW volume-UUID-absence).** Vault subtrees MUST reside on filesystems that expose a stable volume UUID — APFS (macOS), ext4 with UUID set, btrfs, zfs, xfs. Placing any vault subtree (per-org or shared) on a filesystem that does not expose a stable UUID — `tmpfs`, `overlayfs` over a tmpfs upper, network mounts that do not advertise a stable UUID, unformatted block devices — is a Logician PRE-gate failure at pipeline start. No "fallback to inode-only identity" is permitted when the UUID is missing; the identity tuple (volume UUID, FS file ID) is unconditional, and a missing UUID aborts the run rather than silently degrading the gate. | **Section 2 — Vault Topology** |

---

## O. v5-r2 threat-model out-of-model rejections

v5-r1's Red Team challenge (2026-04-16) surfaced three findings that v5-r2 does NOT close architecturally. Each is explicitly rejected and anchored to the trusted-operator v0.1 threat-model boundary. The boundary is: IN-SCOPE for v0.1 — path trickery, symlink-plant, watermark-rollback, file-write-only attacks by a non-privileged caller; OUT-OF-SCOPE for v0.1 — same-uid hostile code, same-uid concurrent writer, compromised operator keyring, hostile OS, physical seizure. Section O names each rejection so future audits do not silently re-introduce them as architectural obligations.

### O.1 Centralisation of trust in the Vault (rejects RT-v5 HIGH-4)

**RT-v5 finding summary.** Naming the Vault as a first-class architectural object concentrates trust in one place that v4's implicit design spread across seats and Section 1 primitives.

**Rejection.** v4 was not actually dispersed — v4 concentrated operator-keyring trust exactly where v5 does, in `router.yaml` signed commits and Section 1 HMAC chains. v5 names the substrate that v4 had implicit; it does not add a new trust root. The operator's keyring is one trust root in both v4 and v5. Making the Vault a named architectural object makes that trust root auditable and delegable to a single blueprint section (Section 2) rather than smearing it across every section that happens to open a file under `orgs/{slug}/vault/`. A named trust root is not a concentrated trust root; an unnamed one is harder to review and easier to silently drift. v0.1's threat model assumes the operator trusts their own keyring; that assumption is identical in v4 and v5.

**What would make this architectural.** A threat model where the operator is adversarial to their own keyring (e.g., multi-tenant v1.0 deployment, compromised-operator scenarios). That is not v0.1 scope.

### O.2 Keyring-compromise blast radius (rejects RT-v5 MEDIUM keyring-compromise)

**RT-v5 finding summary.** Because M15 uses the same operator keyring as S5, a single key compromise catastrophically unlocks both `router.yaml` AND `vault_shared/` seed files.

**Rejection.** Compromised-keyring is explicitly out-of-scope for v0.1. The trust boundary IS the operator's keyring; if the keyring is compromised, all integrity claims fall regardless of whether there is one key or ten. Adding a separate keyring for M15 would increase operational friction without changing the v0.1 threat-model calculus — a determined attacker who compromises one key can compromise another on the same machine. The right architectural layer for multi-key-ring defense-in-depth is a future multi-tenant or HSM-path release (BT4 names the HSM switch; v0.1 defaults to OS keyring).

**What would make this architectural.** A threat model where the operator's machine is partially compromised (one key exposed, another held in a hardware token). That is BT4's future path, not v0.1.

### O.3 Snapshot-mount containment bypass (rejects RT-v5 LOW snapshot-mount)

**RT-v5 finding summary.** APFS snapshot mounts could present an attacker-chosen vantage where per-org containment fails under an OS-level snapshot swap.

**Rejection.** Snapshot-mount attacks require OS-level administrative privilege to create the snapshot and mount it under the attacker's chosen path. OS-level administrative access by a hostile party is out-of-scope for v0.1 (the trusted-operator threat model assumes the OS itself is not adversarial). M14.1's atomic gate-and-open primitive and BT14(g)'s volume-UUID + FS-file-ID binding defend against snapshot-mount variants that do NOT require admin privilege (i.e., a snapshot mount the seat could produce itself); admin-privileged snapshot attacks fall below the v0.1 threat floor.

**What would make this architectural.** A threat model where the OS itself is adversarial, or where a non-privileged caller can produce a snapshot mount. Neither is v0.1 scope on macOS or Linux with default permissions.

### O.4 Same-uid timing observability across orgs (v5-r4 re-anchor — rejects RT-v5-r2 / RT-v5-r3 timing finding via confirmed v0.1 scope A1)

**RT-v5-r2 / RT-v5-r3 finding summary.** Even with M14.2's bucketed-size and day-clamped-mtime metadata homogenization, the latency to stream file content still varies with the file's true size bucket. A seat in one org session, running concurrently with a seat in another org session, could measure its own response-latency to a shared-vault read and infer which size bucket the shared file belongs to, leaking coarse cross-org usage patterns. RT-v5-r3 further observed that the original O.4 anchor ("same-uid seats non-adversarial under trusted-operator v0.1") was load-bearing on an unstated scope assumption about multi-client-on-shared-hardware.

**v5-r4 re-anchor (confirmed scope A1).** v0.1 ships single-client-per-Golden-Quill (preflight assumption A1, confirmed by operator 2026-04-17). A Golden Quill hardware unit delivered to a paying client contains exactly one client's data. There is therefore no "seat-for-client-A timing-attacks seat-for-client-B" scenario in a v0.1 product deployment — only one client's data is present. Cross-org timing observability is not a v0.1 attack surface because cross-org deployments are not a v0.1 product configuration. The attack described requires the multi-client-on-shared-hardware configuration named in Section O.5 as v2 scope.

**Operator dev environment (A2) clarification.** Josh's M1 dev node legitimately carries multiple client orgs under `orgs/` because the operator is the sole authorized party for all of those clients (A2, A4). In this case the seats serve different client data but under a single trusted operator; the operator does not timing-attack their own seats. This mirrors how a consulting firm runs multiple client projects on one workstation — the operator's trust assumption covers the scenario. v0.1 does not harden the operator dev environment against the operator itself.

**What would make this architectural.** The multi-client-on-shared-hardware product configuration (distinct, mutually-adversarial clients sharing one Golden Quill). That configuration is explicitly v2 scope per A3 and Section O.5. v0.1 explicitly does not carry timing-equalization defense because the threat is not a v0.1 product scope.

**Operator guidance (non-architectural).** An operator who anticipates moving to multi-client-on-shared-hardware before v2 ships can run one Tilth instance per client on separate Golden Quill units (the Golden Quill Pro hardware product already supports this). Architecture does not mandate per-client hardware at v0.1 because v0.1 ships as single-client-per-Golden-Quill by scope definition.

### O.5 Multi-client-on-shared-hardware = v2 scope (v5-r4 added — names v2 hardening requirements rather than rejecting)

**Scope statement.** A shipped multi-client Golden Quill configuration — distinct, mutually-adversarial client orgs sharing one hardware unit — is a **v2 product configuration**, not v0.1 (preflight assumption A3). v0.1 does not support this configuration; attempting to run multiple client orgs under different Cedar `org_isolation` boundaries on one Golden Quill and deliver that as a product is out-of-scope for v0.1.

**v2 hardening requirements (named now, audited at v2 lock).** When v2 opens multi-client-on-shared-hardware as a supported product configuration, the following architectural hardening is required and is part of the v2 audit round:
- **O.5.a Constant-time response padding for cross-org-visible reads.** Every Vault-owned skill response whose content originates from a shared-vault read view pads wall-clock response time to the max-bucket worst case for its bucket class. Reads of per-org subtrees are not padded (the observer is the owner). Blueprint Section 2 specifies the padding primitive (monotonic-clock wait, cgroup-based CPU quota, or equivalent).
- **O.5.b Per-org process isolation with CPU-cache-flush between contexts.** Each client org's seats run in a distinct cgroup / jail / sandbox; context switches between org contexts include an architectural CPU-cache-flush barrier so that L1/L2/L3 cache residency does not leak across orgs. Blueprint Section 2 specifies the flush primitive (kernel-side `INVD` equivalent on supported architectures, or software-level eviction).
- **O.5.c Seat-to-seat IPC timing boundary.** Any cross-org communication (e.g., shared cache warming, shared rubric-library access) uses an IPC primitive whose timing is independent of the cross-org content size. No direct shared-memory IPC across org boundaries.
- **O.5.d HSM-backed keyring per BT4.** v2 switches from OS-keyring-default to HSM-default for per-org BYOK keys. Compromise of one org's HSM handle does not expose another org's key material, even under a same-machine attacker.
- **O.5.e eBPF denial is seccomp-enforced.** M14.3.2's option (a) (seccomp denial of `bpf()`) is mandatory at v2; option (b) (LSM-hook permit-with-filter) is not sufficient because a permit-with-filter path is harder to audit against cross-org observation.
- **O.5.f POSIX shm denial is seccomp-enforced.** M14.4.3's option (a) (seccomp denial of `shm_open` / `memfd_create`) is mandatory at v2; option (b) (per-seat shm namespace) is not sufficient at v2 for the same reason.

**Why named rather than deferred silently.** Naming the v2 hardening requirements at v0.1 lock time prevents future architecture rounds from re-inventing them, and gives the v2 audit round a fixed target. Operator who plans to move to multi-client-on-shared-hardware before v2 can read this section and know what will change.

**Why v2 not v1.5.** Multi-client-on-shared-hardware is a substantive product-and-architecture rev, not a surgical amendment. Bundling it with smaller rev windows would compromise the audit discipline.

**Contract with A3.** O.5's existence is what makes A3 load-bearing. Without O.5, A3 would be a silent deferral; with O.5, A3 is an explicit scope boundary that has a named successor configuration.

---

# Audit request (v5 revision 7)

Re-audit this revision (v5-r7). Confirm:

**A. Preflight deployment-assumption block is ground truth (v5-r4/r5/r6/r7).** Preflight A1–A4 remain operator-confirmed. Red Team may not attack A1–A4 as findings; it may only attack whether v5-r7 architecture correctly delivers on A1–A4, or identify new in-scope architectural attacks independent of the scope question.

**B. v5-r7 surgical additions close the RT-v5-r6 residual items.**
- RT-v5-r6 PARTIAL macOS copy-primitive gap (Bucket C Q1 PARTIAL) → closed by v5-r7 M14.2.1 macOS enumeration (`clonefile`, `clonefileat`, `fcopyfile` named explicitly as macOS equivalents of `copy_file_range` / `sendfile` / `splice`)?
- RT-v5-r6 MEDIUM `mach_msg` privileged Mach-port bypass of `sandbox_init(2)` profile → closed by v5-r7 macOS parallel-primitive clause extension (`mach_msg_trap` with `MACH_PORT_RIGHT_SEND` + `task_for_pid` named as required deny entries)?
- RT-v5-r6 LOW trust-root mirror symlink/immutability hardening → closed by v5-r7 N.4.2 trust-root mirror immutability addition (`chattr +i` on Linux, `chflags uchg` on macOS, for mirror file and containing directory during pipeline-run window)?

**C. Section O.4 A1+A4 drift-preempt clause continues to disqualify same-uid-peer attacks at v0.1.** No re-flagging of Bucket A.

**D. v5-r6, v5-r5, v5-r4, v5-r3, v5-r2, v5-r1, v4 lock text preserved verbatim.** v5-r7 additions EXTEND their parents (M14.2.1 macOS enumeration under v5-r6 macOS parallel-primitive clause; mach_msg/task_for_pid under v5-r6 macOS parallel-primitive clause; N.4.2 immutability under v5-r6 N.4.2 trust-root mirror). No prior clause replaced or weakened.

**E. No new rule collision in v5-r7.**
- M14.2.1 macOS enumeration (clonefile/clonefileat/fcopyfile) vs v5-r6 macOS parallel-primitive clause (implicit coverage): [clear/extension/collision]
- macOS parallel-primitive clause mach_msg/task_for_pid extension vs v5-r6 macOS parallel-primitive clause (syscall-only coverage): [clear/widening/collision]
- N.4.2 trust-root mirror immutability vs v5-r6 N.4.2 trust-root mirror (signed-mirror discipline): [clear/extension/collision]

**F. Audit-loop discipline (v5-r7 meta).** If Red Team surfaces any new finding, it must either cite which of A1–A4 is wrong OR be independent of same-uid-peer preconditions. Expected: LOCK.

**G. Overall safety.** Expectation: LOCK. Three surgical additions, all lifting blueprint-level enumeration into architecture-level for defense-in-depth. Zero new scope anchors.

---

## Historical audit request text (v5 revision 6) — preserved for context

Re-audit this revision (v5-r6). Confirm:

**A. Preflight deployment-assumption block is ground truth (v5-r4/r5/r6).** Preflight A1 (v0.1 = single-client-per-Golden-Quill), A2 (operator dev env may run multi-client under trust), A3 (multi-client-on-shared-hardware = v2), A4 (operator is trusted) remain operator-confirmed. Red Team may not attack A1–A4 as findings; it may only attack whether v5-r6 architecture correctly delivers on A1–A4, or identify new in-scope architectural attacks independent of the scope question.

**B. v5-r6 surgical additions close the RT-v5-r5 Bucket B finding and correctly encode the operator's Bucket C scope decisions (1a, 2a).**
- RT-v5-r5 LOW wrapper-verification TOCTOU race → closed by M14.4.4 extension (read-only remount of `vault_shared/process_wrappers/` post-verify + Logician exec-time hash re-check)?
- RT-v5-r5 SCOPE Q1 (macOS sandbox primitive) → closed by v5-r6 macOS parallel-primitive clause binding every Linux-seccomp-deny clause to a `sandbox_init(2)` deny-profile parallel in M14.2.1 / M14.3.2 / M14.3.3 / M14.4.3?
- RT-v5-r5 SCOPE Q2 (lock-marker bootstrap circular dependency) → closed by v5-r6 N.4.2 extension (Logician trust-root mirror of M15 ledger at `~/.tilth/logician_trust_root/` — pre-PRE-gate accessible; operator-signed; hash-manifest committed)?

**C. Section O.4 A1+A4 drift-preempt clause correctly disqualifies RT-v5-r5 Bucket A findings as out-of-model at v0.1.** The six same-uid / capability-gated findings (readahead timing; mmap+msync flush timing; FUSE-ioctl; tracefs/ftrace; `/proc/<pid>/fd` re-open; `open_by_handle_at` reuse) all require either a malicious same-uid peer (ruled out by A1+A4) or a capability the operator does not grant to seats (mount / debugfs / `CAP_DAC_READ_SEARCH`). They are named as O.5.g–O.5.l v2 hardening targets. Red Team: verify future rounds attacking v0.1 via same-uid observability are mis-anchored under A1+A4 unless they cite which of A1/A4 is wrong.

**D. v5-r5, v5-r4, v5-r3, v5-r2, v5-r1, v4 lock text preserved verbatim.** v5-r6 additions EXTEND their parents (M14.4.4 extension under M14.4.4 v5-r5 parent; N.4.2 extension under N.4.2 v5-r5 parent; Section O.4 drift-preempt clause as addition to v5-r4 O.4 re-anchor; Section O.5 extension with O.5.g–O.5.l under the v5-r4 O.5 enumeration; macOS parallel-primitive clause added to each of M14.2.1 / M14.3.2 / M14.3.3 / M14.4.3 without altering Linux seccomp-deny text). No prior clause replaced or weakened.

**E. No new rule collision in v5-r6.**
- M14.4.4 extension (read-only remount + exec-time hash re-check) vs M14.4.4 parent (PRE-gate hash+signature verify): extension/collision?
- N.4.2 extension (trust-root mirror) vs N.4.2 parent (operator-signed marker + ledger-entry verification): extension/collision?
- Section O.4 drift-preempt clause vs Section O.4 v5-r4 re-anchor: extension/collision?
- Section O.5 O.5.g–O.5.l vs Section O.5 O.5.a–O.5.f (v5-r4): enumeration-widening/collision?
- macOS parallel-primitive clause vs parent M14.2.1 / M14.3.2 / M14.3.3 / M14.4.3 Linux-seccomp text: coexistence/collision?
- v5-r6 Logician trust-root mirror vs M15 signed-commit discipline: consistent?

**F. Audit-loop discipline (v5-r6 meta).** Red Team is explicitly asked: under the v5-r6 Section O.4 A1+A4 drift-preempt clause, same-uid-peer observability findings against v0.1 are mis-anchored. If Red Team surfaces a new finding this round it MUST either (i) cite which of A1/A4 it believes is wrong with a specific CLAUDE.md or operator-confirmation line contradicting it, or (ii) be independent of A1+A4 (e.g., an attack that works against a single-seat single-client single-operator deployment). Any finding meeting neither criterion is mis-anchored and not a valid v5-r6 residual. Red Team must classify any residual as (a) implementation-closable, (b) threat-model-anchored-needs-operator-input, or (c) scope-decision — and may not re-flag Bucket A attacks now named in O.5.g–O.5.l.

**G. Overall safety.** Expectation: LOCK if (i) the RT-v5-r5 Bucket B wrapper-TOCTOU is closed at the architectural layer, (ii) macOS and trust-root mirror scope decisions are correctly encoded, (iii) Section O.4 A1+A4 drift-preempt clause is present and correctly disqualifies Bucket A attacks at v0.1, (iv) no new in-scope attack surface is introduced by v5-r6's own additions, and (v) all prior lock text is preserved verbatim.

---

## Historical audit request text (v5 revision 5) — preserved for context

Re-audit this revision (v5-r5). Confirm:

**A. Preflight deployment-assumption block is ground truth (v5-r4/r5).** Preflight A1 (v0.1 = single-client-per-Golden-Quill), A2 (operator dev env may run multi-client under trust), A3 (multi-client-on-shared-hardware = v2), A4 (operator is trusted) remain operator-confirmed. Red Team may not attack A1–A4 as findings; it may only attack whether v5-r5 architecture correctly delivers on A1–A4, or identify new in-scope architectural attacks independent of the scope question.

**B. v5-r5 surgical additions close RT-v5-r4 architectural findings.**
- RT-v5-r4 MEDIUM alternative kernel-mediated copy primitives (tee/vmsplice/process_vm_readv/writev) → closed by M14.2.1 extension?
- RT-v5-r4 MEDIUM FD-passing of vault-derived descriptors via `sendmsg`/`SCM_RIGHTS` over abstract unix sockets → closed by new M14.3.3?
- RT-v5-r4 MEDIUM perf_event_open uprobe/kprobe attachment → closed by M14.3.2 extension?
- RT-v5-r4 MEDIUM wrapper-integrity subversion → closed by new M14.4.4 (wrapper is M15 signed-commit artifact + Logician verify)?
- RT-v5-r4 LOW circular Section-2 lock marker → closed by new N.4.2 (operator-signed marker + Logician verifies at PRE-gate)?
- RT-v5-r4 LOW memfd_create namespace alternative → closed by M14.4.3 tighten (v0.1 mandates seccomp-denial only; namespace path deferred to v2)?

**C. v5-r5 closures do not introduce new scope anchors.** v5-r5 adds zero new out-of-model anchors and zero new scope questions. All closures extend existing architectural patterns (M14's seccomp/LSM enforcement-envelope options; M15 signed-commit discipline applied to wrapper artifacts and lock markers). Verify no finding requires operator confirmation beyond A1–A4.

**D. v5-r4, v5-r3, v5-r2, v5-r1, v4 lock text preserved verbatim.** v5-r5 additions EXTEND their parents (M14.2.1 extension; M14.3.2 extension; M14.3.3 new under M14.3; M14.4.3 tighten — option (b) deferred to v2 but parent text preserved; M14.4.4 new under M14.4; N.4.2 new under N.4.1). No prior clause replaced or weakened.

**E. No new rule collision in v5-r5.**
- M14.2.1 extension (tee/vmsplice/process_vm_readv/writev) vs M14.2.1 parent (copy_file_range/sendfile/splice): widening/collision?
- M14.3.2 extension (perf_event_open) vs M14.3.2 parent (bpf): widening/collision?
- M14.3.3 (FD-passing prohibition) vs M14.3 parent (FD-passing named in (e) clause): widening/collision?
- M14.4.3 tighten (seccomp-only at v0.1) vs M14.4.3 parent (two-option menu): restriction/collision? Does option (b) remaining in the text but deferred to v2 create a contradiction?
- M14.4.4 (wrapper M15 signed-commit) vs M14.4.2 parent (wrapper exists): extension/collision?
- N.4.2 (operator-signed marker) vs N.4.1 parent (presence check): extension/collision?
- M14.4.4 vs M15 (signed-commit discipline applied to wrapper class): consistent?
- N.4.2 vs M15 / M14.4.4 pattern: consistent?

**F. Audit-loop discipline (v5-r5 meta).** Red Team is explicitly asked: if ANY finding this round is threat-model-anchored-needs-operator-input rather than implementation-closable, flag it as "SCOPE QUESTION — escalate to operator before any v5-r6 round." Do not dispatch v5-r6 autonomously on a scope question. Under v5-r5, all prior round findings have been either closed or re-anchored; the audit-loop discipline expects this round to either LOCK or surface a new scope question (not an implementation detail).

**G. Overall safety.** Expectation: LOCK if the six RT-v5-r4 findings are closed at the architectural layer, no new in-scope attack surface is introduced by v5-r5's own additions, and all prior lock text is preserved verbatim. If Red Team finds a new architectural attack surface introduced by v5-r5, flag it specifically with a classification as (a) implementation-closable, (b) threat-model-anchored-needs-operator-input, or (c) scope-decision.

---

## Historical audit request text (v5 revision 4) — preserved for context

Re-audit this revision (v5-r4). Confirm:

**A. Preflight deployment-assumption block is ground truth.** Preflight A1 (v0.1 = single-client-per-Golden-Quill), A2 (operator dev env may run multi-client under trust), A3 (multi-client-on-shared-hardware = v2), A4 (operator is trusted) are operator-confirmed. Red Team may not attack A1–A4 as findings; it may only attack whether v5-r4 architecture correctly delivers on A1–A4.

**B. v5-r4 surgical additions close RT-v5-r3 architectural findings.**
- RT-v5-r3 MEDIUM eBPF-direct-read → closed by M14.3.2 eBPF prohibition?
- RT-v5-r3 MEDIUM abort-signal race → closed by M14.4.2 process-creation-time suppression?
- RT-v5-r3 claimed fork-inherit regression → closed by M14.4.2 (wrapper-level limits inherited by forks)?
- RT-v5-r3 LOW POSIX shm leak → closed by M14.4.3 shm prohibition / per-seat namespace?
- RT-v5-r3 LOW copy_file_range timing → closed by M14.2.1 constant-time kernel-mediated copy?
- RT-v5-r3 claimed N.4 temporal-bridge regression → closed by N.4.1 (v0.1 does not operate during window)?
- RT-v5-r3 LOW io_uring DoS — acknowledged as feature-level and deferred (not architectural)?

**C. v5-r4 re-anchor of Section O.4 is correctly grounded in confirmed scope A1.** The O.4 re-anchor asserts that cross-org timing observability is not a v0.1 attack surface because v0.1 ships single-client-per-Golden-Quill. Does this re-anchor hold given A1? Is Section O.5's naming of v2 hardening requirements (constant-time padding, per-org process isolation, seat-to-seat IPC timing boundary, HSM keyring, seccomp-enforced eBPF/shm denial) sufficient to make A3 a boundary rather than a silent deferral?

**D. v5-r3, v5-r2, v5-r1, v4 lock text preserved verbatim.** v5-r4 additions EXTEND their parents (M14.2 → M14.2.1; M14.3 → M14.3.2; M14.4 → M14.4.2, M14.4.3; N.4 → N.4.1; Section O new O.4 re-anchor and O.5 addition). No prior clause replaced.

**E. No new rule collision in v5-r4.**
- M14.2.1 kernel-mediated-copy prohibition vs M14.2 response-shape homogenization: extension/collision?
- M14.3.2 eBPF prohibition vs M14.3 parent direct-FS prohibition: widening/collision?
- M14.4.2 process-creation-time suppression vs M14.4.1 seat-start suppression: defense-in-depth / collision?
- M14.4.3 shm prohibition vs M14.4 Vault-only-persistence: extension/collision?
- N.4.1 operation-gate vs N.4 provisional-scope: replaces or extends?
- Section O.5 vs A3 preflight: consistent scope boundary?

**F. Audit-loop discipline (v5-r4 meta).** Red Team is explicitly asked: if ANY finding this round is threat-model-anchored-needs-operator-input rather than implementation-closable, flag it as "SCOPE QUESTION — escalate to operator before any v5-r5 round." Do not dispatch v5-r5 autonomously on a scope question.

**G. Overall safety.** Expectation: LOCK if the five RT-v5-r3 findings are closed at the architectural layer, the N.4.1 operation-gate holds, O.4 re-anchor is grounded in A1, and O.5 is a scope-naming (not scope expansion in v0.1). If Red Team finds a new architectural attack surface introduced by v5-r4, flag it specifically.

If findings are implementation-layer (already routed to blueprint via BT1–BT14), acknowledge delegation — do not re-flag as architectural. If an O rejection is mis-anchored given A1–A4, name which assumption is wrong; absent that, the rejection stands.

---

## Historical audit request text (v5 revision 3) — preserved for context

Re-audit this revision (v5-r2). Confirm:

1. **v5-r2 surgical additions close RT-v5 in-scope HIGH and MEDIUM findings at the architectural layer.**
   - RT-v5 HIGH-1 gate-bypass TOCTOU → closed by M14.1 atomic gate-and-open?
   - RT-v5 HIGH-2 metadata-leak side-channel → closed by M14.2 cross-org metadata homogenization?
   - RT-v5 HIGH-3 APFS clones/reflinks → closed by BT14(g) volume-UUID + FS-file-ID binding?
   - RT-v5 MEDIUM direct-FS-via-helper → closed by M14.3 direct-FS primitive prohibition?
   - RT-v5 MEDIUM TOCTOU → closed by M14.1 (same atomic primitive)?
   - RT-v5 MEDIUM crash-handler bypass → closed by M14.4 + Autonomy Rule 1 v5-r2 hardening?
   - RT-v5 MEDIUM seed-vs-cache scope gap → closed by M15.1?
   - RT-v5 LOW commit-race → closed by M15.2 read-only freeze after verify?
   - RT-v5 LOW policy-file social-engineering → closed by M15.3 HIGH-severity ledger entry on Cedar change?
   - RT-v5 LOW missing degradation_log in N.2 → closed by N.2 v5-r2 surface addition?
   - RT-v5 LOW temporal hole → closed by N.4 temporal bridge?
   - RT-v5 LOW inconsistent seed definition → closed by M15.1 path-keyed partition?

2. **v5-r2 out-of-model rejections are correctly anchored to the trusted-operator v0.1 threat-model.**
   - Section O.1 rejection of HIGH-4 trust-centralisation — is the "v4 was not dispersed either" argument defensible?
   - Section O.2 rejection of MEDIUM keyring-compromise — is compromised-keyring correctly out-of-scope for v0.1, with BT4 HSM as the future path?
   - Section O.3 rejection of LOW snapshot-mount — is admin-privileged snapshot creation correctly below the v0.1 threat floor?

3. **v5-r1 amendments (M14, M15, N, BT14) remain coherent after v5-r2 hardening.** The v5-r2 sub-amendments (M14.1–M14.4, M15.1–M15.3, BT14(g), N.2 addition, N.4) EXTEND their parents without replacing any v5-r1 text. Verify no overwrite regression.

4. **No new rule collision introduced by v5-r2.** In particular:
   - M14.4 (crash-handler-through-Vault) vs Autonomy Rule 1 (save-state-always) — does the "exit-without-writing-if-Vault-unreachable" clause collide with the "persist on failure" rule, or does it properly subordinate Rule 1 to M14's single-persistence-path discipline?
   - M15.2 (read-only freeze) vs S5 — does freezing `router.yaml` at verify-time break any runtime path that expected to re-read `router.yaml`?
   - M15.3 (HIGH-severity ledger on Cedar change) vs S2 (admin-risk ledger) — is the re-type confirmation orthogonal to S2's flood-control, or does it collide?
   - BT14(g) volume-UUID binding vs BT2 (canonical path + inode) — is the identity tuple an extension or a replacement?
   - M14.3 (direct-FS prohibition) vs M14 (Logician PRE-gate scan) — is M14.3 a widening of M14's scan or a new enforcement layer?

5. **Prior amendments (M1–M13, S1–S11, v5-r1 M14/M15/N/BT14) remain coherent.** No regression introduced by v5-r2 additions. Specifically: the v4 lock text is preserved verbatim, and v5-r1 text is preserved verbatim except where v5-r2 adds explicit sub-amendments. v5-r2 additions only EXTEND, never replace, prior clauses.

6. **Overall safety — does the architecture pass at the architectural layer with v5 revision 2?** This is a single-round audit because v5-r2 is additive and surgical; the expectation is PASS with LOCK if the RT-v5 in-scope findings are all closed and the out-of-model rejections in Section O are correctly anchored.

If you still find blocking issues at the architectural layer (not implementation), flag them specifically. If your remaining findings are implementation-layer that BT1–BT14 already route to blueprint, acknowledge that delegation is correct — do not re-flag as architectural. If you believe an out-of-model rejection in Section O is incorrectly anchored (i.e., the rejected finding actually IS in v0.1 scope), name the specific threat-model boundary line you believe it crosses.

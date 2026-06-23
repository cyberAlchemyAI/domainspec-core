# Findings: Ternary-Weight LLM Inference on Pre-AVX2 / No-SIMD x86 (Batch-1 Decode)

**Dispatch:** `2026-06-22-ternary-llm-old-cpu` · type `research` · build/deploy decision
**Final approver:** parent (accepted; P9 citation check + P8 trust-but-verify applied)
**Exit:** `resolved` · collected returns: [research.md](research.md)

> **Approver caveat (claim ≤ proof).** The recent arXiv IDs surfaced by the precedent gate — FairyFuse (2604.20913), Litespark (2605.06485), T-SAR (2511.13676), TENET (2509.13765), TerEffic (2502.16473) — and ggml PRs #21636/#22836 are **not yet verified on disk** and must be confirmed before any publication. The decision below does **not** depend on them: path (d) is owned by Microsoft's well-established `I2_S` kernel alone, and the decisive non-vacuity negative rests on verified sources (bitnet.cpp's AVX2/AVX-512 requirement; the disqualified 260K-param Pentium-II demo; the formal cost model).

## Scope correction

The question splits on a hidden variable the request never named: **what counts as "usable."** Once forced, the dispatch resolves into two verdicts. The implicitly-interactive "conditional GO" does not survive non-vacuity scrutiny; it survives only under a batch/offline redefinition with a stated throughput floor. Both branches are below.

A second correction runs through the matrix: under research-type law, **being OWNED is never a KILL.** Every prior "KILL on ownership" verdict is rewritten as build-from-owned or already-deployed-elsewhere. The only force that can KILL here is non-vacuity (no witness), and it lands on the **interactive use-case**, not on any individual kernel.

## Corrected verdict matrix

| Candidate | Owner + citation | Witnessed on pre-AVX2 no-SIMD x86? | Sound? | Verdict | Use-mode |
|---|---|---|---|---|---|
| (a) bitnet.cpp TL1/TL2 LUT | Microsoft (arXiv 2410.16144; github.com/microsoft/BitNet) | No — speedup *is* the SIMD byte-shuffle (`pshufb`/`tbl`); hard-requires AVX2/AVX-512 | Yes, on SIMD | **Build-from-owned, wrong-tool for no-SIMD** (not killed) | Already deployed on SIMD; mechanism absent pre-AVX2 |
| (b) T-MAC LUT | Microsoft (arXiv 2407.00088) | No — wins ARE `tbl`/`pshuf` table lookups | Yes, on SIMD | **Build-from-owned, wrong-tool for no-SIMD** (not killed) | Already deployed on SIMD; inapplicable |
| (c) ggml TQ2_0 scalar reference | ggml-org / compilade, PR #8151; scalar `#else` path owned | **Partial** — correctness owned; throughput witnessed only on ARM **NEON** (Cortex-A72 15.78 GB/s; AWS t4g 44.80 GB/s) = still SIMD. Pre-AVX2 *scalar x86* tok/s **unwitnessed** | Yes (cost-model only) | **Build-from-owned**; gap = scalar-x86 throughput witness only | Batch/offline |
| (d) direct add/sub/skip, packed 2-bit ternary, NO LUT | **Microsoft I2_S** kernel in bitnet.cpp (arXiv 2410.16144) — exactly this design; *also* FairyFuse / T-SAR (unverified) | No — I2_S benchmarked AVX2/NEON only | Yes (cost-model only) | **Build-from-owned** (was mislabeled "novel") | Batch/offline |
| Interactive use-case (several tok/s on pre-AVX2) | — | **No real instance at usable scale** | Estimate says no | **KILL — no-witness negative** | n/a |

### Relabel notes

- **(d) is not novel.** The exact design — 2-bit packed ternary unpacked to {−1,0,+1} with masked add/subtract, zero multiplications, zero LUT — is Microsoft's own **I2_S** kernel (verified design; FairyFuse/T-SAR corroborate but are unverified). The only genuinely-clean residue is a no-SIMD pre-AVX2 **scalar** port of an owned design, witnessed for performance — a **portability gap**, not an invention. Any build cites I2_S and claims only "ported down to scalar," never "new kernel."
- **(c) gap was over-stated.** TQ2_0's real non-AVX2 numbers are on **ARM NEON** (still SIMD). ggml's generic `#else` scalar C path exists and is owned. The single unwitnessed quantity is a **pre-AVX2 scalar-x86 throughput number.**
- **(a)/(b) are not killed.** Ownership ≠ KILL. They are correct, deployed kernels whose *speedup mechanism is the SIMD shuffle itself*; on a no-SIMD target the mechanism is simply absent → **wrong-tool**, not wrong-design.

## The decisive non-vacuity hit

**No real witness exists for a usable-scale ternary LLM on genuinely pre-AVX2 / no-SIMD silicon.**

- The famous **"Windows 98 / Pentium II 350 MHz / 35.9 tok/s"** result (EXO Labs; *Tom's Hardware*) is **disqualified** — a ~260K-parameter Llama2.c TinyStories toy on a float engine, ~4 orders of magnitude below BitNet 2B4T, not a ternary kernel at scale. Must not be cited as if it witnesses the target claim.
- **microsoft/BitNet hard-requires AVX2/AVX-512** (Haswell+/Ryzen+); does not target pre-AVX2.
- **catid/bitnet_cpu** shows a scalar-vs-AVX2 ~2× penalty, but on a *modern* core — an optimistic anchor only.

### Cost-model estimate (projection, NOT measurement)

BitNet 2B4T at ~1.6 bit/weight → ~**0.4 GB weights read per token** (batch-1 decode is memory-bound). A pre-AVX2 x86 part (~2009–2012) delivers ~**2–4 GB/s** usable single-thread bandwidth → a **memory ceiling of ~5–10 tok/s**. Without SIMD the core is **compute-bound**, so reality lands well under that ceiling:

- Path (c) scalar reference: **~0.2–1 tok/s** (projected)
- Path (d) scalar add/sub/skip: **~0.5–2 tok/s** best case (projected)

Seconds per token = **batch-only, not interactive.** The draft's ~2–4× projection does not survive intact: its SIMD-lane term has no lanes to spend on a no-SIMD core and must be dropped; what remains is the smaller scalar-only multiply-free edge.

### Typed negative (banked)

**Contribution it would have made:** a "runs anywhere, no SIMD required, interactive local decode" deployment story. **The fact that zeroes it:** at usable scale on a 2–4 GB/s pre-AVX2 compute-bound core, decode is ~0.2–2 tok/s (seconds/token), batch-only, with no citable real instance. Reusable: this negative pre-empts any future "ternary makes old hardware interactive" proposal.

## Decision — two branches keyed to "usable"

### Branch (i): INTERACTIVE bar (several tok/s) → **NO-GO**
No-witness negative. No real instance at usable scale on pre-AVX2 silicon; the cost model puts the ceiling far below interactive even in the best multiply-free case. **Do not stand this up.** Ship the typed negative as the deliverable.

### Branch (ii): BATCH / OFFLINE bar (tolerate seconds/token) → **conditional GO, build-from-owned**
Contingent on accepting a **stated floor of ~1–2 tok/s best case (projected, batch-only)** and on closing the witness with a real measurement. Build-from-owned, not net-new: every kernel has an owner; the only missing artifact is a pre-AVX2 scalar-x86 throughput number. Falls back to Branch (i) if interactivity is required.

## Build obligations (Branch (ii) only)

1. **Pin a named pre-AVX2 CPU** as the measurement target (e.g. a specific Core 2 / early Nehalem / pre-Haswell part) and record its *measured* single-thread memory bandwidth — replace the ~2–4 GB/s assumption with a real number.
2. **Build path (c) baseline by reusing the owned scalar path** — ggml generic `#else` C path / TQ2_0 (PR #8151); watch PRs #21636/#22836 (unverified) in case they land the scalar witness first. Compile and measure, do not re-author.
3. **Build path (d) by porting an owned design down to scalar** — take Microsoft's **I2_S** masked add/subtract and strip the SIMD intrinsics to a portable scalar loop. Cite I2_S; claim only "scalar port."
4. **Measure tok/s of (c) and (d) against an int8 scalar MAC baseline on the pinned CPU.** This measured number is the proof gate. Until it exists, the ~2–4× and ~0.2–2 tok/s figures remain cost-model projections only.

## Bottom line (one-line answer to the goal)

**No-go for interactive ternary LLM on pre-AVX2 / no-SIMD CPUs (no-witness negative — banked).** For batch/offline use it is a conditional, *build-from-owned* GO (port Microsoft's `I2_S` add/sub/skip and ggml's TQ2_0 scalar path down — nothing novel to invent), gated on one proof: a measured ~1–2 tok/s on a named pre-AVX2 CPU. The headline SIMD-LUT speedups (bitnet.cpp, T-MAC) are SIMD-bound and do not transfer.

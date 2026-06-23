# research.md — collected returns (verbatim)

**Dispatch:** `2026-06-22-ternary-llm-old-cpu` · type `research` · build/deploy decision
**Goal:** Decide whether to stand up ternary-weight LLM inference on genuinely old (pre-AVX2 / no-SIMD) CPUs for a concrete local-inference use, naming build obligations a GO would incur.
**Anti-bias (global):** owned-and-portable-down optimism vs no-SIMD-vacuity skepticism.

> Collected agent returns are reproduced verbatim below. Synthesis (with claim≤proof discipline) is in [findings.md](findings.md). Citation-verification caveat: the recent arXiv IDs in the precedent return (FairyFuse 2604.20913, Litespark 2605.06485, T-SAR 2511.13676, TENET 2509.13765, TerEffic 2502.16473) and ggml PRs #21636/#22836 are **not yet verified** and must be checked before any publication; the decision does not rest on them.

---

## Group: explorers

### Explorer A — Xiao, Guangxuan (modern ternary-LLM CPU runtimes, empirical)

Bottom-line: Every published tok/s in the modern ternary-LLM corpus was produced on a SIMD machine (AVX2/AVX512 on x86, or NEON on ARM); core kernels are written around a SIMD byte-shuffle instruction (`_mm256_shuffle_epi8` on x86, `vqtbl1q_u8`/`tbl` on ARM). Found **zero** published benchmark on a genuinely pre-AVX2 / scalar x86 CPU. Speedup claims (2.4×–6.2× x86, 4×–5× T-MAC) are all SIMD-relative. A scalar reference path exists in llama.cpp/ggml (so it will *run*), but no one has measured it and it forfeits the LUT advantage.

Candidates:
1. **Microsoft bitnet.cpp (TL1/TL2 LUT kernels)** — benchmarks on Apple M2 Ultra (NEON) + Intel i7-13700H (AVX2). SIMD required+explicit (TL1=NEON `vqtbl1q_u8`, TL2=AVX2 `_mm256_shuffle_epi8`). No scalar fallback in LUT kernels; the only cross-platform path is I2_S (plain 2-bit, "compatible all platforms") which is the *un-accelerated baseline* LUT beats — no pre-AVX2 number. Refs: github.com/microsoft/BitNet; arxiv.org/html/2502.11880v1; aclanthology.org/2025.acl-long.457.pdf; arxiv.org/pdf/2410.16144.
2. **T-MAC** — benchmarks on Surface Laptop 7, M2 Ultra, Jetson Orin, RPi 5, Surface Book 3 (all NEON/AVX2). Uses `tbl`/`pshuf` shuffle. README warns it "cannot guarantee significant speedup on all x86 platforms," singling out older x86 as a weak spot. Refs: github.com/microsoft/T-MAC; arxiv.org/abs/2407.00088.
3. **llama.cpp/ggml ternary TQ1_0 (1.69 bpw) / TQ2_0 (2.06 bpw)** — owner ggml-org (PR #8151 by compilade). Benchmarks: Core m3-8100Y (AVX2), Cortex-A72/A53 (NEON), AWS t4g, RPi4. Ships a scalar C reference path → will functionally run on pre-AVX2 x86, but no pre-AVX2 tok/s published. Most portable of the corpus. Ref: github.com/ggml-org/llama.cpp/pull/8151.
4. **BitNet b1.58 2B4T (model)** — runs via bitnet.cpp; ~4 tok/s "standard CPU"; HF-transformers gives no speed benefit (gains live in SIMD kernels). Refs: huggingface.co/microsoft/bitnet-b1.58-2B-4T; arxiv.org/abs/2504.12285.

Practical read: useful (human-reading-speed) ternary inference on pre-AVX2 x86 is unproven and architecturally unlikely (the speedup mechanism is a SIMD byte-shuffle LUT). Only viable "it at least runs" path is llama.cpp TQ1_0/TQ2_0 via scalar reference (un-accelerated, memory-bound; measure yourself). bitnet.cpp's I2_S is all-platform but is the baseline, not the LUT win.

### Explorer B — Nyquist, Harry (historical multiply-free arithmetic + formal scalar cost model)

Lineage: balanced ternary {−1,0,+1} (Colson 1726; Fowler 1840; Setun 1958 — 18-trit balanced ternary in hardware; Knuth's "prettiest number system"); Canonical Signed Digit (CSD) multiplierless FIR/DSP (shift-and-add, {0,+1,−1} recoding minimizing adders); integer-only/fixed-point inference (Jacob et al. 2017 arXiv 1712.05877; ARM CMSIS-NN arXiv 1801.06601 — power-of-two shift rescaling for FPU-less MCUs); ternary weight networks TWN (Li & Liu 2016, arXiv 1605.04711 — products of {−1,0,+1} = conditional add/subtract/bypass; FP mul ~1.31 pJ vs add ~0.38 pJ); LUT-NN (2302.03213), LUT Tensor Core (2408.06003), T-MAC (2407.00088).

Formal scalar cost model (dot product length K, scalar in-order pre-AVX2 core):
- int8 MAC baseline: ~2 loads + ~3 ALU cycles (old IMUL multi-cycle, sometimes non-pipelined).
- ternary direct add/sub/skip: ~2 loads + ~1 ALU cycle, multiplier never touched; zeros (30–50% of TWN weights) skip accumulate entirely.
- ternary LUT: amortizes compute across group g, BUT each lookup = data-dependent memory access.

Decomposition of the advantage:
- **ALU term** — survives no-SIMD, relatively *larger* on old cores (their multiply was slow/non-pipelined).
- **Memory-bandwidth term** — survives no-SIMD; ternary weights ~1.6 bits vs 8 bits = ~5× less weight traffic; batch-1 LLM decode (GEMV) is memory-bound → biggest lever on a weak core.
- **SIMD-lane-parallelism term** — does NOT survive. T-MAC's big wins ARE the in-register SIMD shuffle (`pshufb`/`tbl`, 16–32 lookups/instr); on no-SIMD each LUT entry = scalar data-dependent load, which can be *slower* than the add it replaced.

Verdict: advantage partly survives but you must change technique — prefer **direct ternary add/sub/skip with packed weights + fixed-point (power-of-two-shift) activations**, NOT LUT/bit-serial. Expect modest ~2–4× over int8 MAC (bandwidth + multiply-elimination), gated by load throughput/cache, not vector unit. The spectacular published CPU numbers are SIMD-bound and should be discounted.

---

## Group: reviewers

### Skeptic — Tetlock, Philip (precedent / ownership-attribution gate)

Reminder applied: owned ≠ kill. SIMD-only benchmarks = build-from-owned with a portability gap.

- **(a) bitnet.cpp TL1/TL2** — ownership confirmed; LUT wins are SIMD byte-shuffle; published numbers AVX2/NEON-only; no scalar TL1/TL2 number. SIMD-confined, not a space-kill. Note: the same repo *also* owns I2_S, a non-LUT add/subtract kernel (see (d)).
- **(b) T-MAC** — confirmed SIMD-confined; gain is literally `tbl`/`pshuf`; no scalar number.
- **(c) ggml TQ2_0** — ownership correct and sharpened: author **compilade**, motivated by Eddie-Wang1120 (PR #8151). Correction to the draft hedge: TQ2_0 has **witnessed non-AVX2 numbers — but on ARM NEON** (Cortex-A72 15.78 GB/s; AWS t4g 44.80 GB/s), which is still SIMD; ggml's `#else` generic scalar C path is owned. What is unwitnessed is specifically a **pre-AVX2 scalar-x86 throughput number**.
- **(d) direct add/sub/skip, NO LUT** — **MISLABEL. Not novel — already owned in ≥4 places, all SIMD-benchmarked:** (1) **Microsoft's own I2_S kernel** in bitnet.cpp = exactly this design (2-bit packed ternary → masked add/subtract, no LUT) — DeepWiki bitnet I2_S; arXiv 2410.16144; AVX2+NEON paths only; (2) **FairyFuse** (Zuo et al., arXiv 2604.20913) = "masked addition/subtraction on packed 2-bit weights, zero multiplications and zero lookup-table overhead" — but requires AVX-512F + BMI2, "no scalar fallback"; (3) **T-SAR** (arXiv 2511.13676) = multiplication-free ternary but hardware co-design (ISA extension + SIMD ALU modification). Older lineage (TWN, Jacob, CMSIS-NN, CSD/Setun) is correctly clean. **Corrected label: build-from-owned.** The genuinely-clean residue is narrow: a no-SIMD pre-AVX2 *scalar* build of the add/sub/skip kernel, witnessed for performance — a portability gap on an owned design, not a new invention. No verdict flips to KILL.
- Missed owners to cite: FairyFuse, T-SAR, TerEffic FPGA (2502.16473), TENET edge LUT (2509.13765), Litespark "Custom SIMD Kernels for Ternary NNs on Consumer CPUs" (2605.06485), ggml generic/scalar ternary PRs #21636 and #22836 (active work encroaching the scalar zone).

### Skeptic — Popper, Karl (non-vacuity / witness gate)

**Verdict: NO-WITNESS NEGATIVE (with a stated floor that fails "usable"-interactive).**

Witness search:
1. **EXO Labs Pentium II 350 MHz / Win98 → "35.9 tok/s"** — looks like a witness, is not one. Model was **~260K parameters** (Llama2.c TinyStories toy), ~4 orders of magnitude below BitNet 2B4T, on a custom float engine, not a ternary kernel at scale. **Disqualified.** (tomshardware.com; levysoft.medium.com; EXO press.)
2. **microsoft/BitNet** hard-requires AVX2/AVX-512 (Haswell+/Ryzen+); does not target pre-AVX2 at all. (github.com/microsoft/BitNet; arXiv 2410.16144, 2502.11880.)
3. **catid/bitnet_cpu** — explicit scalar-vs-AVX2 split: ~28 tok/s AVX2 vs ~15 tok/s scalar, but on a *modern* core (Ryzen 9 7950X / i9-12900K) — optimistic anchor only, not a pre-AVX2 witness.

No run of BitNet b1.58 2B4T (or any billions-param ternary transformer) on a Core 2 / early Atom / P4 / pre-2013 x86 / scalar embedded core was found. Closed negative.

Hand estimate: BitNet 2B4T ternary ~1.6 bit → ~0.4 GB weight bytes/token (batch-1 decode memory-bound). Pre-AVX2 ~2009–2012 x86 usable single-thread bandwidth ≈ 2–4 GB/s → pure memory ceiling ~5–10 tok/s — *unreachable* because the no-SIMD core is compute-bound on the ternary GEMV. Realistic: **path (c) scalar ~0.2–1 tok/s; path (d) direct add/sub ~0.5–2 tok/s best case.** Seconds per token = batch-only, not interactive.

Typed negative: what (c)/(d) would contribute = a "runs anywhere, no SIMD required, interactive" deployment story; the fact that zeroes it = at usable scale on a 2–4 GB/s pre-AVX2 compute-bound core, decode is ~0.2–2 tok/s (seconds/token), batch-only, no citable instance; the ~2–4× projection's SIMD-lane term does not survive. Survives ONLY if "usable" is redefined as batch/offline with a stated ~1–2 tok/s floor.

---

## Synthesis passes

- **Draft** (writer Shannon, Claude): conditional GO on (c)+(d), KILL (a)+(b), ~2–4× cost-model projection.
- **Revision** (zig-zag loop 1, after skeptic challenges): relabel (d) build-from-owned (Microsoft I2_S + FairyFuse), narrow (c) gap to scalar-x86-only, reframe (a)/(b) as already-deployed-on-SIMD / wrong-tool (owned ≠ KILL), split verdict by interactive vs batch. See [findings.md](findings.md).

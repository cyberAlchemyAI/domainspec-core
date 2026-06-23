# Acquiring GPUs for Local LLMs in Brazil (2026)

> Deep-research synthesis. Buy-vs-cloud, VRAM sizing, import-tax reality, per-tier picks.
> **Claim ≤ proof:** verified items are marked ✓ (adversarial 2/3 or 3/3 vote). Specific BRL
> retail prices did **not** survive verification — treat them as *check-live*, not fact.

## TL;DR

The technical sizing rules and the Brazilian import-tax change are verified. Almost every
specific consumer-GPU retail price (R$ for 4090/5090, etc.) was **killed** in verification —
those come from 2026 blog/affiliate pages and couldn't be corroborated. Cloud prices below are
vendor-published rates.

---

## 1. VRAM needed (verified 3-0)

**~2 GB VRAM per 1B params at FP16; halve at Q8; quarter at Q4.**

Example: 70B at FP16 ≈ 140 GB (impossible at home); at Q4_K_M ≈ 35–48 GB (doable).

| Model class | Quant | VRAM | Card that fits |
|---|---|---|---|
| 7–9B (Llama 3.1 8B) | Q4_K_M | ~6 GB | RTX 3060 12GB |
| 13B | Q4/Q8 | ~12–16 GB | RTX 3060 12GB / 4070 |
| 32B (DeepSeek-R1-distill) | Q4_K_M | ~22 GB | RTX 3090/4090 24GB |
| 70B (Llama 3.3) | Q4_K_M | **48 GB+** | 2× 3090/4090, A6000 |
| 100B+ | Q4 | 64 GB+ | Multi-GPU / workstation |

**Killed (0-3):** "70B at Q8 fits in 48 GB / dual 4090s." 70B at Q8 needs ~70+ GB. Dual-24GB
realistically caps at **70B at Q4**, not Q8.

---

## 2. Buying in Brazil — tax reality (verified) + price caveat

**Verified ✓:** **Resolução GECEX nº 852/2026** raised the import tax (II) on CPUs, GPUs, RAM,
motherboards, **effective ~Feb 5, 2026**. Imported GPU prices rose in 2026; self-importing via
AliExpress now carries more tax risk.

**Killed:** the specific pass-through claims ("+R$1,000–2,000 per piece") and specific retail
prices ("RTX 5090 = R$20,000 at Pichau") were refuted 0-3 — unsourceable, not necessarily wrong.

Structural guidance:
- **New:** Kabum, Pichau, Terabyte, Mercado Livre (official stores). Compare on Zoom/Buscapé.
- **Best value:** **used RTX 3090 (24 GB)** on Mercado Livre/OLX — 24 GB is what matters for
  models; gaming-gen speed is secondary.
- **Avoid:** importing a single high-end GPU from AliExpress post-Feb-2026 (tax + seizure risk).

---

## 3. Cloud GPU (verified vendor rates)

- **Rollin Host** (São Paulo DC) ✓ — dedicated RTX PRO 6000 etc., BRL-billed, local latency.
- **H200 ≈ R$25.83/hour** ✓ (BRL Brazilian provider).
- **GPUBrasil** ✓ — Brazil-accessible rental.
- **RunPod vs Vast.ai:** **H100 PCIe (80GB) cheaper on RunPod ~$1.99/hr** ✓. The "Vast.ai always
  far cheaper" claim was **killed** — gap is GPU-specific. Check per-card.
- Global (RunPod/Vast.ai/Lambda) bill USD — add ~6.38% IOF + FX exposure.

---

## 4. Buy-vs-cloud break-even (directional; economics not strongly verified)

- **Cloud wins:** bursty/experimental use, need a card you can't buy (H100/H200), under ~2–4 h/day.
- **Buying wins:** daily sustained use. Rough rule: a card pays off vs cloud at ~1,000–2,000
  GPU-hours. A used 3090 (~R$5–7k) breaks even in a few months of daily use.

---

## Recommendation by tier

1. **Experimenting / ≤13B / unsure:** start on **cloud** (RunPod or BRL provider like Rollin Host);
   or a **used RTX 3060 12GB** for cheap always-on small models.
2. **Serious local, best value:** **used RTX 3090 24GB** (Mercado Livre/OLX) — best Brazil buy for
   32B-class.
3. **70B at home:** **2× used RTX 3090** (48 GB total).
4. **100B+ / fine-tuning:** **rent H100/H200** in the cloud; owning rarely pencils out in Brazil.

---

## Caveats

- No verified consumer-GPU BRL retail price survived; verify live on Kabum/Pichau/Mercado Livre.
- Cloud pricing is vendor-published, USD providers carry FX/IOF.
- Import-tax pass-through magnitude unverified beyond "prices rose."

## Sources (selected)
- VRAM sizing: overchat.ai/ai-hub/llm-hardware-requirements; spheron.network; localllm.in
- Import tax: adrenaline.com.br; hardware.com.br (GECEX 852/2026)
- Cloud BR: gpubrasil.com.br; rollinhost.com.br; computeprices.com/compare/runpod-vs-vast
- Break-even: thundercompute.com; spheron.network/blog/renting-gpus

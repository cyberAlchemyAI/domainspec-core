# Acquiring GPUs for Local LLMs in Brazil (2026)

> Deep-research synthesis. Buy-vs-cloud, VRAM sizing, import-tax reality, per-tier picks.
> **Claim ≤ proof:** the original verified items are marked ✓. The retail table is a
> **27 July 2026 live snapshot**, not a durable price claim; recheck price, stock, seller,
> freight, and the final cart before paying.

## TL;DR

**If 70B is the requirement, do not stop at two RTX 5060 Ti 16GB cards.** They make
sense for a new, CUDA-friendly 30–35B machine, but 32GB aggregate VRAM is below the
practical floor for a fully GPU-resident 70B Q4 model. Target **48GB aggregate VRAM plus
128GB host RAM** for 70B Q4 at moderate context; target **80–96GB VRAM** if the intended
use genuinely includes very long context.

The value-first 48GB route is **two locally tested used RTX 3090 24GB cards around
R$5k–6k each**. The checked all-new alternative is **three true-2-slot RTX 5060 Ti
16GB cards for about R$11.4k–11.7k**, but this has a much harder motherboard, slot,
and airflow requirement. `llama.cpp` can shard across either configuration; the result
is multiple VRAM pools connected through the system interconnect, not one transparent
GPU.

The best listed price among the major-retailer pages checked is **R$7,599.98 via Pix**
for two compact PNY cards at Pichau, subject to cart quantity. The best such offer with
explicit pair stock is **R$7,799.98 via Pix** for two 2-slot MSI Ventus cards at
Terabyte. GK lists the same 2-slot PNY at **R$7,198.00/pair**, but its current Reclame
Aqui evidence makes a R$7.2k Pix exposure hard to justify merely to save about R$402
versus KaBuM/Pichau.

---

## 0. 2× RTX 5060 Ti 16GB decision — live update 2026-07-27

### What the pair actually buys

- **32GB aggregate VRAM only in a multi-GPU-aware runtime.** `llama.cpp` supports
  layer splitting by default; its newer tensor-parallel mode is explicitly experimental.
- **Good target:** Qwen3-32B at Q4_K_M (**19.8GB weights**) through Q6_K
  (**26.9GB weights**), with the usable context limited by the remaining VRAM for KV
  cache and runtime buffers.
- **Bad target:** Llama 3.3 70B Q4_K_M is **42.52GB before KV cache and runtime
  overhead**. Even Q3_K_S is 30.91GB and is labeled low quality, leaving almost no
  practical headroom in 32GB.
- **No NVLink:** NVIDIA lists NVLink support as “No.” Inter-card traffic uses the
  motherboard PCIe topology; generation speed will not simply double.
- **Board facts per card:** 16GB GDDR7, 448GB/s memory bandwidth, PCIe 5.0 **x8**,
  and 180W total graphics power.

Sources: [llama.cpp multi-GPU guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md),
[NVIDIA RTX 5060 family specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5060-family/),
[Qwen3-32B GGUF sizes](https://huggingface.co/Qwen/Qwen3-32B-GGUF),
[Llama 3.3 70B GGUF sizes](https://huggingface.co/bartowski/Llama-3.3-70B-Instruct-GGUF).

### Live Brazilian offers

Prices below were read from the linked product pages on **2026-07-27**. “Pair” is
arithmetic before freight; it is not a bundle quote.

| Offer | Cash / card | Cash / pair | Installment / card | Dual-GPU fit and availability |
|---|---:|---:|---:|---|
| [PNY Dual Fan OC — GK Infostore](https://www.gkinfostore.com.br/placa-de-video-pny-geforce-rtx-5060-ti-dual-fan-oc-16gb-gddr7-vcg5060t16dfxpb1-o) | R$3,599.00 Pix | **R$7,198.00** | R$4,234.12 listed | 2-slot, 245×120×39.9mm; page said 10 units |
| [PNY Dual OC — Pichau](https://www.pichau.com.br/placa-de-video-pny-geforce-rtx-5060-ti-dual-oc-16gb-gddr7-128-bit-vcg5060t16dfxpb1-o-nac) | R$3,799.99 Pix | **R$7,599.98** | R$4,470.58 in 12× | 2-slot, 245×120×39.9mm; page did not expose quantity |
| [ASUS Dual OC — KaBuM](https://www.kabum.com.br/produto/730378/placa-de-video-asus-dual-rtx-5060-ti-o16g-nvidia-geforce-16gb-gddr7-2602mhz-128-bits-opengl4-6-dlss-4-ray-tracing-90yv0mh0-m0na00) | R$3,799.99 Pix | **R$7,599.98** | R$4,222.21 in 10× | **2.5-slot**, 229×120×50mm; in stock |
| [MSI Ventus 2X OC Black Plus — Terabyte](https://www.terabyteshop.com.br/produto/39095/placa-de-video-msi-nvidia-geforce-rtx-5060-ti-ventus-2x-oc-black-plus-16gb-gddr7-dlss-ray-tracing) | R$3,899.99 Pix | **R$7,799.98** | R$4,588.22 in 12× | 2-slot, 227×126×41mm; page said 4 units |

**Buying call (local inference):**

1. Try the compact PNY at Pichau first and confirm that the cart accepts quantity two.
2. If not, the MSI Ventus at Terabyte is the cleanest offer with explicitly visible pair
   stock and a true 2-slot cooler.
3. Use the KaBuM ASUS only after measuring slot spacing: 2.5 slots per card can choke
   the upper card or physically block the second installation.
4. GK is the price floor, not the default recommendation. Reclame Aqui classified it
   “Ruim” for Jan–Jun 2026 (5.3/10, 38-day average response time). Saving ~R$402 per
   pair does not compensate for that support signal when payment is by Pix.

Seller-risk source:
[GK Infostore at Reclame Aqui](https://www.reclameaqui.com.br/empresa/gk-infostore/).

### Hard pre-purchase gate

Do not buy the pair until all five answers are known:

1. **Motherboard:** two x16-length physical slots, their electrical wiring documented,
   and enough spacing for two specific coolers. Prefer CPU-connected x8/x8; a chipset
   x4 second slot can work but is a performance risk that must be tested.
2. **Case:** measured card clearance plus at least one empty-slot-width air path where
   the upper card takes air.
3. **PSU:** the two GPUs alone are 360W. Size the full system from the actual CPU and
   PSU model; **850W quality PSU is a baseline local estimate, not a universal
   certification**, and a high-power CPU may justify 1000W. The PNY/MSI models each
   need one independent 8-pin feed.
4. **Host memory:** 64GB RAM is a practical floor; 128GB is preferable if CPU
   offload, 70B experiments, or large contexts are expected.
5. **Runtime:** validate a CUDA `llama.cpp` build and start with default layer split.
   Treat tensor split as experimental and benchmark it on the actual PCIe topology.

---

## 0A. 70B ownership target — live update 2026-07-27

### Capacity tiers

Llama 3.3 70B Q4_K_M has **42.52GB of weights**. The model has 80 layers, eight
key/value heads, and 128-dimensional attention heads. From that published
configuration, an unquantized FP16 KV cache is approximately **0.3125MiB per token**:

| Intended use | GPU memory target | What that means |
|---|---:|---|
| Merely run 70B Q4 | 32GB GPU + 128GB RAM | 2× 5060 Ti can offload roughly 10.5GB+ of weights and some layers to system RAM/CPU; valid, but no longer an all-GPU 70B machine |
| 70B Q4 around 8k context | **48GB aggregate floor** | The 42.52GB file is ~39.6GiB; FP16 KV is ~2.5GiB at 8k, leaving limited but plausible room for runtime buffers |
| 70B Q4 around 16k–32k | **48–64GB** | FP16 KV is ~5GiB at 16k and ~10GiB at 32k; 48GB requires quantized KV and/or careful buffer/offload tuning as context grows |
| 70B Q4 near the advertised 128k limit | **80–96GB practical target** | FP16 KV alone is ~40GiB at 128k. An 80GB setup still needs careful tuning; 96GB provides a more credible margin |

These context figures are **local sizing calculations, not measured throughput or fit
guarantees**. `llama.cpp` supports Q8/Q4 KV cache in its default layer-split mode, which
can materially reduce cache memory; exact overhead varies with runtime options.

Sources:
[official Llama 3.3 70B model card](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct),
[published model configuration](https://huggingface.co/RedHatAI/Llama-3.3-70B-Instruct/blob/187ccb26cd9a54232a96f982100d7df0a9712775/config.json),
[GGUF sizes](https://huggingface.co/bartowski/Llama-3.3-70B-Instruct-GGUF), and
[llama.cpp multi-GPU/KV-cache guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md).

### Current 48GB routes

| Route | Checked acquisition cost | Platform burden | Decision |
|---|---:|---|---|
| **2× used RTX 3090 24GB** | Current OLX asks observed around **R$5,000–6,100/card**; roughly **R$10k–12.2k/pair** | 700W GPU board power, normally large coolers; validated x8/x8 spacing, full tower/open chassis, and a quality ~1200W PSU design target | **Best value if both cards pass local testing** |
| **3× new RTX 5060 Ti 16GB** | Pichau PNY: **R$11,399.97** for three, cart quantity unconfirmed; Terabyte MSI: **R$11,699.97**, page showed four units | 540W GPUs; three full-length slots and three true-2-slot coolers; workstation-like layout strongly preferred | **Best checked all-new path, but mechanically difficult** |
| 2× new RTX A5000 24GB | Pichau: **R$35,199.98/pair** | Dual-slot, 460W GPUs total; simpler than three gaming cards | Rejected on value |
| 1× new RTX 6000 Ada 48GB | Pichau: **R$67,999.99** | One dual-slot 300W card; simplest topology | Rejected on value unless support/workstation requirements dominate |

The RTX 3090 figures are **marketplace asking prices, not validated transactions**.
NVIDIA specifies 24GB and 350W per RTX 3090. A used pair should be bought in person
where possible and accepted only after serial/invoice checks, a VRAM error test, and a
sustained load test with hotspot/memory temperatures observed. NVLink is optional and
is not required by `llama.cpp`'s default layer split.

Price/specification evidence:
[current OLX RTX 3090 search](https://www.olx.com.br/anuncios/geforce-rtx-3090),
[NVIDIA RTX 3090 specifications](https://www.nvidia.com/en-eu/geforce/graphics-cards/30-series/rtx-3090/),
[Pichau RTX A5000](https://www.pichau.com.br/placa-de-video-pny-quadro-rtx-a5000-24gb-gddr6-384-bit-vcnrtxa5000-pb),
and
[Pichau RTX 6000 Ada](https://www.pichau.com.br/placa-de-video-pny-geforce-rtx-6000-ada-generation-48gb-gddr6-384-bit-vcnrtx6000ada-pb).
The 5060 Ti totals use the live per-card offers above.

### Recommended 70B build

1. **First choice:** two locally tested used RTX 3090 24GB cards at **no more than
   roughly R$6k each**, unless condition/warranty evidence justifies more.
2. **Platform:** a board with two physically usable CPU-connected slots, preferably
   x8/x8; measured clearance for the exact card models; full-tower or open-frame
   airflow; quality **1200W-class PSU as a design target**, sized from the actual CPU
   and connectors; 128GB RAM; and at least 2TB NVMe.
3. **Software:** Linux, current NVIDIA/CUDA stack, and `llama.cpp` default layer split.
   Start with Q4_K_M and 8k context, then measure higher context and quantized KV cache
   on the actual machine.
4. **All-new fallback:** three MSI 5060 Ti 16GB cards from the checked Terabyte offer
   only if the board and chassis can genuinely host three dual-slot cards. Do not buy
   three cards for an ordinary two-slot consumer motherboard.

The exact motherboard, CPU, PSU, and case remain a **purchase blocker**: choosing the
GPU route before resolving that topology risks buying cards that cannot be installed
or fed correctly.

---

## 1. VRAM needed (verified 3-0; file sizes refreshed 2026-07-27)

**~2 GB VRAM per 1B params at FP16; halve at Q8; quarter at Q4.**

Example: 70B at FP16 ≈ 140 GB; Llama 3.3 70B Q4_K_M is 42.52GB in weights
before cache and runtime overhead.

| Model class | Quant | VRAM | Card that fits |
|---|---|---|---|
| 7–9B (Llama 3.1 8B) | Q4_K_M | ~6 GB | RTX 3060 12GB |
| 13B | Q4/Q8 | ~12–16 GB | RTX 3060 12GB / 4070 |
| 32B (Qwen3) | Q4_K_M | 19.8GB weights; allow overhead | RTX 3090/4090 24GB or 2× 16GB |
| 32B (Qwen3) | Q6_K | 26.9GB weights; allow overhead | 2× 16GB |
| 70B (Llama 3.3) | Q4_K_M | 42.52GB weights; ~45–48GB+ practical | 2× 24GB, A6000 48GB |
| 100B+ | Q4 | 64 GB+ | Multi-GPU / workstation |

**Killed (0-3):** "70B at Q8 fits in 48 GB / dual 4090s." 70B at Q8 needs ~70+ GB. Dual-24GB
realistically caps at **70B at Q4**, not Q8.

---

## 2. Buying in Brazil — tax reality (verified) + price caveat

**Verified ✓:** **Resolução GECEX nº 852/2026** raised import-tax rates across a broad set of
capital and information-technology goods, with effects beginning in February/March 2026.
This increases landed-cost pressure; this research does **not** prove a GPU-specific retail
pass-through amount.

**Killed:** the specific pass-through claims ("+R$1,000–2,000 per piece") and specific retail
prices ("RTX 5090 = R$20,000 at Pichau") were refuted 0-3 — unsourceable, not necessarily wrong.

Structural guidance:
- **New:** Kabum, Pichau, Terabyte, Mercado Livre (official stores). Compare on Zoom/Buscapé.
- **Used RTX 3090 is conditional, not the default.** On 2026-07-27, directly visible
  Mercado Livre asks started around R$8.2k–8.5k, above a new 32GB aggregate 5060 Ti pair.
  A local/in-person 3090 can still make sense around **R$6k or less** after stress testing;
  that threshold is a buying inference, not a verified market price.
- **Avoid:** importing a single high-end GPU from AliExpress post-Feb-2026 unless the
  landed tax, warranty, and return-path risks are explicitly priced.

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
  GPU-hours. Recompute from the actual checkout total and the exact cloud GPU; the older
  R$5–7k used-3090 example is no longer a verified current market assumption.

---

## Recommendation by tier

1. **Experimenting / ≤13B / unsure:** start on **cloud** (RunPod or BRL provider like Rollin Host);
   or a **used RTX 3060 12GB** for cheap always-on small models.
2. **Serious local 30–35B, buying new:** **2× RTX 5060 Ti 16GB**, after the platform gate.
3. **Serious local 30–35B, simpler machine:** a tested used **RTX 3090 24GB** only at a
   materially lower total price; it avoids multi-GPU setup but has less capacity.
4. **70B at home:** **48GB aggregate VRAM and 128GB RAM** is the practical
   Q4/moderate-context floor. Prefer 2× tested used RTX 3090 for value, or 3× new
   5060 Ti only with a validated triple-GPU platform. Use 80–96GB VRAM for genuinely
   long-context 70B work.
5. **100B+ / fine-tuning:** **rent H100/H200** in the cloud; owning rarely pencils out in Brazil.

---

## Caveats

- The 2026-07-27 retail snapshot was directly checked, but prices and stock can change at
  checkout. Freight was not calculated.
- Compatibility remains unresolved until the exact motherboard, CPU, PSU, and case are known.
- Cloud pricing is vendor-published, USD providers carry FX/IOF.
- GPU-specific import-tax pass-through magnitude remains unverified.

## Sources (selected)
- GPU/runtime/model primary sources:
  [NVIDIA](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5060-family/);
  [PNY board specification](https://www.pny.com/file%20library/company/support/product%20brochures/geforce%20graphics/english/rtx-5060-ti-16gb-dual-fan-oc-brochure.pdf);
  [MSI board specification](https://storage-asset.msi.com/datasheet/vga/us/GeForce-RTX-5060-Ti-16G-VENTUS-2X-OC-BLACK-PLUS.pdf);
  [NVIDIA RTX 3090](https://www.nvidia.com/en-eu/geforce/graphics-cards/30-series/rtx-3090/);
  [llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md);
  [Qwen3-32B GGUF](https://huggingface.co/Qwen/Qwen3-32B-GGUF);
  [Llama 3.3 70B GGUF](https://huggingface.co/bartowski/Llama-3.3-70B-Instruct-GGUF)
- Import tax:
  [MDIC source record for Resolução GECEX 852/2026](https://www.gov.br/mdic/pt-br/assuntos/camex/outros-documentos/notas/deferimentos/caderno-resol-852-2026.pdf/view)
- Cloud BR: gpubrasil.com.br; rollinhost.com.br; computeprices.com/compare/runpod-vs-vast
- Break-even: thundercompute.com; spheron.network/blog/renting-gpus

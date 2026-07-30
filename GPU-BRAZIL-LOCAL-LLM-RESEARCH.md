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

With a **US$25,000** ceiling and a mixed workload—interactive reasoning, coding,
large-MoE experiments, fine-tuning, image generation and video generation—the
capacity-first ranking is no longer the decision rule. The current default is a
**staged Brazilian hybrid**: build one RTX 5090 workstation that can later accept a
second GPU, keep roughly **US$12k–15k nominal** uncommitted for APIs and burst
H200/B300 or multi-GPU training, and add the second 5090 only after measured local
utilization or a 32GB memory blocker justifies it. Hardware-only remains valid for
privacy or sustained use; cloud-only remains strongest while the workload is
experimental and heterogeneous.

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

## 0B. US$25,000 Brazil hardware, cloud and hybrid scenario — live update 2026-07-30

### Budget meaning

This section assumes **US dollars, not R$25,000**. Banco Central do Brasil's latest
available closing PTAX checked for this update was **R$5.1217/US$ on 2026-07-29**,
making US$25,000 approximately **R$128,042.50**. PTAX is a reference conversion, not
a promise of retail, card, remittance, import, tax, or freight buying power. The
comparisons below therefore use **about R$128k as a nominal ceiling** and prioritize
Brazilian retail prices where a live page was available.

### Workload-first decision frame

No single metric governs all of these workloads:

| Workload | Decision metric | Economically matched lane |
|---|---|---|
| Interactive design, architecture and planning | Time to first token, generation rate and accepted-decision quality | Fast managed model API; large MoE as critic/adjudicator |
| Agentic coding | End-to-end tool-loop time and tests passed | Fast API for serial loops; discounted batch for unattended work |
| Large-MoE experiments | Model/context access and cost per accepted evaluation | Hosted API unless weights, logits or runtime control are required |
| LoRA/QLoRA and model research | Training tokens or examples per real, evaluation-adjusted improvement | Managed tuning first; raw H100/H200/B200 burst after a fit test |
| Image generation | Cost per selected image and images per minute | Local CUDA for repeated/custom pipelines; per-image API for premium/occasional work |
| Video generation | Cost per accepted output second, not token rate | Local CUDA for repeated open-model iteration; per-second API for premium models |

MoE requires two numbers: **total parameters govern weight memory; activated
parameters approximate per-token expert compute**. The official
[Qwen3.5-397B-A17B model card](https://huggingface.co/Qwen/Qwen3.5-397B-A17B)
reports 397B total and 17B activated parameters; it does not fit like a 17B dense
model. This is the central reason to keep API or cluster access even when owning a
local GPU.

### Three portfolios under the same ceiling

| Strategy | Brazil acquisition or spend | What it does well | Structural loss |
|---|---:|---|---|
| **Hardware-only** | Spend about **R$110k–125k** on one RTX PRO 6000 96GB workstation, a six-R9700 192GB system, or a conditionally sourced four-A6000 192GB server | Privacy, repeatability, custom runtimes, no usage meter, local image/video pipelines | No clean Brazilian configuration simultaneously provides large-MoE capacity, modern CUDA breadth, simple integration and enough training throughput; capital is locked into one topology |
| **Cloud-only** | Preserve the nominal **US$25k** as API, raw-GPU and managed-training budgets | Maximum model and hardware diversity; scale to H200/B300 or multi-GPU only for the experiment | No residual asset; USD/FX exposure, provider limits, data-placement concerns and continuing storage costs |
| **Staged hybrid — default** | Start with a **one-RTX-5090 workstation at roughly R$52k–65k**, leaving about **R$63k–76k / US$12k–15k nominal** for cloud | Local CUDA for image/video, private data and repeatable experiments; cloud for fast reasoning, 235B–1T MoE and short training clusters | Requires explicit workload routing and spend controls; a second local GPU remains a later decision |

These complete-system totals are **local planning estimates, not retailer or
integrator quotes**. They include host RAM, storage, PSU and chassis allowances, but
exact cart quantity, platform topology, cooling and warranty remain purchase gates.

### Current Brazilian workstation anchors

| Lane | Checked accelerator evidence | Whole-system planning range | Local role | Cloud remaining from nominal ceiling |
|---|---:|---:|---|---:|
| **Staged hybrid phase 1** | 1× RTX 5090 32GB; KaBuM listed an in-stock first-party Inno3D card at **R$25,999.99 Pix** | **R$52k–65k** with 192GB-class RAM, 4TB NVMe, high-airflow chassis and a platform designed for the intended second-GPU topology | Image/video workflows, private inference, 7–32B tuning experiments and local model/runtime development | **R$63k–76k / about US$12k–15k nominal** |
| **Balanced hybrid phase 2** | 2× RTX 5090, **R$51,999.98** at the checked unit price | **R$77k–90k**; specialized spacing, 1,150W GPU power and a 220V electrical plan are mandatory | 64GB aggregate CUDA, concurrent media jobs, 70B Q4 inference and larger parameter-efficient experiments | **R$38k–51k / about US$7k–10k nominal** |
| **Simplest hardware-only CUDA** | RTX PRO 6000 Blackwell 96GB at Pichau, **R$89,999.99 Pix**, 12-month warranty | **R$110k–122k** | One 96GB ECC pool, broad CUDA compatibility, strong media and workstation reliability | Only **about US$1k–3.5k nominal** |
| **New hardware-only capacity** | 4× R9700 costs **R$43,999.96**; 6× costs **R$65,999.94** at the checked Pichau price | **R$84k–104k** for four or **R$115k–125k** for six | 128–192GB aggregate and good capacity per real | ROCm and multi-GPU integration replace financial cloud residue as the main risk |

The phase-one workstation is deliberately **not** a promise that a second air-cooled
5090 will fit a normal tower. The board lanes, card dimensions, riser or water-cooling
plan, PSU and circuit must be designed before calling the host dual-GPU-ready.

### Hardware-only capacity reference, not overall ranking

| Rank/lane | Core hardware and checked acquisition evidence | Whole-system planning status | Model memory | What it maximizes | Decisive gate |
|---|---|---:|---:|---|---|
| **1A. Scarce one-box maximum** | Used M3 Ultra Mac Studio, 512GB; a verified eBay sold listing for a 512GB/4TB unit closed at **US$19,995** | Fits a US-domestic US$25k hardware budget; **Brazilian landed total unresolved** | **512GB unified**; less is available to the model | Largest model fit, lowest integration/power burden; credible 400GB-class files and aggressive 600–700B quantization | Apple no longer offers the 512GB configuration in its current store; the checked unit is sold, had no returns and did not ship to Brazil. MLX/Metal is not CUDA and memory is not upgradeable |
| **1B. Used-server maximum** | 8× Quadro RTX 8000 48GB; current sold-market evidence centers around **US$1.7k–2.0k/card** | Roughly **US$22k–25k before Brazilian landed-cost resolution** with a suitable used 8-GPU server | **384GB aggregate CUDA** | Maximum serviceable CUDA capacity per US dollar among the credible lanes; 400B-class quantized inference | Turing-era hardware, 8-way PCIe sharding, **2,080W GPU power**, passive/active airflow engineering and used-server failure risk; modern kernels must be tested |
| **2. Compact supported capacity** | 2× DGX Spark; a Carrefour marketplace listing showed **R$44,999.10 Pix/unit**, versus NVIDIA's current **US$4,699/unit** price | **R$100k–115k** including approved ConnectX cable, UPS and storage allowance | **2×128GB unified; 256GB distributed** | Largest compact NVIDIA-supported configuration; NVIDIA documents up to 405B on two units | The Brazilian listing is third-party and says **zero supplier warranty**; 273GB/s per node, ARM64 and the inter-node runtime must pass the actual workload |
| **3A. New Brazil-build frontier** | 6× [Radeon AI PRO R9700 32GB at Pichau](https://www.pichau.com.br/placa-de-video-asus-amd-radeon-ai-pro-r9700-32gb-gddr6-256-bit-turbo-ai-pro-r9700-32g), **R$10,999.99/card** or **R$65,999.94/six**, quantity unconfirmed | **R$115k–125k local planning estimate** with a lane-rich host and specialized riser/rack cooling | **192GB aggregate ROCm** | Highest new, locally listed accelerator capacity that plausibly fits the ceiling; 235B-class Q4 with headroom | Not a normal tower: 1,800W of GPUs, six-way topology and ROCm/runtime work. The page retains an expired pre-sale notice; validate one card, then two, before ordering six |
| **3B. Mature-CUDA frontier** | 4× used RTX A6000 48GB; a current US eBay ask was **US$3,599.99/card**, or **US$14,399.96/four**, before Brazilian freight/tax | Roughly **US$20k–25k before Brazilian landed-cost resolution** | **192GB aggregate CUDA** | Best balance of large-model capacity, mature CUDA, dual-slot geometry and 300W/card power | Four new Brazilian cards cost at least R$160k before the host; used import only becomes credible with a fixed landed quote, same-batch burn-in and local RMA |
| **4. Fast 128GB near-miss** | 4× RTX 5090 32GB at the checked first-party KaBuM price of **R$25,999.99/card**, or **R$103,999.96/four** | Already consumes most of the ceiling before the specialized four-GPU host | **128GB** | Highest raw CUDA throughput in this set | Four huge 575W cards need water blocks or a riser/rack design; 128GB still cannot fully hold the checked 142GB Qwen3-235B Q4_K_M file |
| **5. Reliable single-GPU hardware lane** | 1× [RTX PRO 6000 Blackwell 96GB at Pichau](https://www.pichau.com.br/placa-de-video-pny-geforce-rtx-pro-6000-blackwell-workstation-edition-96gb-gddr7-512-bit-vcnrtxpro6000b-pb), **R$89,999.99 Pix** | **R$110k–122k** | **96GB ECC** | Cleanest locally supportable high-speed CUDA workstation | Strong heterogeneous-workload hardware, but buying it leaves little budget for large-MoE APIs or cluster experiments |

Technical anchors:

- Apple specifies **819GB/s** memory bandwidth and at most 480W continuous system
  power for the M3 Ultra Mac Studio. The 512GB model exists, but Apple's current
  configure-to-order page now exposes only the 96GB M3 Ultra memory configuration;
  512GB is therefore a scarce used-stock lane, not a current retail configuration.
- NVIDIA specifies the Quadro RTX 8000 at **48GB, 260W and NVLink support**. Eight
  cards mean 384GB only through runtime-managed sharding; NVLink can join pairs, not
  turn an eight-card host into one transparent 384GB GPU.
- NVIDIA specifies the RTX PRO 6000 Blackwell at **96GB ECC, 1,792GB/s and 600W**.
  Its dual-slot form factor removes most multi-GPU geometry risk, but the current
  workstation edition uses a double-flow-through cooler whose chassis path must still
  be validated.
- NVIDIA specifies the RTX 5090 at **32GB, 1,792GB/s, 575W and no NVLink**. Three
  cards are separate PCIe-connected memory pools; theoretical aggregate bandwidth is
  not a single-GPU bandwidth promise.
- AMD specifies the R9700 at **32GB ECC-capable GDDR6, 640GB/s, 300W, PCIe 5.0 x16
  and dual-slot active cooling**. AMD currently documents R9700 support in ROCm/vLLM,
  and `llama.cpp` supports multi-GPU layer splitting through its ROCm backend. That
  establishes a credible route, not proof of performance or stability for a six-card
  build.
- NVIDIA documents DGX Spark with **128GB unified memory and 273GB/s bandwidth per
  node**, and explicitly documents Spark stacking. A dual node can increase model
  capacity, but the inter-node link and distributed runtime remain part of every
  inference.
- NVIDIA specifies the Ampere RTX A6000 at **48GB ECC in a dual-slot card**. Four
  used cards are a strong nominal capacity design, but only if all four share a
  verified condition, return path and supported workstation topology.
- A multi-GPU workstation should use a lane-rich platform. Threadripper PRO 9000 WX
  exposes up to **128 PCIe 5.0 lanes**; a WRX90 board such as the ASUS Pro WS
  WRX90E-SAGE SE exposes seven physical PCIe 5.0 x16 slots. Six dual-slot cards still
  require a specialized chassis/riser layout; physical slot count alone is not proof
  of fit or cooling.

Sources:
[BCB PTAX](https://ptax.bcb.gov.br/ptax_internet/consultarUltimaCotacaoDolar.do);
[Apple Mac Studio specifications](https://www.apple.com/mac-studio/specs/);
[used 512GB M3 Ultra sold listing](https://www.ebay.com/itm/147250440028);
[NVIDIA Quadro RTX 8000](https://www.nvidia.com/en-au/products/workstations/quadro/rtx-8000/);
[RTX 8000 used sold-price tracker](https://pcpartvalue.com/gpu/nvidia-quadro-rtx-8000-tu102-48-gb-2018);
[NVIDIA RTX PRO 6000](https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-6000/);
[NVIDIA RTX 5090](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/);
[KaBuM Inno3D RTX 5090 listing](https://www.kabum.com.br/produto/710944/);
[AMD R9700](https://www.amd.com/en/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html);
[AMD ROCm/vLLM](https://rocm.docs.amd.com/en/7.12.0-preview/rocm-for-ai/vllm.html);
[llama.cpp multi-GPU](https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md);
[DGX Spark hardware](https://docs.nvidia.com/dgx/dgx-spark/hardware.html);
[DGX Spark stacking](https://docs.nvidia.com/dgx/dgx-spark/spark-clustering.html);
[Carrefour DGX Spark marketplace listing](https://www.carrefour.com.br/produto/dgx-spark-personal-ai-supercomputer-ia-inteligencia-artificial-nvidia-339583905);
[AMD Threadripper PRO 9955WX](https://www.amd.com/en/products/processors/workstations/ryzen-threadripper/9000-wx-series/amd-ryzen-threadripper-pro-9955wx.html);
[ASUS WRX90E-SAGE](https://www.asus.com/us/motherboards-components/motherboards/workstation/pro-ws-wrx90e-sage-se/where-to-buy/);
[NVIDIA RTX A6000](https://www.nvidia.com/pt-br/products/workstations/rtx-a6000/);
[used RTX A6000 listing snapshot](https://www.ebay.com/itm/115925848642);
[OLX RTX 3090 snapshot](https://www.olx.com.br/anuncios/geforce-rtx-3090).

### What the memory tiers buy

These are sizing categories, not measured guarantees:

| Accelerator capacity | Practical model envelope |
|---:|---|
| **64GB** | 70B Q4 with moderate context and useful headroom; not a comfortable 70B Q8 target |
| **96GB** | 70B at higher quantization or context; the official gpt-oss-120b `original` checkpoint folder is 65.2GB, leaving model/runtime-specific headroom |
| **128GB** | More comfortable 120B-class inference and some larger MoE/quantized models; Qwen3-235B-A22B Q4_K_M is 142GB before KV/runtime overhead and therefore does not fully fit |
| **192–256GB** | Credible 200–400B quantized-model experimentation; 192GB has plausible headroom over the 142GB Qwen file, while exact KV cache and distributed-runtime support still govern fit |
| **384GB** | Used eight-GPU RTX 8000 territory: 400B-class Q4 and more aggressive 600–700B quantization become plausible, with substantial PCIe, power and old-kernel costs |
| **512GB unified** | The largest one-box envelope found under the raw US$25k hardware ceiling: credible 400GB-class files and aggressive 600–700B experiments, but only through a scarce used M3 Ultra and the MLX/Metal ecosystem |

Aggregate multi-GPU capacity is runtime-managed. It is not equivalent to one GPU with
that much VRAM, and generation speed can be limited by PCIe or network transfers.
Conversely, DGX Spark's memory is unified *within each node*, but a two-node
configuration is still distributed.

Model-size sources:
[OpenAI gpt-oss-120b repository](https://huggingface.co/openai/gpt-oss-120b/tree/main/original);
[official Qwen3-235B-A22B Q4_K_M repository](https://huggingface.co/Qwen/Qwen3-235B-A22B-GGUF/tree/main/Q4_K_M).

### Training ceiling

US$25k opens meaningful **inference, evaluation, LoRA/QLoRA, distillation and
application-development** options. It does not make full pretraining or conventional
full-parameter fine-tuning of a 70B foundation model economically credible. Optimizer
states, gradients, activations, checkpoints and training throughput raise the memory
and compute requirement far beyond the model's quantized inference file. For rare
training runs, an H100/H200/B200 cloud cluster remains the correct lane.

NVIDIA does publish DGX Spark recipes for **Llama 3.1 70B LoRA and QLoRA**, which
makes parameter-efficient tuning a real supported lane rather than an inference from
memory capacity alone. It remains a recipe-level capability, not a throughput or
completion-time guarantee.

Source:
[NVIDIA DGX Spark PyTorch fine-tuning recipe](https://build.nvidia.com/spark/pytorch-fine-tune/instructions).

M.2 inference accelerators such as Hailo-8 are also excluded from this LLM budget:
their value is efficient compiled edge inference, especially vision pipelines; they
do not provide a general CUDA/ROCm runtime or the tens to hundreds of gigabytes of
accelerator memory required by these LLM classes.

### Cloud-only capacity and Brazil-accessible prices

The checked [Runpod price page](https://www.runpod.io/pricing) listed the following
pod rates on 2026-07-30. If the entire US$25k were spent on one type—an opportunity
ceiling, not the recommended allocation—it would buy:

| Raw cloud lane | Published rate | US$25k capacity |
|---|---:|---:|
| RTX 5090 32GB | US$0.99/hour | **25,253 GPU-hours** |
| RTX PRO 6000 96GB | US$1.99/hour | **12,563 GPU-hours**, about 523 continuous days |
| H200 141GB | US$4.39/hour | **5,695 GPU-hours**, about 237 continuous days |
| B300 288GB | US$7.39/hour | **3,383 GPU-hours**, about 141 continuous days |
| 8× H200 cluster | US$4.31/GPU-hour, or US$34.48/node-hour | **725 node-hours**, about 30 continuous days |

[GPUBrasil](https://gpubrasil.com.br/br/index.html) provides BRL-denominated access;
the checked catalog locates the high-end instances in US/EU regions rather than
claiming a Brazilian data center. At the nominal R$128,042.50 envelope, the listed
rates correspond to roughly **4,957 H200 hours at R$25.83/hour**, **8,892 H100 SXM
hours at R$14.40/hour**, or **16,738 L40 hours at R$7.65/hour**, before availability
and billing-term verification.

Cloud-only should not mean renting one server continuously. The matched portfolio is:

- managed fast and large-MoE APIs for interactive design, architecture and coding;
- serverless image/video APIs for occasional premium generations;
- raw RTX PRO 6000/H200/B300 only when weights, framework or pipeline control matter;
- managed LoRA/SFT for supported open models before renting an eight-GPU node;
- multi-GPU clusters only for a measured distributed-memory or training blocker.

Fireworks' checked managed-training table prices LoRA SFT at **US$6/M training tokens
for 80–300B models** and **US$10/M above 300B**. Those units are not GPU-hours and
should not be converted into them. Dataset tokens times epochs, intermediate traces,
evaluation, hosting and checkpoint policy still determine the real cost.

### Hybrid budget routing

If phase one closes near **R$52k–65k**, keep the remaining roughly **US$12k–15k
nominal** uncommitted and release it through caps:

| Cloud purpose | Initial cap | Example capacity at current published rates |
|---|---:|---|
| Fast interactive and large-MoE APIs | **US$2k** | Billions of tokens on low-cost open-model endpoints; rate limits and accepted-result quality will bind first |
| Raw large-model experiments | **US$4k** | About **911 H200 hours** or **541 B300 hours** |
| Managed tuning and short clusters | **US$3k** | Up to **500M Qwen3-235B-class LoRA SFT tokens** at the published managed rate, or about **87 hours on 8×H200**; actual jobs should start far smaller |
| Premium image/video APIs | **US$1k–2k** | Avoids keeping local hardware occupied for model-specific premium outputs |
| Storage, failed runs, FX/tax and provider reserve | **US$2k–4k** | Remains uncommitted until real checkpoint and transfer behavior is measured |

Local hardware then owns repeated CUDA iteration, private data, open image/video
pipelines and smaller/medium fine-tuning. Cloud owns the rare hardware, 235B–1T MoE
access, high-speed interactive endpoints and short distributed jobs.

### Current break-even evidence

At PTAX only—excluding cloud tax/storage and also excluding local electricity,
cooling, maintenance and residual value—the complete-system planning ranges imply:

| Brazil system | Compared with current Runpod pod rate | Nominal break-even |
|---|---:|---:|
| 1× RTX 5090 workstation, R$52k–65k | US$0.99/hour | **10.3k–12.8k hours**, about 3.5–4.4 years at 8 hours/day |
| 2× RTX 5090 workstation, R$77k–90k | 2 × US$0.99/hour | **7.6k–8.9k node-hours**, about 2.6–3.0 years at 8 hours/day |
| RTX PRO 6000 workstation, R$110k–122k | US$1.99/hour | **10.8k–12.0k hours**, about 3.7–4.1 years at 8 hours/day |

This supersedes the older 1,000–2,000-hour rule for this high-markup Brazilian
scenario. Ownership is justified by sustained use, privacy/control or workflow
friction—not by the existence of the budget.

### Staged buying call

1. Spend **US$200–500 first** reproducing the intended text, tuning, image and video
   pipelines in cloud. Record fit, time to first token, generation rate, accepted
   outputs, wall time, GPU memory and total cost.
2. Obtain a Brazilian quote for a **one-RTX-5090 workstation** with 192GB-class host
   RAM, 4TB NVMe and explicit second-GPU topology, power and cooling documentation.
3. Buy phase one only if local iteration, privacy or persistent workflow friction is
   already demonstrated. Preserve at least **US$10k nominal** for cloud.
4. Add the second 5090 only after 90 days if the first GPU averages sustained use,
   32GB repeatedly blocks admitted workloads, or two concurrent local jobs are worth
   more than the cloud alternative.
5. Keep the 512GB Mac, eight-RTX-8000 server, dual DGX Spark, six-R9700 and
   four-used-A6000 routes as **hardware-only specialists**, not the overall default.

**Current default:** staged hybrid. Cloud-only is the correct pre-purchase experiment;
one local RTX 5090 is the first owned capability; a second local GPU is an
evidence-triggered expansion. Hardware-only is a deliberate sovereignty or
high-utilization choice, not the general maximum-capability winner.

Background-helper closeout:

| Lane | Assigned question | Evidence returned | Integration decision | Rejected material | Final status | Follow-up owner |
|---|---|---|---|---|---|---|
| `usd25k_hardware_survey` | Re-rank Brazil hardware-only, cloud-only and hybrid for the mixed workload | Candidate disposition, workload routing, complete-system allowances and current Runpod comparisons | Integrated the staged 5090 hybrid, CUDA/media routing and specialist-only disposition | Replaced its stale PTAX and older 5090 snapshot with the independently refreshed 2026-07-29/30 evidence | **closed, read-only** | Main research; next evidence owner is the 90-day pilot |

Evidence status:

- **Primary-source:** hardware memory, bandwidth and power; official runtime/model
  properties; vendor cloud billing units.
- **Live-listing evidence:** dated Brazilian accelerator prices and warranty/stock
  language.
- **Local inference:** whole-system allowances, budget allocation, break-even and
  workload routing.
- **Open residue:** actual workload fixtures, accepted-output thresholds, privacy
  requirements, measured utilization, exact host quote, second-GPU geometry and
  checkout-level cloud/tax terms.

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

## 3. Cloud GPU (verified vendor rates refreshed 2026-07-30)

- **Runpod:** RTX 5090 32GB **US$0.99/hour**; RTX PRO 6000 96GB
  **US$1.99/hour**; H200 141GB **US$4.39/hour**; B300 288GB
  **US$7.39/hour**; H200 cluster **US$4.31/GPU-hour**.
- **GPUBrasil:** BRL-denominated access with H200 **R$25.83/hour**, H100 SXM
  **R$14.40/hour**, L40 **R$7.65/hour** and other listed accelerators. The checked
  catalog places these high-end instances in US/EU regions; the brand or BRL billing
  is not proof of Brazilian data residency.
- **Managed training:** Fireworks listed LoRA SFT at **US$6/M training tokens** for
  80–300B models and **US$10/M** above 300B. Managed-token and raw-GPU billing are
  different units.
- Global providers bill in USD and add FX, payment-tax and possible card-spread
  exposure. Recheck the actual account checkout, storage and egress policy.

---

## 4. Buy-vs-cloud break-even (dated planning comparison)

- **Cloud wins:** heterogeneous experiments, bursty use, large MoE/API access,
  temporary H100/H200/B200/B300 requirements and usage that has not been measured.
- **Buying wins:** privacy/control, repeated local pipelines, high sustained
  utilization and workflow friction that a remote service cannot remove.
- At the current PTAX reference and checked complete-system allowances, a one-5090
  Brazil workstation reaches nominal parity with a US$0.99/hour pod only after about
  **10.3k–12.8k hours**; dual 5090 reaches parity after about **7.6k–8.9k node-hours**.
  Local electricity, cooling and repair extend those thresholds; residual value and
  avoided remote friction shorten them.
- The old generic **1,000–2,000 GPU-hour** rule is rejected for these current,
  high-markup Brazilian complete systems.

---

## Recommendation by tier

1. **Experimenting / ≤13B / unsure:** start on **cloud** (Runpod or a BRL-billed
   provider such as GPUBrasil);
   or a **used RTX 3060 12GB** for cheap always-on small models.
2. **Serious local 30–35B, buying new:** **2× RTX 5060 Ti 16GB**, after the platform gate.
3. **Serious local 30–35B, simpler machine:** a tested used **RTX 3090 24GB** only at a
   materially lower total price; it avoids multi-GPU setup but has less capacity.
4. **70B at home:** **48GB aggregate VRAM and 128GB RAM** is the practical
   Q4/moderate-context floor. Prefer 2× tested used RTX 3090 for value, or 3× new
   5060 Ti only with a validated triple-GPU platform. Use 80–96GB VRAM for genuinely
   long-context 70B work.
5. **100B+ / fine-tuning:** use managed LoRA/SFT where the model and checkpoint
   contract fit; rent H100/H200/B200-class capacity for unsupported or empirical
   runtime work. Local parameter-efficient tuning remains useful for smaller models.
6. **US$25k mixed-workload objective:** default to a **staged hybrid**. Validate the
   workload in cloud, build one RTX 5090 workstation with an explicit possible
   second-GPU topology, preserve at least US$10k nominal for large-MoE APIs and burst
   compute, and add the second GPU only from 90-day utilization or fit evidence.

---

## Caveats

- The original retail snapshot is dated 2026-07-27; the US$25k workstation anchors
  were refreshed on 2026-07-30. Prices and stock can change at checkout, and freight
  was not calculated.
- Compatibility remains unresolved until the exact motherboard, CPU, PSU, and case are known.
- Cloud pricing is vendor-published, USD providers carry FX/IOF.
- GPU-specific import-tax pass-through magnitude remains unverified.
- The US$25k complete-system totals are planning estimates, not quotes. Accelerator
  page prices were live snapshots; cart quantity, freight, platform stock and
  integrator warranty were not confirmed.

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
- Cloud:
  [Runpod pricing](https://www.runpod.io/pricing);
  [GPUBrasil catalog](https://gpubrasil.com.br/br/index.html);
  [Fireworks pricing](https://fireworks.ai/pricing)
- Budget reference:
  [BCB closing PTAX](https://ptax.bcb.gov.br/ptax_internet/consultarUltimaCotacaoDolar.do)

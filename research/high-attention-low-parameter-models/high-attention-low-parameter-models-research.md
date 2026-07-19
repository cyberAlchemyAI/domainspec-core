# Explorer Transcript: High Attention, Low Parameter Models

Dispatch: `2026-06-29-high-attention-low-parameter-models`

This file preserves the explorer returns for the research dispatch. The downstream
`findings.md` cites these sections as its evidence boundary.

## Agent 1: Abramsky, Samson

Read-only: no files changed.

**Abramsky Explorer Return**

Yes: a small-parameter LM can have a very large _visible_ context window. Parameter count and context length are not the same knob. But a very large _usable_ context window is harder: long-context inference remains bottlenecked by attention compute, KV-cache memory/bandwidth, positional generalization, training distribution, and the model's ability to select relevant evidence.

Let:

`L` = context length, `P` = parameter count, `N_layer` = layers, `H_q` = query heads, `H_kv` = KV heads, `d_h` = head dim, `b` = bytes per KV scalar.

For dense decoder attention:

`KV cache memory ~= B * L * N_layer * 2 * H_kv * d_h * b`

The factor `2` is for keys and values. Parameter memory is roughly `P * b_weight`, independent of `L`; KV cache grows linearly with `L`. Thus small `P` helps weight memory, but at long context the KV cache can dominate. GQA/MQA reduces only the `H_kv` term, not the number of visible tokens. Ainslie et al.'s GQA explicitly trades KV-head count for inference efficiency while trying to preserve MHA quality ([GQA](https://arxiv.org/abs/2305.13245)). Llama 3 also uses GQA for inference efficiency ([Meta Llama 3 model card](https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md)).

Dense prefill attention per layer is approximately:

`QK^T + AV ~= O(H_q * L^2 * d_h) = O(L^2 * d_model)`

Across layers: `O(N_layer * L^2 * d_model)`, plus projection/MLP work `O(L * P)`. During autoregressive decode, each new token attends over prior cached tokens:

`decode attention per token ~= O(N_layer * L * d_model)`

So dense attention makes long context expensive even for small models. FlashAttention is important because it computes _exact_ attention with much better IO/memory behavior, but it does not remove the quadratic FLOP scaling of dense prefill ([FlashAttention](https://arxiv.org/abs/2205.14135)). PagedAttention/vLLM improves serving memory management for KV cache, but again does not make the model semantically better at using far tokens ([PagedAttention/vLLM](https://arxiv.org/abs/2309.06180)).

**Visible vs Useful Context**

A token is _visible_ if it is inside the model's context window, has a positional representation, and can be attended to by the architecture. A token is _useful_ only if the model can retrieve, bind, and reason over it under interference. Liu et al. show that long-context models can degrade sharply when relevant information is placed in the middle of the context, despite being technically visible ([Lost in the Middle](https://arxiv.org/abs/2307.03172)). This is the key distinction: context length is a hardware/architecture affordance; usable context is an empirical capability.

**Exact Dense Attention**

Dense attention is the cleanest definition of "big attention": every token can directly score every previous token. It preserves maximum pairwise visibility, but costs `O(L^2)` prefill and `O(L)` decode per generated token, plus `O(L)` KV cache. Small parameters reduce projection/MLP cost and weight memory, but not the fundamental dense-attention dependence on `L`.

This means a 1B-3B model can advertise 128K context. Meta says Llama 3.2 1B and 3B support 128K tokens ([Meta Llama 3.2](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/)); Microsoft reports Phi-3-mini at 3.8B parameters with a 128K variant via LongRoPE ([Phi-3 Technical Report](https://arxiv.org/abs/2404.14219)). These are real examples of small-ish parameter count plus long visible context. They do not prove that all 128K tokens are equally useful.

**Approximate/Sparse Attention**

Sparse/windowed attention reduces the attention graph. Longformer uses local window attention plus selected global tokens, giving linear scaling in sequence length for its sparse pattern ([Longformer](https://arxiv.org/abs/2004.05150)). BigBird combines random, window, and global attention and argues that sparse attention can preserve important theoretical properties while reducing quadratic dependence to linear ([BigBird](https://arxiv.org/abs/2007.14062)).

But sparse attention is not dense attention. A token outside the local window may be reachable only through global tokens or multi-hop routing. Cost improves roughly from `O(L^2)` to `O(L*w + L*g)` for window size `w` and global/random edges `g`, but the architecture has chosen which interactions are cheap. This can scale visible length while reducing arbitrary pairwise access.

**Positional Limits**

Long context also requires positional generalization. Learned absolute embeddings usually fail outside trained positions. RoPE gives relative-position structure through rotations ([RoFormer/RoPE](https://arxiv.org/abs/2104.09864)), but RoPE models often still fail beyond trained lengths. ALiBi was designed for train-short/test-long extrapolation with linear attention biases ([ALiBi](https://arxiv.org/abs/2108.12409)). Position Interpolation scales positions back into the trained range and argues interpolation is more stable than extrapolation ([Position Interpolation](https://arxiv.org/abs/2306.15595)). YaRN and LongRoPE extend RoPE-based models further with efficient fine-tuning and non-uniform interpolation ([YaRN](https://arxiv.org/abs/2309.00071), [LongRoPE](https://arxiv.org/abs/2402.13753)).

These methods extend addressability. They do not erase attention/KV cost or guarantee robust reasoning.

**Retrieval/External Memory**

RAG and MemGPT-like systems do not give the model dense attention over all external tokens. They give the model a smaller selected subset. RAG combines parametric memory with a non-parametric retrieved index ([RAG](https://arxiv.org/abs/2005.11401)); MemGPT manages memory tiers to create the illusion of larger context ([MemGPT](https://arxiv.org/abs/2310.08560)). This can be more scalable than raw context, but failure moves to retrieval, compression, ranking, and memory-update policy.

**Recurrent, Linear, State-Space Alternatives**

Linear attention rewrites attention with kernel feature maps so recurrent state can summarize history in linear time ([Transformers are RNNs](https://arxiv.org/abs/2006.16236)); Performers approximate softmax attention with random features and linear space/time ([Performers](https://arxiv.org/abs/2009.14794)). RetNet and Mamba replace dense attention with retention/state dynamics, offering recurrent or linear-time sequence processing ([RetNet](https://arxiv.org/abs/2307.08621), [Mamba](https://arxiv.org/abs/2312.00752)). The tradeoff is compression: a fixed-size state cannot preserve arbitrary token-token relations without loss. Mamba explicitly targets content-selective propagation, but it is not exact pairwise attention.

**Bottom Line**

A small-parameter, huge-context model is feasible when "huge context" means addressable input length. It becomes difficult when it means reliable use of arbitrary evidence across that length. Parameter count can shrink independently of `L`; dense attention compute, KV cache, positional reliability, and evidence-selection quality cannot.

**Concrete Hypotheses**

1. **KV-dominance threshold:** For 1B-4B dense/GQA models, there is a context length beyond which KV memory/bandwidth, not weight memory, dominates latency and batch size. Measure latency, VRAM, and throughput at 8K/32K/128K with fixed model weights.

2. **Visible-useful gap:** A 1B-3B 128K model will pass simple needle retrieval but fail multi-hop or conflicting-evidence tasks earlier than larger models. Test passkey, key-value retrieval, multi-doc QA, and adversarial middle-position evidence.

3. **GQA sweet spot:** Reducing `H_kv` improves deployability, but too few KV heads harms far-context binding. Train or adapt matched models with MHA, GQA, and MQA; compare KV memory against long-context QA accuracy.

4. **Hybrid wins on utility:** For small models, retrieval plus 16K-32K dense context may outperform raw 128K dense context on realistic document QA, because selection reduces interference. Compare raw-long-context, RAG-short-context, and RAG-plus-long-context under provenance-scored evaluation.

## Agent 2: Shannon, Claude

**Read-Only Explorer: Shannon / Methodology Lens**

A small-parameter language model can have a very large advertised context window, but that does not mean it has a very large _usable information window_. The context window is an input visibility claim: "these tokens are present in the model's attention computation or memory mechanism." Usable context is a behavioral claim: "task-relevant evidence at those positions can be selected, preserved, composed, and used in the output."

In a dense Transformer, self-attention gives each token a route to attend over earlier tokens, as introduced in [_Attention Is All You Need_](https://papers.neurips.cc/paper/7181-attention-is-all-you-need.pdf). Visibility means the token is encoded into key/value states and is not masked away. But the downstream path is narrow: each layer maps all available evidence into fixed-width hidden states; attention weights compete; later layers transform and compress; final logits only expose whatever survived. In information-channel terms, the context is the input bandwidth, but the model's hidden dimension, number of heads, trained retrieval circuits, positional encoding, and decoding objective determine channel capacity and noise tolerance.

This distinction explains how a small model can "see" a huge context. Context length is partly a systems and architecture property, not only a parameter-count property. Dense attention is expensive because attention over a sequence grows quadratically during prefill; [_FlashAttention_](https://arxiv.org/abs/2205.14135) shows that memory traffic and attention implementation are major constraints. KV cache memory during generation also scales with sequence length, layer count, hidden/key-value width, precision, and batch size. Smaller models usually have fewer layers and narrower states, so their KV cache is cheaper; on the same hardware they may fit longer visible contexts than a larger model. Sparse/sliding attention, recurrent memory, compression, retrieval, and optimized kernels can extend visibility further.

But small parameter count also reduces the machinery available to use that context. The model must learn position-robust search, distinguish signal from distractors, bind evidence across long distances, and carry the answer through subsequent computation. Long context is not just storage; it is retrieval plus reasoning under interference.

The long-context literature repeatedly shows that advertised length overstates usable information. [_Lost in the Middle: How Language Models Use Long Contexts_](https://arxiv.org/abs/2307.03172) found that models often perform best when relevant information is near the beginning or end of the prompt and degrade when it appears in the middle. [_RULER: What's the Real Context Size of Your Long-Context Language Models?_](https://arxiv.org/abs/2404.06654) argues that simple needle-in-haystack tests are too weak: models that pass vanilla retrieval can drop sharply as length and task complexity increase. [_LongBench_](https://arxiv.org/abs/2308.14508) similarly separates long-context benchmarks into QA, summarization, few-shot learning, code, synthetic retrieval, and multi-document tasks, showing that long-context understanding is not a single capability.

Mechanistically, several bottlenecks matter:

- **Positional generalization:** If the model was trained mostly on shorter sequences, long positions may be out-of-distribution. RoPE, ALiBi, position interpolation, and YaRN address this partially. See [RoFormer / RoPE](https://arxiv.org/abs/2104.09864), [ALiBi](https://arxiv.org/abs/2108.12409), [Position Interpolation](https://arxiv.org/abs/2306.15595), and [YaRN](https://arxiv.org/abs/2309.00071).
- **Attention competition:** Many irrelevant tokens create interference. Even if the correct token is visible, its attention score must beat distractors.
- **Representation compression:** Each layer compresses many possible facts into fixed-width vectors. Small models have less room for simultaneous evidence, aliases, entities, and chains.
- **Retrieval versus reasoning:** A model may retrieve a literal key-value pair but fail multi-hop tracing, aggregation, contradiction resolution, or synthesis.
- **Recency and boundary bias:** Beginning/end tokens often get privileged by training distribution, instruction placement, attention sinks, or decoding dynamics. [StreamingLLM](https://arxiv.org/abs/2309.17453) shows that initial tokens can act as attention sinks even when not semantically important.
- **Compute tradeoff:** Longer context consumes inference budget. For a fixed latency or FLOP budget, one may choose more parameters and shorter context, fewer parameters and longer context, or external retrieval/compression.

So the answer is: yes, a small model can have an unusually large _visible_ context window, especially if it uses efficient attention, cheap KV cache, extrapolating positional schemes, or trained/finetuned long-context methods such as [LongLoRA](https://arxiv.org/abs/2309.12307). But a large _usable_ context window requires evidence that the model can reliably use information across positions, distractor densities, and reasoning forms. Advertised context length should be treated like channel bandwidth, not channel fidelity.

**Research Hypotheses / Experiments**

1. **Effective context decays with distractor entropy faster in small models.**<br>
   Test same architecture family across parameter sizes with fixed visible context. Vary distractor semantic similarity, answer position, and number of competing facts. Measure retrieval accuracy and calibration.

2. **Small models can gain long-context utility more from retrieval-shaped training than from longer windows alone.**<br>
   Compare position-extension-only finetuning against tasks requiring key-value retrieval, multi-hop tracing, aggregation, and contradiction resolution.

3. **Usable context is better predicted by "evidence survival curves" than max token length.**<br>
   Insert probes at multiple positions and layers; measure whether relevant facts remain decodable from hidden states after unrelated spans.

4. **Compression can outperform raw visibility for small models.**<br>
   Compare full-context prompting against learned or retrieval-based summaries under equal compute. Evaluate not just exact retrieval, but multi-hop QA and source-grounded synthesis.

## Agent 3: Hewitt, Carl

**Read-Only Explorer: Hewitt, Carl**

Yes: a small-parameter LM can have an unusually large _visible_ context window, because parameter count and context length are not the same resource. But "large usable attention" is a stricter claim. A model can be allowed to see 128k or 1M tokens while still failing to reliably use information buried in the middle, especially if it was not trained or adapted for that regime. "Lost in the Middle" is the cautionary primary result here: long-context models often perform best when relevant evidence is near the beginning or end, and degrade when it is in the middle of the prompt. See **"Lost in the Middle: How Language Models Use Long Contexts"**: https://arxiv.org/abs/2307.03172.

**How Visibility Works**

In dense causal attention, the prompt is tokenized, embedded, position-encoded, and run through a prefill pass that computes keys/values for every visible token. During decode, each new token attends over the cached K/V states of prior prompt and generated tokens. Thus a "context window" is the maximum number of tokens the runtime and model position scheme will accept and retain in attention state. It is not proof that the model has learned robust algorithms for global search, long-range binding, or multi-hop synthesis.

For a small model, the hard limits become:

- **Prefill compute:** dense attention prefill is quadratic in sequence length.
- **Decode memory bandwidth:** every generated token repeatedly reads the KV cache.
- **KV cache size:** grows linearly with layers, heads, head dimension, batch size, and context length.
- **Training distribution:** positional interpolation can make longer positions legal, but capability depends on adaptation data.
- **Capacity:** fewer parameters means fewer circuits for compression, retrieval, disambiguation, and long-range reasoning.

**Dense Attention Routes**

These preserve true token visibility, at least conceptually.

**FlashAttention / FlashAttention-2** keep exact attention but reduce GPU memory traffic using IO-aware tiling. They help training and prefill memory/runtime, but do not remove dense attention's quadratic arithmetic. See **"FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"** https://arxiv.org/abs/2205.14135 and **"FlashAttention-2"** https://arxiv.org/abs/2307.08691.

**PagedAttention / vLLM** does not make attention smarter; it makes serving feasible by paging KV cache blocks instead of requiring contiguous allocation. It reduces fragmentation and improves batching/throughput. See **"Efficient Memory Management for Large Language Model Serving with PagedAttention"** https://arxiv.org/pdf/2309.06180.

**MQA/GQA** reduce decode bandwidth by sharing keys/values across query heads. This preserves dense access over retained tokens, but changes the attention architecture. See **"Fast Transformer Decoding: One Write-Head is All You Need"** https://arxiv.org/abs/1911.02150 and **"GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints"** https://arxiv.org/abs/2305.13245.

**RoPE extension methods** make longer positions usable with limited fine-tuning. **Position Interpolation** extends LLaMA-style RoPE models by scaling positions into the trained range: https://arxiv.org/abs/2306.15595. **YaRN** reduces the training needed for context extension and reports long extrapolation: https://arxiv.org/abs/2309.00071. These are visibility enablers, not guarantees of deep usefulness.

**Approximate / Sparse Attention**

These increase reachable length by reducing which tokens can directly interact.

**Longformer** combines local sliding windows with selected global tokens, turning attention into near-linear scaling for long documents: https://arxiv.org/abs/2004.05150. **BigBird** uses local, random, and global sparse patterns and gives theoretical expressivity results while reducing quadratic cost: https://arxiv.org/abs/2007.14062. These are not full dense attention; they are structured approximations. They help train-time and prefill costs, but can miss arbitrary long-distance dependencies unless the sparse pattern routes them.

**StreamingLLM** keeps recent tokens plus initial "attention sink" tokens, enabling stable streaming beyond the original window without fine-tuning: https://arxiv.org/abs/2309.17453. This is useful for continuity, but it is not true global recall over all prior tokens.

**KV Eviction / Compression**

These operate mostly at serving time.

**H2O** keeps recent tokens plus "heavy hitter" tokens that dominate attention, reducing KV memory and improving throughput: https://arxiv.org/abs/2306.14048. **Scissorhands** similarly relies on persistence of token importance and keeps a fixed KV budget: https://arxiv.org/abs/2305.17118. **SnapKV** selects important prompt positions per head from an observation window, reporting strong speed/memory improvements on long inputs: https://arxiv.org/abs/2404.14469.

These are approximated attention over a retained subset. They reduce KV memory, memory bandwidth, and decode cost. They can preserve quality when attention is sparse in practice, but they can fail on adversarial tasks where the needed token looked unimportant early.

**KIVI** quantizes KV cache to 2-bit asymmetric formats, reducing memory without changing which tokens are retained: https://arxiv.org/abs/2402.02750. This is closer to compressed dense attention than eviction, but still approximate numerically.

**Recurrent / Compressed Memory**

These distinguish "remembering" from "attending."

**Transformer-XL** reuses hidden states from prior segments, extending dependency beyond fixed windows and reducing evaluation cost: https://arxiv.org/abs/1901.02860. **Compressive Transformer** adds compressed past memory: https://arxiv.org/abs/1911.05507. These offer recurrent state, not full visibility into every prior token. They help long streams but force lossy summarization.

**Mamba** and selective state-space models replace attention with recurrent state that scales linearly and can handle very long sequences efficiently: https://arxiv.org/abs/2312.00752. But this is not attention over visible tokens; it is learned state propagation. Good for throughput and long signals, risky for exact retrieval unless trained for it.

**Retrieval / External Memory**

RAG and RETRO decouple parametric size from knowledge and context. **RAG** combines a generator with non-parametric retrieved memory: https://arxiv.org/abs/2005.11401. **RETRO** shows a retrieval-enhanced transformer can match much larger models on some LM metrics using far fewer parameters by conditioning on retrieved chunks from a huge database: https://arxiv.org/abs/2112.04426.

This is not a large attention window. It is external memory injection. The model sees only retrieved chunks, not the whole corpus. It reduces prompt length and parameter memorization pressure, but adds retriever quality, index latency, freshness, and provenance constraints.

**Bottom Line**

A small model can have a huge advertised context via RoPE extension, FlashAttention, paged KV, GQA/MQA, and KV compression. It can have a huge _effective_ context via sparse attention, recurrent memory, retrieval, or controller-driven chunking. But "usable attention" depends on task shape. Exact dense attention preserves maximum theoretical access but is expensive. Approximate attention and memory systems buy scale by deciding what not to look at. Retrieval buys scale by moving selection outside the model.

**Research Hypotheses / Experiments**

1. **Small dense model plus strong KV systems can beat larger short-context models on exact-evidence tasks.**<br>
   Test a 1B-3B RoPE-extended dense model with FlashAttention, GQA, paged KV, and KIVI against 7B short-context baselines on Needle-in-a-Haystack, RULER-style key-value retrieval, and long-document QA.

2. **Hybrid retrieval plus short dense windows will outperform huge raw context for small models.**<br>
   Compare full 128k prompting versus retrieve-rerank-pack into 8k/16k for the same small model. Measure accuracy, latency, token cost, and citation fidelity.

3. **KV eviction policies fail predictably on delayed-salience prompts.**<br>
   Construct prompts where crucial evidence appears unimportant until a late question. Compare H2O, Scissorhands, SnapKV, sliding window, and full KV retention.

4. **Controller chunking can turn weak long attention into usable long context.**<br>
   Build a controller that chunks, summarizes, indexes, and rehydrates evidence into a small model's active window. Evaluate against raw long-context prompting on multi-hop synthesis and codebase-navigation tasks.

## Agent 4: Simon, Herbert

No files edited.

A small-parameter LM can expose a very large context window because "context" is mostly runtime state, not stored knowledge. Parameters are the fixed policy; the prompt/KV cache is temporary working material. In a causal Transformer, each new token forms a query over keys/values from prior visible tokens, with positional encodings telling the model where those tokens sit. That is interface capacity: the model can receive and attend over N tokens. It is not the same as behavioral use: selecting the right evidence, ignoring distractors, composing remote facts, and spending enough computation to do so.

The strongest distinction is:

- **Visible tokens:** accepted by tokenizer/runtime and represented in activations or KV cache.
- **Useful tokens:** tokens that measurably improve task success after controlling for position, distractors, task complexity, latency, and cost.

Modern claims show the gap. Microsoft's Phi-3 Mini-128K is a 3.8B model offered in a 128K-token variant, and LongRoPE reports extending pretrained LLMs to 2,048K tokens by changing positional scaling plus limited long-context tuning. ([microsoft.com](https://www.microsoft.com/en-us/research/publication/phi-3-technical-report-a-highly-capable-language-model-locally-on-your-phone/)) ([arxiv.org](https://arxiv.org/abs/2402.13753)) Gemini 1.5 reports near-perfect retrieval beyond 10M tokens, but it is a frontier-scale system, not proof that small models reason over millions of tokens. ([arxiv.org](https://arxiv.org/abs/2403.05530)) RULER is the useful corrective: vanilla needle-in-haystack is often too easy, and many models that claim 32K+ context drop sharply when task complexity rises. ([arxiv.org](https://arxiv.org/abs/2404.06654)) "Lost in the Middle" found strong position effects: models often do best when relevant evidence is near the beginning or end, and worse in the middle. ([arxiv.org](https://arxiv.org/abs/2307.03172))

The older lens says this is a bounded-rationality problem, not just a storage problem. Simon framed rational choice under limited computational ability. ([rand.org](https://www.rand.org/pubs/papers/P365.html)) LSTM attacked long time-lag learning with gated memory; Memory Networks and Neural Turing Machines separated controller from external memory; Transformer-XL added segment recurrence to reduce fixed-window fragmentation. ([cri.minesparis.psl.eu](https://www.cri.minesparis.psl.eu/people/silber/cours/2025/nlp/bib/HochreiterS1997.pdf)) ([arxiv.org](https://arxiv.org/abs/1410.3916)) ([arxiv.org](https://arxiv.org/abs/1410.5401)) ([arxiv.org](https://arxiv.org/abs/1901.02860)) Modern long-context LMs are the same old question with a larger scratchpad: can the controller use memory under compute limits?

The tradeoff is sharp. Full self-attention is expensive on long sequences; FlashAttention reduces memory traffic and enables longer contexts, but the underlying long-sequence burden remains real. ([arxiv.org](https://arxiv.org/abs/2205.14135)) Smaller models reduce layer/hidden-size cost, making big windows cheaper, but they may have weaker attention control, world knowledge, abstraction, and multi-hop reasoning. State-space/recurrent alternatives such as Mamba improve sequence-length scaling, but even that paper notes content-based reasoning is the hard part. ([arxiv.org](https://arxiv.org/abs/2312.00752))

Concrete measurement plan:

- **Retrieval accuracy by position:** accuracy as a curve over normalized position `p = token_index / context_length`, across 4K, 16K, 32K, 64K, 128K. Report area under the position curve, middle-window accuracy, and begin/end bias.
- **Distractor robustness:** hold answer evidence fixed while adding semantically similar decoys, contradictory snippets, stale versions, and instruction-like distractors. Report accuracy versus distractor density.
- **Multi-hop over distance:** require two to five facts placed far apart, with answer impossible from any one fact. Report hop accuracy by max span and average pairwise distance.
- **Latency/memory per successful task:** `p95_latency`, `prefill_time`, `decode_time`, peak VRAM/KV-cache size, and cost per correct answer.
- **Parameter-normalized utility:** `(task_success_auc_over_lengths * task_complexity_score) / parameter_count`, optionally divided by dollar or joule cost. This asks whether the small model is actually efficient, not merely impressive for its size.

Expected failure modes: lost-middle retrieval, recency overuse, instruction hijack from irrelevant long-context text, false synthesis from decoys, brittle exact-match retrieval without reasoning, degraded short-context quality after RoPE/context extension, and "answerable only when prompted with the right search strategy."

**Research Hypotheses**

1. A 3B-4B long-context model will maintain high single-needle retrieval to 128K but collapse faster than larger models on multi-hop tasks once evidence spans more than 25%-50% of the window.
2. LongRoPE-style extension improves visibility more than reasoning; gains should be largest on retrieval and weakest on contradiction resolution and remote evidence synthesis.
3. Parameter-normalized utility will favor small long-context models at low distractor density, but larger models once distractors are semantically close or hops exceed two.
4. A recurrent or external-memory scaffold around a small model will beat raw 128K prompting on latency/memory per successful multi-hop task, even if raw prompting wins on simple retrieval.

# Findings: High-Attention, Low-Parameter Models

Dispatch: `2026-06-29-high-attention-low-parameter-models`

## Answer

Small-parameter models can expose large visible context windows because parameter count and accepted context length are separate resources, with examples in the transcript including 1B-3B/3.8B models advertised around 128K tokens ([research.md:L14](research.md#L14), [research.md:L44](research.md#L44), [research.md:L210](research.md#L210)). That does not establish large usable context: usable context is the behavioral ability to retrieve, bind, and reason over evidence under position bias, distractors, and task complexity ([research.md:L36-L39](research.md#L36-L39), [research.md:L84-L92](research.md#L84-L92), [research.md:L203-L210](research.md#L203-L210)). Strict big attention should mean dense retained-token attention, where every retained token can directly score every prior token; it remains costly because dense prefill scales roughly quadratically in sequence length, decode attention and KV cache grow with length, and FlashAttention/PagedAttention improve implementation or serving without making far evidence semantically easier to use ([research.md:L20-L34](research.md#L20-L34), [research.md:L40-L43](research.md#L40-L43), [research.md:L137-L145](research.md#L137-L145)). Retrieval, cache engineering, recurrence, compression, sparse attention, and positional extension are neighboring mechanisms that can increase visibility or effective memory, but they are not synonyms for strict dense big attention ([research.md:L46-L64](research.md#L46-L64), [research.md:L147-L179](research.md#L147-L179), [research.md:L181-L183](research.md#L181-L183)). The clean lane is therefore not a novelty claim about any known mechanism; it is an empirical harness for parameter-normalized usable context under position, distractor, reasoning, KV-policy, and raw-context-versus-retrieval stress ([research.md:L70-L79](research.md#L70-L79), [research.md:L216-L224](research.md#L216-L224)).

## Definitions

- **Big context:** a large accepted input window or addressable prompt length, not proof of reliable use ([research.md:L36-L39](research.md#L36-L39), [research.md:L125-L128](research.md#L125-L128)).
- **Strict big attention:** dense causal attention over retained tokens, preserving direct pairwise visibility while carrying `O(L^2)` prefill, `O(L)` decode attention, and `O(L)` KV-cache pressure ([research.md:L20-L34](research.md#L20-L34), [research.md:L40-L43](research.md#L40-L43)).
- **Sparse/approximate attention:** reduced interaction graphs such as local/global/random patterns that improve scaling while choosing which interactions are cheap or reachable ([research.md:L46-L50](research.md#L46-L50), [research.md:L149-L155](research.md#L149-L155)).
- **KV cache:** retained key/value state for visible tokens; it grows with context length, layers, KV heads, head dimension, precision, and batch size ([research.md:L20-L24](research.md#L20-L24), [research.md:L127-L134](research.md#L127-L134)).
- **Positional extension:** RoPE/ALiBi/interpolation-style mechanisms that make long positions addressable, without removing attention/KV cost or guaranteeing reasoning ([research.md:L52-L56](research.md#L52-L56), [research.md:L147-L148](research.md#L147-L148)).
- **Retrieval/external memory:** RAG/RETRO-style selection from an index, where the model sees retrieved chunks rather than attending over the whole corpus ([research.md:L58-L60](research.md#L58-L60), [research.md:L175-L179](research.md#L175-L179)).
- **Recurrent/state memory:** reused or learned state that extends history through compression, not exact attention over every prior token ([research.md:L62-L64](research.md#L62-L64), [research.md:L167-L173](research.md#L167-L173)).
- **Usable context:** measured improvement from evidence across positions after controlling for distractors, task complexity, latency, and cost ([research.md:L203-L209](research.md#L203-L209), [research.md:L216-L224](research.md#L216-L224)).
- **Parameter efficiency:** task utility normalized by parameter count, optionally also by dollar or energy cost ([research.md:L221-L222](research.md#L221-L222)).

## Already Owned vs Research

The visible/usable distinction, dense-attention cost story, positional extension families, GQA/MQA, FlashAttention/PagedAttention, sparse/windowed/global attention, KV eviction/compression, RAG/RETRO, controller memory, and recurrent/state-space alternatives should be treated as precedent rather than owned novelty ([research.md:L24-L34](research.md#L24-L34), [research.md:L46-L64](research.md#L46-L64), [research.md:L137-L179](research.md#L137-L179)). What remains buildable as owned work is the exact measurement bundle: fixtures, metrics, baselines, and kill criteria for parameter-normalized usable context across position, distractors, reasoning, KV policy, and retrieval-versus-raw-context comparisons ([research.md:L70-L79](research.md#L70-L79), [research.md:L185-L197](research.md#L185-L197), [research.md:L216-L224](research.md#L216-L224)).

## Verdict Matrix

| candidate                                   | owner/precedent                                                                                                                                                                                                         | witnessed? |  sound? | verdict                                             |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------: | ------: | --------------------------------------------------- |
| Small model with large visible context      | Precedent: examples include Llama 3.2 1B/3B and Phi-3 mini 128K in the transcript ([research.md:L44](research.md#L44), [research.md:L210](research.md#L210)).                                                           |        Yes |     Yes | Real as visibility; not evidence of full usability. |
| Visible vs usable context distinction       | Precedent: all explorer lanes distinguish accepted tokens from behavioral use ([research.md:L36-L39](research.md#L36-L39), [research.md:L84-L92](research.md#L84-L92), [research.md:L203-L210](research.md#L203-L210)). |        Yes |     Yes | Keep as core framing, not novelty.                  |
| Strict dense big attention                  | Precedent: dense attention preserves direct token-token access but carries length-scaling costs ([research.md:L20-L34](research.md#L20-L34), [research.md:L40-L43](research.md#L40-L43)).                               |        Yes |     Yes | Valid definition; costly baseline.                  |
| Positional extension as big attention       | Precedent: RoPE/ALiBi/interpolation/YaRN/LongRoPE extend addressability, not guaranteed reasoning ([research.md:L52-L56](research.md#L52-L56), [research.md:L147-L148](research.md#L147-L148)).                         |        Yes |      No | Reject as synonym; classify as visibility enabler.  |
| Flash/Paged/GQA/MQA as big attention        | Precedent: these improve IO, serving, or KV bandwidth, not semantic far-token use ([research.md:L24-L34](research.md#L24-L34), [research.md:L141-L145](research.md#L141-L145)).                                         |        Yes | Partial | Keep as systems levers, not usability proof.        |
| Sparse/windowed/global attention            | Precedent: reduced routing graph improves scaling while limiting arbitrary pairwise access ([research.md:L46-L50](research.md#L46-L50), [research.md:L149-L155](research.md#L149-L155)).                                |        Yes | Partial | Neighbor mechanism; benchmark separately.           |
| KV eviction/compression                     | Precedent: retained subsets or quantized cache reduce memory and bandwidth, with delayed-salience failure risk ([research.md:L157-L165](research.md#L157-L165), [research.md:L193-L194](research.md#L193-L194)).        |        Yes | Partial | Useful policy class; must stress adversarially.     |
| RAG/RETRO/external memory                   | Precedent: external selection injects chunks rather than attending over the corpus ([research.md:L58-L60](research.md#L58-L60), [research.md:L175-L179](research.md#L175-L179)).                                        |        Yes | Partial | Strong comparator; not raw big attention.           |
| Recurrent/state memory                      | Precedent: recurrence/state extends streams through compressed state, not exact full-token visibility ([research.md:L62-L64](research.md#L62-L64), [research.md:L167-L173](research.md#L167-L173)).                     |        Yes | Partial | Separate architecture lane.                         |
| Parameter-normalized usable-context harness | Precedent inputs exist; exact bundle/fixtures may be built as project-owned measurement work ([research.md:L216-L224](research.md#L216-L224), [research.md:L226-L231](research.md#L226-L231)).                          |   Proposed |     Yes | Best research lane.                                 |

## Minimal Experiment Harness

Each claim should ship with a witness tuple: `model size + context length + attention/memory mechanism + task + baseline + metric + kill criterion`.

| suite                          | witness tuple                                                                                                                                                                                                                                                                                                                                                                     | kill criterion                                                                                                                                                                                                                                  |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Visible-useful gap             | `1B-3B long-context dense/GQA model + 8K/32K/128K + retained KV + passkey, key-value retrieval, multi-hop QA, adversarial middle evidence + larger short-context baseline + position AUC/middle accuracy` ([research.md:L72-L75](research.md#L72-L75), [research.md:L218-L220](research.md#L218-L220)).                                                                           | Kill any claim of large usable context if single-needle succeeds but middle-position or multi-hop accuracy collapses relative to baseline ([research.md:L92-L103](research.md#L92-L103), [research.md:L224-L230](research.md#L224-L230)).       |
| Compute/KV bottleneck          | `1B-4B dense/GQA model + 8K/32K/128K + FlashAttention/PagedAttention/KV cache + fixed generation task + short-context or larger-model baseline + p95 latency, prefill time, decode time, peak VRAM, throughput` ([research.md:L72-L73](research.md#L72-L73), [research.md:L131-L145](research.md#L131-L145), [research.md:L221-L222](research.md#L221-L222)).                     | Kill deployability claims when KV memory/bandwidth or prefill latency dominates successful-task cost at target length ([research.md:L22-L34](research.md#L22-L34), [research.md:L101-L103](research.md#L101-L103)).                             |
| Distractor entropy             | `same architecture family across parameter sizes + fixed visible window + dense or GQA attention + answer evidence with similar decoys, contradictions, stale versions, instruction-like distractors + no-distractor baseline + accuracy/calibration versus distractor density` ([research.md:L107-L108](research.md#L107-L108), [research.md:L219-L224](research.md#L219-L224)). | Kill robustness claims when semantically close distractors erase gains from longer context or small models degrade faster than larger baselines ([research.md:L97-L101](research.md#L97-L101), [research.md:L228-L230](research.md#L228-L230)). |
| Raw context vs RAG             | `small long-context model + raw 128K dense prompt vs retrieve-rerank-pack into 8K/16K vs hybrid + long-document QA and source-grounded synthesis + accuracy, latency, token cost, citation fidelity` ([research.md:L78-L79](research.md#L78-L79), [research.md:L190-L191](research.md#L190-L191)).                                                                                | Kill raw-context preference if retrieval/compression wins on accuracy-per-cost or citation fidelity under equal compute ([research.md:L116-L117](research.md#L116-L117), [research.md:L221-L222](research.md#L221-L222)).                       |
| KV eviction/compression stress | `1B-3B long-context model + 32K/128K + full KV, sliding window, H2O, Scissorhands, SnapKV, KIVI + delayed-salience prompts + full-retention baseline + accuracy, latency, peak KV memory` ([research.md:L157-L165](research.md#L157-L165), [research.md:L193-L194](research.md#L193-L194)).                                                                                       | Kill safe-eviction claims if crucial evidence is evicted or downweighted before late questions reveal its relevance ([research.md:L161-L163](research.md#L161-L163), [research.md:L193-L194](research.md#L193-L194)).                           |

## Near-Term Recommendation

Build the parameter-normalized harness first, using dense retained-KV attention as the strict baseline and treating positional extension, sparse attention, KV policies, retrieval, and recurrent/controller memory as separate intervention arms ([research.md:L40-L43](research.md#L40-L43), [research.md:L58-L64](research.md#L58-L64), [research.md:L181-L183](research.md#L181-L183)). The first release should prioritize falsifiable curves over mechanism novelty: position AUC, middle-window accuracy, distractor-density decay, multi-hop span accuracy, latency/KV cost per correct answer, and parameter-normalized utility ([research.md:L216-L224](research.md#L216-L224)).

## Closeout Notes

- `exit_reason`: `resolved`; the auditor approved `findings.md` with no revision required.
- `agents_spawned`: `{total: 10, tree: {explorer: 4, synthesizer: 1, skeptic: 3, writer: 1, auditor: 1, helpers: 0}, loops_used: 1}`.

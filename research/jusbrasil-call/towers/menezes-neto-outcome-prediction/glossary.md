# Glossary

Plain-language terms for reading this paper and mapping it to the Jusbrasil outcome-prediction product.

| Term | Meaning (in this paper's context) |
|---|---|
| **Legal Judgment Prediction (LJP)** | The task of predicting a court's decision (here, affirm vs reverse) from case text, before/without reading the actual ruling. The research family this paper belongs to. |
| **Outcome prediction / "Probabilidade de Êxito"** | The Jusbrasil product framing: estimating a litigant's/lawyer's probability of a favorable result. LJP is the academic name; "Probabilidade de Êxito" is the commercial framing. |
| **Juizados Especiais Federais (JEF) / Federal Small Claims Courts (FSCC)** | Brazilian federal small-claims courts handling high-volume, lower-value federal disputes (benefits, taxes, etc.). High case volume makes them the natural first target for prediction/automation. |
| **TRF5 (5a Região)** | The 5th Regional Federal Court, covering 6 NE Brazilian states. The single region this study's data comes from. |
| **Affirm vs Reverse** | The binary target: did the appellate panel uphold (affirm) or overturn (reverse) the first-instance decision. ~79% affirm in this data. |
| **ULMFiT** | "Universal Language Model Fine-tuning" — an LSTM-based (AWD-LSTM) transfer-learning method: pretrain a language model, then fine-tune a classifier. The **best performer** here (MCC 0.3688). |
| **BERT** | Transformer encoder pretrained with masked-language modeling. Here a Portuguese BERT, limited to 512 tokens, so long decisions are chunked and recombined via an LSTM. |
| **Big Bird** | A sparse-attention transformer built to handle long documents (up to 7,680 tokens here) — relevant because legal decisions are long. Pretrained from scratch on Portuguese corpora. |
| **MCC (Matthews Correlation Coefficient)** | A balanced classification metric (range -1 to +1; 0 = random) that stays honest under class imbalance. The paper's primary metric *because* the data is 79/21 imbalanced. |
| **Calibration** | Whether predicted probabilities match real-world frequencies (a "70% win" should win ~70% of the time). The paper reports MCC, **not** calibration — a gap that matters for a product showing probability numbers. |
| **Label leakage / data leakage** | When information not legitimately available at prediction time bleeds into training, inflating scores. Two faces here: (a) *temporal* leakage (future cases informing the model) — mitigated by the time-sequential split; (b) *label-construction* risk — the target was reverse-engineered from filenames/regex/metadata. |
| **Time-sequential split** | Splitting train/test by date rather than randomly, so the model is only ever tested on cases that occurred *after* its training data — the realistic deployment condition. |
| **BrCAD-5** | The dataset the authors released (765,602 appeals, full decision texts + labels) on Kaggle. A reusable public asset. |
| **OAB (Ordem dos Advogados do Brasil)** | The Brazilian bar association. Governs lawyer professional ethics — the body whose norms an outcome-probability product would have to reckon with. The paper does **not** engage OAB. |

## Agent 1 — official Numerai example-scripts code archaeology

## Turing return — executable code archaeology

Evidence frozen at official `master` SHA [`2447005`](https://github.com/numerai/example-scripts/tree/2447005b3f2af1fd45b883f2e63d1ebb80f75981/numerai), 2026-07-16. Inspection was static/read-only; large dataset downloads and training were not run.

### Surface inventory

- Four tutorials: [`hello_numerai.ipynb`](https://github.com/numerai/example-scripts/blob/2447005b3f2af1fd45b883f2e63d1ebb80f75981/numerai/hello_numerai.ipynb), `feature_neutralization.ipynb`, `target_ensemble.ipynb`, `example_model.ipynb`.
  - Inputs: NumerAPI `v5.3` features metadata and train/validation/live parquet; meta-model or benchmark-model parquet where relevant.
  - Outputs: validation plots/tables and cloudpickled prediction functions.
- Experiment harness:
  - Data assembly/downsampling: `agents/code/data/build_full_datasets.py`.
  - Config-driven LightGBM training: `agents/code/modeling/`, with expanding/blocked era CV and embargo in [`numerai_cv.py`](https://github.com/numerai/example-scripts/blob/2447005b3f2af1fd45b883f2e63d1ebb80f75981/numerai/agents/code/modeling/utils/numerai_cv.py).
  - Metrics: per-era CORR/MMC/BMC, benchmark correlation, mean/std/Sharpe/max drawdown, and recent-200-era summaries in [`numerai_metrics.py`](https://github.com/numerai/example-scripts/blob/2447005b3f2af1fd45b883f2e63d1ebb80f75981/numerai/agents/code/metrics/numerai_metrics.py).
  - Outputs: OOF prediction parquet plus machine-readable results JSON; analysis scripts emit comparison tables and plots.
  - Tests: pipeline metric-range integration test and exact target-transform unit tests.
- Dependencies: Python version matching Numerai Compute; `numpy`, `pandas`, `pyarrow`, `numerapi`, `numerai-tools`, `lightgbm`; notebooks additionally use `matplotlib`, `scipy`, `scikit-learn`, `seaborn`, `cloudpickle`, Jupyter/Colab. There is no repository dependency lock or installable package manifest.

### Candidate matrix

| Pattern | Verdict | Portability prerequisite | Mismatch / coupling |
|---|---|---|---|
| Ordered-era CV + horizon embargo + OOF predictions | **Transfer** | Map “era” to local decision time and derive embargo from the actual label horizon | Default expanding 5-fold CV silently skips the first fold because it has no training eras; only four folds contribute OOF. Numerai defaults `13` eras while notebooks use `4`; neither is portable without derivation. |
| Config → immutable prediction artifact → JSON metrics | **Transfer** | Local data adapter, result schema, dependency lock, reproducible environment | Current model factory supports only LightGBM; paths and defaults assume `numerai/v5.3`. |
| Performance plus uniqueness against a reference model | **Adapt concept** | An owned baseline/reference and a locally meaningful contribution test | Exact BMC/MMC and `numerai_corr` require Numerai scoring semantics and benchmark/meta-model predictions. |
| Recent-window metrics alongside full-history metrics | **Transfer** | Predeclare window size and promotion thresholds | “Last 200 eras” is tournament-specific and may encourage window selection after seeing results. |
| Feature exposure and proportional neutralization | **Adapt as diagnostic** | Interpretable local feature matrix, per-period exposure policy, before/after OOS evidence | Obfuscated feature groups are proprietary. Neutralization can erase useful signal. The tutorial’s MMC drawdown cell uses `rolling_max` instead of `mmc_rolling_max`, so that reported value is unreliable. |
| Rank-average models trained on auxiliary targets | **Adapt experiment only** | Genuinely distinct targets, leakage-safe OOF predictions, ensemble ablation | Numerai target names/semantics are proprietary; notebook evaluation is a single held-out workflow, not the harness’s full OOF protocol. |
| Versioned dataset materialization and ID/era alignment checks | **Transfer** | Local immutable snapshots, stable IDs, explicit missing-coverage policy | Download/build logic is NumerAPI/parquet-schema specific; benchmark coverage begins later than the full dataset and metrics drop unavailable rows. |
| Pickled upload function and compute deployment | **Reject for transfer** | None absent an equivalent trusted sandbox | Coupled to Numerai’s live-feature signature, cloudpickle ABI, API credentials, and compute image; unsafe as a general artifact boundary. |
| Live submissions or staking | **Reject / out of scope** | Separate authority and risk review | Tournament runtime and token economics, not validation infrastructure. |

### Explicit unknowns

- No clean-environment execution proves the current harness installs or runs from declared dependencies.
- No code here models local transaction costs, slippage, position sizing, portfolio construction, execution delay, or capital loss.
- Official docs state that the obfuscated dataset cannot be used outside the tournament; observed performance therefore does not evidence external investment performance. [Numerai overview](https://docs.numer.ai/)
- The appropriate local benchmark, time unit, embargo, recent-window length, and uniqueness metric remain design decisions—not values to inherit from Numerai.

## Agent 2 — official Numerai scoring and staking mechanism analysis

## Shannon, Claude — sourced mechanism map

Current official documentation supports a strong separation between measurement and economics.

| Mechanism | Measures or changes | Prerequisites / timing | Proof limit |
|---|---|---|---|
| CORR | Standalone rank quality against Numerai’s target. Predictions are rank-normalized, Gaussianized, and tail-weighted before correlation, emphasizing extreme predictions. | Aligned predictions and target; the transform is tailored to Numerai’s trading process. [CORR](https://docs.numer.ai/numerai-tournament/scoring/correlation-corr) | A proxy for target alignment, not realized portfolio return, calibration, robustness, or uniqueness. |
| MMC | Incremental contribution: prediction is orthogonalized against the current Meta Model, then its covariance with the target is measured. | Requires the contemporaneous Meta Model and target. It is peer/context dependent: changing ensemble composition or stake weights changes the baseline. [MMC](https://docs.numer.ai/numerai-tournament/scoring/meta-model-contribution-mmc) | High MMC means useful residual information relative to that baseline—not independent truth or standalone performance. High CORR can coexist with low MMC through redundancy. |
| FNC | Residual target correlation after removing linear exposure to Numerai features. | Requires the feature matrix and a declared neutralizer set/version. [FNC](https://docs.numer.ai/numerai-tournament/scoring/feature-neutral-correlation) | Detects linear feature dependence only; it does not establish nonlinear independence, causal signal, regime robustness, or portfolio neutrality. |
| Live scoring | Repeated out-of-sample evidence. A 20D2L round begins scoring after roughly four days, receives 20 accumulating updates, and resolves around one month later; 60D2L evidence resolves over roughly 12 weeks. Only final scores count toward live performance. | Timely repeated submissions; patience for target realization. [Scoring](https://docs.numer.ai/numerai-tournament/scoring) | Intermediate updates are provisional and share accumulating return data; they are not 20 independent experiments. |
| Validation discipline | Walk-forward, time-respecting evaluation with purged gaps; Numerai benchmarks purge 8 eras for 20-day targets and 16 for 60-day targets. | Era-aware splits, point-in-time features, leakage control, and treatment of overlapping forward targets. [Data](https://docs.numer.ai/numerai-tournament/data), [Models](https://docs.numer.ai/numerai-tournament/models) | Diagnostics repeatedly consulted during development become another training surface. Numerai explicitly warns that validation success need not generalize live. |

Documentation variance should be preserved rather than silently normalized: the scoring overview calls FNC neutralization against “all features,” while the FNC page identifies the displayed `FNCv3` as neutral to a medium V3 subset and describes a Spearman calculation. Any transferred metric therefore needs explicit target, neutralizer set, transform, and version—not merely the name “FNC.”

### Portable measurement abstractions

- Separate absolute performance from incremental contribution.
- Residualize a candidate against known exposures or an owned baseline ensemble, then score the residue.
- Keep raw score, contribution score, exposure score, and live evidence distinct.
- Use walk-forward, purged evaluation for overlapping targets.
- Treat diagnostics as a bounded final check and maintain an unstaked/paper live track record.
- Version targets, neutralizers, transforms, baselines, and metric definitions so historical results remain interpretable.

### Tournament-specific elements

Numerai’s obfuscated data, engineered targets, tail-weighted CORR transform, stake-weighted Meta Model, NMR payout/burn rules, and blockchain allocation contracts are local mechanism choices. Their exact forms do not transfer as general evidence standards.

### What staking establishes—and what it does not

Staking is optional; unstaked submissions receive the same scores and can build a live paper-trading record. Only staked submissions receive weight in the Stake-Weighted Meta Model. Numerai describes stake as a costly signal of a good-faith attempt, while explicitly saying trust is not the same as being right. [Staking](https://docs.numer.ai/numerai-tournament/staking)

Therefore staking may establish:

- willingness to bear tournament-defined loss;
- eligibility to influence Numerai’s ensemble;
- alignment with Numerai’s payout/burn mechanism.

It does **not** establish:

- predictive correctness or out-of-sample generalization;
- model calibration, causal validity, uniqueness, or robustness;
- investment ownership, hedge-fund participation, security status, or claim on fund returns;
- suitability for importing token incentives or exposing live capital elsewhere.

Current docs describe a transition to per-model, per-round atomic blockchain stakes with claims after resolution, while listing Numerai Tournament migration timing as TBD. That makes staking implementation status configuration-dependent and further weakens it as a portable design precedent. [Atomic Blockchain Staking](https://docs.numer.ai/numerai-tournament/atomic-blockchain-staking)

**Lane verdict:** transfer the measurement separation, residual-contribution test, versioned neutralization, purged walk-forward evaluation, and paper-live evidence loop. Reject transfer of staking, token economics, stake-weighted authority, or live-capital exposure.

## Agent 3 — local ownership, gap, and authority-boundary audit

Ashby adversarial audit — local evidence only; no files changed.

Core verdict: Numerai does not reveal a missing product layer. Most transferable ideas are already owned by Investiment Strategy’s quant-validation contract, while Ontologize should govern evidence and reuse—not calculate financial scores or attach capital to truth.

| Mechanism | Local status | Collision / gap verdict |
|---|---|---|
| Rank/correlation scoring | **Specified, unbuilt** | Pearson and Spearman lag surfaces already exist in the L0 algorithm contract. A Numerai-style CORR import would mostly rename existing work. [l0-method-design.md](/home/vrondelli/projects/investiment-strategy/docs/features/quant-delay-validation-mvp/l0-method-design.md:61) |
| OOS evaluation and anti-overfit | **Specified, unbuilt** | Purged/embargoed walk-forward testing, OOS-only promotion inputs, multiple-testing controls, PBO/Deflated Sharpe, baselines, placebos, ablations, cost stress, and parameter plateaus already cover the substantive need. [QUANT-VALIDATION-PLAYBOOK.md](/home/vrondelli/projects/investiment-strategy/docs/QUANT-VALIDATION-PLAYBOOK.md:435), [l0-method-design.md](/home/vrondelli/projects/investiment-strategy/docs/features/quant-delay-validation-mvp/l0-method-design.md:179) |
| Era/regime robustness | **Specified, unbuilt** | Crisis-vs-control periods, rolling regimes, nearby-lag stability, and daily/intraday sensitivity already play the role that era-wise scoring would serve. Adapt terminology only if it adds a concrete test obligation. |
| Incremental/meta-model contribution | **Partly specified, unbuilt** | “Current monolithic score” baseline plus feature ablation already tests incremental lift. MMC would be premature without an implemented aggregate model and could obscure the simpler owned question: does this delay feature add OOS lift? |
| Feature neutralization/exposure control | **Genuinely absent from L0** | Potential future diagnostic for broad factor/beta exposure, but not a direct transplant: existing baselines already reject broad beta and target momentum. Admit only as L1 evidence if it answers a named exposure question; do not make it a tournament-style headline score. |
| Multi-model ensemble | **Genuinely absent and premature** | The project intentionally validates two bounded delay lanes before multi-strategy optimization. Ensemble machinery should wait for multiple independently validated models. |
| Live leaderboard/tournament API | **Incompatible now** | The harness is research-only, daily, CLI/file-based, and excludes broker/live trading. [SPEC.md](/home/vrondelli/projects/investiment-strategy/docs/features/quant-delay-validation-mvp/SPEC.md:3), [PILOT-DECISIONS.md](/home/vrondelli/projects/investiment-strategy/docs/features/quant-delay-validation-mvp/PILOT-DECISIONS.md:24) |
| Staking/NMR economics | **Reject** | Financial stake is not evidence quality. It conflicts with research/paper-trading boundaries and must not become a proxy for `veracidade`, owner approval, or promotion authority. |

Implementation reality is stricter than the documents’ richness suggests: Investiment Strategy has no root `pyproject.toml`, `src/`, `tests/`, `configs/`, or `artifacts`; all QDV implementation and verification tasks remain `not-started`. [WORK-PACK.md](/home/vrondelli/projects/investiment-strategy/docs/features/quant-delay-validation-mvp/WORK-PACK.md:32)

Ontologize ownership boundary:

- It may represent CORR, neutralization, incremental lift, or live paper results as evidence-linked `N3 MetricObservation`s, then govern candidate/review/owner-decision/reuse.
- It does not own the financial calculation, model selection, portfolio decision, broker action, or staking economy.
- Its existing contracts already require evidence refs, denominator semantics, bounded claim labels, contradiction paths, privacy scope, and explicit owner approval. [OPTIMIZATION-CHAIN-METHOD.md](/home/vrondelli/projects/domainspec-core/projects/ontologize/OPTIMIZATION-CHAIN-METHOD.md:127)
- `veracidade` measures external evidential support; topology records commitment. Monetary stake would collapse those independent concepts. [DAG-AND-METRICS.md](/home/vrondelli/projects/domainspec-core/projects/ontologize/DAG-AND-METRICS.md:53)

Historical-lineage warning: Ontologize’s entrypoints disagree. `README.md` says the research dispatch is unexecuted; `NEXT.md` says it is closed and claims `ENGINE.md` was authored, but `ENGINE.md`, `pilots/`, and `GENERALIZATION.md` are absent. Treat product/promotion machinery as candidate design plus schemas/examples—not a deployed Ontologize runtime. Do not silently repair this drift during the Numerai transfer.

Recommended transfer envelope: retain only testable calculation patterns for Investiment Strategy; emit their results into Ontologize-compatible evidence records later. Reject staking, tournament incentives, and any claim that Numerai mechanics validate Ontologize itself.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| `./findings.md` | `derives` | The dispatch findings derive their candidate verdicts from these verbatim explorer returns. |

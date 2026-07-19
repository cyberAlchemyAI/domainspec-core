# Events: High-Attention, Low-Parameter Experiment Protocol

| Event | Produced By | Required Payload | Consumers |
| --- | --- | --- | --- |
| `DefineCompleted` | Invoke define | spec hash, glossary status, gaps | Invoke design |
| `ProtocolFrozen` | FreezeProtocol | protocol id/hash, approvals | corpus builder, admission |
| `CorpusMaterialized` | MaterializeCorpus | corpus/manifest hashes, validation | renderer, scorer reviewer |
| `ModelStackAdmitted` | AdmitModelStack | stack id, admitted cells, capacity receipts | trial planner |
| `ReadinessPassed` | readiness validator | protocol/stack/corpus ids, zero blockers | experiment owner |
| `PhaseStarted` | experiment owner | phase id, authorization, matrix hash | experiment harness |
| `TrialCompleted` | ExecuteTrialCell | run receipt handle | scorer, observer |
| `TrialFailed` | ExecuteTrialCell | typed failure receipt | repair owner, analysis |
| `PhaseAnalyzed` | AnalyzePhase | analysis/frontier handles | phase gate, reviewer |
| `PhaseClosed` | EvaluatePhaseGate | decision, rationale, residue | work-pack, Inventory candidate |

Events are append-only audit facts. They do not grant promotion authority.

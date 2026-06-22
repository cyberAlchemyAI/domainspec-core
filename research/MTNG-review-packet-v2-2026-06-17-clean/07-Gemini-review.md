MTNG Proposal Architectural Review

To: ResonantOS Dev Team

From: Outside Architectural Reviewer

Context: Review of 01-MTNG-build-spec.md using 02-technical-review-analog6.pdf and 06-Raptor mini review.md as context.
1. Executive Verdict

Strongly Recommended with Strict Boundary Conditions. The Modal Tonal Nodal Graph (MTNG) proposal is an exceptional architectural approach to a pervasive problem in agentic engineering: state-space collapse. Agents fail most often when forced to hold multiple conflicting intents, contexts, and validation metrics in a single flat runtime context. MTNG successfully decomposes these "mixed signals" into isolated, deterministic, contract-bound processing pipelines.

However, MTNG must never be implemented as an active, online runtime orchestration layer or control system in V1. If allowed to dynamically branch live user intent during execution, it will introduce massive non-deterministic latency, token overhead, and state management traps. It is highly valuable exclusively as an on-demand, batch-processed context distiller and artifact extraction pipeline.
2. Strongest Parts of the Proposal

    The "Branch Only on Boundary Shifts" Rule (Section 4): Restricting branching exclusively to changes in validation contracts, tools, context, output artifacts, safety boundaries, or contribution types prevents the graph from exploding based on text semantic length or user sentiment. This keeps the scope bounded and engineering-focused.

    The On-Demand/Sidecar Deployment Model (Section 8): Shifting away from an always-on ambient monitor to a discrete, startable process (e.g., mtng run --profile ...) respects local machine compute boundaries and establishes a strong data-minimization perimeter.

    The "Validator as a Safety Net" Recovery Model (Section 18): Using validation failures as a heuristic to detect structural misrouting (e.g., a provider routing branch failing because it lack endpoint evidence, thereby flagging a reroute candidate to a UX mode) is brilliant. It transforms standard quality gates into deterministic routing correctors.

    Decoupled Contribution Accounting (Section 12): Separating structural attribution (recording who clarified, triaged, or validated an artifact) from economic or governance valuation protects the V1 engineering scope from getting mired in community tokenomics arguments.

3. Weakest or Riskiest Parts

    The Metaphor Trap ("Tones"): The concept of "Tones" is currently too abstract. Defining it as a "detectable routing signature" using unstructured substrings like "I clicked around" makes it highly fragile. If built purely around regex or naive LLM classification, mode detection will experience significant misrouting loops.

    Rereouting Loop Instability (Section 18): The misrouting recovery loop ("return unresolved evidence to mode detection... optionally create a new branch") introduces a high risk of execution oscillation. If two validators both reject a mixed snippet, the engine could spin out of control unless bound by rigid execution limits.

    Undefined Graph State and Lifecycle Ownership (Section 15): The document defers the actual architectural storage of the graph state. Because MTNG is a graph that can recombine, the underlying data layer must explicitly track state branching, yet the specification fails to define whether this state sits in a shared database, a temporary memory context, or a persistent file structure.

4. Integration Questions for ResonantOS

Before writing a single line of code, the team must address these questions via the proposed Phase 0 Integration Mapping Pass:

    State Ownership: Which existing component owns the state of a running pipeline? If MTNG runs as an on-demand sidecar, should its runtime state be broadcasted over the ResonantOS Event Bus, or injected into the Blackboard architecture as a transient context surface?

    Guardian Core Boundary: How does MTNG pass authority signatures back to the Guardian Core? If an on-demand pass extracts a "functional agent improvement packet" or an "anti-bifurcation prompt update," what is the security handshake required for ResonantOS to ingest it?

    The Bridge Server Handshake: Since the Bridge Server connects the core system to local developer surfaces (like VS Code), can MTNG run headless inside a git hook, or does it require a continuous IPC connection to the main desktop shell?

5. V1 Pilot Recommendation: The "Post-Hoc Issue Packager"

To prove MTNG's value without introducing runtime risks to ResonantOS, the initial pilot should be a schema-only, CLI context-distiller for development handoffs.
Plaintext

mtng run --profile resonantos_debug_session \
  --terminal ./crash.log \
  --chat ./agent-transcript.json \
  --git-diff ./broken_state.diff \
  --out ./output/

The Walkthrough of the Pilot:

    Intake: Feed the pipeline a messy log where a developer struggled to fix a local agent routing failure.

    Processing: MTNG applies static rules and a highly lightweight local model to separate the environment information from the reproduction steps and the git diff evaluation.

    Validation: Run basic structural validators (e.g., verifying if the environment block actually extracted an OS and a node version).

    Synthesis: Output a completely clean, multi-faceted developer-issue-packet.md alongside an okf/ knowledge bundle.

This delivers an immediate productivity multiplier for the maintainers while safely validating the underlying branch and merge rules.
6. Sections to Remove, Defer, or Simplify

    DEFER COMPLETELY: Section 19 (Branch Pressure Scoring Weights)

        Why: Specifying hardcoded numbers (validation_contract_changed: 5, safety_boundary_changed: 6) is premature and artificial. We do not yet have empirical data on what constitutes "context pollution". For V1, simplify the logic to a binary configuration: Branch strictly when the expected output artifact type changes.

    SIMPLIFY: Section 5 & 17 (Tone & Mode Detection Levels)

        Why: Collapse the 5-tier detection system (suggested, candidate, active, validated, rejected) down to a simpler 3-state system: Proposed, Processing, and Closed. This drastically lowers the state tracking overhead required in the initial pilot database schema.

7. Questions to Take Back to the Maintainers

    Overhead Limits: What is the maximum acceptable latency and token budget for an on-demand run profile executing on a small, fully localized model architecture?

    OKF Standardization: How cleanly do the custom schemas of our output families (such as Contribution Records or Regression Checklists) align with the evolving specifications of Google’s Open Knowledge Framework (OKF)?

    Human Interactivity Loop: If an automated validator reports a failed_mode_mismatch, does the engine halt execution to wait for human intervention via a CLI prompt, or does it write its uncertainty to an audit log and move forward autonomously?


Gemini is AI and can make mistakes.
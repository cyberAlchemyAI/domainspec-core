---
tags: [robot-talks, multi-agent, orchestration, investigation, shareable]
node_type: knowledge-guide
is_session: false
status: complete
version: 1.0.0
last_updated: 2026-05-12
---

# Robot-Talks: Complete Guide

## A Comprehensive Framework for Multi-Perspective Investigations

> This is a consolidated reference guide for **robot-talks mode** — a structured approach to parallel multi-agent investigation where N participants take turns producing perspectives on a topic, with tensions surfaced explicitly rather than synthesized away. This document combines definitions, premises, decisions, examples, and operational rules into a single shareable resource.

---

## Quick Start

**Robot-talks is for:** When you need to understand what's wrong with a system across multiple layers (frontend, backend, infrastructure, user experience). You have cross-layer contradictions that no single investigator can see.

**What you get:** A discussion log that shows all perspectives, explicitly names tensions between them, traces every claim to evidence, and surfaces contradictions instead of hiding them.

**What it's not for:** Direct implementation. Robot-talks is an auditing tool. Implementation happens separately, informed by the tensions the investigation surfaced.

**Typical flow:** (1) Define scope → (2) Run parallel investigations → (3) Synthesize tensions → (4) Human review → (5) Implement based on findings.

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Premises — Why Robot-Talks Works](#premises--why-robot-talks-works)
3. [Decisions Governing the Mode](#decisions-governing-the-mode)
4. [Operational Rules](#operational-rules)
5. [How to Run a Robot-Talks Discussion](#how-to-run-a-robot-talks-discussion)
6. [Real-World Example](#real-world-example)
7. [Common Mistakes](#common-mistakes)
8. [Schema Relationships](#schema-relationships)

---

## Core Concepts

### What Is Robot-Talks?

Robot-talks is one of five **dispatch modes** within multi-agent strategy execution:

| Mode              | Description                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| `single`          | One agent, one task                                                      |
| `task-fan-out`    | N agents, N independent tasks                                            |
| **`robot-talks`** | **N participants, same topic, declared perspectives, surfaced tensions** |
| `sequential`      | Agent A → Agent B (piped output)                                         |
| `mixed`           | Combination of modes within one strategy                                 |

Robot-talks requires **at least 2 participants** (can be agents or the main thread), **a shared topic**, and **a discipline of declaring perspective before contributing**.

### Key Definitions

**Participant** — an actor that takes a turn (e.g., "backend-engineer-agent", "frontend-agent", "main-thread"). Each participant has a role and a declared perspective.

**Turn** — one participant's contribution. Opens with their id, perspective, and findings. Cites every load-bearing claim.

**Perspective** — the declared stance from which a participant speaks. Examples:

- "neutral state-of-play, no judgment, no recommendations"
- "epistemic-rigor critic with a bias toward surfacing ambiguity"
- "implementation/design-owner viewpoint"

**Tension** — a conflict between two findings, or between a finding and a documented contract. Tensions are _found_, not constructed.

**Synthesis** — identifying tensions across turns. NOT aggregating findings into consensus. Synthesis is the act of exposing contradictions.

**Discussion artifact** — the vault document produced by robot-talks. Its `node_type` is `discussion` and it preserves traceability.

### Why It Works

**Premise P-RT-1:** Cross-layer contradictions are invisible to single investigators. Backend engineer says "my code is correct"; frontend engineer says "mine too"; tension lives between them. Multiple perspectives see what one perspective cannot.

**Premise P-RT-2:** Signal quality depends on **scope design**, not just parallelization. If you cut the problem along the wrong boundaries, you get blind spots. Good scope = non-overlapping concerns + complete coverage.

**Premise P-RT-3:** Synthesis is tension discovery. Combining 10 findings into a summary destroys the information robot-talks was designed to surface. Findings without explicit contradictions are opinion aggregation, not synthesis.

**Premise P-RT-4:** Robot-talks is an auditing tool. Tensions identified here inform implementation _later_. You cannot reduce complexity you do not understand.

---

## Premises — Why Robot-Talks Works

### P-RT-1 — Cross-Layer Tensions Require Multi-Perspective Investigation

**Claim:** When a system spans multiple abstraction layers, a single investigator trades depth for breadth. Assigning bounded concerns to parallel agents, then synthesizing for contradictions, resolves this trade-off.

**Evidence:** POC (frontend-backend alignment, 2026-04-10): 4 agents identified 4 cross-layer tensions that would be invisible to single-agent investigation.

**Test:** This is false if a single agent investigating the same problem in the same time (90 min) produces equivalent or better results (fewer false tensions, more actionable contradictions).

### P-RT-2 — Scope Design Determines Signal Quality

**Claim:** Parallel agents reduce entropy _only if_ scope decomposition is correct. Good signal quality depends on:

- **Coverage:** the union of all scopes covers the investigation space
- **Independence:** concerns do not overlap

Given investigation space $S$ and decomposition $D = \{S_1, S_2, \ldots, S_k\}$:

$$Q(D) \propto \text{coverage}(D) \cdot \text{independence}(D)$$

Quality is maximized when concerns are complete and non-overlapping.

**Evidence:** POC used backend mutation, frontend error handling, API contract, and communication patterns (non-overlapping); synthesis was clean. File-based decomposition ("frontend agents" vs. "backend agents") created concern overlap and was abandoned before execution.

### P-RT-3 — Synthesis Is Tension Discovery, Not Aggregation

**Claim:** Combining agent reports is not synthesis. Synthesis is identifying _where findings contradict documented contracts or each other_. A robot-talk with 10 findings and 1 systemic tension is more valuable than one with 100 findings and no tensions.

If you cannot point to which agent finding contradicts which other finding, there is no tension. Tensions are found, not created.

**Evidence:** POC identified 4 specific contradictions (error inconsistency, idempotency mismatch, race condition, missing job tracking) with cross-agent evidence. One "tension" (API key difference) was validated as intentional design choice and discarded.

### P-RT-4 — Localization Precedes Reduction

**Claim:** Robot-talks are an _auditing tool_. You cannot invoke them to "fix this thing" — only to understand "what are all the ways this is misaligned?" Once tensions are mapped, implementation (a separate step) can address them.

**Evidence:** POC tensions (error standardization, idempotency-key header, pessimistic lock) directly informed implementation. Early implementation without full audit would have solved error inconsistency but missed idempotency + race condition, requiring a second pass.

### P-RT-5 — Robot-Talks Implement Pulsed Orchestration

**Claim:** The phases map to a pulsed orchestration model:

- **Descida (Top-Down):** Scope definition — fidelity dominates
- **Execução (Execution):** Parallel exploration — efficiency dominates
- **Subida (Bottom-Up):** Synthesis + Human Gate — entropy and fidelity dominate

**Evidence:** POC timing aligned with predictions (scope 10 min, exploration 40 min, synthesis 20 min, gate 20 min).

### P-RT-6 — Bounded Scope Is a Precondition

**Claim:** If you cannot state what an agent is _not_ investigating, you do not have a robot-talk. Every agent must have an explicitly stated scope _and_ an explicitly stated exclusion.

**Evidence:** POC: all 4 agents had explicit "out of scope" lists; synthesis was unambiguous. Initial planning without exclusions created confusion.

### P-RT-7 — Concerns Must Not Overlap; Evidence May

**Claim:** No two agents investigate the same question. But two agents may read the same artifact (e.g., an API contract) from different perspectives. Concern overlap creates synthesis ambiguity. Evidence overlap is often necessary for tension discovery.

**Evidence:** POC: backend mutation and API contract agents both read the same contract but from different questions; synthesis was clean. Two agents asking "is this idempotent?" created concern overlap; merged into single agent.

### P-RT-8 — Fidelity Increases as Information Rises

**Claim:** Every synthesis statement must be traceable to agent findings. Every finding must be traceable to code, documentation, or observable behavior. 100% traceability is required. Breaking this chain turns the process into opinion aggregation.

The chain — evidence → finding → tension → recommendation — must preserve a back-reference at each step.

**Evidence:** POC: all 4 tensions traced to specific code locations and documented expectations. One finding ("error handling differs") was excluded from synthesis until traced to backend error paths and frontend parsing logic.

---

## Decisions Governing the Mode

### D-1 — Robot-Talks Is a Dispatch Mode, Not a Sibling Concept

**Decision:** Robot-talks is one of five operational dispatch modes within multi-agent strategy execution. It is not a peer of "multi-agent strategy"; it is a value of the `mode` field.

**Why:** Treating robot-talks as a sibling produced ontology problems (duplicated rules, unspecified relationships to other modes). Naming it as a `mode` value resolves both: shared rules live in multi-agent strategy; mode-specific rules (declared perspective, tension-not-aggregation) live here.

**Consequence:** Any dispatch invoking robot-talks must do so via a multi-agent strategy declaration that names `mode: robot-talks`.

### D-2 — Each Turn Carries Participant ID, Declared Perspective, and Per-Claim Citations

**Decision:** Every turn opens with the participant's id, declared perspective, and every load-bearing claim within the turn is cited to its source as `[file.md:line-range]` or `[file.md §section]`.

**Why:** Without perspective declaration, downstream readers cannot distinguish a critic's stance from a state-of-play stance. Without citations, the chain evidence → finding → tension → recommendation breaks.

**Consequence:** A turn that omits its perspective declaration or contains uncited claims is non-conformant. Reviewers may reject the synthesis.

### D-3 — Synthesis Is Tension Discovery, Not Aggregation

**Decision:** Synthesis identifies _conflicts_ between turns or between turns and documented contracts, not summaries of agreement. A synthesis without explicit, evidence-traced tensions is a summary, not a synthesis.

**Why:** Permitting aggregation as "synthesis" would collapse robot-talks back into a more expensive variant of parallel investigation.

**Consequence:** Every synthesis must produce at least: (1) an enumerated tension, (2) a "RESOLVED" mark on a prior tension, or (3) a documented "no tensions found" note justified with evidence.

### D-4 — The Schema Chain Is: Axiom → Premise → Constitution → Skill

**Decision:** Robot-talks follows the canonical schema chain:

- **Premises** (this guide): working bets with explicit confidence levels
- **Constitution:** codifies premises as enforceable rules
- **Skill:** operationalizes the constitution

**Why:** The chain provides traceability and governance.

### D-5 — Discussion Artifacts Declare `node_type: discussion`

**Decision:** A vault artifact produced by robot-talks dispatch (multi-perspective log with declared turns and surfaced tensions) declares `node_type: discussion`.

**Why:** Different challenge response: a discussion says "it's multi-perspective debate — close it with a decision or escalate"; a discovery says "supersede it with a new discovery."

### D-6 — Robot-Talks Is an Auditing Tool, Not an Implementation Tool

**Decision:** Robot-talks dispatch is invoked to _understand_ (map tensions) a system, not to _fix_ one. Implementation actions are out of scope and must be performed in a separate session downstream of the human gate.

**Why:** Mixing investigation and implementation produces partial fixes that miss cross-layer tensions only visible after the full audit completes.

**Consequence:** A robot-talks dispatch that produces direct code edits or implementation plans within its own turns has overflowed the mode.

---

## Operational Rules

### R-1: Invocation Criteria

Robot-talks dispatch is invoked when:

1. You need to audit system-wide alignment (not fix individual bugs)
2. Tensions cross multiple abstraction layers
3. You have 2+ agents available or the main thread + 1+ agents
4. You have 60–120 minutes available

Robot-talks dispatch is NOT invoked for:

- Single-layer investigations (use `mode: single`)
- Parallel independent tasks (use `mode: task-fan-out`)
- Implementation (use `mode: sequential` or `mode: single`)

### R-2: Scope Definition (Descida Phase)

Before agents investigate:

1. Define the investigation question in one sentence
2. Decompose into N bounded agent concerns (typically N ≥ 2, N ≤ 5)
3. For each concern, state:
   - **In scope:** what this agent investigates
   - **Out of scope:** what this agent explicitly excludes
   - **Perspective:** the declared stance (e.g., "neutral state-of-play", "performance critic")
4. Verify: concerns are non-overlapping; union covers the question

**Common mistake:** Scope is too broad ("backend agent") instead of specific ("backend error handling consistency").

### R-3: Execution Discipline (Execução Phase)

Each agent produces a turn containing:

1. **Turn header:** `### [@participant-id, perspective]` or `### [@participant-id] - [Perspective: ...]`
2. **Stance:** 1–2 sentences declaring the agent's position
3. **Findings:** organized subsections (e.g., "Error Handling", "API Contracts", "State Management")
4. **Citations:** every load-bearing claim includes `[file.md:line-range]` or `[file.md §section]`
5. **Out-of-scope note:** 1 sentence confirming what the agent deliberately excluded

**Common mistake:** Claims without citations ("the code is inefficient") instead of traced findings ("lines 42–68 of handler.ts perform three redundant database round-trips").

### R-4: Synthesis Discipline (Subida Phase)

The synthesizer produces one section containing:

1. **Tensions raised:** a numbered list of cross-agent contradictions, with references to which turns conflict
2. **Resolution status:** mark each tension as **OPEN** or **RESOLVED** with evidence
3. **No consensus summary:** do not collapse perspectives into agreement
4. **Chain of evidence:** every tension must trace: agent1-finding → agent2-finding → documented-contract (or lack thereof) → tension name

**Common mistake:** "Both agree the API is poorly documented" (summary) instead of "Agent A found 3 contract mismatches in the code; Agent B found the docs describe different behavior; tension is contract-code mismatch" (tension).

### R-5: Human Gate

A human reviewer (role: design owner, architect, or project lead) must verify before the discussion is considered closed:

1. ✅ All perspectives are represented (no omitted agents)
2. ✅ Cited evidence actually supports each claim
3. ✅ Synthesis contains only tensions, not summaries
4. ✅ Each tension is traceable to evidence
5. ✅ Out-of-scope exclusions are defensible

If the gate detects issues, the discussion is returned to the synthesizer for revision.

### R-6: Implementation Gate (Optional)

After the human gate passes:

1. Document decisions about which tensions to address immediately vs. defer
2. Create implementation tasks with explicit links to the tension that triggered them
3. Do not attempt implementation within the robot-talks dispatch; invoke `mode: sequential` or `mode: single` separately

### R-7: Heartbeat / Partial Synthesis (30-Minute Timeout)

If an agent or the synthesizer runs longer than 30 minutes without an update:

1. Request a partial submission (findings + perspective so far, even if incomplete)
2. Continue with what is available rather than wait indefinitely
3. Mark partial contributions as such in the final discussion

---

## How to Run a Robot-Talks Discussion

### Phase 1: Descida (Top-Down Scope Definition) — 10–15 minutes

**Orchestrator does:**

1. Write investigation question (1 sentence)
2. Propose N bounded agent concerns
3. For each agent, write: scope, out-of-scope, perspective
4. **Run this past participants before execution** (2-minute review)

**Example scope definition:**

```
Investigation question: "Why is order-submission latency > 500ms despite frontend/backend optimization?"

Agent 1 (Backend performance agent):
- Scope: database queries, cache hits/misses, service-to-service calls
- Out of scope: network latency, frontend rendering
- Perspective: Performance engineer measuring throughput bottlenecks

Agent 2 (Frontend diagnostics agent):
- Scope: browser event loop, React rendering cycles, network request timing
- Out of scope: backend algorithm efficiency
- Perspective: Frontend performance analyst tracking user-perceived latency

Agent 3 (Infrastructure agent):
- Scope: network topology, DNS resolution, CDN behavior, observability gaps
- Out of scope: application code
- Perspective: Infrastructure ops focused on system visibility
```

### Phase 2: Execução (Parallel Execution) — 45–60 minutes

**Each agent independently:**

1. Investigates their concern
2. Gathers evidence (code, logs, documentation, metrics)
3. Produces one turn containing findings + citations
4. Keeps findings concise (agents should work in ~20–40 min)

**Orchestrator:** monitors timeline, invokes R-7 (heartbeat) if needed.

### Phase 3: Subida (Bottom-Up Synthesis) — 20–30 minutes

**Synthesizer does:**

1. Reads all agent turns
2. Identifies contradictions (turn A says X, turn B says ¬X, or both contradict documented contract)
3. Writes "Tensions raised" section (numbered list with cross-references)
4. Marks each tension: OPEN or RESOLVED
5. Ensures synthesis contains no new claims (only contradictions of findings already present)

**Example tension:**

```
**T-1: Response-time responsibility mismatch**
- Agent 1 (Backend) finds: "database query avg 50ms, caching returns < 2ms"
- Agent 2 (Frontend) finds: "network request takes 400–600ms; backend response time is 100–200ms of that"
- Agent 3 (Infrastructure) finds: "service-to-frontend round trip spans 3 regional data centers; latency adds ~250ms"
- Tension: Frontend observes 500ms latency; Backend reports database at 50ms; Infrastructure measures 250ms transit.
  Where is the remaining 200ms?
- Status: OPEN — requires deeper instrumentation to locate.
```

### Phase 4: Human Gate — 10–15 minutes

**Human reviewer verifies:**

1. All perspectives represented ✓
2. Evidence supports claims ✓
3. Synthesis is tension-focused ✓
4. Tensions are traceable ✓
5. Reasonable scope + out-of-scope decisions ✓

**Decision:**

- **PASS:** close discussion, document for downstream implementation
- **REVISE:** return to synthesizer with specific feedback
- **REJECT:** escalate to leadership if fundamental disagreement

---

## Real-World Example

### Investigation: Frontend-Backend Alignment (POC)

**Participants:**

- Agent 1 (@scribe): neutral state-of-play, documents findings
- Agent 2 (@backend-critic): performance + error-handling perspective
- Agent 3 (@frontend-critic): user-experience + contract perspective
- Main thread (@design-owner): implementation/design viewpoint

**Scope:**

- Question: "Why do users report 'error occurred' while backend logs success?"
- Agent 1: document current error-handling flow (code + behavior)
- Agent 2: trace backend error semantics and idempotency guarantees
- Agent 3: trace frontend error parsing and retry logic
- Out of scope: network layer, infrastructure observability

**Turn 1 (@scribe perspective: neutral state-of-play):**

```
### @scribe — Perspective: Neutral State-of-Play

Backend error definitions:
- HTTP 409: Conflict (mutation attempted on stale object)
- HTTP 503: Service unavailable (temporary failure)
- HTTP 400: Bad request (invalid input)
[backend/handler.ts:42–68]

Frontend error parsing:
- Shows "error occurred" for all 4xx/5xx responses
- No differentiation by status code
- Retry logic: exponential backoff for 5xx, no retry for 4xx
[frontend/api-client.ts:120–145]

Documented API contract:
- 409 responses are safe to retry (conflict means stale data)
- 503 responses should use exponential backoff
- 400 responses should not retry
[docs/api-contract.md §error-handling]

Tension noted: Frontend does not retry 409 conflicts despite contract.
```

**Turn 2 (@backend-critic perspective: performance + error semantics):**

```
### @backend-critic — Perspective: Backend Performance & Error Semantics

Backend idempotency guarantee:
- Mutations include client-generated trace-id
- Duplicate trace-ids are idempotent (same trace-id = same mutation result)
[backend/idempotency.ts:15–30]

Current behavior:
- Frontend does NOT send trace-ids on retry
- Each retry is treated as a new mutation
- Result: user retries conflict → new entry created instead of idempotent replay
[frontend/api-client.ts:125–132]

Contract gap:
- API contract says 409 conflicts are safe to retry
- But contract does NOT mandate trace-id requirement
- Developers are not told "retry only works if trace-id is sent"
[docs/api-contract.md — checked, trace-id requirement is missing]

Tension: Contract + code guarantee idempotency, but frontend has no way to achieve it.
```

**Turn 3 (@frontend-critic perspective: user experience + contract):**

```
### @frontend-critic — Perspective: User Experience & Contract Fidelity

Frontend observes:
- Mutation succeeds on backend (user sees success, entry created)
- Network timeout occurs
- Frontend retries (per backoff logic)
- Backend receives retry as new mutation (trace-id not preserved)
- Second entry created
- User sees "error occurred" after their initial success notification
[frontend/api-client.ts §retry-logic; backend logs from 2026-05-01]

User experience consequence:
- User submitted order, saw success, then error
- Database now has duplicate entry
- User is confused (was it created or not?)

Root cause chain:
1. Frontend does not generate or preserve trace-id on retry
2. Backend receives retry as new mutation, not as idempotent replay
3. Error response (409 conflict) reaches frontend
4. Frontend shows generic "error occurred"
5. User is left uncertain

Contract gap (confirms backend-critic's finding):
- API contract says conflicts are safe to retry
- API contract does NOT say trace-id is required for idempotent retry
- Frontend developers followed the documented contract and still got it wrong
```

**Synthesis:**

```
### Tensions Raised

**T-1: Idempotency is guaranteed but unreachable — Status: OPEN**
- Backend provides idempotency via trace-ids [backend/idempotency.ts:15–30]
- Frontend does not send trace-ids on retry [frontend/api-client.ts:125–132]
- API contract does not document trace-id requirement [docs/api-contract.md — verified absent]
- Result: retry mechanism exists but cannot achieve idempotency as promised
- Evidence trail: agent-2-finding ("trace-id requirement missing") + agent-3-finding ("user sees two entries") + backend code

**T-2: Contract inconsistency between documented + enforced behavior — Status: RESOLVED**
- Frontend observes: 409 conflicts returned despite initial success
- Backend observes: intentional, per design (pessimistic lock prevents race)
- Frontend has no way to distinguish "conflict because of race" from "conflict because of duplicate"
- Resolution: Design-owner decision — add trace-id to API contract and frontend client library
  Evidence: all three agents agree on the root cause; implementation fix identified

**T-3: Error messaging obscures root cause — Status: RESOLVED**
- Frontend shows generic "error occurred" for all error codes
- User cannot tell if conflict is intentional (idempotency), timeout (retry), or bad request (user error)
- Resolution: Frontend error handling should map error codes to user-friendly messages
  Evidence: agent-3 traced user confusion to error UI; agent-1 and agent-2 confirm intent
```

**Human Gate Decision:**

✅ **PASS**

- All three perspectives represented and non-overlapping
- Evidence is concrete (file paths, code line numbers, documented behavior)
- Tensions are actionable (specific contract edits, code changes needed)
- Out-of-scope (network layer) is justified
- Implementation tasks are clear: (1) update contract, (2) update client lib, (3) update error UI

---

## Common Mistakes

### Mistake 1: Overlapping Concerns (Breaks Synthesis)

**Wrong:** "Frontend agent" + "Backend agent"

- Both end up investigating "why is the latency high?"
- Both collect overlapping evidence
- Synthesis cannot distinguish legitimate contradiction from "we looked at different data"

**Right:**

- "Frontend rendering performance agent" (React cycles, event loop)
- "Backend query optimization agent" (database + cache)
- Concerns are non-overlapping; synthesis can identify cross-layer gaps

### Mistake 2: Missing Citations (Breaks Traceability)

**Wrong:** "The backend has poor error handling."

- No source; opinion
- Cannot verify or dispute

**Right:** "Backend error handler [handler.ts:42–68] returns HTTP 500 for validation errors, but HTTP 400 is semantically correct [RFC 7231]. All validation errors in this path should return 400 instead."

- Traceable to code
- Disputable with evidence
- Can be fixed

### Mistake 3: Aggregating Instead of Synthesizing

**Wrong:** "All three agents agree the system needs optimization."

- This is a summary
- Not synthesis
- No tension identified

**Right:** "Agent A (backend) found queries average 50ms. Agent B (frontend) observed 400ms total latency. Agent C (infrastructure) measured 250ms network transit. The 100ms gap is unaccounted for [open tension: where is it?]"

- Explicit contradiction
- Traceable finding
- Actionable

### Mistake 4: Implementing During Investigation

**Wrong:** Agent finds a bug, fixes it inline, includes code patch in their turn.

- Mixes investigation with implementation
- Misses other cross-layer tensions
- Partial fix

**Right:** Agent finds a bug, documents it, cites the code, stops. Separate dispatch implements the fix after synthesis completes.

### Mistake 5: No Out-of-Scope Declaration

**Wrong:** Agent investigates broadly without stating what they are NOT doing.

- Reviewer cannot verify completeness
- Synthesis cannot be sure concerns don't overlap

**Right:** Agent states: "Scope: database indexes and query planner. Out of scope: network layer, cache coherence, third-party service latency."

- Clear boundaries
- Can verify completeness
- Synthesis is unambiguous

---

## Schema Relationships

### The Epistemic Chain

Robot-talks fits the canonical schema chain:

```
Axiom (foundational truth)
    ↓ grounds
Premise (testable working hypotheses) ← [This guide + separate premise docs]
    ↓ codified as
Constitution (enforceable rules) ← [Separate constitution doc]
    ↓ operationalized by
Skill (executable artifact) ← [Slash command /robot-talks]
```

### This Guide's Place

This document consolidates:

- **Premises (P-RT-1 through P-RT-8):** why robot-talks works
- **Decisions (D-1 through D-6):** governance rules
- **Operational rules (R-1 through R-7):** how to execute the mode
- **Example:** real POC demonstration
- **Common mistakes:** what breaks synthesis

Separate artifacts implement:

- **Constitution:** detailed operational rules enforced by orchestrators
- **Skill:** the slash command that invokes the mode
- **Registry:** index of all robot-talks investigations conducted

---

## Frequently Asked Questions

### Q: How many agents do I need?

**A:** Minimum 2 participants (agent + main thread). Typically 3–4 agents work well. More than 5 makes synthesis expensive without proportional benefit.

### Q: What if agents disagree on facts?

**A:** That's a tension. Document which agent found what evidence and let synthesis surface the contradiction. Often one agent misread the code or both found different code paths with different behavior.

### Q: Can I use robot-talks for implementation?

**A:** No. Robot-talks is an auditing tool. Use it to understand what's wrong, then implement separately.

### Q: What's the difference between robot-talks and a code review?

**A:** Code review checks "is the code correct?" Robot-talks asks "do layers agree on what correctness means?" Robot-talks often finds cross-layer contradictions that individual code review misses.

### Q: How long does a typical robot-talks investigation take?

**A:** 90–120 minutes total: scope (10–15 min) + execution (45–60 min) + synthesis (20–30 min) + gate (10–15 min).

### Q: What if there are no tensions?

**A:** Document it. "All three agents independently verified that X is correctly implemented at all layers. No cross-layer contradictions found." This is valuable information and closes the investigation.

---

## Summary

Robot-talks is a structured investigation mode that:

1. **Decomposes** problems into bounded agent concerns
2. **Executes** in parallel, each agent investigating their concern
3. **Surfaces tensions** (contradictions across perspectives) rather than aggregating findings
4. **Preserves traceability** (evidence → finding → tension → recommendation)
5. **Stops at auditing** (does not implement; informs implementation later)

The mode works because it respects P-RT-2 (signal quality depends on scope design) and P-RT-3 (synthesis is tension discovery). Use it when you need to understand system-wide misalignment that no single layer can see.

---

## Additional Resources

For deeper reading, see the separate documents:

- **Robot-Talks Premises** (`robot-talks-premises.md`): detailed P-RT-1 through P-RT-8 with evidence
- **Robot-Talks Constitution**: operational rules and enforcement mechanisms
- **Example Discussion** (`robots-discussing.md`): full POC investigation showing all turns and synthesis

---

**Last updated:** 2026-05-12  
**Status:** Complete reference guide, shareable  
**Feedback:** Report issues or suggestions to the research team

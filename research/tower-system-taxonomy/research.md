# Tower System Taxonomy — Explorer Returns (verbatim)

## Explorer 1 — Hewitt (debate/scoring literature, L4 ownership)

ELO: owner = Chatbot Arena/LMSYS (Chiang et al. 2024, arXiv:2403.04132) on Elo (1978); moved to Bradley-Terry; "Elo Uncovered" (Boubdir 2023, arXiv:2311.17295, verify) audits robustness. use-mode BUILD-FROM-OWNED.
TOURNAMENT: no single owner; anchors LLM-Blender (Jiang 2023, arXiv:2306.02561), TourRank (verify arXiv), Arena-Lite, Auto-Arena, Knockout-LLM, Swiss-system. BUILD-FROM-OWNED.
ORACLE-CONSENSUS: SPLIT owners — self-consistency/majority-vote (Wang 2022, arXiv:2203.11171), LLM-as-a-Jury "Replacing Judges with Juries" (Verga 2024, arXiv:2404.18796 verify), ChatEval (Chan 2023), Universal Self-Consistency (Chen 2023 verify). NOT precedent-clean — a named composition of owned components; the 4-layer staged escalation (unanimous→supermajority→ELO-weighted→human-flag) may be novel as an integrated protocol. ALREADY-DEPLOYED (components) / NOVEL-ATTEMPT (staged escalation).
SYNTHESIS: owner = Mixture-of-Agents (Wang 2024, arXiv:2406.04692) aggregator layer; also LLM-Blender GenFuser, Self-Refine (Madaan 2023), debate→summary (Du 2023, arXiv:2305.14325 verify). BUILD-FROM-OWNED.
MOGT: NOT a standard named term (cutoff early 2025); most plausible = "Mixture of Ground Truths" (parallels MoA naming, fits adjudication register); almost certainly COINED. Closest prior = self-consistency (Wang 2022). NOVEL-ATTEMPT (must differentiate from self-consistency & MoA).
Cross-cutting: oracle-consensus ≈ majority-vote/self-consistency/LLM-as-a-jury (owned under 3 names); ELO and tournament overlap (Arena-Lite = sparsified Elo tournament); DPO (Rafailov 2023) + debate-disagreement→DPO pairs (Self-Improvement via Multi-Agent Debate 2025, verify) — not a scoring mode but interacts with L4.

## Explorer 2 — Ahrens (KM/notes/graph literature, L1/L2 + umbrella)

L1 traversable knowledge graph — owned under multiple names, all build-from-owned, persona-set is Tower's distinguishing add: Zettelkasten (Luhmann; Ahrens 2017); Concept Maps (Novak 1972/1998); Ontologies RDF/OWL (W3C 1999/2004); Knowledge Graphs (Google 2012, Wikidata, Nickel 2016); Pattern Language (Alexander 1977 — a traversable expert-knowledge graph with cross-refs).
L1 persona — HCI: goal-directed persona (Cooper 1999), Persona Lifecycle (Pruitt & Adlin 2006) model USERS not knowledge nodes → "persona anchored to a knowledge-graph node" PARTIAL/novel; deliberative role personas: Six Thinking Hats (de Bono 1985). build-from-owned (idiom) + novel-attempt (graph-anchoring).
L2 distill-build — owned: information extraction / KB population (OpenIE Etzioni 2008, NELL Carlson 2010). build-from-owned; persona-output target is the add.
L2 read-through — PARTIAL; antecedents syntopical reading (Adler & Van Doren 1940/1972) + Zettelkasten noting; NOT a single named method → integrated graph-persona accrual is Tower's claim. build-from-owned + novel-attempt.
L2 promote — no canonical named method; precedent-clean as a named construction mode. NOVEL-ATTEMPT (first obligation: distinguish from distill-build — input is pre-structured artifact, not raw text).
UMBRELLA NAMES: "Second Brain" (Forte 2022) = KILL, live brand. "Exocortex" = generic, no single owner, usable but generic. "Knowledge Base" = too generic. "Epistemic Graph" = in academic use (epistemic network analysis, Shaffer 2009, verify), GO as novel-attempt umbrella, differentiate from ENA. "Research Tower" = precedent-clean; recommend keep for L1–L2, separate umbrella for L1–L4.

## Explorer 3 — Spivak (in-repo structural verification)

Row1 L1 substrate+L2 distill-build => research-tower: PARTIAL. research-tower builds a markdown file scaffold (TOWER.md, levels/, glossary, definitions, claim ledger, related-work map) but the word "persona" never appears (no persona artifact) and there is NO queryable/traversable graph (related-work map is prose, not a graph object). distill is a SEPARATE sigil, not invoked by research-tower.
Row2 L2 read-through => NET-NEW: HOLDS. research-tower is fully agent/subagent-driven; no human-guided read-through path. Genuine net-new.
Row3 L4 tournament+elo => distill: PARTIAL. distill HAS Tournament mode + Proposer/Balancer pitch-off (qualitative multi-criteria), but NO ELO (word never appears), no oracle-consensus, no MOGT.
Row4 L3 debate+human gate => robot-talks: HOLDS. robot-talks = parallel multi-agent investigation + Phase-4 human gate. Caveat: it's a tension-DISCOVERY/audit tool, not a scoring engine.
Row5 L4 tension+aggregation(P7)+verdicts => constitution/research skill: HOLDS. P5 tension via check-tension; P7 aggregation rule; research skill has the GO/KILL verdict matrix; exit_reason vocabulary.
Row6 persona tension design => anti-bias-vector-composition: PARTIAL. It designs agent ANGLES (4 axes) for single-dispatch groups (ephemeral roles), NOT durable reusable personas; principle transfers, mechanism does not.
NET-NEW confirmations: (a) persona-as-artifact + library — CONFIRMED ABSENT; (b) traversable queryable graph — CONFIRMED ABSENT (markdown only); (c) scoring engine ELO+oracle-consensus+DPO — CONFIRMED ABSENT.
MISLABELS: (1) L4 elo/oracle/MOGT claimed as distill reuse = FALSE, genuinely net-new (only "tournament" maps). (2) L1 "persona set" claimed as research-tower = FALSE, net-new; split L1 into "graph" (partial reuse) + "persona set" (net-new). (3) L2 distill-build "inside research-tower" = FALSE, distill is a sibling sigil. (4) "persona tension design"=anti-bias overstates coverage.

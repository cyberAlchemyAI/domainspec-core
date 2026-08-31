# Chapter 1 Reader-Discovery Tournament — Verbatim Auditions

- Dispatch: `2026-08-26-lucifers-chapter-01-discovery-tournament`
- Candidate SHA-256: `8b33827b68d2761381cdc0f61b4c3f92bb2b4a80fea55137174424c358cb8d7d`
- Native run: `native-run-001`
- Receipt admission: PASS
- Worker authority: read-only

The three persisted task-result objects follow verbatim. They are audition evidence, not selected prose, reader-effect proof, manuscript acceptance, or publication authority.

## Subtractive restraint — spawn-0001

```json
{
  "task_status": "completed",
  "domain_gate_status": "not_evaluated",
  "artifacts": [
    {
      "ref": "receipts/subtractive-restraint.json",
      "delivery": "inline_receipt",
      "written": false,
      "role": "read-only passage audition"
    }
  ],
  "validation": {
    "declared_inputs_read": [
      "chapter-candidate",
      "voice-guide",
      "factory-config",
      "strategy-inventory-packet"
    ],
    "full_chapter_audited": true,
    "candidate_sha256": "8b33827b68d2761381cdc0f61b4c3f92bb2b4a80fea55137174424c358cb8d7d",
    "expected_sha256_match": true,
    "candidate_word_count": 3352,
    "configured_word_count_range": {
      "minimum": 2500,
      "maximum": 4500
    },
    "required_markers_present": "10/10",
    "forbidden_markers_present": "0/5",
    "required_markers_preserved_by_all_auditions": true,
    "continuity_preserved": [
      "transaction-first opening and 2:13 clock",
      "Mara's agreement, escape, station, and tracker-removal choices",
      "Elena's prior Light and voluntary amendment",
      "mundane-supernatural ambiguity",
      "sunrise clock, Michael request, and final symmetry reversal"
    ],
    "files_written": [],
    "reader_effect_status": "unproven",
    "manuscript_acceptance_status": "not_authorized",
    "evidence_emission_status": "not_required",
    "telemetry_status": "caller_owned"
  },
  "proposal": {
    "objective": "Remove post-discovery interpretation while preserving the minimum mechanics, tethered Lucifer voice, agency, danger, and clock needed for closure.",
    "mode": "tournament",
    "role_execution_path": "bounded role simulation inside the assigned subtractive-restraint audition",
    "recursive_rounds": {
      "completed": 2,
      "budget": 2,
      "round_1": "Locate interpretive tails whose removal leaves the discovery legible.",
      "round_2": "Restore only indispensable mechanics, voice, or clock pressure."
    },
    "tracks": [
      {
        "id": "hard-deletion",
        "claim": "Trust action, dialogue, and juxtaposition to carry meaning.",
        "balancer_objection_category": "meaning-loss",
        "reconciliation": "Eligible only where the adjacent scene still closes the causal or emotional turn."
      },
      {
        "id": "mechanics-only",
        "claim": "Compress interpretation into the smallest explicit rule or anomaly statement.",
        "balancer_objection_category": "reader-orientation",
        "reconciliation": "Retain one causal sentence where omission could obscure contract or app behavior."
      },
      {
        "id": "tethered-voice",
        "claim": "Keep one Lucifer line only when it sharpens person, rule, danger, choice, or time.",
        "balancer_objection_category": "voice-flattening",
        "reconciliation": "Preserve the strongest tethered line and remove its explanatory echo."
      }
    ],
    "optimization_point": "Five independent passage-level auditions. Further reduction would begin removing live mechanics, required markers, or the final symmetry rather than redundant interpretation.",
    "auditions": [
      {
        "id": "SR-01",
        "source_lines": "193-211",
        "operation": "delete interpretive thesis",
        "original_exact": "Mara looked unconvinced.\n\nGood. Thinking for herself was the entire point.\n\nMara looked toward the door again. The rain was growing heavier. Soon the underpass would flood, closing the quickest road out of the district.\n\nTime had begun charging interest.\n\n“I don’t care about angels,” she said. “I just want my sister back.”\n\nThere it was: humanity in one sentence.\n\nPeople like me prefer humanity in the plural. It turns suffering into philosophy. Mara had reduced Heaven, Hell, knowledge, and rebellion to one missing woman and one diminishing night.\n\nSingular love is inconvenient that way. It refuses to become an idea.\n\nGod, I love humans.\n\nI smiled. Mara shifted away from me.",
        "replacement_exact": "Mara looked toward the door again. The rain was growing heavier. Soon the underpass would flood, closing the quickest road out of the district.\n\nTime had begun charging interest.\n\n“I don’t care about angels,” she said. “I just want my sister back.”\n\nI smiled. Mara shifted away from me.",
        "proposer_claim": "Mara's rejection, the worsening rain, and Lucifer's unsettling smile already complete the turn; the humanity thesis explains what her line lets the reader discover.",
        "balancer_objection": {
          "category": "character-development",
          "detail": "The deletion removes Lucifer's explicit fascination with singular human love."
        },
        "reconciliation": "Accept deletion for audition. His smile preserves fascination without converting Mara's choice into his philosophical lesson.",
        "recomposition_proof": "The preceding parable now collides directly with Mara's concrete need, and the retained clock pressure carries the scene into acceptance."
      },
      {
        "id": "SR-02",
        "source_lines": "485-499",
        "operation": "delete thematic and comic echoes",
        "original_exact": "Ruth had once needed a Light. Tonight she repaid it with nine seconds and a coffee pot.\n\nA Light is seldom magnificent.\n\nTonight, it was boiling coffee, nine stolen seconds, and a debt remembered just in time.\n\nMara and I crossed the kitchen, passed through a storeroom, and emerged into an alley behind the café. Rainwater had already risen above my shoes.\n\nWhite leather.\n\nRuined.\n\nYou see what I sacrifice for humanity?\n\nA tragedy for after sunrise.",
        "replacement_exact": "Ruth had once needed a Light. Tonight she repaid it with nine seconds and a coffee pot.\n\nMara and I crossed the kitchen, passed through a storeroom, and emerged into an alley behind the café. Rainwater had already risen above my shoes.\n\nWhite leather.\n\nRuined.\n\nA tragedy for after sunrise.",
        "proposer_claim": "Ruth's action already demonstrates what a Light can be; repeating its ingredients halts the escape, while the final shoe line keeps vanity tethered to sunrise.",
        "balancer_objection": {
          "category": "theme-visibility",
          "detail": "Removing the aphoristic restatement may weaken the chapter's concrete definition of a Light."
        },
        "reconciliation": "Accept deletion for audition. The retained debt sentence explicitly names the Light and its repayment.",
        "recomposition_proof": "The escape proceeds immediately from Ruth's intervention to the alley, with one clock-aware Lucifer joke rather than two."
      },
      {
        "id": "SR-03",
        "source_lines": "571-583",
        "operation": "delete inferred preparation and approval",
        "original_exact": "I examined the timestamp.\n\nThe message had arrived tonight.\n\nIt had been scheduled three days earlier.\n\nElena had known this might happen before she disappeared.\n\nShe had planned for the possibility that her disappearance would fail, then built Mara a path through the wreckage.\n\nI began to like her.\n\nThe station was almost empty. A drunk slept beneath a timetable. Somewhere below us, a violinist played for an audience that had already gone home.",
        "replacement_exact": "I examined the timestamp.\n\nThe message had arrived tonight.\n\nIt had been scheduled three days earlier.\n\nElena had known this might happen before she disappeared.\n\nThe station was almost empty. A drunk slept beneath a timetable. Somewhere below us, a violinist played for an audience that had already gone home.",
        "proposer_claim": "The scheduled timestamp and Elena's foreknowledge reveal her preparation; restating the whole plan and recording Lucifer's approval closes discovery too tightly.",
        "balancer_objection": {
          "category": "relationship-signal",
          "detail": "The cut removes an explicit step in Lucifer's growing regard for Elena."
        },
        "reconciliation": "Accept deletion for audition. Elena's agency remains observable and does not need Lucifer's approval to validate it.",
        "recomposition_proof": "The evidence lands, receives one minimal inference, and returns to the exposed station without losing why Mara has a route."
      },
      {
        "id": "SR-04",
        "source_lines": "671-679",
        "operation": "delete explanatory metaphor extension",
        "original_exact": "“Lucifer, if you’re hearing this, the app has been compromised. Someone is collecting requests under your name.”\n\nMy amusement faded.\n\nThe screen was presentation. The promise behind it was mine. If someone was collecting requests under my name, they had not merely entered my system. They had put my word in their mouth.\n\n“If a client called Michael contacts you, do not answer. He doesn’t want a Light. He wants you to remember.”\n\nThe recording ended.",
        "replacement_exact": "“Lucifer, if you’re hearing this, the app has been compromised. Someone is collecting requests under your name.”\n\nMy amusement faded.\n\nThe screen was presentation. The promise behind it was mine.\n\n“If a client called Michael contacts you, do not answer. He doesn’t want a Light. He wants you to remember.”\n\nThe recording ended.",
        "proposer_claim": "The required presentation/promise line already makes the violation personal; the following system-entry and borrowed-mouth explanation repeats Elena's warning before Michael appears.",
        "balancer_objection": {
          "category": "stakes-intensity",
          "detail": "The shorter reaction may underplay how seriously Lucifer treats misuse of his promise."
        },
        "reconciliation": "Accept compression for audition. Fading amusement plus ownership of the promise supplies the stake without delaying Michael.",
        "recomposition_proof": "The required marker remains exact and now acts as the hinge directly into Elena's Michael warning."
      },
      {
        "id": "SR-05",
        "source_lines": "697-711",
        "operation": "compress anomaly explanation",
        "original_exact": "Mara read over my shoulder.\n\n“What does that mean?”\n\n“I don’t know.”\n\nIt was the first answer I had given her that needed no qualification.\n\nI had designed every field in Lucifer’s Lights. Clients submitted requests. I decided the price. There was no mechanism through which a client could offer me compensation.\n\nThere was also no client named Michael.\n\nThe station clock changed to 2:51.\n\nTwo hours and forty-seven minutes until sunrise.",
        "replacement_exact": "Mara read over my shoulder.\n\n“What does that mean?”\n\n“I don’t know.”\n\nI had designed every field in Lucifer’s Lights. A client could not offer me compensation, and there was no client named Michael.\n\nThe station clock changed to 2:51.\n\nTwo hours and forty-seven minutes until sunrise.",
        "proposer_claim": "Lucifer's unqualified uncertainty is evident in the dialogue; one compact mechanics sentence is sufficient to prove both anomalies before the clock resumes.",
        "balancer_objection": {
          "category": "rule-clarity",
          "detail": "Compression could blur the normal request-price roles established earlier."
        },
        "reconciliation": "Revise rather than fully delete. Retain Lucifer's authorship of every field and state both impossible system conditions explicitly.",
        "recomposition_proof": "The Michael request remains mechanically impossible, then the 2:51 clock and approaching footsteps restore danger."
      }
    ],
    "technique_trace": {
      "abstraction_level_guard": "pass; proposals remain passage-level",
      "recomposition_proof": "pass for all five auditions",
      "cognitive_load_check": "triggered; removed interpretation following already legible discoveries",
      "concept_vs_knowledge_status": "audition evidence only; no reader-response proof",
      "premortem": "The cumulative cuts could make Lucifer merely efficient rather than intimate; guard by selecting auditions independently and retaining one tethered voice beat per turn.",
      "frame_expiry": "Reassess if the author chooses explicit interiority over reader discovery, or if later chapters do not carry Lucifer's fascination and service philosophy.",
      "navigation": "Compare each audition independently against the unchanged candidate; any selected change requires a new manuscript candidate, digest, complete reread, and author decision.",
      "next_route": "decision-gate"
    }
  },
  "risks": [
    {
      "id": "R1",
      "risk": "Applying all five cuts together may overcorrect and flatten Lucifer's intimate interior register.",
      "mitigation": "Judge each audition independently and reread the cumulative candidate aloud."
    },
    {
      "id": "R2",
      "risk": "SR-01 and SR-03 remove explicit fascination beats.",
      "mitigation": "Confirm that Lucifer's retained smiles, observations, and later choices carry the relationship arc."
    },
    {
      "id": "R3",
      "risk": "SR-04 may make the app compromise feel less personally violating.",
      "mitigation": "Retain the exact presentation/promise marker and test the pause before Michael during full-chapter review."
    },
    {
      "id": "R4",
      "risk": "Passage-level reasoning cannot establish actual reader discovery or ending impact.",
      "mitigation": "Treat these as auditions only; require author reread against the exact resulting digest."
    }
  ],
  "elimination_conditions": [
    {
      "audition_id": "SR-01",
      "eliminate_if": "The author requires an explicit Chapter 1 statement of Lucifer's attraction to singular human love at this exact turn."
    },
    {
      "audition_id": "SR-02",
      "eliminate_if": "Readers cannot infer from Ruth's repayment that a mundane intervention can itself be a Light."
    },
    {
      "audition_id": "SR-03",
      "eliminate_if": "The chapter's intended relationship arc requires Lucifer to state approval of Elena before the locker opens."
    },
    {
      "audition_id": "SR-04",
      "eliminate_if": "Full-chapter reading shows that the retained promise sentence does not establish the personal cost of app compromise."
    },
    {
      "audition_id": "SR-05",
      "eliminate_if": "A first-time reader cannot distinguish the impossible compensation field from Lucifer merely disliking Michael's offer."
    },
    {
      "audition_id": "ALL",
      "eliminate_if": "Any integrated candidate alters a required marker, continuity invariant, Mara's agency, the clock, the Michael request, or the final symmetry reversal."
    }
  ]
}
```

## Delayed recomposition — spawn-0002

```json
{
  "task_status": "completed",
  "domain_gate_status": "not_evaluated",
  "artifacts": [
    {
      "ref": "receipts/delayed-recomposition.json",
      "delivery": "inline",
      "written": false,
      "artifact_type": "read-only audition receipt"
    }
  ],
  "validation": {
    "read_coverage": {
      "chapter_candidate": "lines 1-729",
      "voice_guide": "lines 1-47",
      "factory_config": "lines 1-206",
      "strategy_inventory_packet": "lines 1-80"
    },
    "candidate_sha256": "8b33827b68d2761381cdc0f61b4c3f92bb2b4a80fea55137174424c358cb8d7d",
    "expected_sha256_match": true,
    "current_word_count": 3352,
    "configured_word_range": [2500, 4500],
    "required_markers": "10/10 present",
    "forbidden_markers": "0/5 present",
    "full_chapter_causal_audit": {
      "result": "pass",
      "preserved_spine": [
        "2:13 Halo Café transaction opening",
        "Mara's concrete request and open-favor price",
        "prior-Light conflict and zero-payment hold",
        "voluntary amendment",
        "Halo pursuit and Saint Orison route",
        "Elena's prepared locker and recording",
        "Mara's station, stay, and tracker-removal choices",
        "app-compromise warning",
        "Michael request and final symmetry reversal"
      ]
    },
    "exact_match_simulation": {
      "DR-01": [1],
      "DR-02": [1],
      "DR-03": [1, 1],
      "DR-04": [1],
      "DR-05": [1, 1]
    },
    "combined_non_authoritative_simulation": {
      "word_count": 3239,
      "within_configured_range": true,
      "required_markers_retained": true,
      "forbidden_markers_absent": true,
      "sha256_if_combined": "a9898bebc659e46aef52fe4ba3b9fa99a64ee00d38ae9efc96a42db1991696f9",
      "notice": "Compatibility simulation only; it does not recommend applying all auditions together."
    },
    "writes_performed": 0,
    "evidence_emission": "not-required",
    "telemetry": "caller-owned; no telemetry written by this helper"
  },
  "proposal": {
    "target_context": "One complete Chapter 1 candidate, with delayed thematic payoff achieved through existing choices, objects, and callbacks.",
    "objective_and_output_artifact": "Five exact, read-only passage auditions; each is bound to the validated candidate digest.",
    "mode_and_budget": "tournament; three proposal tracks, two finite rounds, one set-based pitch-off",
    "proposal_tracks": [
      {
        "id": "T1",
        "method": "subtractive latency",
        "claim": "Remove early thematic gloss where later chapter mechanics already complete the meaning.",
        "auditions": ["DR-01", "DR-02"]
      },
      {
        "id": "T2",
        "method": "choice and object relay",
        "claim": "Replace abstraction with observable behavior, allowing the knife, key, locker, and choice surfaces to carry meaning.",
        "auditions": ["DR-03", "DR-04"]
      },
      {
        "id": "T3",
        "method": "proof before interpretation",
        "claim": "Delay Lucifer's interpretation until the anomalous field proves the violation.",
        "auditions": ["DR-05"]
      }
    ],
    "recursive_rounds": "2/2",
    "verdict": "pass",
    "tournament_result": {
      "best_first_tests": ["DR-03", "DR-05"],
      "reason": "They produce the clearest delayed payoff while preserving rule clarity and ending mechanics.",
      "selection_status": "unselected audition recommendation only"
    },
    "smallest_coherent_unit": "One exact replacement, or one paired relocation, plus its named downstream payoff anchor.",
    "optimization_point": "Smaller sentence-level cuts would lack recomposition proof; broader scene rewrites would add unnecessary continuity and authority risk.",
    "concept_layer_map": [
      "chapter theme",
      "scene-level delayed payoff",
      "passage-level setup and payoff",
      "exact replacement operation"
    ],
    "auditions": [
      {
        "id": "DR-01",
        "title": "Let the chapter answer the locked-door question",
        "baseline_lines": "27-33",
        "method": "subtractive latency",
        "edit_operations": [
          {
            "operation": "replace_exact",
            "source_text": [
              "By the time someone receives an invitation to Lucifer’s Lights, the respectable world has already told them no. They enter a request. I name a price. They accept, refuse, or walk away. The app records the bargain; it does not grant wishes. Even desperate people deserve to know the cost before someone saves them.",
              "",
              "Every locked door creates three questions: what is behind it, where is the key, and who gets to decide whether it opens.",
              "",
              "Lucifer’s Lights is my answer.",
              "",
              "Or perhaps my way of postponing one."
            ],
            "replacement_text": [
              "By the time someone receives an invitation to Lucifer’s Lights, the respectable world has already told them no. They enter a request. I name a price. They accept, refuse, or walk away. The app records the bargain; it does not grant wishes. Even desperate people deserve to know the cost before someone saves them.",
              "",
              "Lucifer’s Lights is my answer.",
              "",
              "Or perhaps my way of postponing one."
            ]
          }
        ],
        "delayed_payoff": "The amendment buttons, brass key, sealed locker, departing train, and Lucifer's final offered choice answer the omitted checklist through events.",
        "role_trace": {
          "proposer_claim": "The explicit three-question thesis pre-solves imagery that the chapter subsequently dramatizes.",
          "evidence_or_assumption": "The complete chapter contains repeated doors, keys, and autonomous choices; reader-effect remains unproved.",
          "balancer_objection_category": "meaning-loss",
          "balancer_objection": "Without the checklist, 'my answer' and 'postponing one' become more elliptical.",
          "reconciliation": "Advance as an audition because the preceding service explanation supplies the referent; eliminate if first-read clarity falls."
        }
      },
      {
        "id": "DR-02",
        "title": "Make free refusal a demonstrated rule",
        "baseline_lines": "143-150",
        "method": "subtractive latency",
        "edit_operations": [
          {
            "operation": "replace_exact",
            "source_text": [
              "“And if I refuse when you come to collect?”",
              "",
              "“Then you refuse.”",
              "",
              "A laugh escaped me—bright, sharp, gone. Mara’s fingers tightened around her cup.",
              "",
              "“Free will would be a poor brand if I did not honor it. Refuse me when I collect, and whatever darkness comes next, you face it without a Light.”"
            ],
            "replacement_text": [
              "“And if I refuse when you come to collect?”",
              "",
              "“Then you refuse.”",
              "",
              "A laugh escaped me—bright, sharp, gone. Mara’s fingers tightened around her cup.",
              "",
              "“Whatever darkness comes next, you face it without a Light.”"
            ]
          }
        ],
        "delayed_payoff": "Mara later chooses the amendment, chooses to stay, cuts the bracelet herself, and finally watches Lucifer receive his own accept-or-decline surface.",
        "role_trace": {
          "proposer_claim": "The rule and consequence remain exact while the chapter stops naming free will before repeatedly staging it.",
          "evidence_or_assumption": "The dialogue already says refusal is permitted; later choices supply four independent demonstrations.",
          "balancer_objection_category": "rule-clarity",
          "balancer_objection": "Removing the branding sentence may reduce Lucifer's explicit rationale for honoring refusal.",
          "reconciliation": "Advance; rationale is less important than the operative rule and consequence, both retained."
        }
      },
      {
        "id": "DR-03",
        "title": "Delay Lucifer's fascination until Mara acts without permission",
        "baseline_lines": "201-211 and 657-663",
        "method": "choice and object relay",
        "edit_operations": [
          {
            "operation": "replace_exact",
            "source_text": [
              "“I don’t care about angels,” she said. “I just want my sister back.”",
              "",
              "There it was: humanity in one sentence.",
              "",
              "People like me prefer humanity in the plural. It turns suffering into philosophy. Mara had reduced Heaven, Hell, knowledge, and rebellion to one missing woman and one diminishing night.",
              "",
              "Singular love is inconvenient that way. It refuses to become an idea.",
              "",
              "God, I love humans.",
              "",
              "I smiled. Mara shifted away from me."
            ],
            "replacement_text": [
              "“I don’t care about angels,” she said. “I just want my sister back.”",
              "",
              "I smiled. Mara shifted away from me."
            ]
          },
          {
            "operation": "replace_exact",
            "source_text": [
              "I offered her a knife.",
              "",
              "She took it and cut the bracelet herself.",
              "",
              "Of course she did.",
              "",
              "The plastic separated, revealing a thread of copper and a glass capsule no larger than a grain of rice."
            ],
            "replacement_text": [
              "I offered her a knife.",
              "",
              "She took it and cut the bracelet herself.",
              "",
              "She did not look at me first.",
              "",
              "Of course she didn’t.",
              "",
              "The plastic separated, revealing a thread of copper and a glass capsule no larger than a grain of rice."
            ]
          }
        ],
        "delayed_payoff": "Lucifer's unexplained smile becomes legible only when Mara performs autonomous courage with the knife.",
        "role_trace": {
          "proposer_claim": "The paired edit converts a general declaration about humanity into a character-specific observation caused by Mara's action.",
          "evidence_or_assumption": "The voice guide explicitly prefers admiration when Mara acts without Lucifer's permission.",
          "balancer_objection_category": "approval-contamination",
          "balancer_objection": "The added reaction could still sound like Lucifer is grading Mara.",
          "reconciliation": "Advance as the strongest audition because it records her refusal to seek permission, not his approval."
        }
      },
      {
        "id": "DR-04",
        "title": "Let the literal key carry the contract metaphor",
        "baseline_lines": "391",
        "method": "choice and object relay",
        "edit_operations": [
          {
            "operation": "replace_exact",
            "source_text": [
              "A contract is a door you lock from this side. Your future self is the one who discovers where you left the key."
            ],
            "replacement_text": [
              "The words did not change. Her breathing did."
            ]
          }
        ],
        "delayed_payoff": "The brass key, sealed locker, departing train, and Mara's decision to take the phone embody the future-self choice without a second explanatory lock-and-key aphorism.",
        "role_trace": {
          "proposer_claim": "The replacement reads Mara in the live moment and allows the later literal key to complete the parable.",
          "evidence_or_assumption": "The amendment's operative meaning is already explicit in its fields and dialogue.",
          "balancer_objection_category": "contract-consequence",
          "balancer_objection": "The original sentence uniquely warns that present consent binds a future self.",
          "reconciliation": "Advance with a flag; retain the original if author review finds that future-cost nuance is otherwise too quiet."
        }
      },
      {
        "id": "DR-05",
        "title": "Make the impossible compensation field prove the stolen voice",
        "baseline_lines": "675 and 705-707",
        "method": "proof before interpretation",
        "edit_operations": [
          {
            "operation": "replace_exact",
            "source_text": [
              "The screen was presentation. The promise behind it was mine. If someone was collecting requests under my name, they had not merely entered my system. They had put my word in their mouth."
            ],
            "replacement_text": [
              "The screen was presentation. The promise behind it was mine."
            ]
          },
          {
            "operation": "replace_exact",
            "source_text": [
              "I had designed every field in Lucifer’s Lights. Clients submitted requests. I decided the price. There was no mechanism through which a client could offer me compensation.",
              "",
              "There was also no client named Michael."
            ],
            "replacement_text": [
              "I had designed every field in Lucifer’s Lights. Clients submitted requests. I decided the price. There was no mechanism through which a client could offer me compensation.",
              "",
              "Whoever had done this had put my word in their mouth.",
              "",
              "There was also no client named Michael."
            ]
          }
        ],
        "delayed_payoff": "The ownership wound is named only after the forbidden compensation field supplies concrete proof, while 'There was also no client named Michael' retains the final punch.",
        "role_trace": {
          "proposer_claim": "Moving the metaphor after the anomaly turns explanation into earned interpretation.",
          "evidence_or_assumption": "The required presentation/promise marker remains exact; the mechanism mismatch remains unchanged.",
          "balancer_objection_category": "cliffhanger-pacing",
          "balancer_objection": "Any added pause after Michael appears can reduce acceleration toward the footsteps and final choice.",
          "reconciliation": "Advance as a top audition; the relocated sentence precedes the shorter Michael sentence so the latter still closes the diagnostic beat."
        }
      }
    ],
    "technique_pack_trace": [
      {
        "technique": "abstraction-level guard",
        "decision": "pass",
        "output": "All auditions remain passage-level and introduce no scene rewrite."
      },
      {
        "technique": "recomposition proof",
        "decision": "pass",
        "output": "Every removed abstraction has a named downstream action, object, or callback."
      },
      {
        "technique": "boundary-object check",
        "decision": "triggered",
        "output": "Knife, key, locker, agreement surface, and compensation field carry cross-scene meaning."
      },
      {
        "technique": "concept-vs-knowledge status",
        "decision": "triggered",
        "output": "Proposals are composition hypotheses, not proven reader effects."
      },
      {
        "technique": "set-based tournament",
        "decision": "triggered",
        "output": "Three methodologies compared; DR-03 and DR-05 are best-first tests."
      },
      {
        "technique": "requisite-variety check",
        "decision": "skipped",
        "reason": "No new system complexity or variant pressure is present."
      }
    ],
    "closure_and_recomposition_proof": "Each unit has an exact source match, preserves the causal scene engine, and reconnects its removed meaning to a later observable event without hidden narrative glue.",
    "evolution_profile": "If later chapters establish recurring thematic callbacks, the smallest extension boundary is another exact setup/payoff pair; no canonical writing framework is justified.",
    "deferred_complexity": [
      "No chapter-wide rewrite",
      "No voice-guide mutation",
      "No canonical Whisper rule",
      "No reader-response claim",
      "No manuscript acceptance"
    ],
    "tension_ledger": {
      "resolved": [
        "Required markers survive every audition.",
        "Contract, clock, agency, ambiguity, and cliffhanger mechanics remain unchanged."
      ],
      "unresolved": [
        "Whether subtraction makes Lucifer's voice more compelling or merely less lush requires author reading.",
        "Whether DR-04 removes too much future-cost clarity requires side-by-side review.",
        "No evidence proves the intended reader discovery effect."
      ]
    },
    "premortem": "The combined edits could make Lucifer feel unusually austere. Guardrail: audition DR-03 and DR-05 first, then restore any cut whose absence reduces character, rule, danger, choice, or time.",
    "frame_expiry_note": "These exact operations expire if the candidate digest changes or later continuity assigns new importance to the removed sentences.",
    "navigation_guide": "Start with DR-03, then DR-05. Read each in the complete chapter, separately first. Treat DR-01, DR-02, and DR-04 as optional subtractive tests. Any selected change requires a new authorized candidate mutation and exact author gate.",
    "next_route": "decision-gate"
  },
  "risks": [
    "No reader-response experiment proves that delayed payoff will improve discovery.",
    "Applying all five together may over-compress Lucifer's philosophical register.",
    "DR-04 has the highest rule-clarity risk.",
    "DR-03 intentionally leaves Lucifer's smile unexplained for several pages and may make it feel more predatory.",
    "DR-05 must not be read as proof of who compromised the app.",
    "All line locators and replacements are bound to the validated candidate digest."
  ],
  "elimination_conditions": {
    "global": [
      "Eliminate any audition that changes contract priority, payment status, amendment mechanics, Mara's agency, the clock, ambiguity, Michael's request, or the final symmetry.",
      "Eliminate any audition that removes a required marker or introduces a forbidden marker.",
      "Eliminate any audition whose complete-chapter reading makes Lucifer generic, doctrinal, or omniscient.",
      "Eliminate the combined set if cumulative subtraction weakens voice more than it strengthens delayed payoff.",
      "Eliminate any reader-effect claim absent separate evidence."
    ],
    "DR-01": "Eliminate if 'Lucifer’s Lights is my answer / postponing one' loses a clear referent on first reading.",
    "DR-02": "Eliminate if readers no longer understand that refusal is genuinely permitted and has a stated consequence.",
    "DR-03": "Eliminate if the knife callback sounds like Lucifer's approval made Mara's choice meaningful.",
    "DR-04": "Eliminate if the open favor's future-self cost becomes materially less legible.",
    "DR-05": "Eliminate if the relocated metaphor slows the Michael cliffhanger or overstates the unknown attacker's identity or capability."
  }
}
```

## Performative scene-writing — spawn-0003

```json
{
  "task_status": "completed",
  "domain_gate_status": "not_evaluated",
  "artifacts": [
    {
      "ref": "receipts/performative-scene.json",
      "kind": "performative-scene-audition-receipt",
      "delivery": "inline-to-parent",
      "materialized": false,
      "reason": "Read-only action with empty write scope."
    },
    {
      "ref": "chapter-candidate",
      "path": "projects/lucifers-lights/development/chapter-factory-runs/chapter-01-monologue-revision-002/candidate/chapter-01.md",
      "sha256": "8b33827b68d2761381cdc0f61b4c3f92bb2b4a80fea55137174424c358cb8d7d",
      "word_count": 3352,
      "audit_coverage": "Complete chapter, lines 1-729."
    }
  ],
  "validation": {
    "declared_inputs_read_in_full": [
      "chapter-candidate",
      "voice-guide",
      "factory-config",
      "strategy-inventory-packet"
    ],
    "candidate_digest": {
      "expected": "8b33827b68d2761381cdc0f61b4c3f92bb2b4a80fea55137174424c358cb8d7d",
      "observed": "8b33827b68d2761381cdc0f61b4c3f92bb2b4a80fea55137174424c358cb8d7d",
      "result": "pass"
    },
    "word_count": {
      "observed": 3352,
      "allowed_minimum": 2500,
      "allowed_maximum": 4500,
      "result": "pass"
    },
    "required_markers": {
      "present": 10,
      "missing": [],
      "result": "pass"
    },
    "forbidden_markers": {
      "present": [],
      "absent": 5,
      "result": "pass"
    },
    "clock_markers": {
      "present": 6,
      "missing": [],
      "result": "pass"
    },
    "audition_marker_preservation": {
      "result": "pass-by-inspection",
      "detail": "Audition PS-01 retains both required opening markers it touches. PS-02 through PS-05 do not remove or rewrite required markers."
    },
    "mutation": {
      "files_written": 0,
      "write_capable_commands_invoked": 0,
      "result": "pass"
    },
    "verdict": "pass_for_audition_only"
  },
  "proposal": {
    "target_context": "Chapter 1 revision candidate, preserving transaction-first pacing, Mara's agency, contract priority, app ambiguity, sunrise clock, Michael request, and final symmetry.",
    "objective_and_output_artifact": "Replace five abstract explanation clusters with exact, locally replaceable scene-writing auditions that perform a tether-rule job.",
    "mode_and_budget": {
      "mode": "tournament",
      "proposal_tracks": 3,
      "recursive_rounds_completed": 2,
      "recursive_rounds_budget": 2,
      "role_execution_path": "Single auditionist within the caller-owned multi-agent tournament, with local Proposer/Balancer traces."
    },
    "verdict": "pass",
    "authority_boundary": "Audition evidence only. No manuscript acceptance, rule canonicalization, promotion, publication, Git action, or reader-effect claim.",
    "chapter_audit": [
      {
        "part": "opening_and_client_request",
        "finding": "Flag lines 27-33. Service mechanics arrive as a compact essay before Lucifer and Mara begin negotiating. Privacy-as-timing and the subsequent identity exchange are already live and should remain."
      },
      {
        "part": "price_rules_and_choice",
        "finding": "Flag lines 203-211. Mara's concrete dismissal of mythology earns Lucifer's interest, but the plural-versus-singular humanity explanation repeats what her choice already demonstrates. The hope and contract-door metaphors remain tethered."
      },
      {
        "part": "prior_light_conflict_and_amendment",
        "finding": "Flag lines 351-367. The three rules are necessary, but existing status labels can make Lucifer demonstrate them while physically returning the decision surface to Mara."
      },
      {
        "part": "halo_escape",
        "finding": "Pass. Ruth's coffee-pot intervention, the train interval, the ruined shoes, and the remembered debt already perform rule, danger, and time. The repeated Light summary is compressible later but remains action-backed."
      },
      {
        "part": "pursuit_and_station_entry",
        "finding": "Flag lines 517-525. The two-map aside pauses an active pursuit; making Mara cross one of its physical boundaries lets the idea move with the chase."
      },
      {
        "part": "station_revelation",
        "finding": "Pass. The scheduled timestamp earns the Elena-preparation inference; Mara cuts the tracker herself; the ordinary-technology ambiguity and compromised-promise metaphor perform live danger."
      },
      {
        "part": "michael_cliffhanger",
        "finding": "Flag lines 703-707. The impossible compensation mechanic is necessary, but Lucifer can test the displayed field and let Mara infer the breach."
      }
    ],
    "proposal_tracks": [
      {
        "track": "screen-as-stage",
        "method": "Use only visible app language and Lucifer's handling of the phone to expose rules and anomalies.",
        "auditions": [
          "PS-01",
          "PS-03",
          "PS-05"
        ],
        "proposer_claim": "The phone is already the chapter's boundary object; its resistance can carry exposition without resolving whether the system is magical or engineered.",
        "balancer_objection": {
          "category": "continuity-and-hidden-glue",
          "detail": "Extra taps must not invent fields, grant access to Elena's protected terms, or imply unsupported app behavior."
        },
        "reconciliation": "Use existing labels only and make non-response, not a new feature, the visible event."
      },
      {
        "track": "choice-in-the-body",
        "method": "Let Mara's handling of the photograph and the worsening rain replace Lucifer's generalized humanity thesis.",
        "auditions": [
          "PS-02"
        ],
        "proposer_claim": "Her autonomous dismissal of Lucifer's mythology is more revealing when Lucifer notices the concrete choice rather than praising humanity in general.",
        "balancer_objection": {
          "category": "character-agency",
          "detail": "Lucifer's admiration must not become approval language or imply that Mara acts for his benefit."
        },
        "reconciliation": "Frame the action as Mara dismissing him without permission and keep the weather clock independent of his judgment."
      },
      {
        "track": "danger-in-motion",
        "method": "Turn the two-map explanation into an obstacle, exchange, and route choice during pursuit.",
        "auditions": [
          "PS-04"
        ],
        "proposer_claim": "Crossing a broken boundary proves the hidden map while preserving Lucifer's metaphorical register.",
        "balancer_objection": {
          "category": "location-continuity",
          "detail": "The declared inputs do not establish the produce market's shutter geometry."
        },
        "reconciliation": "Keep PS-04 conditional on location-continuity review and eliminate it if the added physical staging conflicts with the story bible."
      }
    ],
    "current_smallest_coherent_unit": "One exact replaceable passage with one named tether job, stable entry and exit state, and no altered plot decision.",
    "optimization_point": "Smaller word-level edits would not transfer the explanatory job into action; larger scene rewrites would risk continuity, clock, agency, and authority boundaries.",
    "concept_layer_map": [
      "Chapter-wide Lucifer voice",
      "Scene-level tether performance",
      "Passage-level explanation cluster",
      "Exact replaceable audition"
    ],
    "auditions": [
      {
        "id": "PS-01",
        "priority": 5,
        "methodology": "screen-as-stage plus sensory evidence",
        "source_line_span": "27-33",
        "tether_jobs": [
          "read_a_person",
          "expose_a_rule"
        ],
        "source_paragraphs": [
          "By the time someone receives an invitation to Lucifer’s Lights, the respectable world has already told them no. They enter a request. I name a price. They accept, refuse, or walk away. The app records the bargain; it does not grant wishes. Even desperate people deserve to know the cost before someone saves them.",
          "Every locked door creates three questions: what is behind it, where is the key, and who gets to decide whether it opens.",
          "Lucifer’s Lights is my answer.",
          "Or perhaps my way of postponing one."
        ],
        "audition_paragraphs": [
          "By the time someone receives an invitation to Lucifer’s Lights, the respectable world has already told them no.",
          "Mara set the phone between us. The white flame lit the half-moons her nails had bitten into her palm.",
          "Every locked door creates three questions: what is behind it, where is the key, and who gets to decide whether it opens. A client names the door. I name a price. They accept, refuse, or walk away. The app records the bargain; it does not grant wishes.",
          "Lucifer’s Lights is my answer.",
          "Or perhaps my way of postponing one."
        ],
        "recomposition": "Entry still follows the invitation screen; exit still hands directly to Mara asking whether he is Lucifer. Both required opening markers remain exact.",
        "selection_note": "Conditional. It removes Lucifer's self-certifying courtesy claim and grounds desperation, but the opening read-aloud must prove that the added hand image does not delay the identity exchange."
      },
      {
        "id": "PS-02",
        "priority": 2,
        "methodology": "choice-in-the-body",
        "source_line_span": "203-211",
        "tether_jobs": [
          "read_a_person",
          "advance_the_clock"
        ],
        "source_paragraphs": [
          "There it was: humanity in one sentence.",
          "People like me prefer humanity in the plural. It turns suffering into philosophy. Mara had reduced Heaven, Hell, knowledge, and rebellion to one missing woman and one diminishing night.",
          "Singular love is inconvenient that way. It refuses to become an idea.",
          "God, I love humans.",
          "I smiled. Mara shifted away from me."
        ],
        "audition_paragraphs": [
          "Mara put two fingers on the photograph and drew Elena back to her side of the table.",
          "Heaven, Hell, knowledge, rebellion—four splendid subjects, and she had dismissed them all without asking my permission.",
          "Outside, rainwater climbed over the curb and swallowed the gutter.",
          "I smiled. Mara shifted away from me."
        ],
        "recomposition": "Mara's preceding line still causes Lucifer's reaction; his smile still produces her withdrawal and the agreement choice follows unchanged.",
        "selection_note": "Recommended. It replaces the most voice-guide-sensitive general declaration with Mara's autonomous action and a live loss-of-access cue."
      },
      {
        "id": "PS-03",
        "priority": 1,
        "methodology": "screen-as-stage",
        "source_line_span": "351-367",
        "tether_jobs": [
          "expose_a_rule",
          "change_a_decision"
        ],
        "source_paragraphs": [
          "“Convenience has nothing to do with it. Three rules: the older promise holds; conflicted work stops; no amendment proceeds without your choice. Entire civilizations have survived with fewer.”",
          "She glanced toward the rain-streaked window.",
          "“What can you do?”",
          "“I can use the emergency channel Elena created herself. I can confirm whether she is alive and ask whether she will speak to you.”",
          "“And if she says no?”",
          "“I will not reveal her location.”",
          "“I paid you to bring her home.”",
          "“You have paid me nothing.”",
          "I touched the screen. Her original request faded, replaced by a narrower one."
        ],
        "audition_paragraphs": [
          "“Convenience has nothing to do with it.”",
          "I touched **REASON: PRIOR LIGHT**. The screen did not yield another word.",
          "“The older promise holds.”",
          "I touched **STATUS: HELD**.",
          "“Conflicted work stops.”",
          "Then I set the phone in front of her and took my hand away.",
          "“No amendment proceeds without your choice.”",
          "She glanced from the screen to the rain-streaked window.",
          "“What can you do?”",
          "“I can use the emergency channel Elena created herself. I can confirm whether she is alive and ask whether she will speak to you.”",
          "“And if she says no?”",
          "“I will not reveal her location.”",
          "“I paid you to bring her home.”",
          "“You have paid me nothing.”",
          "I touched the empty space beneath the two lines. Her original request faded, replaced by a narrower one."
        ],
        "recomposition": "The same three rules govern the same amendment. Mara retains the next move, and the exact amended request, deadline, and acceptance remain unchanged.",
        "selection_note": "Strongest audition. Existing status labels perform priority and suspension; Lucifer physically withdrawing his hand performs the choice boundary."
      },
      {
        "id": "PS-04",
        "priority": 4,
        "methodology": "danger-in-motion",
        "source_line_span": "517-529",
        "tether_jobs": [
          "sharpen_danger",
          "advance_the_clock"
        ],
        "source_paragraphs": [
          "Like every city, Vesper has two maps.",
          "One is printed for tourists, taxpayers, and police officers. It contains streets, monuments, and the comforting suggestion that the city was designed by someone.",
          "The second map exists only in memory. It is made of service tunnels, broken fences, bribed doormen, unfinished buildings, and doors that remain unlocked for exactly three minutes each night.",
          "That was the map we followed.",
          "We crossed a shuttered produce market, descended through a parking garage, and entered Saint Orison Station through a maintenance door whose lock had not worked since the spring floods.",
          "By the time the two men reached the alley, the rain had erased our footprints.",
          "At least, that was what I told myself."
        ],
        "audition_paragraphs": [
          "The produce market’s shutters were down. I found the one that had jammed two feet above the pavement and held it for Mara.",
          "“This is your shortcut?”",
          "“This is Vesper’s second map.”",
          "The first is printed for tourists, taxpayers, and police officers. Mine lives in service tunnels, broken fences, bribed doormen, and doors that remain unlocked for exactly three minutes each night.",
          "We crossed the dark market at a run, descended through a parking garage, and entered Saint Orison Station through a maintenance door whose lock had not worked since the spring floods.",
          "By the time the two men reached the alley, the rain had erased our footprints.",
          "At least, that was what I told myself."
        ],
        "recomposition": "The route remains market to garage to maintenance door to station; the pursuers and tracker discovery remain in their existing order.",
        "selection_note": "Conditional on location review. It improves chase continuity but introduces one concrete shutter detail absent from the declared evidence."
      },
      {
        "id": "PS-05",
        "priority": 3,
        "methodology": "screen-as-stage plus Mara inference",
        "source_line_span": "703-707",
        "tether_jobs": [
          "expose_a_rule",
          "sharpen_danger"
        ],
        "source_paragraphs": [
          "It was the first answer I had given her that needed no qualification.",
          "I had designed every field in Lucifer’s Lights. Clients submitted requests. I decided the price. There was no mechanism through which a client could offer me compensation.",
          "There was also no client named Michael."
        ],
        "audition_paragraphs": [
          "I pressed **COMPENSATION OFFERED**.",
          "Nothing opened. No cursor. No menu. No field I had built.",
          "“Clients submit requests,” I said. “I decide the price.”",
          "Mara looked from the impossible line to me. “Then who made you an offer?”",
          "There was no client named Michael."
        ],
        "recomposition": "Lucifer's unqualified uncertainty remains in the preceding dialogue; the same impossible field and nonexistent client lead into 2:51, the footsteps, and his offered choice.",
        "selection_note": "Recommended if app interaction reads naturally. It lets the interface fail Lucifer's own model and gives Mara one final act of inference before the cliffhanger."
      }
    ],
    "tournament_pitch_off": {
      "recommended_low_risk_core": [
        "PS-03",
        "PS-02",
        "PS-05"
      ],
      "conditional_extensions": [
        "PS-04",
        "PS-01"
      ],
      "ranking_basis": [
        "voice-guide fit",
        "continuity cost",
        "Mara agency",
        "clock preservation",
        "ambiguity preservation",
        "amount of invented staging"
      ]
    },
    "technique_pack_trace": [
      {
        "technique": "abstraction-level-guard",
        "result": "pass",
        "effect": "Stopped at exact passage units rather than redesigning the scene."
      },
      {
        "technique": "recomposition-proof",
        "result": "pass",
        "effect": "Each audition names stable entry and exit state."
      },
      {
        "technique": "cognitive-load-check",
        "result": "pass-with-flag",
        "effect": "PS-03 stages three rules sequentially; reject it if the extra beats feel instructional."
      },
      {
        "technique": "boundary-object-check",
        "result": "pass",
        "effect": "Phone, photograph, weather, and route carry meaning already present in the chapter."
      },
      {
        "technique": "concept-vs-knowledge-status",
        "result": "pass",
        "effect": "All revisions remain auditions; no reader-effect or lore claim is promoted."
      },
      {
        "technique": "set-based-tournament",
        "result": "pass",
        "effect": "Three methodologies were balanced independently before ranking."
      },
      {
        "technique": "premortem",
        "result": "pass",
        "effect": "Primary failure is over-choreographing Lucifer until his intimate monologue loses ease."
      },
      {
        "technique": "frame-expiry",
        "result": "recorded",
        "effect": "Auditions expire if accepted app behavior, location geometry, scene order, or candidate digest changes."
      },
      {
        "technique": "navigable-result-check",
        "result": "pass",
        "effect": "Exact source and replacement passages plus selection order are supplied."
      }
    ],
    "closure_and_recomposition_proof": "All five units have named inputs, outputs, abstraction level, tether jobs, and stable surrounding plot state. None changes the agreement, Elena's priority, Mara's choices, the clock, Michael's request, or the ending.",
    "evolution_profile": "If the project later applies this method across chapters, the smallest safe extension is a passage-audition rubric using the existing tether jobs. This receipt does not justify a canonical Whisper framework or voice-guide mutation.",
    "deferred_complexity": [
      "No new app architecture.",
      "No explanation of Michael, the ledger, Lucifer's name, or supernatural mechanics.",
      "No location-lore canonicalization.",
      "No reader-response claim.",
      "No manuscript mutation or acceptance."
    ],
    "tension_ledger": {
      "resolved": [
        "Abstract rule explanation can be transferred to existing screen labels.",
        "Lucifer's attraction to Mara can be shown without approving her choice.",
        "The map metaphor can remain while the chase keeps moving."
      ],
      "unresolved": [
        "Whether PS-01 improves or delays the opening when read aloud.",
        "Whether PS-04's shutter geometry matches the location authority.",
        "Whether tapping non-interactive labels in PS-03 and PS-05 over-specifies app behavior.",
        "Whether adopting multiple auditions overcorrects the intended monologue density."
      ]
    },
    "premortem": {
      "likely_failure": "The bundle replaces elegant narration with conspicuous stage business, making Lucifer feel mechanically edited rather than effortlessly observant.",
      "guardrail": "Apply the voice guide's pacing test to each audition separately: read action and dialogue alone, restore the revised aside, and eliminate any passage that does not alter character, rule, danger, choice, or time."
    },
    "frame_expiry_note": "Re-audit against new exact bytes if the candidate digest, app interaction model, Halo or station staging, event order, or voice guide changes.",
    "navigation_guide": {
      "start_here": "Compare PS-03, PS-02, and PS-05 in that order.",
      "then": "Continuity-check PS-04 and read PS-01 aloud against the existing opening.",
      "before_mutation": "Select passages through the caller's tournament reconciliation and obtain the required exact author decision for any new candidate digest.",
      "remaining_boundary": "This receipt is not manuscript acceptance."
    },
    "evidence_emission": {
      "status": "not-required",
      "reason": "No accepted event context was supplied; the caller requested an inline read-only receipt."
    },
    "telemetry": {
      "status": "caller-owned-not-recorded",
      "reason": "Telemetry writes are outside this action's authority and explicitly forbidden."
    },
    "next_route": "decision-gate after caller-owned tournament reconciliation"
  },
  "risks": [
    "The declared read scope excludes location-bible verification, so PS-04's added shutter geometry is conditional.",
    "Visible taps in PS-03 and PS-05 may imply app behavior beyond the accepted candidate.",
    "PS-01 may slow the transaction-first opening despite preserving its required markers.",
    "Combining all five auditions could overcorrect Lucifer's monologue density.",
    "No reader-response evidence proves that these changes improve discovery, thrill, voice, or pacing.",
    "Any applied replacement creates new candidate bytes requiring fresh digest validation and exact author review."
  ],
  "elimination_conditions": {
    "global": [
      "Eliminate any audition that removes a required marker or introduces a forbidden marker.",
      "Eliminate any audition that changes contract priority, Mara's voluntary choices, the sunrise clock, ambiguity, Michael's request, or final symmetry.",
      "Eliminate any bundle whose action-and-dialogue read is slower or less intelligible than the current scene.",
      "Eliminate any revision that requires unstated lore or app mechanics to connect its entry and exit states.",
      "Eliminate any reader-effect claim not supported by separate evidence."
    ],
    "by_audition": {
      "PS-01": "Eliminate if the added hand image delays Mara's identity question or reads as redundant with the hospital-bracelet evidence.",
      "PS-02": "Eliminate if photograph placement conflicts with adjacent blocking or Lucifer's permission line sounds like approval rather than surprised observation.",
      "PS-03": "Eliminate if the status labels are not visibly available at this moment, touching them implies protected access, or the three beats feel like a tutorial.",
      "PS-04": "Eliminate if location authority contradicts the shutter, if crawling under it alters pursuit logic, or if the dialogue sounds like generic noir.",
      "PS-05": "Eliminate if pressing the field falsely implies interactivity or Mara's added question weakens the speed of the Michael reveal."
    }
  }
}
```

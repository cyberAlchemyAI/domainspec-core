#!/usr/bin/env python3
"""Generate one read-decompose dispatch per tower paper, then validate each."""
import json
import subprocess
from pathlib import Path

ROOT = Path("/home/vrondelli/projects/domainspec-core")
TOWERS = ROOT / "research/jusbrasil-call/towers"
VALIDATOR = ROOT / "arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py"

PAPERS = [
    {
        "slug": "magesh-hallucination-free",
        "title": "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools (Magesh et al., 2024)",
        "ident": "arXiv:2405.20362",
        "feature": "Jus IA research-assistant reliability / internal hallucination audit",
    },
    {
        "slug": "juru-legal-llm",
        "title": "Juru: Legal Brazilian Large Language Model from Reputable Sources (Malaquias Junior et al., 2024)",
        "ident": "arXiv:2403.18140",
        "feature": "foundation-model layer / build-vs-buy for the Jus IA assistant",
    },
    {
        "slug": "robertalexpt",
        "title": "RoBERTaLexPT: A Legal RoBERTa Model Pretrained with Deduplication for Portuguese (Garcia et al., 2024)",
        "ident": "ACL:2024.propor-1.38",
        "feature": "encoder/foundation layer + corpus deduplication for millions of redundant judgments",
    },
    {
        "slug": "jua-benchmark",
        "title": "JUA: A Benchmark for Information Retrieval in Brazilian Legal Text Collections (Pereira et al., 2026)",
        "ident": "arXiv:2604.06098",
        "feature": "similar-jurisprudence retrieval evaluation / tribunal-heterogeneity yardstick",
    },
    {
        "slug": "feijo-moreira-entailment-summ",
        "title": "Improving abstractive summarization of legal rulings through textual entailment (Feijo & Moreira, 2023)",
        "ident": "DOI:10.1007/s10506-021-09305-4",
        "feature": "Jus IA smart-summaries (ementa) with entailment-based faithfulness control",
    },
    {
        "slug": "multi-lexsum",
        "title": "Multi-LexSum: Real-World Summaries of Civil Rights Lawsuits at Multiple Granularities (Shen et al., 2022)",
        "ident": "arXiv:2206.10883",
        "feature": "principais teses / multi-document multi-granularity summarization",
    },
    {
        "slug": "ulysseslegalner-br",
        "title": "UlyssesLegalNER-Br: a comprehensive corpus of Brazilian legal documents for NER (Albuquerque et al., 2026)",
        "ident": "ACL:2026.propor-1.33",
        "feature": "ingestion pipeline: legal NER / entity normalization",
    },
    {
        "slug": "menezes-neto-outcome-prediction",
        "title": "Using deep learning to predict outcomes of legal appeals better than human experts (de Menezes-Neto et al., 2022)",
        "ident": "DOI:10.1371/journal.pone.0272287",
        "feature": "next product: judicial outcome prediction (Probabilidade de Exito)",
    },
]

EXTERNAL_META = {
    "source": "arcanum-repository-local-skill",
    "note": "Installed Arcanum skill, not in the hardcoded canonical capability set.",
}


def build(p):
    slug = p["slug"]
    base = f"research/jusbrasil-call/towers/{slug}"
    return {
        "dispatch_id": f"read-decompose-{slug}-20260610",
        "parent_dispatch_id": "jusbrasil-legal-nlp-deep-research-20260610",
        "intent": {
            "raw": "create a research tower of each of one of first 8 and then a dispatch for each of the paper, so we can full decompose the papers and accelerate our read",
            "objective": f"Decompose '{p['title']}' into a reusable, source-backed reading path that accelerates understanding for the Jusbrasil call, mapped to: {p['feature']}.",
            "target_artifact": f"{base}/LEARNING-PACK.md",
            "arcanum_vocabulary": ["research-tower", "claim-ledger", "distill", "frame", "residue", "handoff", "promotion guardrail"],
            "operator_sentence": "Recover the source, build a claim ledger, govern the definitions, distill the operator model, then synthesize a learning pack and hand off an accelerated reading plan.",
        },
        "mode": "research",
        "steps": [
            {
                "step_id": "recover-source",
                "name": "Confirm source record and section map",
                "capability_ref": "context-builder",
                "pattern": "route",
                "parallel": False,
                "techniques": ["frame_handoff"],
                "inputs": [
                    {"kind": "intent", "ref": "operator-decompose-request"},
                    {"kind": "external_context", "ref": p["ident"]},
                ],
                "outputs": [
                    {"kind": "frame", "ref": f"{slug}-source-record-frame"},
                    {"kind": "trace_event", "ref": f"{slug}-source-recovered"},
                ],
                "join_policy": "none",
                "stop_conditions": [
                    "Flag if the source identifier cannot be resolved or the paper is inaccessible (record as open-residue, do not fabricate).",
                ],
            },
            {
                "step_id": "claim-ledger",
                "name": "Build claim ledger and notation bridge",
                "capability_ref": "research-tower",
                "capability_metadata": EXTERNAL_META,
                "pattern": "sequential",
                "parallel": False,
                "techniques": ["residue_ledger"],
                "inputs": [
                    {"kind": "frame", "ref": f"{slug}-source-record-frame"},
                ],
                "outputs": [
                    {"kind": "ledger", "ref": f"{slug}-claim-ledger"},
                    {"kind": "artifact", "ref": f"{base}/claim-ledger.md"},
                ],
                "join_policy": "none",
                "stop_conditions": [
                    "Every quantitative claim is tagged primary-source or demoted to open-residue when unverifiable.",
                ],
            },
            {
                "step_id": "governed-definitions",
                "name": "Govern glossary and load-bearing definitions",
                "capability_ref": "definitions-governance",
                "capability_metadata": EXTERNAL_META,
                "pattern": "sequential",
                "parallel": False,
                "techniques": ["sequence"],
                "inputs": [
                    {"kind": "ledger", "ref": f"{slug}-claim-ledger"},
                ],
                "outputs": [
                    {"kind": "artifact", "ref": f"{base}/definitions.md"},
                ],
                "join_policy": "none",
            },
            {
                "step_id": "distill-operator-model",
                "name": "Distill the operator model and borrow/block decisions",
                "capability_ref": "distill",
                "pattern": "distill",
                "parallel": False,
                "techniques": ["scu_swu_reduction"],
                "inputs": [
                    {"kind": "ledger", "ref": f"{slug}-claim-ledger"},
                    {"kind": "artifact", "ref": f"{base}/definitions.md"},
                ],
                "outputs": [
                    {"kind": "frame", "ref": f"{slug}-operator-model-frame"},
                    {"kind": "artifact", "ref": f"{base}/distill.md"},
                ],
                "join_policy": "none",
                "convergence_criteria": [
                    "Produce a one-sentence model and a compositional spine.",
                    "Separate borrow-carefully, analogy-only, and block decisions for Jusbrasil.",
                ],
            },
            {
                "step_id": "learning-pack",
                "name": "Synthesize the accelerated learning pack",
                "capability_ref": "research-tower",
                "capability_metadata": EXTERNAL_META,
                "pattern": "synthesis",
                "parallel": False,
                "techniques": ["frame_handoff"],
                "inputs": [
                    {"kind": "frame", "ref": f"{slug}-operator-model-frame"},
                    {"kind": "artifact", "ref": f"{base}/claim-ledger.md"},
                ],
                "outputs": [
                    {"kind": "artifact", "ref": f"{base}/LEARNING-PACK.md"},
                    {"kind": "trace_event", "ref": f"{slug}-learning-pack-synthesized"},
                ],
                "join_policy": "none",
                "convergence_criteria": [
                    "Source-backed claims are separated from operator readings.",
                    "Honest cutoff names what still requires the full PDF.",
                ],
            },
            {
                "step_id": "handoff-read-plan",
                "name": "Hand off the accelerated reading plan",
                "capability_ref": "invoke",
                "pattern": "handoff",
                "parallel": False,
                "inputs": [
                    {"kind": "artifact", "ref": f"{base}/LEARNING-PACK.md"},
                ],
                "outputs": [
                    {"kind": "handoff", "ref": f"{slug}-accelerated-read-handoff"},
                    {"kind": "trace_event", "ref": f"{slug}-read-plan-prepared"},
                ],
                "join_policy": "none",
            },
        ],
        "gates": [
            {
                "gate_id": "source-evidence",
                "kind": "quality",
                "owner": "research-tower",
                "condition": "Every claim cites the source or is labeled local-inference/analogy/open-residue; no invented numbers.",
                "on_fail": "flag",
            },
            {
                "gate_id": "private-boundary",
                "kind": "policy",
                "owner": "domainspec-core",
                "condition": "Tower artifacts stay under research/jusbrasil-call/ in the private parent; never written into the public arcanum submodule.",
                "on_fail": "block",
            },
            {
                "gate_id": "no-promotion",
                "kind": "promotion_guardrail",
                "owner": "arcanum",
                "condition": "Tower outputs are local research artifacts; they must not promote inventory, ontology, glossary, sigil, or spell knowledge.",
                "on_fail": "block",
            },
        ],
        "observability": {
            "dispatch_id_required": True,
            "parent_dispatch_id": "jusbrasil-legal-nlp-deep-research-20260610",
            "trace_events": [
                f"{slug}-source-recovered",
                f"{slug}-learning-pack-synthesized",
                f"{slug}-read-plan-prepared",
            ],
            "signal_grouping": "jusbrasil-paper-towers",
        },
        "promotion_guardrails": [
            "Tower findings remain local research artifacts pending a separate governed promotion decision.",
            "Do not write paper-decomposition content into the public arcanum submodule.",
        ],
    }


results = []
for p in PAPERS:
    out = TOWERS / p["slug"] / "read-decompose.dispatch.json"
    out.write_text(json.dumps(build(p), indent=2, ensure_ascii=False), encoding="utf-8")
    proc = subprocess.run(
        ["python3", str(VALIDATOR), str(out)],
        capture_output=True, text=True,
    )
    line = proc.stdout.strip().splitlines()[0] if proc.stdout.strip() else "NO-OUTPUT"
    extra = proc.stdout.strip() + "\n" + proc.stderr.strip()
    results.append((p["slug"], line, extra.strip()))

print("=== VALIDATION SUMMARY ===")
for slug, line, extra in results:
    print(f"{line:18}  {slug}")
nonpass = [r for r in results if r[1] != "VALIDATION=pass"]
if nonpass:
    print("\n=== NON-PASS DETAIL ===")
    for slug, line, extra in nonpass:
        print(f"\n--- {slug} ---\n{extra}")
else:
    print("\nALL 8 PASS")

## Agent 1 — competition mechanics

{
  "action_id": "spawn-0001",
  "role": "competition-explorer",
  "capability": "research",
  "status": "pass_with_limits",
  "mutation_policy": "read-only",
  "writes_performed": [],
  "authority_ceiling": "Candidate game-mechanics research only. No Body War rule, geometry, score authority, RunCoin behavior, reward, or adoption decision is established.",
  "observations": [
    {
      "claim": "The supplied Inventory packet says generic Challenge and Season concepts exist, while rolling record bounties, ability divisions, sponsor redemption, and RunCoin behavior remain unresolved.",
      "source": "STRATEGY-INVENTORY-PACKET.md#unresolved-gaps-and-residue",
      "proof_status": "discovery-only; direct owners not inspected in this bounded action"
    },
    {
      "claim": "No source-backed Taquaral route geometry or lap boundary is established.",
      "source": "STRATEGY-INVENTORY-PACKET.md#unresolved-gaps-and-residue",
      "proof_status": "active gap; prohibits guessed dimensions"
    }
  ],
  "external_source_table": [
    {
      "source": "Strava Help Center, Strava Challenges",
      "identity": "https://support.strava.com/en-us/articles/15401916-strava-challenges",
      "selector": "lines 23-65 and 80-87",
      "evidence": "Challenges may span a day through a month and use distance, time, segment, or active-day goals. Leaderboard eligibility excludes manual activities, requires qualifying public activity, varies sorting metrics, supports flagging, and separates partner prize eligibility from participation. Strava explicitly acknowledges GPS inaccuracy.",
      "proof_status": "current official platform precedent; not authority for Body War"
    },
    {
      "source": "Patel et al., STEP UP randomized clinical trial",
      "identity": "doi:10.1001/jamainternmed.2019.3505; https://pmc.ncbi.nlm.nih.gov/articles/PMC6735420/",
      "selector": "Key Points, Abstract Results, Interventions",
      "evidence": "Among 602 adults, support, collaboration, and competition gamification increased activity during intervention; competition produced the largest measured increase. The design used a baseline/run-in, precommitment, points, levels, and small comparison groups.",
      "proof_status": "peer-reviewed empirical evidence; population and intervention do not prove track-racing outcomes"
    },
    {
      "source": "Patel et al., BE FIT randomized clinical trial",
      "identity": "doi:10.1001/jamainternmed.2017.3458; https://pmc.ncbi.nlm.nih.gov/articles/PMC5710273/",
      "selector": "Key Points, Abstract Results, Discussion",
      "evidence": "Behaviorally designed gamification with social incentives increased goal achievement and steps during intervention, but effects declined in follow-up.",
      "proof_status": "peer-reviewed empirical evidence supporting cadence/feedback, with durability caution"
    },
    {
      "source": "Patel et al., veterans randomized clinical trial",
      "identity": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8271358/",
      "selector": "Key Points and Abstract Results",
      "evidence": "Loss-framed financial incentives plus gamification produced a modest intervention-period increase that was not sustained during follow-up.",
      "proof_status": "peer-reviewed caution against assuming durable motivation from material incentives"
    }
  ],
  "candidate_rules": {
    "common": [
      "Require explicit opt-in before each event window.",
      "Freeze division at window opening; results never retroactively change division.",
      "Admit only one best verified result per participant per event and mode; retain rejected attempts for audit without leaderboard effect.",
      "Separate Open Record, Ability Division, and Personal Breakthrough leaderboards.",
      "Treat every result as provisional until the geometry and verification lanes admit it.",
      "Use elapsed time, not moving time, for Speed; Distance uses a fixed duration and only verified qualifying distance.",
      "Resolve ties first by exact primary metric, then earliest verified submission; if timestamps are not reliably comparable, declare a shared placing rather than inventing precision.",
      "Provide a free participation path and avoid charging more for repeated attempts; attempt-cost economics remain outside this lane."
    ],
    "daily": {
      "purpose": "low-friction personal engagement",
      "window": "local calendar day, announced timezone",
      "modes": "one fixed verified course for Speed; one fixed short duration for Distance",
      "ladder": "Personal Breakthrough primary; Ability Division secondary; no Open Record bounty settlement",
      "attempt_rule": "unlimited recordings but only best verified result counts",
      "reset": "result closes daily; personal baseline rolls forward only after verification"
    },
    "weekly": {
      "purpose": "peer competition with enough time for schedule flexibility",
      "window": "seven fixed calendar days",
      "modes": "Speed and Distance are separate events",
      "ladder": "frozen Ability Division primary; Open Record separately visible",
      "attempt_rule": "best verified result counts; publish attempt count to expose brute-force advantage",
      "reset": "division placing resets weekly; verified records persist"
    },
    "monthly": {
      "purpose": "record-focused championship",
      "window": "fixed calendar month",
      "modes": "separate Speed and Distance championships",
      "ladder": "Open Record plus frozen Ability Division and Personal Breakthrough",
      "attempt_rule": "best verified result counts; candidate reward eligibility may impose a product-decided attempt cap, never inferred here",
      "reset": "event standings reset monthly; record persists until validly broken or geometry version retires"
    },
    "newcomer_placement": "Collect a noncompetitive calibration set before division placement. Until the minimum sample is met, newcomer results may appear in Open/Personal views but cannot win a division reward.",
    "division_movement": "Recalculate only between windows from a trailing verified-performance measure. Promotion requires repeated performance above the boundary; demotion requires repeated performance below it plus an inactivity-neutral rule. Exact thresholds require simulation and owner decision.",
    "inactivity": "Do not demote solely due to inactivity. Mark rating stale and require recalibration after a product-decided interval.",
    "rollover": "A failed record attempt does not transfer participant-paid value into a pot in this lane. If a sponsor-funded bounty exists, it may roll only under separately approved economy rules and a published cap/expiry.",
    "safety": "Daily goals should emphasize achievable participation; weekly/monthly maximum-performance events need recovery guidance, voluntary withdrawal, and no mechanic that rewards unsafe repeated maximal attempts."
  },
  "failure_modes": [
    {
      "risk": "sandbagging",
      "control": "calibration period, frozen divisions, delayed movement, Open leaderboard visibility",
      "residual_decision": "rating formula and thresholds"
    },
    {
      "risk": "attempt-volume advantage",
      "control": "one best result plus visible attempt count; no pay-to-retry advantage",
      "residual_decision": "whether reward-bearing events need an attempt cap"
    },
    {
      "risk": "newcomer prize farming",
      "control": "provisional placement cannot win division rewards"
    },
    {
      "risk": "elite dominance discourages ordinary runners",
      "control": "Personal Breakthrough primary in daily cadence and frozen ability divisions weekly/monthly"
    },
    {
      "risk": "short-lived incentive effect",
      "control": "periodic fresh starts, social feedback, and meaningful personal progress rather than escalating monetary stakes"
    },
    {
      "risk": "unsafe overexertion",
      "control": "separate participation cadence from record cadence; do not reward repeated maximal daily efforts"
    }
  ],
  "worked_examples": [
    {
      "cadence": "daily",
      "example": "Ana has a verified 2 km personal baseline of 14:00. Today she records 13:52 and 13:40; the latter is provisionally best. After verification it becomes her 13:40 Personal Breakthrough. It does not establish track control or an Open Record."
    },
    {
      "cadence": "weekly",
      "example": "Bruno and Carla enter Division B frozen at Monday opening. Bruno submits verified 5 km times of 27:10 and 26:55; Carla submits 26:55 once. Both share the exact primary metric. If reliable verification timestamps exist, the earlier verified submission ranks first; otherwise they share placing. Neither moves division until the window closes."
    },
    {
      "cadence": "monthly",
      "example": "Diego leads the verified fixed-duration Distance event at 42.4 km. Elisa submits 42.8 km, but verification flags a vehicle-like segment; her result remains provisional and cannot settle the event. If cleared before the published evidence deadline, she wins; otherwise Diego wins and any sponsor bounty follows the separately approved settlement policy."
    }
  ],
  "recommendations": {
    "adopt_as_candidate": [
      "three distinct ladders",
      "frozen divisions per event window",
      "provisional newcomer status",
      "best verified result per window",
      "daily personal-progress emphasis",
      "weekly division competition",
      "monthly record emphasis"
    ],
    "owner_decisions_required": [
      "rating inputs, division count, boundaries, promotion/demotion thresholds, and stale-rating interval",
      "timezone and evidence deadlines",
      "tie policy where timestamp precision is insufficient",
      "attempt cap for reward-bearing events",
      "whether any reward or bounty exists",
      "health eligibility, minors, and recovery policy"
    ],
    "defer": [
      "all exact Taquaral distances, lap counts, and route-specific Speed rules",
      "all RunCoin, paid-attempt, rolling-pot, and sponsor-redemption semantics",
      "record settlement until geometry and verification contracts are admitted"
    ],
    "kill_in_this_lane": [
      "pay-to-retry affecting competitive odds",
      "immediate division demotion from inactivity",
      "newcomer division-prize eligibility before calibration",
      "daily maximum-effort record bounty",
      "treating provisional GPS output as a verified record"
    ]
  },
  "limitations": [
    "The action inputs named only the dispatch sheet and Inventory packet. Direct Body War owner files were therefore not inspected; owner-alignment claims remain unverified.",
    "No geometry evidence was researched or invented.",
    "Economic, legal, privacy, and anti-cheat conclusions belong to the other explorer lanes.",
    "External evidence supports candidate design rationale, not adoption or guaranteed outcomes."
  ],
  "receipt_target": "receipts/explorer-competition.json",
  "persistence": "not_written because write_scope was empty"
}

## Agent 2 — track geometry and verification

{
  "receipt_id": "explorer-geometry",
  "action": "spawn-0002",
  "role": "geometry-explorer",
  "capability": "research",
  "mode": "explore",
  "status": "complete",
  "mutation": {
    "policy": "read-only",
    "files_written": [],
    "persistence_note": "Receipt content returned to parent for persistence because this action had no write scope."
  },
  "authority_ceiling": "Research candidate only. No geometry, challenge rule, score authority, product behavior, or adoption decision is established.",
  "verdict": {
    "volta_do_taquaral_exact_binding": "UNRESOLVED",
    "reason": "The inspected official Campinas sources establish that municipal spatial metadata and some downloadable shapefiles exist, but no inspected source identifies a runnable Volta do Taquaral centerline, start/finish gates, direction, usable corridor, or certified length. No coordinate, length, or lap boundary may be inferred from place descriptions or an unlabeled municipal layer.",
    "gap_preserved": "GAP-TAQUARAL-GEOMETRY-001"
  },
  "evidence": [
    {
      "id": "dispatch-sheet",
      "kind": "dispatch authority",
      "identity": "projects/body-war/development/research/20260812-track-challenge-rules-geometry/DISPATCH-SHEET.json",
      "selector": "$.groups[?(@.group_id=='explorers')].agents[1]",
      "claim": "Requires exact source identity, selector or structured pointer, and proof status for every load-bearing Taquaral geometry claim.",
      "proof_status": "observed-local"
    },
    {
      "id": "inventory-packet",
      "kind": "discovery-only read model",
      "identity": "projects/body-war/development/research/20260812-track-challenge-rules-geometry/STRATEGY-INVENTORY-PACKET.md",
      "selector": "#unresolved-gaps-and-residue",
      "claim": "GAP-TAQUARAL-GEOMETRY-001 is active; no source-backed route geometry or lap boundary is established.",
      "proof_status": "observed-local; not owner authority"
    },
    {
      "id": "pmc-spatial-metadata-service",
      "kind": "official municipal service",
      "identity": "https://portal-adm.campinas.sp.gov.br/servico/consultar-metadados-espaciais",
      "selector": "lines 58-64, 89-104, 106-111 as retrieved 2026-08-12",
      "claim": "Campinas exposes metadata about municipal GIS layers, including dates, projection, origin and construction method; some layers can be downloaded as shapefiles.",
      "proof_status": "official-current service description; no Taquaral running-route layer identified"
    },
    {
      "id": "pmc-environmental-spatial-data-service",
      "kind": "official municipal service",
      "identity": "https://portal-adm.campinas.sp.gov.br/servico/cessao-de-informacoes-ambientais",
      "selector": "lines 54-64, 66-100, 111-117 as retrieved 2026-08-12",
      "claim": "Environmental shapefiles can be requested through Campinas SEI, require an authenticated account and identity documents, and are supplied after municipal review.",
      "proof_status": "official-current acquisition route; not executed because credentials/external submission were forbidden"
    },
    {
      "id": "geojson-standard",
      "kind": "stable technical standard",
      "identity": "RFC 7946, August 2016, https://www.rfc-editor.org/info/rfc7946/",
      "selector": "Section 4 and Section 11.2",
      "claim": "GeoJSON uses WGS 84 longitude/latitude coordinates and defines interoperability and coordinate-precision considerations.",
      "proof_status": "normative format source"
    },
    {
      "id": "osm-license",
      "kind": "provider license",
      "identity": "https://www.openstreetmap.org/copyright",
      "selector": "OpenStreetMap licensing; How to credit OpenStreetMap",
      "claim": "OSM data is ODbL-licensed and requires attribution and license disclosure.",
      "proof_status": "license evidence only; OSM geometry was not treated as official municipal geometry"
    }
  ],
  "track_geometry_contract_v0": {
    "classification": "product proposal derived from the dispatch requirements and technical standards; not adopted",
    "identity_and_provenance": {
      "required": [
        "geometry_id",
        "geometry_version",
        "canonical serialized artifact",
        "sha256 digest of exact canonical bytes",
        "source organization",
        "source dataset title and immutable release/version",
        "source-local feature identifier or selector",
        "retrieval timestamp",
        "license identifier and attribution text",
        "transformation recipe and tool versions",
        "review status"
      ],
      "canonical_encoding": "RFC 7946 GeoJSON, positions ordered longitude then latitude; canonicalization algorithm must be named before digesting."
    },
    "shape": {
      "centerline": "LineString or closed MultiLineString forming one ordered base lap",
      "corridor": "Explicit polygon derived from a stated buffer algorithm and width, or independently sourced polygon; never an implicit visual tolerance",
      "start_gate": "Directed line segment intersecting the centerline once",
      "finish_gate": "Directed line segment; may equal start gate only for a closed lap",
      "direction": "clockwise, counterclockwise, or ordered segment traversal",
      "base_lap": "Ordered traversal from start gate to finish gate with no skipped mandatory segment",
      "challenge_definition": "Either integer lap multiplier for distance/speed challenges or fixed elapsed-duration window; geometry does not decide event semantics"
    },
    "matching": {
      "input_minimum": [
        "ordered timestamped positions",
        "declared device/source",
        "accuracy estimate per sample when available",
        "activity owner consent binding"
      ],
      "procedure": [
        "Reject non-monotonic timestamps and duplicate/replayed evidence identifiers.",
        "Project to one pinned local metric CRS or use one pinned geodesic library/version.",
        "Map-match samples to the versioned corridor and ordered centerline.",
        "Require directed start-gate crossing, ordered mandatory-segment coverage, and directed finish-gate crossing.",
        "Compute route completion independently from device-reported distance.",
        "Retain quality metrics and rule-version identity with the decision."
      ],
      "threshold_policy": "No numeric corridor, sample gap, accuracy, speed, or completion threshold is proposed as fact. Each must be calibrated from consented field traces plus synthetic fixtures, versioned, and owner-approved.",
      "partial_laps": "Never count toward a completed speed lap. For fixed-duration distance, count only verified centerline progress since the last completed lap; freeze the interpolation algorithm and cap progress at the next mandatory segment.",
      "pauses": "Use wall-clock elapsed time between gate crossings for speed records. Fixed-duration distance stops exactly at the event-duration boundary. Device auto-pause cannot reduce elapsed time.",
      "geometry_change": "Any coordinate, gate, direction, corridor, transformation, or threshold change creates a new geometry version and digest. Results remain bound to their original version and are not directly merged into the new record table without an explicit comparability decision."
    },
    "evidence_states": [
      "candidate",
      "calibrating",
      "verified",
      "suspended",
      "retired"
    ],
    "privacy_and_safety": {
      "activity_ownership": "Require authenticated ownership or explicit delegation plus consent for challenge use.",
      "data_minimization": "Store the smallest verification trace; public views expose result and geometry version, not raw timestamps or home-adjacent trace tails.",
      "exclusions": "A separately governed safety mask may exclude road crossings, closed areas, construction, or hazardous segments. A safety-mask change triggers geometry revalidation.",
      "vehicle_detection": "Flag physically implausible speed/acceleration and discontinuities for review; do not automatically label a participant fraudulent from GPS alone.",
      "appealability": "Preserve rule version, quality metrics, flags and deterministic reason codes."
    }
  },
  "deterministic_synthetic_fixtures": [
    {
      "id": "SYN-GEO-001",
      "geometry": "Closed square centerline with four ordered mandatory vertices and an explicit start/finish gate; arbitrary local metric coordinates, clearly non-Taquaral.",
      "trace": "One ordered loop entirely inside the corridor, monotonic timestamps, directed gate crossings.",
      "expected": "one completed lap"
    },
    {
      "id": "SYN-GEO-002",
      "geometry": "SYN-GEO-001",
      "trace": "Starts after the gate, covers three sides, never crosses finish.",
      "expected": "zero speed laps; partial distance only if fixed-duration rules explicitly permit it"
    },
    {
      "id": "SYN-GEO-003",
      "geometry": "SYN-GEO-001",
      "trace": "Traverses the full square in reverse direction.",
      "expected": "route-direction failure"
    },
    {
      "id": "SYN-GEO-004",
      "geometry": "SYN-GEO-001",
      "trace": "Cuts diagonally across the square and rejoins near finish.",
      "expected": "mandatory-segment coverage failure"
    },
    {
      "id": "SYN-GEO-005",
      "geometry": "Two versions differing by one coordinate or gate endpoint.",
      "expected": "different canonical digest; old result remains bound to old version"
    }
  ],
  "adversarial_examples": [
    {
      "case": "replayed GPX under a second account",
      "required_outcome": "duplicate-evidence flag and no automatic settlement"
    },
    {
      "case": "vehicle-assisted lap",
      "required_outcome": "speed/acceleration quality flag and manual-review state"
    },
    {
      "case": "GPS jump from start to finish",
      "required_outcome": "sample-gap or ordered-coverage failure"
    },
    {
      "case": "parallel sidewalk just outside calibrated corridor",
      "required_outcome": "deterministic mismatch; calibration evidence must show whether exclusion is fair"
    },
    {
      "case": "legitimate drift under tree cover",
      "required_outcome": "quality/provisional state rather than fabricated precision or silent rejection"
    }
  ],
  "taquaral_acquisition_protocol": [
    "Search the official Campinas metadata catalog for pedestrian paths, park boundaries, gates, closures and transport/safety layers; capture dataset title, custodian, feature ID, release date, CRS, lineage, accuracy, license and downloadable release URL.",
    "If no public layer contains the intended running course, an authorized owner may request the relevant municipal shapefile through SEI. This requires credentials and personal documentation and was not performed.",
    "Obtain written identification from the municipal park or sports authority of the intended runnable course, direction, operational start/finish location, closures and permitted hours. A generic park boundary is insufficient.",
    "Freeze received source bytes and compute their digest. Record the exact selected features and deterministic transformation into RFC 7946 GeoJSON.",
    "Conduct a consented field survey with multiple device classes and repeated traversals; keep this as calibration evidence, not as municipal authority.",
    "Optionally compare against a timestamped OSM extract with exact element IDs/versions and required ODbL attribution. Treat mismatches as review signals; do not silently substitute OSM for the municipal source.",
    "Run synthetic, replay, shortcut, reverse-direction, drift, partial-lap and geometry-version fixtures. Publish thresholds only after calibration and owner review.",
    "Advance from candidate to verified only when source identity, license, exact artifact digest, safety review, calibration evidence and owner acceptance all close."
  ],
  "missing_exact_evidence": [
    "Official or explicitly consented course centerline",
    "Exact start and finish gates",
    "Required travel direction",
    "Authoritative runnable corridor and exclusions",
    "Certified or reproducibly computed base-lap length",
    "Source release/version and feature-level identifiers",
    "Applicable reuse license for the selected geometry",
    "Current closures and safety constraints",
    "Field-calibrated GPS tolerance and quality thresholds",
    "Owner acceptance of the exact geometry bytes and digest"
  ],
  "decision_matrix": [
    {
      "item": "TrackGeometry Contract v0 field set",
      "recommendation": "ADOPT AS CANDIDATE FOR SPECIFICATION",
      "basis": "Operationally testable structure; numerical thresholds remain open."
    },
    {
      "item": "Volta do Taquaral geometry",
      "recommendation": "DEFER",
      "basis": "Exact-binding evidence is absent."
    },
    {
      "item": "Guessing route from maps, prose, screenshots or reported popular distance",
      "recommendation": "KILL",
      "basis": "Cannot satisfy provenance, exact selector, license and digest requirements."
    },
    {
      "item": "OSM as cross-check",
      "recommendation": "ALLOW WITH LABEL",
      "basis": "Useful separately licensed evidence, but not municipal authority."
    },
    {
      "item": "Automatic fraud finding from GPS anomaly",
      "recommendation": "KILL",
      "basis": "Measurement anomaly is not proof of intent; use provisional review and appeal."
    }
  ],
  "handoff": {
    "next_owner": "synthesizer",
    "material_conflict_to_preserve": "A reproducible geometry contract can be proposed now, but a named Taquaral course cannot be represented as source-backed or verified.",
    "required_claim_label": "candidate contract plus unresolved municipal/field evidence acquisition"
  }
}

## Agent 3 — economy, sponsor, and participant risk

{
  "action_id": "spawn-0003",
  "role": "economy-risk-explorer",
  "status": "pass",
  "mutation_policy": "read-only",
  "writes": [],
  "output_ref": "receipts/explorer-economy-risk.json",
  "authority_ceiling": "Research and product-risk classification only; not Brazilian legal, tax, regulatory, accounting, sponsor, or product approval.",
  "source_boundary": {
    "observed_owner_state": [
      "STRATEGY-INVENTORY-PACKET.md#Unresolved-Gaps-And-Residue: RunCoin earning, spending, purchase, transfer, expiration, and redemption remain unresolved.",
      "STRATEGY-INVENTORY-PACKET.md#Design-Consequences: attempt token, reward credit, RunCoin, voucher, and legal tender must remain distinct.",
      "STRATEGY-INVENTORY-PACKET.md#Lookup-Status: Inventory is discovery-only and cannot adopt rules or establish authority."
    ],
    "limitation": "The persisted action supplied only DISPATCH-SHEET.json and STRATEGY-INVENTORY-PACKET.md as input references. No additional Body War owner files were opened, so owner-specific implementation claims remain unresolved."
  },
  "official_sources": [
    {
      "identity": "Brazil, Lei 5.768/1971, compiled text",
      "url": "https://www.planalto.gov.br/ccivil_03/leis/l5768compilado.htm",
      "selector": "art. 3, II",
      "fact": "The statutory exception concerns free prizes from an exclusively cultural, artistic, sporting, or recreational contest without chance, contestant payment, or linkage to acquisition/use of goods, rights, or services.",
      "proof_status": "official-primary"
    },
    {
      "identity": "Brazil, Lei 14.790/2023",
      "url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14790.htm",
      "selector": "arts. 2(I)-(III), 3-5, 20",
      "fact": "An aposta places value at risk expecting a prize; authorized fixed-odds betting is separately regulated, and sports-integrity/manipulation controls are explicit.",
      "proof_status": "official-primary"
    },
    {
      "identity": "Brazil, Código de Defesa do Consumidor, Lei 8.078/1990",
      "url": "https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm",
      "selector": "arts. 30-31 and advertising provisions",
      "fact": "Sufficiently precise offers bind suppliers, while offer information must be clear, accurate, prominent, in Portuguese, and disclose relevant health and safety risks.",
      "proof_status": "official-primary"
    },
    {
      "identity": "ANPD, LGPD FAQ",
      "url": "https://www.gov.br/anpd/pt-br/acesso-a-informacao/perguntas-frequentes/perguntas-frequentes",
      "selector": "questions 2.5-2.6",
      "fact": "Health data are sensitive; processing requires an applicable legal basis, and publicly accessible data do not escape LGPD principles and rights.",
      "proof_status": "official-regulator"
    },
    {
      "identity": "ANPD, RIPD guidance",
      "url": "https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/relatorio-de-impacto-a-protecaode-dados-pessoais-ripd",
      "selector": "questions 1-3",
      "fact": "ANPD recommends a data-protection impact report where processing may create high risk and requires description of processing, risks, safeguards, and mitigation.",
      "proof_status": "official-regulator"
    },
    {
      "identity": "ANPD, children and adolescents statement",
      "url": "https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-divulga-enunciado-sobre-o-tratamento-de-dados-pessoais-de-criancas-e-adolescentes",
      "selector": "Enunciado CD/ANPD 1/2023 summary",
      "fact": "Any LGPD legal basis may potentially apply to minors’ data, but the child’s or adolescent’s best interests must prevail.",
      "proof_status": "official-regulator"
    },
    {
      "identity": "Anvisa, RDC 243/2018",
      "url": "https://bvsms.saude.gov.br/bvs/saudelegis/anvisa/2018/rdc0243_26_07_2018.pdf",
      "selector": "arts. 1-2 and authorized-claims/labeling regime",
      "fact": "Supplements are subject to composition, safety, labeling, and permitted-claim requirements.",
      "proof_status": "official-primary"
    },
    {
      "identity": "Anvisa, Cuidado com a propaganda enganosa",
      "url": "https://www.gov.br/anvisa/pt-br/assuntos/alimentos/suplementos-alimentares/cuidado-com-a-propaganda-enganosa/",
      "selector": "prohibited-claims list",
      "fact": "Anvisa warns against unapproved performance and health claims, including miraculous physical-performance and muscle-gain claims.",
      "proof_status": "official-regulator"
    }
  ],
  "model_comparison": [
    {
      "model": "Participant-paid attempts feeding a rolling pot",
      "risk": "critical",
      "verdict": "KILL_FOR_PILOT",
      "reasons": [
        "Directly resembles placing participant value at risk for a prize under Lei 14.790 art. 2(I).",
        "Conflicts with the clean sporting-contest exception’s no-payment condition in Lei 5.768 art. 3(II).",
        "Creates whale advantage, sunk-cost chasing, collusion, chargeback, refund, minors, accounting, and pooled-liability problems.",
        "A skill-dominant outcome does not itself close promotion, betting, consumer, or prize-law classification."
      ]
    },
    {
      "model": "Earned-only capped bounty",
      "risk": "medium",
      "verdict": "VIABLE_WITH_GATES",
      "required_shape": [
        "Credits cannot be purchased, transferred, cashed out, gifted, or funded through participant consideration.",
        "A genuinely free attempt route has equal eligibility and verification treatment.",
        "Per-person earning, burn, and bounty caps are published before the event.",
        "Credits are gameplay accounting units, not ownership, money, deposit, investment, or guaranteed redeemable value.",
        "Any material redemption receives separate legal, tax, accounting, and consumer review."
      ]
    },
    {
      "model": "Split ledger: gameplay credits burned; sponsor funds fixed vouchers",
      "risk": "lowest of compared candidates",
      "verdict": "RECOMMEND_PILOT_CANDIDATE",
      "required_shape": [
        "Participant credits never fund, size, or determine the voucher pool.",
        "Sponsor commits fixed voucher quantity/value before opening the event.",
        "Voucher availability is reserved or guaranteed; participant losses never roll into prizes.",
        "No purchase is required and no paid attempt receives competitive advantage.",
        "Settlement and voucher terms remain separate ledgers with auditable immutable entries."
      ]
    }
  ],
  "safest_viable_candidate": {
    "competition": "Verified sporting performance determines the winner under prepublished deterministic rules.",
    "access": "Adults-only initial pilot; one equal free qualifying path; no paid attempts.",
    "gameplay_credit": "Earned-only, non-purchasable, non-transferable, non-cashable, capped, and burnable only for non-economic gameplay functions.",
    "reward": "A fixed sponsor-funded voucher inventory, reserved before event opening and independent of attempts or burned credits.",
    "bounty": "If rollover is retained, only unfunded sponsor inventory rolls forward; no participant stake or purchase-derived value enters the bounty.",
    "settlement": "Provisional result, fraud-review hold, appeal deadline, final result, and voucher issuance are distinct states.",
    "privacy": "Public leaderboard uses a pseudonym and minimized result fields; raw route, device, health, and fraud evidence remain access-controlled with stated retention.",
    "legal_gate": "Brazilian counsel and, where applicable, SPA/Ministry of Finance classification before public launch or any prize-bearing promotion."
  },
  "mandatory_terms_and_disclosures": [
    "Promoter and sponsor legal identities; territorial and age eligibility.",
    "No purchase required; exact free-entry mechanism and equal treatment.",
    "Event window, timezone, course/version, performance rule, evidence deadline, and deterministic tie rule.",
    "Attempt limits; duplicate-account prohibition; device/activity ownership and consent representations.",
    "Verification criteria, fraud flags, manual-review authority, decision evidence, appeal window, and finality.",
    "Fixed voucher description, face value, quantity, expiry, transfer restrictions, tax responsibility, inventory reservation, and fulfillment party.",
    "Cancellation/postponement rules; treatment of provisional results and sponsor nonperformance.",
    "No cash equivalent; gameplay credits’ non-purchase, non-transfer, non-withdrawal, and no-property-interest status.",
    "Privacy notice covering controller/operator roles, purposes, legal bases, raw geolocation and inferred health/performance data, recipients, retention, deletion, security, and data-subject channels.",
    "Safety warning, voluntary participation, stop/withdraw path, emergency guidance, and explicit statement that rewards do not imply medical or performance suitability.",
    "No unauthorized therapeutic, muscle-gain, or performance claims for supplement rewards."
  ],
  "adversarial_controls": {
    "collusion_and_multi_accounting": "Identity uniqueness without public legal identity; device/account graph flags; delayed settlement; no shared activity evidence; appealable manual review.",
    "sandbagging": "Freeze divisions before the event using prior verified evidence; exclude current event performance from downward placement; impose upward movement without retroactive prize reassignment.",
    "whales_and_prize_farming": "No purchasable attempts; per-person attempt and reward caps; one prize per defined period; credits cannot raise prize probability or value.",
    "unsafe_overexertion": "Finite attempts, recovery interval, no streak multiplier for repeated maximal efforts, withdrawal without forfeiting unrelated balances, and high-risk weather/course cancellation.",
    "ties": "Prepublish exact rule: equal performance within measurement precision shares rank; use equal fixed vouchers or a disclosed deterministic non-economic tiebreaker—never a surprise extra paid attempt.",
    "chargeback": "Eliminated from competitive entry by forbidding paid attempts; ordinary sponsor/payment disputes cannot reverse verified athletic results.",
    "sponsor_insolvency_or_inventory_failure": "Reserve inventory or escrow equivalent before opening; otherwise do not launch. Sponsor failure cannot be covered from participant credits.",
    "expiry": "Voucher expiry and claim window disclosed before entry; gameplay-credit expiry, if any, cannot erase purchased value because purchase is prohibited.",
    "minors": "Exclude from the first prize-bearing pilot. Any later minor route requires a separate best-interests, guardian, safety, advertising, and privacy design.",
    "auditability": "Append-only ledger separating credit issuance/burn, sponsor commitment, provisional result, holds, appeals, final settlement, and voucher fulfillment."
  },
  "owner_decisions": [
    {
      "decision": "Is any participant payment, purchasable credit, or purchase-linked eligibility intended?",
      "recommendation": "No",
      "gate": "If yes, stop and obtain specialist Brazilian promotion/betting/consumer analysis."
    },
    {
      "decision": "Is sponsor reward inventory fixed and secured before entry?",
      "recommendation": "Yes",
      "gate": "No launch without a fulfillment backstop."
    },
    {
      "decision": "Do gameplay credits have material redemption?",
      "recommendation": "No for pilot",
      "gate": "If yes, separately decide valuation, expiry, accounting, tax, consumer, and insolvency treatment."
    },
    {
      "decision": "Are minors eligible?",
      "recommendation": "No for pilot",
      "gate": "Separate child-safety and LGPD review required."
    },
    {
      "decision": "Will raw routes or health/performance inferences be public or sponsor-accessible?",
      "recommendation": "No",
      "gate": "Publish minimized derived results only; define controller, processor, basis, retention, and RIPD."
    }
  ],
  "kill_conditions": [
    "Any participant-funded or purchase-derived rolling prize pool.",
    "Pay-to-attempt, pay-to-improve odds, or purchasable competitive energy.",
    "Cash-out, transfer, secondary market, or promised monetary equivalence for gameplay credits.",
    "Prize launch without precommitted inventory, cancellation terms, and an accountable fulfiller.",
    "Eligibility or reward terms changed after the event opens.",
    "Public precise route traces or sponsor access to raw geolocation/health evidence without a separately approved lawful-purpose design.",
    "Minor participation in the initial prize-bearing pilot.",
    "Unlimited or rapid-repeat maximal-effort attempts.",
    "Supplement rewards marketed with unauthorized health or performance claims.",
    "A launch claim that the sporting-skill format alone makes the scheme lawful."
  ],
  "residual_uncertainties": [
    "Whether the final promotion requires SPA authorization or qualifies for an exception depends on exact organizer, advertising purpose, consideration, prize, and entry mechanics.",
    "Tax and accounting treatment depends on promoter/sponsor entities, voucher structure, valuation, and settlement flow.",
    "The current Body War owner files must be inspected before claiming that any proposed ledger, privacy, verification, or reward field is already owned or implemented."
  ]
}

## Connections

- derives -> `./findings.md`

# Arcanum Add-on Selection Revalidation Strategy

## P1 Trigger

Dispatch is required by isolation and parallelism. `B-DESIGN-001` can close
only if two fresh judgments independently inspect the same repaired bytes.
Combining static coverage and executable falsification before return would erase
the disagreement evidence needed for the audit.

## Lanes And Subagents

One read-only group runs two agents in parallel over the same complete corpus:

| Lane | Pooled identity | Role | Anti-bias angle | Expected output |
| --- | --- | --- | --- | --- |
| Proposer | Nyquist, Harry | explorer | formal one-to-one closure over 25 SWUs, selection inputs, gate bindings, terminal echoes, internal-node exclusions, joins, and prior findings | exact-byte closure receipt with eight-finding matrix and PASS/BLOCK |
| Balancer | Niqui, Milad | explorer | executable falsification of replay, substitution, drift, sibling, internal-node, and crash paths | exact-byte adversarial receipt with eight-finding matrix and PASS/BLOCK |

The anti-bias axis is methodology: formal exact-mapping proof versus executable
admission falsification. Neither pooled identity was used by the immediately
prior review.

## Dependency Flow

The lanes are independent and have no feedback edge. After exact human
confirmation, the parent will:

1. register one schema-0.8.0 dispatch row;
2. spawn both agents once in one parallel wave;
3. join and close both;
4. preserve the raw receipts and synthesize the parent findings;
5. close `B-DESIGN-001` only if both validations pass over the exact current
   digest with no new CRITICAL or MAJOR finding; and
6. append exactly one close row.

The route does not mutate target planning files, create a real selection,
implement the add-on, refresh Bootstrap, run a browser, or change GitHub state.

## Inventory Preflight

- Owner machine index: ready; 267 entries; projection conformance pass.
- Warnings: 121 uncontrolled historical tags, non-blocking.
- Target machine index: unavailable.
- Selected:
  - completed repair-revalidation result;
  - completed Invoke re-entry repair result;
  - accepted Arcanum/ResonantOS/Augmentor owner topology.
- Excluded:
  - older strategy projections bound to 75-file or earlier corpora;
  - broader Augmentor architecture that cannot prove current admission behavior.
- Design consequence: use fresh identities, bind the complete 77-file corpus,
  separate formal mapping proof from executable falsification, and refuse
  authored labels or Inventory summaries as proof.
- Authority ceiling: Inventory is discovery only.

Machine packet: `strategy-inventory-packet.json`.

## Bound Corpus

- Product worktree:
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha-arcanum-addon-plan`
- `HEAD` and `origin/dev`:
  `80dcd79677ad73b21dbaded12e0e9cd47aace82b`
- File count: `77`
- Define digest:
  `dadac41fc6f10fe006da6307cb5b9b77168efd753a19ddcf1771aaf6e9cca375`
- Design digest:
  `49734371e38bac3f36fd8f6c523af21f604256caed321679c19d8bea02bdbb82`
- Plan digest:
  `120973d0bbae70610e4cdf3be1c536356bcd6904199615a399d00e2cd8e096cb`
- Aggregate corpus digest:
  `5fad9693428f841a10cec7d2ee0c5e599826ea204a75ac57177fe70f55f466a0`
- Dispatch digest:
  `a482f98a5dbf6fea4b6684c6fc788b9552be360fb5365f836276f3bd9c9acbc4`
- Work-pack digest:
  `a34a5d8ff52d944c6edeb9a6c5511feecfa72501c8201dac7fd30d369740148f`
- Selection schema digest:
  `b37f50f5dec1ceb04a8dc7ad3e1c1282ed156fe94d6d1ed4723c6d80e1655cbc`
- Selection validator digest:
  `353eaffa406083b70ee42c0eb14e86fd89bcac2faed87679d1a74233a38d0877`

## Gate And Ledger State

- Decision route: fresh independent exact-byte revalidation.
- Dispatch type: live `review`.
- DomainSpec form: schema `0.8.0`.
- Candidate sheet: `DISPATCH-SHEET.json`.
- Confirmation-readiness: pass at sheet SHA-256
  `6df73de5703c0a7740bb070c495d908482df468ff5f3b10b52492b17eb690274`;
  ledger mutation none.
- Dispatch Spec: pass at route SHA-256
  `62f49cfa93216aa1aca2e15fc810353577ce6116e0d5db9b72525c01c42820fe`.
- Check-tension: PASS/PASS with two independent handles bound to the exact
  sheet digest; see `CHECK-TENSION.md`.
- Human confirmation: required after readiness and PASS/PASS tension.
- Registration: not started.
- Review execution: not started.
- Closeout expectation: one resolved close row after both agents are joined and
  closed, even if the artifact verdict is FIX.

## Claim Ceiling

A later double-PASS review may close only `B-DESIGN-001`. `B-GOV-001`,
`B-BOOT-001`, `B-OWNER-001`, `B-ADAPTER-001`, and `B-RETENTION-001` remain
independent. SWU selection, implementation, browser evidence, readiness,
promotion, deployment, and release remain unclaimed.

## Next Human Action

After deterministic readiness and PASS/PASS tension are recorded, confirm the
exact persisted sheet digest once. Only then may registration and reviewer
execution start.

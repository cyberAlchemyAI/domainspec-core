# Golden Quill Task and Role Breakdown Handoff

Source workbook: `C:\Users\vlad_\Downloads\Golden Quill Task and Role Breakdown.xlsx`
Generated: 2026-06-12 16:25

## Purpose

This handoff extracts the workbook into Markdown so the task, role, staffing, and gap data can be used directly without opening Excel.

## Sheet Index

- [1. Node on the Desk](#node-on-the-desk)
- [2. After Acceleration](#after-acceleration)
- [3. Roles & Gaps](#roles-gaps)

## 1. Node on the Desk

**Workbook title:** GOLDEN QUILL — EVERYTHING REQUIRED TO PUT A WORKING NODE ON A CUSTOMER'S DESK

### Context / Legend

- BUILD = one-time (capital requirement)
- PER-NODE = repeats per customer (deployment cost)
- ONGOING = operating floor
- Staffed by the four
- Onboard NOW
- Onboard LATER
- Add hours/rates per row to budget

### Data

| Workstream | Task | Effort Type | Role | Filled By | Est. Hrs | Notes / Rate |
| --- | --- | --- | --- | --- | --- | --- |
| A. Hardware & Physical Node | Final hardware spec + certification of reference workstation; validate one approved alternative | BUILD | AI Engineer | Koichi |  |  |
| A. Hardware & Physical Node | Procurement process: supplier accounts, ordering, receiving, inventory | BUILD + PER-NODE | Founder / Ops | Josh |  |  |
| A. Hardware & Physical Node | Burn-in & acceptance test procedure per unit (thermal, memory, storage, inference benchmark) | BUILD, then PER-NODE | AI Engineer → Field Tech | Koichi → onboard later |  |  |
| A. Hardware & Physical Node | OS baseline: hardened config, disk encryption, accounts, drivers, network profile | BUILD | Backend Engineer | Vlad |  |  |
| A. Hardware & Physical Node | Imaging/cloning process — write Golden Image onto a unit repeatably, with verification | BUILD, then PER-NODE | Backend Engineer → Field Tech | Vlad → onboard later |  |  |
| A. Hardware & Physical Node | Peripherals kit + branded kit incl. cast-vinyl insignia | BUILD + PER-NODE | Founder / Ops | Josh |  |  |
| A. Hardware & Physical Node | Backup & export posture: local backup, customer-owned export, recovery | BUILD | Backend Engineer | Vlad |  |  |
| A. Hardware & Physical Node | Update-and-signing mechanism for deployed nodes | BUILD | Backend Engineer | Vlad |  |  |
| B. Software — Tilth Build | Local inference layer: primary model, embeddings, routing model, on-demand checkpoint swap | BUILD | AI Engineer | Koichi |  |  |
| B. Software — Tilth Build | Multi-model routing layer: policy-driven selection, card defaults, per-task override | BUILD | AI Engineer | Koichi |  |  |
| B. Software — Tilth Build | Vault: storage, classification labels, full-text + semantic indexes, classification-aware assembly | BUILD | Backend Engineer | Vlad |  |  |
| B. Software — Tilth Build | Ingestion pipeline: parsing, OCR, evidence extraction, document inventory | BUILD | AI Engineer | Koichi |  |  |
| B. Software — Tilth Build | Scout: source manifest, governed fetch, fetch ledger, refresh engine, opportunity DB, reality report | BUILD | AI + Backend Engineer | Koichi + Vlad |  |  |
| B. Software — Tilth Build | Grant Module Mapper: RFA decomposition into section plan (rubric weights, evidence, sensitivity) | BUILD | AI Engineer | Koichi |  |  |
| B. Software — Tilth Build | Section-by-section drafting workflow with human editorial loop | BUILD | AI Engineer | Koichi |  |  |
| B. Software — Tilth Build | Rubric review + compliance: multi-model ensemble + deterministic rule engine (kept separate) | BUILD | AI + Backend Engineer | Koichi + Vlad |  |  |
| B. Software — Tilth Build | Posture system: Unrestricted / Hybrid / Sanitized / Sovereign, technically enforced | BUILD | Backend Engineer | Vlad |  |  |
| B. Software — Tilth Build | Sanitization pipeline + split-context drafting pattern | BUILD | AI + Backend Engineer | Koichi + Vlad |  |  |
| B. Software — Tilth Build | Audit log: every invocation, payload class, cross-boundary event, hash | BUILD | Backend Engineer | Vlad |  |  |
| B. Software — Tilth Build | Operator console UI: read-only projection over real backend first, then interactive | BUILD | AI Engineer (full-stack) | Koichi |  |  |
| B. Software — Tilth Build | Evidence capture & report drafting from captured material | BUILD | AI Engineer | Koichi |  |  |
| B. Software — Tilth Build | Golden Image assembly: everything packaged as one installable, versioned, signed artifact | BUILD | Backend (lead) + AI Engineer | Vlad + Koichi |  |  |
| C. Quality, Security & Proof | Test plan + guardrails-as-tests: posture enforcement, classification, audit completeness, fail-closed | BUILD | QA / Measurement | Victor |  |  |
| C. Quality, Security & Proof | Internal deployment test: full install from checklist by someone who didn't write it | BUILD | QA / Measurement | Victor |  |  |
| C. Quality, Security & Proof | Independent security review: data boundary, Sovereign build, signing chain | BUILD | External Security Reviewer | Onboard NOW |  |  |
| C. Quality, Security & Proof | Claims register: every external claim mapped to its evidence category | BUILD + ONGOING | QA / Measurement | Victor |  |  |
| C. Quality, Security & Proof | Canonical demo standard (Scout population sequence) — live, never staged-as-live | BUILD | QA / Measurement | Victor |  |  |
| C. Quality, Security & Proof | Instrumentation: support hrs/node, usage metrics, baselines, renewal-intent capture | BUILD, then ONGOING | QA / Measurement | Victor |  |  |
| D. Capital Logic Content | Card schema + governance: structure, section-level defaults, testability rules | BUILD | Founder + Backend Engineer | Josh + Vlad |  |  |
| D. Capital Logic Content | Author & validate five launch cards (Farmer v1; four in authoring) with paid expert review | BUILD | Founder + Domain Experts | Josh + onboard NOW |  |  |
| D. Capital Logic Content | Search seed libraries + source universes per segment | BUILD | Founder | Josh |  |  |
| D. Capital Logic Content | Program rule packs for recurring funders (codified hard requirements) | BUILD + ONGOING | Founder + Backend Engineer | Josh + Vlad |  |  |
| E. Selling & Contracting | Sales materials: one-pager, demo, segment framing, pipeline tracker w/ disclosure rules | BUILD | Founder | Josh |  |  |
| E. Selling & Contracting | Qualification: readiness checklist, organizational-fluency test, fit/no-fit referral | PER-NODE | Founder | Josh |  |  |
| E. Selling & Contracting | Customer agreement, LOI template, data-policy spec, procurement notes, insurance | BUILD | Legal (fractional) + Founder | Onboard NOW + Josh |  |  |
| E. Selling & Contracting | Deposit handling, invoicing, deployment cost tracking | PER-NODE | Bookkeeper (fractional) | Onboard at first revenue |  |  |
| F. White-Glove Delivery (every customer) | Pre-deployment: document request, onboarding questionnaire, posture conversation, deployment record | PER-NODE | Customer Success | Josh early → onboard later |  |  |
| F. White-Glove Delivery (every customer) | Day 0 install: hardware, network, accounts, posture, Applied As, orientation, branded closeout | PER-NODE | Deployment Lead | Josh early → CS + Field Tech |  |  |
| F. White-Glove Delivery (every customer) | Vault build: ingestion, classification, applicant profile, evidence ledger, missing-doc list | PER-NODE | Customer Success + Founder | Josh early → onboard later |  |  |
| F. White-Glove Delivery (every customer) | Source universe: manifest, search grammar, refresh cadence, first Scout scan, scored opportunities | PER-NODE | Founder + Customer Success | Josh early → onboard later |  |  |
| F. White-Glove Delivery (every customer) | First opportunity packet: selection, decomposition, evidence map, blockers, draft plan | PER-NODE | Founder | Josh |  |  |
| F. White-Glove Delivery (every customer) | First draft workflow + training sessions 2–4 (Scout, drafting, capture/report/remember) | PER-NODE | Customer Success | Josh early → onboard later |  |  |
| F. White-Glove Delivery (every customer) | Day 60 use review: metrics, support load, renewal signal, next-cycle plan | PER-NODE | Customer Success + QA | Josh/Victor → onboard later |  |  |
| G. Company Operations | Entity hygiene, banking, bookkeeping, contracts filing, insurance | ONGOING | Founder + Bookkeeper | Josh + onboard later |  |  |
| G. Company Operations | Support channel + issue log; triage rules (support absorbs vs. engineering sees) | BUILD, then ONGOING | Customer Success + Engineers | Team early → onboard later |  |  |
| G. Company Operations | Node Care delivery: updates, source-index maintenance, quarterly check-ins, vault care | ONGOING | Customer Success + Backend | Team early → onboard later |  |  |
| G. Company Operations | Investor/funder relations, validation packet maintenance | ONGOING | Founder + QA / Measurement | Josh + Victor |  |  |

## 2. After Acceleration

**Workbook title:** WHAT COMES NEXT — AFTER STARTUP CAPITAL / ACCELERATION

### Data

| Theme | Tasks | Role | Est. Hrs | Notes / Rate |
| --- | --- | --- | --- | --- |
| Repeatability | Deployment playbook hardened until a non-founder runs an install end-to-end; install labor driven down; training curriculum standardized | Customer Success lead + Field Tech (built from Founder's first installs) |  |  |
| Sales beyond founder network | Partner channels (ag, municipal, co-op, arts); reference case studies with written permission; segment campaigns; pipeline discipline at volume | Founder → dedicated Sales/Partnerships role |  |  |
| Product hardening | Sovereign-mode build finished & audited; sanitization GA; multi-seat + role permissions; institutional/consortium governance; fleet-scale updates & monitoring | AI + Backend Engineers; full-time technical hire absorbs knowledge |  |  |
| Capital Logic Library | Outcome-data opt-in pipeline; anonymized pattern feedback into cards; offline refinement; new cards & extensions; expert bench expansion | Founder (editorial) + AI Engineer + Domain Experts |  |  |
| Service line validation | Grant-administration pilots at controlled scope; measure labor & reputational risk; hire admin lead only if pilots prove it | Founder (scoping); Admin Lead (conditional hire) |  |  |
| New markets | Tribal-nation Sovereign-mode pilots; institutional research offices; multi-site consortiums — governance + assurance before sales | Founder + Backend Engineer; Security Reviewer |  |  |
| Next financing | Data room, measured unit economics, support-load evidence, renewal data, channel plan | Founder + QA / Measurement |  |  |
| Team build-out | Full-time technical hire; customer-success hire; field tech; possibly sales — sequenced against deployed-node count | Founder (hiring); whole team (onboarding) |  |  |

## 3. Roles & Gaps

**Workbook title:** ROLE MAP — WHO CARRIES WHAT, AND WHAT TO ONBOARD

### Data

| Role | Carries | Filled By | Onboard Form / Trigger |
| --- | --- | --- | --- |
| Founder / Grant Strategy / Deployment Lead | Sales, qualification, Capital Logic synthesis, first-opportunity strategy, early installs, capital track | Josh | Staffed |
| AI Engineer (full-stack) | Inference, routing, ingestion, Scout, Mapper, drafting workflow, ensemble review, console UI, evidence capture | Koichi | Staffed |
| Backend Engineer / Domain Modeler | Vault, classification, posture enforcement, audit log, rule engine, OS baseline, imaging, signing, Golden Image | Vlad | Staffed |
| QA / Measurement / Epistemics | Guardrails-as-tests, deployment test, claims register, demo standard, instrumentation, Day 60 evidence | Victor | Staffed |
| Customer Success | Intake, weeks 1–4 cadence, training delivery, support front line, Node Care, Day 60 reviews | Josh absorbs first nodes | Part-time contract as deployments stack |
| Field / Install Tech | Burn-in, imaging execution, on-site hardware, peripherals | Engineers + Josh early | Part-time at volume; trained from checklist |
| Domain Experts (×4 segments) | Structured input + field correction on Educator, Municipal, Arts, Cooperative cards | — | Contract, paid structured input |
| Legal (fractional) | Customer agreement, LOI, data-policy terms, procurement language, FERPA / AI-transparency reading | — | Fractional, before first LOI signs |
| Security Reviewer | Independent audit of boundary enforcement + signing chain | — | One-time, recurring at major releases |
| Bookkeeper (fractional) | Deposits, invoicing, cost tracking, investor schedules | — | Few hrs/month at first revenue |
| Skills to weigh later | Technical writing/documentation; instructional design; public-procurement fluency (Municipal expert criterion); hardware logistics; privacy/compliance counsel | — | Fold into above roles where possible |

## Extraction Notes

- Blank leading workstream/phase cells were filled down in this Markdown version so each row remains self-contained.
- Empty cells from the workbook are left blank.
- Formula cells, if present, are preserved as formula text rather than computed-only values.

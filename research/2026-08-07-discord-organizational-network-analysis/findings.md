# Discord API and organizational network analysis: evidence-bound findings

Status: final research findings for the bounded dispatch. The official Discord documentation and policy pages summarized here were accessed by the explorer lane on 2026-08-07 and are mutable; they support current documentation claims, not runtime or target-server proof. [`research.md`, Agent 1, “Source inventory,” S1–S13 named headings/selectors; Agent 3, “Source register,” D1–D4 named headings/selectors]

## Executive verdict

Live, person-linked organizational network analysis (ONA) using Discord API Data is **BLOCKED** by the current Discord Developer Policy. Rule 16 prohibits using API Data to profile Discord users, their identities, or their relationships with other users, and prohibits its use for eligibility considerations such as employment. On its ordinary reading, user-user, user-channel, and role-user Discord relationship graphs fall inside that prohibition. Server-owner approval, participant consent, pseudonymization, content-free metadata, or an “organizational improvement” label cannot override the platform rule. Employment use is prohibited. [`research.md`, Agent 1, “Policy blocker and claim ceilings,” S11 “Handle Data with Care,” rules 15–21, especially rule 16; Agent 3, “Decisive gate,” D1 “Handle Data with Care,” items 15–21, especially item 16]

A coarse, non-relational channel/time aggregate is not cleared. It remains **HOLD** pending written Discord clarification of the exact fields, transformations, purpose, and outputs. Such clarification would be necessary but not sufficient: it could reopen only the platform-authorization gate, while observability, data quality, descriptive validity, privacy/ethics, and organizational decision authority would still require independent evidence or decisions. [`research.md`, Agent 1, “Metadata-only minimum” and “Policy blocker and claim ceilings,” S11 “Handle Data with Care,” rules 15–16; Agent 3, “Safer alternatives,” D1 “Handle Data with Care,” items 15–16]

The finite Discord-shaped fixture below is admitted only as an **unexecuted, manually recomputable synthetic paper specification**. It can be used to inspect proposed transformations and arithmetic. It is not API compatibility, collector, runtime, privacy, organizational-validity, deployment, or production evidence.

Voluntary self-report ONA and participatory team mapping remain **HOLD** as independently collected, non-Discord alternatives. Their protocols, population boundaries, voluntariness, privacy review, construct tests, and use authority are not established. Communication traces and survey networks are empirically related but materially different, and employee consent can be compromised by power imbalance. [`research.md`, Agent 2, “Defensible question ceiling,” Johnson, Kovács & Vicsek 2012, Abstract and Introduction; Agent 3, “Source register,” E1 Belmont Report, “Informed Consent—Information / Comprehension / Voluntariness,” and E2 EDPB Guidelines 05/2020, paragraphs 21–24 under “3.1.1 Imbalance of power”]

No credentials were requested or used. No Discord server was accessed. No bot was created or installed. No API was called. No data was collected. No collector or analysis runtime was executed. This document is not legal advice and grants no live-access, data, privacy, organizational-decision, implementation, publication, deployment, or production authority.

## Six independent gates

`PASS` applies only to the named gate. `BLOCK` stops the candidate. `OPEN` means evidence or an accountable decision is absent. `N/A` means the gate does not apply to the bounded candidate. Passing one gate never passes another.

| Candidate | API observability | Platform authorization | Data quality / completeness | Analytical / construct validity | Privacy / ethics | Organizational decision authority | Overall |
|---|---|---|---|---|---|---|---|
| Live person-linked Discord ONA | `OPEN`: relevant fields and events are documented in principle, but no target was tested. [`research.md`, Agent 1 “Observability matrix,” S1–S10 named selectors] | `BLOCK`: relationship profiling and employment-eligibility use are prohibited. [`research.md`, Agent 1 “Policy blocker,” S11 “Handle Data with Care” rule 16; Agent 3 “Decisive gate,” D1 item 16] | `OPEN`: no installation, permission, coverage, gap, history, denominator, or replay proof. [`research.md`, Agent 1 “Missing observations and blockers”] | `OPEN`: no external construct test; graph values are not organizational qualities. [`research.md`, Agent 2 “Defensible question ceiling,” Johnson et al. 2012, Abstract/Introduction] | `OPEN`: no acceptance decision; consent, admin approval, and pseudonyms do not cure rule 16. [`research.md`, Agent 3 “Minimum control set,” D1 item 16] | `OPEN`: none exists; organizational owners cannot override Discord policy. | **BLOCK** at the platform gate |
| Non-relational channel/time aggregates | `OPEN`: source events and counts are documented in principle, not verified on a target. [`research.md`, Agent 1 “Observability matrix,” S2 named event sections and S3 “Message Object”] | `OPEN`: written Discord clarification is required for exact design. [`research.md`, Agent 1 “Metadata-only minimum,” S11 rules 15–16; Agent 3 “Safer alternatives,” D1 items 15–16] | `OPEN`: no population, accessible-surface, gap, or denominator evidence | `N/A` for ONA; descriptive-count validity is `OPEN` | `OPEN`: no privacy or disclosure determination | `OPEN`: no release or use owner | **HOLD**; clarification is necessary, never sufficient |
| Fully synthetic Discord-shaped paper specification | `N/A`: no API access | `N/A`: no API Data | `PASS` only for the declared fictional inputs; transformation runtime is unexecuted | `OPEN`: arithmetic was manually reviewed, but no execution receipt or external construct evidence exists | `PASS` only while every identifier and record remains irreversibly fictional | `N/A`: no real organizational-use authority follows | **ADMIT** for paper review only |
| Voluntary, independently administered self-report ONA | `N/A` | `N/A` only if no Discord-derived data or identifiers enter | `OPEN`: boundary, recall, and nonresponse bias untested. [`research.md`, Agent 2 “Bias register,” Marsden 1990, Abstract/pp. 435–463; Kossinets 2006, Abstract/pp. 247–268] | `OPEN`: relation-specific validation absent. [`research.md`, Agent 2 “Discriminating validation,” item 1; Johnson et al. 2012, Abstract and Introduction] | `OPEN`: voluntariness, labor, privacy, and nonparticipant effects undecided. [`research.md`, Agent 3 “Source register,” E1 Belmont “Informed Consent” and E2 EDPB paragraphs 21–24] | `OPEN`: no release/use authority | **HOLD**; no readiness claim |
| Participatory team mapping | `N/A` | `N/A` only if independently created | `OPEN`: participation boundary and missing voices unresolved | `OPEN`: at most a participant-authored map; protocol unclosed. [`research.md`, Agent 2 “Bias register,” Marsden 1990, Abstract and pp. 435–463] | `OPEN`: participant control and disclosure review undecided. [`research.md`, Agent 3 “Safer alternatives,” E1 Belmont “Respect for Persons” and “Informed Consent”] | `OPEN`: no release/use authority | **HOLD**; candidate for owner evaluation only |

The non-collapse chain is:

`documented field -> analyst-defined graph projection -> graph-theoretic value -> externally tested organizational hypothesis -> separately authorized use`

No arrow is automatic.

## Current official Discord observability, permissions, and missingness

All rows describe documented potential visibility, not authorization, completeness, or live proof.

| Signal | Current official surface | Permission / intent gate | Missingness and claim boundary |
|---|---|---|---|
| Guild | REST guild object; Gateway `GUILD_CREATE/UPDATE/DELETE`; IDs, features, roles/channels/counts where supplied. [`research.md`, Agent 1 “Observability matrix—Guild,” S1 “Gateway Intents—List of Intents” and S4 “Guild Resource”] | Authorized installation; `GUILDS` for events | Unavailable guilds and outages exist; no target availability was tested |
| Members | REST List Guild Members; Gateway add/update/remove/chunks; user, role IDs, `joined_at`, flags, timeout. [`research.md`, Agent 1 “Members,” S2 “Guilds” event subsections; S4 “Guild Member Object” and “List Guild Members”] | Privileged `GUILD_MEMBERS`; REST listing also requires application intent | Pages 1–1000; initial/chunk coverage is scale/intent dependent; current state does not reconstruct historical membership |
| Roles | REST roles and Gateway role create/update/delete; ID, name, position, permissions, tags. [`research.md`, Agent 1 “Roles,” S4 “Get Guild Roles”; S5 “Role Object”] | `GUILDS`; ordinary guild access | A Discord role is a permission construct, not a documented team or job role |
| Channels | REST guild channels and Gateway channel create/update/delete; type, parent, overwrites, last-message pointer. [`research.md`, Agent 1 “Channels,” S4 “Get Guild Channels”; S6 “Channel Object”] | `GUILDS`; message operations remain channel-permission dependent | Hierarchy does not prove ownership, team boundary, membership, or use |
| Threads | Visible active threads, thread events, and public/private archived listings; member/join/archive data and approximate counts. [`research.md`, Agent 1 “Threads,” S2 “Threads”; S6 “Thread Member Object,” “List Public Archived Threads,” “List Private Archived Threads”] | `GUILDS`; broader member updates may need `GUILD_MEMBERS`; archived public history needs `READ_MESSAGE_HISTORY`; private archived listing needs `MANAGE_THREADS` | Only viewable threads synchronize; `member_count` is approximate and capped at 50; historical participation is lossy |
| Messages | REST history and Gateway create/update/delete; author/member, IDs, timestamps, mentions, reactions, references, bot/webhook markers. [`research.md`, Agent 1 “Messages,” S2 “Messages”; S3 “Message Object” and “Get Channel Messages”] | `GUILD_MESSAGES`; REST needs `VIEW_CHANNEL` and `READ_MESSAGE_HISTORY` (and `CONNECT` for voice channels); content fields need privileged `MESSAGE_CONTENT` | REST pages 1–100; only extant accessible messages; no fixed documented age ceiling and no live completeness proof |
| Replies | `message_reference` identifies originating message/channel/guild and may resolve a referenced message. [`research.md`, Agent 1 “Replies,” S3 “Message Reference Object”] | Message gates above | Reference presence does not prove reading, response quality, intent, collaboration, or knowledge transfer; deleted/inaccessible targets may not resolve |
| Mentions | Message objects expose user/role selectors and `mention_everyone`. [`research.md`, Agent 1 “Mentions,” S3 “Message Object”] | Message gates above | A mention does not prove receipt, attention, collaboration, endorsement, or a social tie |
| Reactions | REST Get Reactions returns current users for an emoji; Gateway add/remove/all/emoji events expose relevant IDs and emoji. [`research.md`, Agent 1 “Reactions,” S2 “Messages” reaction-event subsections; S3 “Get Reactions”] | `GUILD_MESSAGE_REACTIONS`; channel visibility/history for REST | Gateway reaction events have no native reaction timestamp; REST is current state, not full history; emoji meaning is unknown |
| Presence | Gateway `PRESENCE_UPDATE` with status, activities, and client status. [`research.md`, Agent 1 “Presence,” S1 “Gateway Intents—Privileged Intents”; S2 “Presence”] | Privileged `GUILD_PRESENCES` | No historical REST backfill; invisible appears offline; online does not mean working or reading |
| Voice state | Current REST state and Gateway join/leave/move state with mute/deaf/video/stream flags. [`research.md`, Agent 1 “Voice state,” S2 “Voice”; S7 “Voice State Object”] | `GUILD_VOICE_STATES`; another user’s REST state also requires channel connection permission | No audio, transcript, speaking turns, or conversation content; duration inferred from paired events is gap-sensitive |
| Audit logs | REST actor/target/action/changes/options/reason, paginated. [`research.md`, Agent 1 “Audit logs,” S8 opening retention statement, “Audit Log Entry Object,” and “Get Guild Audit Log”] | `VIEW_AUDIT_LOG` | Exactly 45 days; pages 1–100; changes need not be complete and do not cover all moderation/message activity |
| Moderation | Ban/member events, audit entries, Auto Moderation rules and execution events. [`research.md`, Agent 1 “Moderation,” S2 “Auto Moderation”; S8 “Audit Log Entry Object”; S9 “Auto Moderation Rule Object,” “Action Object,” “Permission Requirements”] | `GUILD_MODERATION`, `AUTO_MODERATION_CONFIGURATION`, `AUTO_MODERATION_EXECUTION`; Auto Moderation REST needs `MANAGE_GUILD` | Blocked content may lack a message ID; events are not a complete enforcement history |
| Bots/webhooks | User `bot`, managed-role tags, application/webhook message fields, and `WEBHOOKS_UPDATE`. [`research.md`, Agent 1 “Bots” and “Webhooks,” S2 “Webhooks”; S3 “Message Object”; S5 “Role Object”] | Containing-object access; `GUILD_WEBHOOKS` for update events | Does not detect all automation; update event does not identify the changed webhook or reconstruct provenance |
| Edits/deletions | `MESSAGE_UPDATE`, current `edited_timestamp`, delete/bulk-delete ID events. [`research.md`, Agent 1 “Edits” and “Deletions,” S2 “Messages”; S3 “Message Object”] | Message gates above | No version history; delete events contain no deleted bytes, author, deleter, reason, or original timestamp |
| Time | Object-specific timestamps, snowflakes, and Gateway sequence numbers. [`research.md`, Agent 1 “Time,” S1 “Receiving Events”; S2–S8 named object/event sections] | Surface-specific | Sequence is relative order, not wall time; reactions/deletions lack event timestamps; receipt time would be collector-generated |

Additional missing observations include DMs, inaccessible private spaces, read receipts, views, lurkers, downloads, off-platform work, semantic meaning, and actual app installation/approval/notice/consent. [`research.md`, Agent 1, “Missing observations and blockers,” S3 “Message Object” and S6 “Channel Object”; Agent 3, D4 “The information we collect—Content you create / Information from actions you take / Information about your use”]

## REST, Gateway, rates, and checkpoints: design only

REST is the documented snapshot/backfill side for current guild/member/role/channel state, extant accessible message history, current reactions, archived threads, and the 45-day audit window. Gateway is the documented forward-event side for creates, updates, deletes, joins/leaves, reactions, presence, voice state, and moderation execution after connection. Resume can cover some interruption, but Discord documents no durable general event-replay log. REST reconciliation cannot recover deleted bytes, previous edit versions, reaction event times, historical presence/voice transitions, or events outside a non-resumable gap. [`research.md`, Agent 1, “REST versus Gateway,” S1 “Receiving Events” and S2 named event sections; “Documented deletion and retention limits,” S8 opening retention statement]

Any future, separately authorized design would therefore need two explicit checkpoints:

1. A REST coverage checkpoint keyed by route, guild/channel scope, page cursor, oldest/newest observed object ID or timestamp, fetch time, permission snapshot, and declared gap. It would parse Discord’s bucket, reset, and retry headers rather than hard-code request timing.
2. A Gateway checkpoint keyed by session, last acknowledged sequence, connection interval, resume result, receipt time, and declared non-resumable gap. Receipt time could never be relabeled as Discord event time.

Reconciliation would append a coverage manifest rather than silently filling gaps. A failed permission, missing page, invalid reply target, or non-resumable session would remain an explicit missingness record and trigger the relevant abstention rule. This is an implementation-neutral design proposal; no collector or checkpoint runtime exists.

Discord’s current docs describe dynamic REST limits, a 50-request/second bot global limit, 10,000 qualifying invalid requests per 10 minutes, and a Gateway client-send limit of 120 events per connection per 60 seconds. The send limit does not prove complete received-event processing. [`research.md`, Agent 1, “Permissions, rates, and history constraints,” S10 “Rate Limits,” “Global Rate Limit,” and “Invalid Request Limit”; S1 “Rate Limiting”]

## Bounded research questions

Only the following descriptive or hypothesis-forming questions are methodologically candidate-worthy, and only for synthetic data or separately governed non-Discord data while the platform block stands:

- How concentrated is observed participation within a declared boundary and window?
- Where do observed replies or mentions cross independently owner-validated, time-bounded group boundaries?
- Which vertices occupy potential structural bridge positions in one declared partial graph?
- How segregated is channel participation, and how does it change across preregistered windows?
- What is the distribution of reply-reference delays, conditional on observed activity opportunity?
- Are layer-specific interaction patterns stable across preregistered windows or interventions?

“Collaboration,” “knowledge flow,” and “silo” remain externally testable hypotheses. Productivity, performance, influence, sentiment, and informal leadership are not Discord-trace constructs. [`research.md`, Agent 2, “Defensible question ceiling,” Johnson, Kovács & Vicsek 2012, Abstract and Introduction]

## Exact synthetic-only event-to-graph bindings

These bindings are mechanical definitions for fictional inputs. They are not established organizational relations and must not be applied to live Discord person-linked data under the current policy block.

| Event/record | Exact synthetic projection | Weight, time, normalization | Construct ceiling and method basis |
|---|---|---|---|
| Reply | Directed `author i -> author j` only when the referenced message resolves to human `j`; reply layer remains separate | Event count, binary tie, active-day count; fixed UTC windows; optional normalization by sender activity/opportunities | Addressed reference only, not agreement, reading, collaboration, quality, or knowledge transfer. [`research.md`, Agent 2 “Candidate graph bindings—Reply”; Johnson et al. 2012, Abstract/Introduction] |
| Mention | Directed `author i -> mentioned human j`; exclude self/bot targets as declared and never expand broadcasts/group mentions without separately verified semantics | Raw count; optional `1/k` per message across `k` human targets; normalize by sender output/channel volume | Explicit mention token only, not attention received, influence, or tie. [`research.md`, Agent 2 “Candidate graph bindings—Mention”; Johnson et al. 2012, Abstract and Introduction] |
| Authorship | Primary bipartite `user <-> channel`, one edge/cell per in-scope authored item or declared binary participation | Keep binary, count, and active days; normalize by user total and channel volume/population | Participation footprint only. Preserve two-mode form because projection loses information. [`research.md`, Agent 2 “User–channel”; Latapy et al. 2008, Introduction and “Projection,” pp. 31–48] |
| Role assignment | Temporal bipartite `user <-> role` over an exact observed interval | Binary state; duration only for availability, never tie strength | Platform affiliation/permission, not a team unless separately owner-validated and construct-tested. [`research.md`, Agent 2 “User–role”; Marsden 1990, Abstract and pp. 435–463] |
| Reaction | Primary tripartite `reactor -> message <- author`, token retained; optional `reactor -> author` projection; self-reactions separate | Unique events and active days; fractionalize declared multi-reaction bundles; normalize by eligible messages/channel volume | Recorded interaction only; no polarity, endorsement, sentiment, trust, or approval. [`research.md`, Agent 2 “Reaction”; Johnson et al. 2012, Abstract and Introduction] |
| Thread participation | Primary bipartite `user <-> thread`; optional undirected projection between co-participants | Binary per user-thread; projected pair weight `1/(n_t-1)` for a thread of size `n_t`; keep direct replies separate | Shared forum participation, not dyadic interaction or collaboration. [`research.md`, Agent 2 “Thread co-participation”; Newman 2001, §III, Eq. 2, pp. 016132-5–6, by analogy] |
| Temporal event | `(actor, relation, target, event_time, context)` within one declared layer | Strictly increasing event time for a time-respecting path; window and local-work-period sensitivity only if legitimately available | Order, bursts, persistence, and possible pathways—not causation or actual transmission. [`research.md`, Agent 2 “Temporal sequence”; Holme & Saramäki 2012, §§2–3, pp. 97–108] |

Reply, mention, reaction, affiliation, authorship, and co-participation layers remain multiplex. There is no default “social graph.” Cross-layer coupling would require a declared rule, sensitivity analysis, external validation, and separate authority; it cannot be inferred from chronological adjacency. Multislice methods preserve link type and time precisely because layers differ. [`research.md`, Agent 2, paragraph after “Candidate graph bindings,” Mucha et al. 2010, Abstract and Eq. 2, pp. 876–878]

Time windows must be fixed in UTC, half-open, and preregistered; join/leave intervals, seasonality, incidents, and multiple window lengths need sensitivity analysis. Gateway sequence numbers and collector receipt times are not event wall time. Static aggregation can erase order, while short- and long-term stability can reflect different processes. [`research.md`, Agent 1 “Observability matrix—Time,” S1 “Receiving Events”; Agent 2 “Temporal sequence,” Holme & Saramäki 2012, §§2–3; “Metric matrix—Temporal stability,” Quintane et al. 2013, Abstract/pp. 528–540]

## Metric, construct, and misuse matrix

| Metric | Defensible output for one declared partial graph | Mandatory rejection |
|---|---|---|
| Degree / strength | Unique observed counterparts or layer-specific event volume. [`research.md`, Agent 2 “Metric-to-construct / misuse matrix—Degree/strength”; Freeman 1979, pp. 215–239, especially summary pp. 237–238] | Popularity, productivity, workload, importance, performance |
| Reciprocity | Bidirectionality relative to an activity-preserving null. [`research.md`, Agent 2 “Metric matrix—Reciprocity,” Garlaschelli & Loffredo 2004, Abstract] | Trust, mutual support, agreement |
| Betweenness | Potential geodesic intermediary position in one explicit projection. [`research.md`, Agent 2 “Betweenness,” Freeman 1979, pp. 215–239, especially pp. 237–238] | Control, indispensability, influence, knowledge brokerage |
| Eigenvector / PageRank | Recursive connectivity under explicit edge orientation and sink/component handling. [`research.md`, Agent 2 “Eigenvector/PageRank,” Brin & Page 1998, §2.1] | Leadership, authority, expertise, influence |
| k-core | Subgraph satisfying minimum degree `k`. [`research.md`, Agent 2 “k-core,” Seidman 1983, pp. 269–287] | High-performing core, inner circle, indispensability |
| Brokerage | Intermediary triad counts across independently validated groups, by Gould–Fernandez role. [`research.md`, Agent 2 “Brokerage,” Gould & Fernandez, pp. 89–126, especially pp. 91–97] | Actual transmission, translation, control |
| Modularity | Partition strength against a declared null model. [`research.md`, Agent 2 “Modularity,” Fortunato & Barthélemy 2007, Abstract/pp. 36–41] | Organizational silos or official teams; ignore neither resolution limit nor boundary error |
| Assortativity | Mixing by a validated attribute. [`research.md`, Agent 2 “Assortativity,” Newman 2003, §II] | Preference, discrimination, homophily, causality |
| Density | Observed binary ties divided by possible ties in one fixed universe/window. [`research.md`, Agent 2 “Metric-to-construct / misuse matrix—Density”; Marsden 1990, Abstract and pp. 435–463] | Cohesion, health, or cross-size comparison without opportunity correction |
| Centralization | Inequality of one declared centrality relative to its graph-theoretic maximum. [`research.md`, Agent 2 “Metric-to-construct / misuse matrix—Centralization”; Freeman 1979, pp. 215–239, especially summary pp. 237–238] | Hierarchy, effectiveness, resilience, managerial control |
| Temporal stability | Edge/rank/partition similarity across preregistered windows and lengths. [`research.md`, Agent 2 “Temporal stability,” Quintane et al. 2013, Abstract/pp. 528–540] | Adaptability, health, or causal effect |

An absent population denominator allows only explicitly partial-graph arithmetic. It blocks population comparisons, rankings, and organizational-community claims. [`research.md`, Agent 2 “Bias register—Denominator”; Marsden 1990, Abstract and pp. 435–463]

## Validation and bias register

Required bias entries are: permission and channel exclusion; private and off-platform communication; departed users, edits/deletions, and backfill gaps; role/timezone/tenure/adoption differences; notifications and alternative tools; bot/broadcast inflation; reply undercount; reaction ambiguity; co-participation clique inflation; missing active-time, membership-interval, and opportunity denominators; join/leave censoring; seasonality, incident bursts, and window choice; role/team mismatch; and disclosed-measurement reactivity. Network boundaries, temporal relations, sampling, and error must be explicit, and systematic platform loss cannot be excused by robustness results limited to random error. [`research.md`, Agent 2, “Bias register,” Marsden 1990, Abstract/pp. 435–463; Kossinets 2006, Abstract/pp. 247–268; Borgatti, Carley & Krackhardt 2006, §4 pp. 134–135]

Homophily, influence, and shared causes are observationally confounded; correlation cannot establish influence. [`research.md`, Agent 2, “Bias register—Construct,” Shalizi & Thomas 2011, Abstract and §§2–4]

For any independently authorized non-Discord study, preregister the construct, graph, population, window, exclusions, denominator, null, validation threshold, and abstention outcome. Then require:

1. Relation-specific surveys tested with dyadic precision/recall, calibration, and QAP association; failure blocks that construct. Surveys are neither gold truth nor consent for another source. [`research.md`, Agent 2 “Discriminating validation and negative controls,” item 1; Johnson et al. 2012, Abstract and Introduction]
2. Independently sourced, time-valid boundary records compared through ARI/AMI and permutation baselines; Discord roles are not gold truth. [`research.md`, Agent 2 “Discriminating validation and negative controls,” item 2; Marsden 1990, Abstract and pp. 435–463]
3. Stratified blinded coding only under separate access, ethics, privacy, and release approval; otherwise abstain. [`research.md`, Agent 2 “Discriminating validation and negative controls,” item 3; Marsden 1990, Abstract and pp. 435–463]
4. Temporal holdout against sender activity, receiver popularity, channel, and recency baselines; recurrence is not construct validity. [`research.md`, Agent 2 “Discriminating validation and negative controls,” item 4; Holme & Saramäki 2012, §§2–3, pp. 97–108]
5. Missingness simulations stratified by permission/channel/member class, with stability envelopes. [`research.md`, Agent 2 “Discriminating validation and negative controls,” item 5; Kossinets 2006, Abstract and pp. 247–268; Borgatti, Carley & Krackhardt 2006, §4 pp. 134–135]
6. Negative controls: target permutation within sender/channel/time strata; within-actor-day timestamp shuffling; role-label permutation preserving role sizes; human-only versus bot/system-only layers; impossible future-to-past paths; separate self-reaction and broadcast-only tests. A signal surviving the control intended to destroy it is non-discriminating. [`research.md`, Agent 2 “Discriminating validation and negative controls,” item 6; Lipsitch, Tchetgen Tchetgen & Cohen 2010, Abstract and Fig. 1, pp. 383–388]

Failed validation returns `ABSTAIN`. It never degrades into a weaker organizational claim. [`research.md`, Agent 2 “Discriminating validation and negative controls” and “Hard abstention rules”; Johnson et al. 2012, Abstract and Introduction]

## Finite synthetic paper specification

Every identifier is invented, content is absent, `synthetic=true`, and each human record has `is_bot=false` and `is_webhook=false` unless stated. This fixture was manually recomputed by reviewers; it was not executed.

### Frozen configuration

| Field | Exact value |
|---|---|
| Guild | `g-syn` |
| Window | `[2026-01-01T09:00:00Z, 2026-01-01T09:15:00Z)` |
| Human universe | `{u1,u2,u3,u4,u5,u6}`; include isolates in directed density |
| Directed density | Simple binary directed arcs, no self-loops, denominator `n*(n-1)` |
| Layers | Reply, mention, reaction, role, channel, and thread remain separate |
| Channel rule | Thread messages roll up to `parent_channel_id` for user-channel participation |
| Thread rule | User-thread bipartite graph primary; optional projected pair weight `1/(n_t-1)` |
| Reaction time | `event_time=null`; `observed_at` is receipt time, never event time |
| Role interval | Full frozen window; `owner_validated_team=false` |
| Suppression | Distinct participating humans per parent channel/window; provisional fixture `k=5`, not a safe harbor |
| Mutation | Each mutant independently alters baseline; recompute normalized data, graphs, aggregates, caches, and exports |

### Exact normalized baseline

Empty lists are `[]`; nulls are explicit.

| id | type | actor | parent | thread | message | reply | mentions | reaction target/token | event_time | observed_at | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `m1` | `MESSAGE_CREATE` | `u1` | `c-public` | `t1` | `m1` | null | `[]` | null | `09:00Z` | `09:00Z` | human |
| `m2` | `MESSAGE_CREATE` | `u2` | `c-public` | `t1` | `m2` | `m1` | `[]` | null | `09:02Z` | `09:02Z` | human |
| `m3` | `MESSAGE_CREATE` | `u3` | `c-public` | null | `m3` | null | `[u4]` | null | `09:03Z` | `09:03Z` | human |
| `m4` | `MESSAGE_CREATE` | `u4` | `c-public` | null | `m4` | null | `[]` | null | `09:05Z` | `09:05Z` | human |
| `m5` | `MESSAGE_CREATE` | `u5` | `c-public` | `t1` | `m5` | `m2` | `[]` | null | `09:06Z` | `09:06Z` | human |
| `m6` | `MESSAGE_CREATE` | `u1` | `c-small` | null | `m6` | null | `[u6]` | null | `09:07Z` | `09:07Z` | human |
| `m7` | `MESSAGE_CREATE` | `u6` | `c-small` | null | `m7` | `m6` | `[]` | null | `09:08Z` | `09:08Z` | human |
| `x1` | `REACTION_ADD` | `u3` | `c-public` | `t1` | null | null | `[]` | `m1/check` | null | `09:09Z` | human |
| `x2` | `REACTION_ADD` | `u1` | `c-public` | `t1` | null | null | `[]` | `m1/check` | null | `09:10Z` | human; self-reaction control |
| `b1` | `MESSAGE_CREATE` | `bot1` | `c-public` | null | `b1` | null | `[]` | null | `09:11Z` | `09:11Z` | `is_bot=true`; excluded from human projections |
| `bc1` | `MESSAGE_CREATE` | `u2` | `c-public` | null | `bc1` | null | `[]` | null | `09:12Z` | `09:12Z` | `mention_everyone=true`; no mention edge |

Role records `rs1`–`rs6` cover the full role interval: `u1,u2,u6 -> role-x` and `u3,u4,u5 -> role-y`. The baseline manifest declares both parent channels included for the full window, no known gaps, a fixed six-human universe, and complete fictional records by construction. It says nothing about real completeness.

### Exact expected projections

| Test | Exact expectation |
|---|---|
| Reply | `{u2->u1,u5->u2,u6->u1}`; out-degree `u2=u5=u6=1`; in-degree `u1=2,u2=1`; reciprocity `0`; density `3/30=0.10` |
| Mention | `{u3->u4,u1->u6}`; `bc1` adds none; density `2/30=0.0667` |
| User-channel | Seven human edges; `c-public={u1,u2,u3,u4,u5}`, `c-small={u1,u6}`; `degree(u1)=2`, others `1`; bot excluded |
| Roles | Six edges; each user degree `1`; both roles degree `3`; team/mixing query abstains |
| Reaction | Two raw receipts; non-self `{u3->u1}` weight `1`; self-control `{u1->u1}` count `1`; no latency |
| Thread | `{u1-t1,u2-t1,u5-t1}`; optional projected pairs `{u1,u2},{u1,u5},{u2,u5}` each `0.5`; each strength `1`; total `1.5` |
| Reply-reference delay | `[2m,4m,1m]`; sorted `[1m,2m,4m]`; median `2m`; mean `7/3m`; not human response-time evidence |
| Cross-layer chronology | 09:02 reply and 09:07 mention are only separate chronological events; no cross-layer path |
| Suppression | `c-public n=5` may display only its declared coarse count; `c-small n=2` suppresses; no differencing-safety claim |
| Controls | `b1` absent from human graphs; `bc1` adds authorship in an occupied cell and no mention edge |

### Independent mutants and exact expected states

| Mutant | Exact expected post-state |
|---|---|
| `DELETE_m1` | `m1` becomes a non-attributable tombstone; replies `{u5->u2,u6->u1}`, density `2/30`; delays `[4m,1m]`, median `2.5m`; reactions empty; `c-public={u2,u3,u4,u5}`; thread `t1={u2,u5}` projected weight `1`; mentions/roles unchanged; invalidate every `m1`-derived cache/export; infer no author or deleter from delete event |
| `ERASE_u1` | Universe `{u2,u3,u4,u5,u6}`; reply `{u5->u2}`, density `1/20`; mention `{u3->u4}`, density `1/20`; reactions empty; `c-public={u2,u3,u4,u5}`, `c-small={u6}`; thread `{u2,u5}` weight `1`; reply median `4m`; roles `role-x={u2,u6}`, `role-y={u3,u4,u5}`; recompute all attributable raw/normalized data, edges, aggregates, caches, exports |
| `GAP_c-small` | Remove all `c-small` observations; add `{channel:c-small,gap_kind:permission,whole_window:true}`; reply `{u2->u1,u5->u2}`, density `2/30`; mention `{u3->u4}`, density `1/30`; delays `[2m,4m]`, median `3m`; cross-channel comparison/ranking abstains; labeled within-`c-public` partial arithmetic may remain |
| `NULL_REPLY_m2` | Set `m2.reply_ref=null`; replies `{u5->u2,u6->u1}`, density `2/30`; projection must not manufacture a target; this is not a permutation test |
| `SUPPRESS_after_ERASE_u1` | `c-public n=4`, `c-small n=1`; both suppress under fixture rule |

Exact query outcomes are:

- `ABSTAIN(TEAM_BOUNDARY_UNVALIDATED)` for “which role is the silo?”
- `ABSTAIN(REACTION_SEMANTICS_UNVALIDATED)` for “does `check` mean endorsement?”
- `ABSTAIN(KNOWN_PERMISSION_GAP)` for cross-channel comparison or ranking after `GAP_c-small`
- `BLOCK(PROHIBITED_PERSON_RANKING)` for any contributor ranking

No target-permutation, timestamp-shuffle, role-label-permutation, differencing-safety, or stratified-loss result is claimed by this fixture. These would require separate frozen inputs and expected statistics. The fixture source is the reviewed `SYNTHESIS.md` “Finite synthetic fixture” and closure row C7; those artifact labels are not external evidence.

## Privacy and governance controls

The following are prerequisites for a materially narrower candidate only after Discord clears the exact non-relational design. They are necessary, not sufficient, and are not legal conclusions:

- lock one narrow purpose, field allowlist, outputs, owners, expiry, forbidden reuse, and stop rule; “research” alone is not a sufficient purpose;
- exclude DMs, group DMs, private/restricted channels, message content, attachments, voice/video, deleted content, minors, guests, nonparticipants, and cross-server identities;
- use least privilege, reviewed channel allowlists, a separate pilot application, visible bot identity, accessible privacy notice, and a non-manager rights channel;
- require genuine no-detriment participation and worker consultation; consent cannot cure rule 16 and is generally problematic under employment power;
- treat stable hashes as pseudonyms, not anonymity; separate the identity map and analysis store, use distinct keys, prohibit linkage and re-identification, and test singling-out/linkability;
- encrypt in transit and at rest, keep keys outside datasets, apply RBAC, provide analysts pseudonyms only, firewall managers/HR, and require two-person export approval;
- predeclare finite schedules for raw data, edges, aggregates, caches, exports, backups, and audit logs; cascade correction/deletion/withdrawal through every derivative;
- suppress isolates, named communities, exact low counts, rare-role combinations, and unsafe longitudinal differences; provisional `k>=5` is only a test floor, never a safe harbor;
- log access, queries, exports, approvals, corrections, and deletions without message content; preassign incident containment, Discord/participant notification, evidence, and review owners;
- release no person-level graph, rank, label, alert, downloadable microdata, or employment output; re-review every purpose expansion.

These controls are grounded in Discord’s purpose, privacy, deletion, and security terms and broader ethics/privacy principles. [`research.md`, Agent 3, “Control findings” and “Minimum control set,” D1 “Handle Data with Care” items 15–21; D2 Developer Terms §5(a)–(c) and §9; E1 Belmont “Respect / Beneficence / Justice” and “Informed Consent”; E2 EDPB paragraphs 21–24; E3 OECD Part Two ¶¶7–14 and Part Three ¶15; E4 NISTIR 8053 Abstract; E6 ICO “difference between anonymisation and pseudonymisation” and “K-anonymisation”]

## Uncleared aggregate dashboard

Only after all six applicable gates pass could an aggregate, non-ONA dashboard be considered. Its candidate contents are coarse channel/time event totals, bot/webhook share, observed edit/delete counts, a coverage-and-gaps panel, and a retention/review panel. This candidate is not approved, safe, authorized, validated, or implemented.

It must contain no node-link diagram, ego network, centrality table, inferred silo, named small group, sentiment result, individual alert, person-level trend, downloadable microdata, or HR output. Aggregate creation is itself processing and upstream policy still applies. [`research.md`, Agent 3, “Control findings—Aggregation/reporting,” D1 item 16 and E6 “If we anonymise personal data, does this count as processing?”]

## Red lines

- No Discord API Data for user-relationship profiling or person-linked ONA. [`research.md`, Agent 1 “Policy blocker,” S11 rule 16; Agent 3 “Red lines,” D1 item 16]
- No employment eligibility, hiring, promotion, pay, discipline, termination, attendance, productivity, performance, leadership, influence, engagement, misconduct, or retention-risk scoring. [`research.md`, Agent 3 “Employment power” and “Covert surveillance/scoring,” D1 item 16]
- No scraping, self-bots, user-token automation, or limit circumvention. [`research.md`, Agent 3 “Red lines,” D1 items 15–21 and D3 “Restrictions on your use”]
- No covert collection or reliance on server-admin installation as participant consent. [`research.md`, Agent 3 “Notice and consent,” D2 §5(a), E1 Belmont “Informed Consent,” and E2 paragraphs 21–24; “Covert surveillance / scoring,” E5 “Can we use covert monitoring?”]
- No DMs, private/restricted spaces, message bodies, attachments, voice/video, deleted content, sentiment, minors, guests, or nonparticipants. [`research.md`, Agent 3 “Private channels and DMs,” D3 “Third-party services” and D4 “Content you create”; “Minors and guests,” D1 items 9 and 16]
- No re-identification, cross-dataset linkage, sparse network publication, secondary use, or indefinite retention. [`research.md`, Agent 3 “Pseudonymization/re-identification,” D1 item 19 and E4 NISTIR 8053 Abstract; “Retention/deletion,” D2 §5(b)]
- No claim that a documented field proves availability, complete data, legitimate use, consent, an organizational construct, or decision authority. [`research.md`, Agent 1 “Policy blocker and claim ceilings,” S11 “Handle Data with Care” rules 15–16; Agent 2 “Hard abstention rules,” Johnson et al. 2012, Abstract/Introduction]

## Candidate decision and review routes

No decision below was made in this run. Each route is narrow; no owner can substitute for another.

| Route | Exact unresolved decision |
|---|---|
| Discord / platform owner | Written clarification whether the exact non-relational fields, transformations, purpose, and outputs are permitted; this can reopen only platform authorization |
| Sponsor / data controller | Exact non-employment purpose, population, outputs, expiry, forbidden uses, and stop rule |
| Data / coverage owner | Population, accessible surfaces, history, gaps, denominators, and quality thresholds |
| Method owner | Event constructs, preregistered windows, validation thresholds, negative controls, and abstention behavior |
| Independent ethics/IRB and worker representatives | Review category, voluntariness, consultation, vulnerable/nonparticipant effects, and no-detriment protections |
| DPO/privacy, labor, and jurisdiction-dependent counsel | Separate privacy, monitoring, labor, lawful-basis, transfer, access/deletion, and jurisdictional determinations; this document is not legal advice |
| Security owner | Architecture, credentials, encryption, access review, logging, backups, deletion, and incident response |
| Disclosure-control owner | Suppression threshold, differencing/linkage testing, and release review |
| Organizational-use authority | A scope-limited descriptive use only after every other gate passes; HR/executives cannot authorize a Discord-prohibited use |

## Implementation-neutral next steps

1. Preserve the current block. Do not request credentials, install a bot, access a server, call Discord APIs, collect data, or build a live person-linked collector.
2. If desired, convert the frozen fixture into a local synthetic-only test contract. Pin every record, projection, mutant, abstention code, and expected value above; produce a distinct execution receipt. Such a receipt could prove only internal transformation and arithmetic.
3. Ask Discord for written clarification only if a specific coarse non-relational aggregate design has first been frozen. Include exact fields, transformations, purpose, retention, and outputs. Treat any response as evidence for the platform gate only.
4. If an organization still needs relationship research, evaluate independently administered self-report or participant-controlled mapping without Discord-derived data. Freeze a separate protocol and route it through method, ethics, privacy, labor, security, disclosure, and use-authority review.
5. Do not reopen live or release work until every applicable gate has its own evidence and accountable decision. A failed or absent gate returns `BLOCK`, `HOLD`, or `ABSTAIN`, never implied clearance.

## Claim ceiling and residue

This run establishes only that current official Discord documentation describes named schemas, events, endpoints, intents, permissions, rates, pagination, and retention boundaries, and that current Developer Policy rule 16 blocks live person-linked relationship profiling and employment-eligibility use. [`research.md`, Agent 1, “Source inventory” and “Policy blocker,” S1–S11 exact selectors above; Agent 3, “Decisive gate,” D1 item 16]

It does not establish a live target, app authorization, permissions, coverage, complete history, dataset, collector, runtime, platform clearance for aggregates, participant consent, privacy acceptance, legal basis, construct validity, causal effect, organizational use authority, implementation, publication, deployment, release, or production readiness. The synthetic paper specification remains unexecuted and cannot prove any real Discord or organizational study.

Open residue is finite and explicit:

- Discord has not clarified whether an exact coarse non-relational aggregate design is permitted.
- No target population, server, installation, accessible-surface map, coverage manifest, denominator, gap threshold, or retention schedule exists.
- No synthetic execution receipt exists.
- No relation-specific validation, discriminating control result, or independently governed alternative-study protocol exists.
- No ethics, privacy, labor, security, disclosure, or organizational-use decision exists.
- Current source pages are mutable documentation evidence, not immutable runtime proof.

Until that residue is separately closed, the correct operational posture is: **live person-linked Discord ONA BLOCKED; employment use PROHIBITED; aggregate candidate HOLD; synthetic paper specification UNEXECUTED; self-report and participatory alternatives HOLD.**

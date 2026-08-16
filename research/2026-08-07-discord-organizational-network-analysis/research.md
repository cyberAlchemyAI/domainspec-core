# Discord API and Organizational Network Analysis Explorer Returns

The strategist mechanically preserves the three explorer returns below. These
returns are research evidence, not implementation, policy clearance, legal advice,
participant consent, or authority to access a Discord server.

## Agent 1 — Discord API observability

Completed read-only research. No credentials were requested or used; no bot was created; no server was joined; no API call or live collection occurred.

Legend: **O** = directly documented by Discord; **I** = inference from documented surfaces; **U** = not verified/documented.

### Source inventory

All accessed 2026-08-07. These are current first-party pages, not immutable snapshots.

- **S1:** [Gateway](https://docs.discord.com/developers/events/gateway) — “Receiving Events,” “Gateway Intents” → “List of Intents,” “Privileged Intents,” “HTTP Restrictions,” “Message Content Intent,” “Rate Limiting.”
- **S2:** [Gateway Events](https://docs.discord.com/developers/events/gateway-events) — “Guilds,” “Auto Moderation,” “Threads,” “Messages,” “Presence,” “Typing,” “Voice,” and “Webhooks,” including each named event subsection.
- **S3:** [Message Resource](https://docs.discord.com/developers/resources/message) — “Message Object,” “Message Reference Object,” “Get Channel Messages,” “Get Reactions,” “Delete Message,” and “Bulk Delete Messages.”
- **S4:** [Guild Resource](https://docs.discord.com/developers/resources/guild) — “Guild Member Object,” “List Guild Members,” “Get Guild Channels,” “List Active Guild Threads,” and “Get Guild Roles.”
- **S5:** [Permissions](https://docs.discord.com/developers/topics/permissions) — “Role Object” and channel permission calculation.
- **S6:** [Channel Resource](https://docs.discord.com/developers/resources/channel) — “Channel Object,” “Thread Member Object,” “List Public Archived Threads,” and “List Private Archived Threads.”
- **S7:** [Voice Resource](https://docs.discord.com/developers/resources/voice) — “Voice State Object,” “Get Current User Voice State,” and “Get User Voice State.”
- **S8:** [Audit Logs Resource](https://docs.discord.com/developers/resources/audit-log) — opening retention statement, “Audit Log Entry Object,” and “Get Guild Audit Log.”
- **S9:** [Auto Moderation](https://docs.discord.com/developers/resources/auto-moderation) — “Auto Moderation Rule Object,” “Action Object,” and “Permission Requirements.”
- **S10:** [Rate Limits](https://docs.discord.com/developers/topics/rate-limits) — “Rate Limits,” “Exceeding A Rate Limit,” “Global Rate Limit,” and “Invalid Request Limit.”
- **S11:** [Discord Developer Policy](https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy) — “Handle Data with Care,” rules 15–21; effective 2024-07-08, last-updated label 2024-06-06.
- **S12:** [Discord Developer Terms](https://support-dev.discord.com/hc/en-us/articles/8562894815383-Discord-Developer-Terms-of-Service) — §5 “User Privacy and Security,” especially “API Data Sharing & Retention,” and §9 “Your Obligations Post-Termination.”
- **S13:** [How long Discord keeps your information](https://support.discord.com/hc/en-us/articles/5431812448791-How-long-Discord-keeps-your-information) — “Information you can delete directly,” “Retention periods for specific purposes,” and account deletion.

### Observability matrix

| Signal | Documented surface and fields | Gates | Boundary / missingness |
|---|---|---|---|
| Guild | REST guild object; Gateway `GUILD_CREATE/UPDATE/DELETE`; IDs, name, features, roles/channels and counts where supplied. **O** [S1,S4] | App installed and authorized; `GUILDS` intent for events. | Outages can produce unavailable guilds; no actual guild availability was tested. **O/U** |
| Members | REST List Guild Members: user, role IDs, `joined_at`, flags, timeout; Gateway add/update/remove and chunks. **O** [S2,S4] | Privileged `GUILD_MEMBERS`; REST list also requires the application intent independently of Gateway Identify. | REST pages 1–1000. Gateway initial/chunk membership is scale- and intent-dependent; add may also be emitted for an existing member. Current membership does not reconstruct past membership. **O/I** |
| Roles | REST Get Guild Roles; Gateway role create/update/delete; ID, name, position, permissions, managed/integration tags. **O** [S2,S4,S5] | `GUILDS`; ordinary guild access. | A Discord role is a permission construct, not documented as an organizational team or job role. **O/I** |
| Channels | REST Get Guild Channels; Gateway channel create/update/delete; ID, type, parent, permission overwrites, name, last-message pointer. **O** [S1,S4,S6] | `GUILDS`; channel access remains permission-dependent for message operations. | Existence and hierarchy do not prove team ownership or use. |
| Threads | Active visible threads in `GUILD_CREATE`; thread events; REST active/archived listings; thread/member IDs, join/archive timestamps, counts. **O** [S2,S6] | `GUILDS`; broader member updates need `GUILD_MEMBERS`; archived public threads need `READ_MESSAGE_HISTORY`; private archived threads additionally need `MANAGE_THREADS`. | Only threads the app can view synchronize; event `member_count` is approximate and capped at 50. Historical participation is lossy. **O** |
| Messages | REST channel history and Gateway create/update/delete; IDs, author/member, channel/guild, type, timestamp, edited timestamp, mentions, reactions, references, webhook/application markers. **O** [S2,S3] | `GUILD_MESSAGES`; REST requires `VIEW_CHANNEL` and `READ_MESSAGE_HISTORY`, plus `CONNECT` for voice channels. `MESSAGE_CONTENT` is privileged for content, embeds, attachments, components, and polls. | REST page size 1–100. No documented maximum message age, but only extant, accessible messages can be returned. No live completeness proof. **O/U** |
| Replies | `message_reference` exposes originating message/channel/guild IDs and optional resolved `referenced_message`. **O** [S3, “Message Reference Structure”] | Same message permissions/intents. | Reference existence is observable; reply intent, knowledge transfer, or response quality is not. Deleted/inaccessible referenced messages can prevent resolution. **I** |
| Mentions | Message objects contain user/role mention selectors and `mention_everyone`. **O** [S3] | Same message surface; content itself remains separately privileged. | A mention is not documented as attention received, collaboration, or endorsement. |
| Reactions | REST Get Reactions returns users for one emoji; Gateway add/remove/all/emoji events expose user, message, channel, guild, emoji, and sometimes message-author ID. **O** [S2,S3] | `GUILD_MESSAGE_REACTIONS`; channel visibility/history permissions for REST. | Gateway reaction events have no reaction timestamp field; REST is current state, not complete reaction history. Emoji meaning is unobserved. |
| Presence | Gateway `PRESENCE_UPDATE`: user, guild, status, activities, client status. **O** [S1,S2] | Privileged `GUILD_PRESENCES`. | No historical REST backfill. Invisible appears offline; “online” does not mean working or reading Discord. |
| Voice state | REST current voice state and Gateway join/leave/move state: guild/channel/user IDs, mute/deaf/video/stream/suppress flags. **O** [S2,S7] | `GUILD_VOICE_STATES`; REST access to another user requires permission to connect to the channel. | No audio, transcript, speaking-turn, or conversation-content field. Duration must be inferred from paired events and is vulnerable to gaps. |
| Audit logs | REST entries: actor/target/action/changes/options/reason; pagination. **O** [S8] | `VIEW_AUDIT_LOG`. | Stored for exactly 45 days; 1–100 per request. Changes are not guaranteed complete. This is administrative action evidence, not all moderation or message activity. |
| Moderation | Ban/member events, audit entries, Auto Moderation rules and execution events. Execution includes rule/action/user/channel/message IDs; content fields need `MESSAGE_CONTENT`. **O** [S2,S8,S9] | `GUILD_MODERATION`, `AUTO_MODERATION_CONFIGURATION`, or `AUTO_MODERATION_EXECUTION` as appropriate; Auto Moderation REST requires `MANAGE_GUILD`. | Blocked content may have no message ID; configuration/execution events are not a complete policy-enforcement history. |
| Bots | User `bot` indicator, bot-owned role tags, message application/webhook fields. **O** [S3,S5] | Same containing-object access. | Supports classification of documented bot/webhook traffic, not detection of every automated or externally relayed human account. |
| Webhooks | REST webhook resources; `WEBHOOKS_UPDATE` supplies guild/channel when a webhook changes; messages may carry `webhook_id`. **O** [S2,S3] | `GUILD_WEBHOOKS`; listing/managing webhooks is permission-gated. | Update event does not identify the changed webhook or reconstruct historic provenance. |
| Edits | Gateway `MESSAGE_UPDATE`; message `edited_timestamp`; REST returns current object. **O** [S2,S3] | Message gates above. | No version-history endpoint. Prior bytes exist only if captured live and retained legitimately. |
| Deletions | Gateway delete contains only message ID, channel ID, optional guild ID; bulk delete contains IDs. **O** [S2] | `GUILD_MESSAGES`. | No deleted content, author, deleter, reason, or original timestamp in the delete event. Some moderator actions may separately appear in audit logs, but correlation is incomplete. |
| Time | Object-specific ISO timestamps, snowflake IDs, and Gateway sequence numbers. **O** [S1–S8] | Surface-specific. | Gateway sequence is relative ordering, not event wall time. Reactions/deletes lack their own event timestamp; receipt time would be collector-generated. |

### REST versus Gateway

- **REST is snapshot/backfill:** current guild/member/role/channel state, extant message history, reaction state, archived threads, and the 45-day audit window. It is paginated, permission-filtered, and dynamically rate-limited. **O**
- **Gateway is forward observation:** creates, updates, deletes, joins/leaves, reactions, presence, voice state, and moderation execution after a connection exists. Resume supports interrupted sessions, but Discord documents no durable general replay log. **O/I**
- **Reconciliation is incomplete:** REST can repair some current state, but cannot recover deleted message bytes, prior edit versions, reaction times, historical presence/voice transitions, or events outside a non-resumable gap. **I**
- Both routes require an authorized app/bot and applicable intents/permissions. Documentation proves possible interfaces, not that any proposed server would grant them. **O/U**

### Permissions, rates, and history constraints

- Privileged intents are `GUILD_MEMBERS`, `GUILD_PRESENCES`, and `MESSAGE_CONTENT`. Current Gateway documentation says applications exceeding 10,000 unique users require review for continued privileged-intent access; privileged access must be purpose-required and Developer-Policy-consistent. **O** [S1]
- Intents select Gateway event families; guild/channel permissions separately control what the bot may view or retrieve. REST privileged-intent restrictions are independent of intents sent during Gateway Identify. **O**
- Discord says REST limits vary and may change: clients must parse bucket and retry headers rather than hard-code limits. The currently documented bot global limit is 50 requests/second; the invalid-request limit is 10,000 qualifying 401/403/429 responses per 10 minutes. **O** [S10]
- Gateway clients may send 120 events per connection per 60 seconds and are also subject to Identify/session-start and sharding limits. This is a send/connection constraint, not proof that an event consumer can process every received event. **O/I** [S1]
- Message history: 1–100 per page, no documented fixed age ceiling; only undeleted and accessible messages. Members: 1–1000 per page. Audit logs: 1–100 per page and 45-day retention. **O**
- Bulk deletion’s two-week age restriction is an operation limit, not evidence that Discord retains messages for only two weeks. **O**

### Documented deletion and retention limits

- Audit-log entries are stored for 45 days. **O** [S8]
- An application must promptly update or delete API Data on applicable user/Discord request, when it is no longer needed for permitted stated functionality, when the app stops, or when law requires; it must expose an accessible modification/deletion route and encrypt API Data at rest. **O** [S12 §5]
- After API termination, cached/stored API Data must be deleted. **O** [S12 §9]
- Discord states specifically deleted content becomes unavailable and is deleted from its systems, subject to cache-clearing delay, legal retention, and possible 180-day-to-two-year retention for public posts. Account deletion may retain shared content in dissociated form unless the user deletes it first. These are Discord-side policies, not API retrieval guarantees. **O** [S13]
- No fixed allowable research-retention period or general message-history retention period is documented for third-party apps. The app must define a shorter purpose-bound schedule consistent with the terms; the exact acceptable schedule remains **U**.

### Metadata-only minimum

A technically minimal, content-free candidate would use only `GUILDS`, `GUILD_MESSAGES`, and optionally `GUILD_MESSAGE_REACTIONS`; omit `MESSAGE_CONTENT`, `GUILD_PRESENCES`, `GUILD_MEMBERS`, voice, audit logs, names, nicknames, avatars, content, embeds, attachments, components, polls, and Auto Moderation text. Allowlist only guild/channel/thread/message IDs, pseudonymized author or reactor ID, message timestamp/edit flag, bot/webhook classification, reply reference IDs, and optional mention/reaction selectors.

However, this is only a **technical minimization**. Stable pseudonyms plus reply/mention/reaction edges still describe user relationships.

A safer platform-aggregate alternative would discard persistent user IDs and report sufficiently large channel/time-bucket totals. That ceases to support person-to-person ONA and still needs a stated, permitted app purpose.

### Policy blocker and claim ceilings

**Observed policy:** Developer Policy rule 16 says API Data must not be used to profile Discord users, their identities, or their relationships with other users, and must not be used for eligibility considerations such as employment. Rule 15 restricts collection/use to necessary stated functionality. [S11]

**Inference:** Conventional person-to-person organizational network analysis is relationship profiling. Therefore server-owner authorization, participant consent, metadata minimization, or lack of message content does not by itself clear Discord’s platform-policy gate. No live ONA collector should proceed unless Discord confirms the exact non-employment, non-profiling use is permitted or the design is reduced to non-relational aggregates.

Documentation supports only claims about:

- Available schemas, events, endpoints, permissions, intents, and published limits.
- Potential observation of platform interactions under an authorized installation.

It does **not** support claims of complete data, legitimate collection, consent, collaboration, influence, knowledge transfer, leadership, productivity, performance, sentiment, team structure, organizational importance, or causal effect.

### Missing observations and blockers

- Member-to-member DMs; private channels or threads the app cannot access.
- Views, read receipts, lurkers, downloads, or whether a recipient noticed a message.
- Off-platform work and communication.
- Historical presence, voice transitions, reaction times, edit versions, and deleted bytes outside a live legitimate capture.
- Semantic meaning of roles, channels, emojis, replies, mentions, moderation actions, or silence.
- Actual bot installation, server approval, user notice/consent, privileged-intent approval, purpose, jurisdiction, retention schedule, or live completeness.
- Platform-policy clearance for relationship profiling is absent and is the principal downstream blocker.

```json
{
  "action_id": "spawn-0001",
  "status": "pass",
  "validation": "pass",
  "artifacts": [
    "discord-first-party-source-inventory",
    "discord-api-observability-matrix",
    "discord-rest-gateway-boundary",
    "discord-metadata-minimum-and-claim-ceilings"
  ],
  "blockers": [
    "developer-policy-rule-16-prohibits-use-of-api-data-to-profile-user-relationships",
    "no-live-server-or-application-authorization",
    "no-consent-purpose-jurisdiction-or-retention-basis",
    "no-live-completeness-or-permission-validation",
    "no-documented-general-message-retention-or-event-replay-guarantee"
  ],
  "handoff": "Synthesis must keep the technical map, but treat person-to-person Discord ONA as platform-policy blocked unless Discord clears the exact use; non-relational aggregates are the only currently defensible reduction."
}
```

## Agent 3 — Privacy, governance, and platform policy

### Decisive gate

**Platform-policy claim:** Discord Developer Policy §16 prohibits using API Data to profile Discord users, their identities, or their relationships, and prohibits using it for employment eligibility considerations. A person-linked or tie-level Discord ONA—including user-user, user-channel, or role-user graphs—would therefore fall within the prohibition’s ordinary meaning. Consent, server-admin approval, pseudonymization, or an organizational-improvement label does not override that rule.

**Result:** `BLOCK` any live Discord API collection or Discord-derived relationship analysis unless Discord provides authoritative written clarification that the exact non-person-level design is permitted. This research action itself passes because it established the boundary without accessing a server or collecting data.

### Source register

All current web sources were accessed 2026-08-07.

- **D1 — Platform policy:** [Discord Developer Policy](https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy), selectors `## Protect Discord Users` items 1–3; `## Respect Our Platform Rules` item 9; `## Handle Data with Care` items 15–21 and the incident-notification paragraph. Load-bearing rules: stated-purpose limitation; relationship profiling and employment-use prohibition; minors/sensitive data; no re-identification, scraping, or unauthorized message-content model training.
- **D2 — Platform contract:** [Discord Developer Terms of Service](https://support-dev.discord.com/hc/en-us/articles/8562894815383-Discord-Developer-Terms-of-Service), selectors `Section 1(b): Registration & Application Information`; `Section 4: Compliance with Laws & Third-Party Rights`; `Section 5(a): Implement Good Privacy Practices`; `5(b): API Data Sharing & Retention`; `5(c): Implement Good Security`; `Section 6: Monitoring & App Review`.
- **D3 — User/platform terms:** [Discord Terms of Service](https://discord.com/terms), selectors `Age requirements and responsibility of parents and legal guardians`; `Software in Discord’s services > Third-party services`; `Restrictions on your use of Discord’s services`.
- **D4 — Discord privacy representation:** [Discord Privacy Policy](https://discord.com/privacy), selectors `A little bit about Discord`; `The information we collect > Content you create / Information from actions you take / Information about your use`; `How we disclose your information`; `Data retention`; `How we protect your information`; `How to control your privacy`.
- **E1 — Research ethics:** [HHS OHRP Belmont Report](https://www.hhs.gov/ohrp/sites/default/files/the-belmont-report-508c_FINAL.pdf), selectors `B. Basic Ethical Principles > 1. Respect for Persons / 2. Beneficence / 3. Justice`; `C. Applications > 1. Informed Consent > Information / Comprehension / Voluntariness`; `2. Assessment of Risks and Benefits`; `3. Selection of Subjects`.
- **E2 — Employment consent, EU/EEA guidance:** [EDPB Guidelines 05/2020](https://www.edpb.europa.eu/system/files/documents/files/file1/edpb_guidelines_202005_consent_en.pdf), selectors paragraphs 3, 5, 13, and 21–24 under `3.1 Free / freely given` and `3.1.1 Imbalance of power`. Consent is generally problematic in employment because refusal may carry feared or real detriment.
- **E3 — International nonbinding privacy principles:** [OECD Privacy Guidelines](https://legalinstruments.oecd.org/public/doc/114/body-text.en.html), selectors `Part Two` paragraphs 7–14 and `Part Three` paragraph 15: collection limitation, purpose specification, use limitation, safeguards, openness, individual participation, correction, accountability, and incident planning.
- **E4 — De-identification:** [NISTIR 8053, De-Identification of Personal Information](https://www.nist.gov/publications/de-identification-personal-information), selector `Abstract`; de-identification reduces risk but some de-identified datasets can be re-identified.
- **E5 — UK employment-regulator guidance:** [ICO, Data protection and monitoring workers](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/monitoring-workers/data-protection-and-monitoring-workers/), selectors `What must we tell workers about our monitoring?`, `Can we use covert monitoring?`, and `What do we need to consider if we use a third-party provider...`; [ICO automated monitoring](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/monitoring-workers/what-do-we-need-to-do-if-we-use-monitoring-tools-that-use-solely-automated-processes/), selectors `What do we mean...`, `What should we tell workers...`, and `What is the role of human oversight?`. This jurisdiction-specific guidance is currently marked under review.
- **E6 — Anonymization:** [ICO, Introduction to anonymisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/introduction-to-anonymisation/), selectors `If we anonymise personal data, does this count as processing?` and `What is the difference between anonymisation and pseudonymisation?`; [ICO, effectiveness](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/how-do-we-ensure-anonymisation-is-effective/), selectors `What approaches can we take to anonymisation?`, `What is generalisation?`, and `K-anonymisation`.
- **L1 — EU/EEA law, applicability for counsel:** [GDPR official text](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng), selectors Articles 5, 13–17, 22, 25, 32–35. This is not a conclusion that GDPR applies to a particular organization or participant.

### Control findings

| Area | Policy/source claim | Recommended synthesis |
|---|---|---|
| Purpose limitation | D1 §15 confines API Data to necessary stated/approved app functionality; §16 separately forbids relationship profiling. E3 ¶¶9–10 and L1 Art. 5 provide broader purpose/use-limitation models. | Write one narrow question, prohibited downstream uses, outputs, owners, and expiry before collection. “Research” is not a purpose broad enough to authorize reuse. |
| Notice and consent | D2 §5(a) requires an accurate, accessible privacy policy. E1 requires information, comprehension, and voluntariness; E2 explains employment-power defects. | Layered pre-collection notice plus affirmative, revocable participation. Refusal must have no employment, access, or reputational consequence. Consent cannot cure D1 §16. |
| Bot disclosure | D2 §1(b) requires an accurate application identity/description; §5(a) requires an accessible privacy policy. Discord does not thereby establish research consent from every server member. | Persistent bot label, owner/contact, data categories, purposes, recipients, retention, opt-out/withdrawal, and deletion route in the bot profile and server notice—not merely an installation dialog. |
| Least privilege | D1 §15 and D2 §2 limit access to what is necessary for approved functionality. | Default-deny scopes and channels; no administrator-wide permissions; reviewed allowlist; separate pilot application; periodic permission review. |
| Metadata versus content | D4 treats messages, roles, communities, interactions, channel visits, and event/log information as information about users. D1 §16 applies to relationship profiling regardless of whether content is read. | Metadata-only is lower risk, not anonymous or automatically permitted. Do not collect message bodies, attachments, voice/video, sentiment, keywords, or inferred topics for this study. |
| Private channels and DMs | D3/D4 distinguish DMs and permission-bounded spaces; permissions can change. | Absolute study red line: no DMs, group DMs, private/restricted channels, deleted content, drafts, or spaces whose members did not receive notice. Admin access is not participant consent. |
| Minors and guests | D3 permits qualifying users from 13 upward; D1 §§9 and 16 impose youth restrictions. | Exclude minors by design; do not infer age or collect proof of age. Exclude external guests, contractors, former members, and cross-server identities unless separately governed and voluntarily enrolled. |
| Employment power | D1 §16 directly prohibits employment-purpose use and relationship profiling. E2 ¶¶21–24 says employee consent is generally not freely given; E1 flags authority pressure. | Firewall research from HR, managers, promotion, pay, discipline, hiring, termination, attendance, productivity, and performance processes. No manager may see individual or small-team data. |
| Pseudonymization/re-identification | D1 §19 prohibits re-identification attempts. E4 and E6 show pseudonymization remains linkable and de-identification can fail. | Separate identity map and analysis store; distinct keys; prohibit linkage; test singling-out, linkability, and inference. Never call stable hashed Discord IDs anonymous. |
| Access and encryption | D2 §5(c) requires encryption at rest and safeguards; E3 ¶11 and L1 Art. 32 add risk-based security models. | Encrypt in transit and at rest; keys outside datasets; role-based access; two-person export approval; analyst access to pseudonyms only; no raw data on laptops or collaboration tools. |
| Retention/deletion | D2 §5(b) requires prompt update/deletion when no longer necessary, requested, or operation stops. | Predeclare finite raw, edge-table, aggregate, backup, and audit-log schedules. Deletion must cascade through identity maps, graphs, metric caches, exports, and backups. No indefinite longitudinal store. |
| Access/correction | D2 §5(b) requires accessible modification/deletion requests; E3 ¶13 and L1 Arts. 15–17 define access/correction models. | Provide a non-manager request channel, identity-verification process, response SLA, correction provenance, graph recomputation, and appeal route. |
| Small-group suppression | E6 explains generalization, suppression, and k-anonymity while warning about inference attacks. | Suppress isolated nodes, named communities, exact low counts, rare-role combinations, and longitudinal differencing. A provisional `k ≥ 5` may be a floor, never a safe harbor; determine a stricter threshold through disclosure-risk testing. |
| Aggregation/reporting | E6 states creating aggregates is itself processing; D1 §16 remains upstream. | Release only non-relational, team-level descriptive aggregates after policy clearance. No node-link diagrams, individual ranks, ego networks, centrality tables, inferred “silos,” or downloadable microdata. |
| Audit and incidents | D2 §5(c) requires prompt Discord notification, user notification where applicable, remediation, and cooperation. E3 ¶15 calls for oversight and incident plans. | Log access, queries, exports, approvals, corrections, and deletions without message content. Preassign containment, Discord notification, participant notification, evidence preservation, and post-incident review owners. Counsel determines jurisdictional deadlines. |
| Covert surveillance / scoring | D1 §16 blocks relationship profiling and employment uses. E5 says routine covert worker monitoring is generally unjustifiable and describes automated-decision safeguards under UK law. | Prohibit covert monitoring, hidden bots, behavioral risk scores, productivity/performance/influence/leadership scores, automated alerts about workers, and any employment decision based on trace metrics—even with nominal human review. |

### Minimum control set if Discord first clears a non-relational design

1. Written Discord policy clarification for the exact fields, transformation, purpose, and outputs.
2. Named data controller/sponsor; approved protocol, threat model, DPIA-equivalent assessment, and independent ethics review.
3. Worker/participant consultation, layered notice, genuine no-detriment choice, and visible bot disclosure.
4. Exclusion of DMs, private channels, content, minors, guests, and nonparticipants.
5. No person-level graphs, scores, rankings, labels, or employment use.
6. Field/channel allowlist, least-privilege permissions, pseudonymization, separated keys, encryption, and analyst/manager firewall.
7. Precommitted retention, deletion propagation, access, correction, withdrawal, and appeal procedures.
8. Small-group suppression, disclosure-risk review, aggregate-only release, and no downloadable microdata.
9. Auditable access/export/deletion trail and tested incident-response procedure.
10. Periodic review that can stop collection; purpose expansion requires fresh platform, ethics, privacy, and participant review.

These controls do **not** make the currently proposed Discord relationship ONA permissible; they are prerequisites only for a materially narrower design after platform clearance.

### Red lines

- Discord API Data used to build or infer user relationships.
- Any employment eligibility, productivity, performance, influence, leadership, engagement, misconduct, retention-risk, or promotion score.
- Scraping, self-bots, user-token automation, or circumvention of Discord limits.
- Covert collection or relying solely on server-admin installation.
- DMs, private/restricted channels, message content, attachments, voice/video, deleted content, or sentiment.
- Minors, external guests, and nonparticipants.
- Re-identification, cross-dataset linkage, or publishing sparse network structures.
- Secondary use, indefinite retention, or collection before rights/deletion mechanisms exist.

### Safer alternatives

- Continue with a fully synthetic Discord-shaped fixture; test schemas, suppression, deletion propagation, and reporting without live traces.
- Use independently administered, voluntary self-report collaboration surveys with no manager access to individual responses.
- Use participatory team workshops where members construct and control their own aggregate collaboration map.
- Ask Discord for written clarification about a strictly non-relational, channel-level aggregate design.
- Use organization-owned operational data collected for a compatible purpose only after separate ethics, privacy, labor, and legal review; do not call it Discord ONA.
- Prefer qualitative interviews and model-free team summaries over inferred person-level networks.

### Owner decisions required

- **Discord/platform owner:** Is any exact non-relational aggregate design permitted under §16?
- **Study sponsor/data controller:** Operational improvement or generalizable research; exact purpose, participants, outputs, and stop rule.
- **Independent ethics/IRB owner:** Review category, consent/waiver question, nonparticipant effects, vulnerable groups.
- **Privacy counsel/DPO:** Applicable jurisdictions, controller/processor roles, lawful basis, DPIA, transfers, access/deletion duties.
- **Employment/labor counsel and worker representatives:** Monitoring, collective consultation, non-retaliation, and management firewalls.
- **Security owner:** Architecture, credentials, encryption, access review, logging, backups, incident response.
- **Disclosure-control owner:** Suppression threshold, linkage testing, release review.
- **HR/executive owner:** Binding prohibition on person-level access and employment decisions.

```json
{
  "action_id": "spawn-0003",
  "status": "pass",
  "validation": "pass",
  "artifacts": [
    "privacy-governance-evidence-return",
    "minimum-governance-control-set",
    "red-lines-and-safer-alternatives",
    "owner-decision-register"
  ],
  "blockers": [
    "current Discord Developer Policy section 16 blocks API-Data profiling of users or their relationships",
    "current Discord Developer Policy section 16 blocks employment-purpose eligibility use",
    "no jurisdiction, data controller, participant population, ethics determination, retention policy, or Discord written clarification is selected"
  ],
  "handoff": "Synthesis must mark live person-linked Discord ONA as platform-policy-blocked and keep synthetic or independently collected non-Discord alternatives as the safe research path."
}
```

## Agent 2 — ONA methods and validity

Completed `spawn-0002` read-only. No Discord server was accessed and no data was collected.

Legend: **SB** = directly source-backed; **SYN** = methodological synthesis conditional on the API explorer verifying the required Discord observations. API observability, consent, and organizational authority remain separate gates.

### Defensible question ceiling

**SYN—legitimate questions**

- How concentrated or unequal is observed participation?
- Where do observed replies/mentions cross owner-validated team boundaries?
- Which users occupy potential structural bridge positions in the chosen trace graph?
- How segregated is channel participation, and how does it change over time?
- What is the distribution of observed reply delays, conditional on activity opportunity?
- Are interaction patterns stable across preregistered windows or interventions?

“Collaboration,” “knowledge flow,” and “silo” are hypotheses requiring external validation. “Productivity,” “performance,” “influence,” “sentiment,” and “informal leadership” are not trace-level constructs.

This ceiling is material: email traces have been empirically related to, but significantly different from, survey-measured communication, friendship, and advice networks ([Johnson, Kovács & Vicsek 2012, Abstract and Introduction](https://doi.org/10.1016/j.socnet.2012.02.004)). **SB**

### Candidate graph bindings

| Observation | Explicit graph | Direction, weight, time, normalization | Construct ceiling and missingness |
|---|---|---|---|
| Reply | User author `i → j` where `j` authored referenced message; separate layer from mentions | Raw event count plus binary tie and active-day count; fixed UTC windows with rolling-window sensitivity; normalize by sender activity/opportunities | Addressed response, not agreement, collaboration, knowledge transfer, or exposure. Requires complete in-scope reply references, messages, deletions, bots, and membership intervals. |
| Mention | Author `i → mentioned user j`; one edge per human target; broadcast/group mentions excluded unless expansion semantics are verified | Preserve raw count; optional fractional `1/k` per message with `k` human targets; normalize by sender output and channel volume | Addressed attention only. A mention does not prove reading, response, influence, or a social tie. |
| User–channel | Bipartite `user ↔ channel`, one participation event per authored in-scope item | Binary participation, count, and active days; normalize both by user total and channel event volume/active population; retain bipartite graph as primary | Participation footprint and cross-channel breadth, not channel membership, exposure, team, or collaboration. Projection loses information; two-mode analysis should remain primary ([Latapy et al. 2008, Introduction and “Projection,” pp. 31–48](https://doi.org/10.1016/j.socnet.2007.04.006)). **SB** |
| User–role | Temporal bipartite affiliation `user ↔ role` over verified effective intervals | Binary state; duration-weight only for availability, never “tie strength”; role changes split intervals | Declared platform affiliation/permission. It is a team boundary only after owner validation; cosmetic, permission, bot, and overlapping roles otherwise confound it. |
| Reaction | Primary tripartite event `reactor → message ← author`, retaining reaction token; candidate projection `reactor → author` | Count unique reaction events, active days, and fractionalize multi-reaction/message bundles; normalize by eligible authored messages and channel volume; report self-reactions separately | Observable acknowledgment/interaction. Emoji cannot support signed polarity, endorsement, sentiment, trust, or approval without context-specific blinded coding. |
| Thread co-participation | Primary bipartite `user ↔ thread`; candidate undirected projection between co-participants | Binary per user-thread; projected weight `Σ_t 1/(n_t−1)` to reduce large-thread clique inflation; separate direct replies | Shared forum participation, not dyadic interaction. Fractional weighting follows the same event-size correction logic as Newman’s Eq. 2 ([§III, pp. 016132-5–6](https://doi.org/10.1103/PhysRevE.64.016132)). **SB analogy / SYN binding** |
| Temporal sequence | Events `(actor, relation, target, timestamp, context)`; time-respecting paths require increasing timestamps | Preserve event time; report inter-event intervals and windowed aggregates; UTC plus local-work-period sensitivity if legitimately available | Order, bursts, persistence, and possible pathways—not causation or actual information transmission. Static aggregation can erase ordering ([Holme & Saramäki 2012, §§2–3, pp. 97–108](https://doi.org/10.1016/j.physrep.2012.03.001)). **SB** |

All layers should remain multiplex. Combining replies, mentions, reactions, affiliations, and co-participation into one “social graph” is invalid; multislice methods exist precisely because link type and time are distinct ([Mucha et al. 2010, abstract and Eq. 2, pp. 876–878](https://doi.org/10.1126/science.1184819)). **SB**

### Metric-to-construct / misuse matrix

| Metric | Defensible use | Mandatory misuse rejection |
|---|---|---|
| Degree/strength | Unique observed counterparts or event volume in one declared layer/window | Popularity, productivity, workload, importance, or performance |
| Reciprocity | Excess bidirectionality in a directed relation against an activity-preserving null ([Garlaschelli & Loffredo 2004, abstract](https://doi.org/10.1103/PhysRevLett.93.268701)) | Trust, mutual support, agreement |
| Betweenness | Potential geodesic intermediary position in a specified projection | Actual control, indispensability, influence, or knowledge brokerage; Freeman distinguishes potential control from degree activity ([Freeman 1979, pp. 215–239, especially summary pp. 237–238](https://doi.org/10.1016/0378-8733(78)90021-7)) |
| Eigenvector/PageRank | Recursive connectivity/prestige under explicitly oriented edges and component/sink handling | Leadership, authority, expertise, influence; PageRank’s original construct is hyperlink-based recursive importance ([Brin & Page 1998, §2.1](https://doi.org/10.1016/S0169-7552(98)00110-X)) |
| k-core | Repeated-interaction subgraph satisfying minimum degree `k` ([Seidman 1983, pp. 269–287](https://doi.org/10.1016/0378-8733(83)90028-X)) | “High-performing core,” inner circle, indispensability |
| Brokerage | Counts of intermediary triads across owner-validated groups; report Gould–Fernandez role type ([pp. 89–126, especially pp. 91–97](https://doi.org/10.2307/270949)) | Proof that information was transmitted, translated, or controlled |
| Modularity | Partition strength relative to a declared null model | Organizational silos or official teams; modularity has a size-dependent resolution limit ([Fortunato & Barthélemy 2007, abstract and pp. 36–41](https://doi.org/10.1073/pnas.0605965104)) |
| Assortativity | Mixing by a validated categorical/scalar attribute ([Newman 2003, §II](https://doi.org/10.1103/PhysRevE.67.026126)) | Preference, discrimination, homophily, or causality |
| Density | Realized observed ties divided by possible ties inside one fixed boundary/window | Cohesion, health, or cross-size comparison without opportunity correction |
| Centralization | Inequality of one declared centrality relative to its graph-theoretic maximum | Hierarchy, effectiveness, resilience, managerial control |
| Temporal stability | Edge/rank/partition similarity across preregistered windows and multiple window lengths | Adaptability, organizational health, causal effect; short- and long-term regularity can represent different processes ([Quintane et al. 2013, abstract, pp. 528–540](https://doi.org/10.1016/j.socnet.2013.07.001)) |

### Bias register

**SB:** Network measurement must distinguish perceived ties from actual exchanges, define population boundaries and temporal relations, and test sampling/error effects ([Marsden 1990, Abstract, pp. 435–463](https://doi.org/10.1146/annurev.so.16.080190.002251)). Boundary exclusion, non-response, and fixed-choice censoring can substantially alter network statistics ([Kossinets 2006, Abstract, pp. 247–268](https://doi.org/10.1016/j.socnet.2005.07.002)). Centrality robustness under random error does not license confidence under systematic platform missingness; the authors explicitly limit their experiment to random error on random graphs ([Borgatti, Carley & Krackhardt 2006, §4 pp. 134–135](https://doi.org/10.1016/j.socnet.2005.05.001)).

**SYN—Discord-specific risks to register before analysis**

- Boundary/coverage: excluded channels, permissions, private spaces, departed users, edits/deletions, backfill limits.
- Adoption/opportunity: Discord use varies by role, timezone, tenure, access, notification settings, and substitution to meetings, DMs, email, or other tools.
- Measurement: broadcasts and bots inflate degree; replies omit unthreaded responses; reactions are context-dependent; co-participation creates artificial cliques.
- Denominator: message counts without active time, channel opportunity, membership interval, and event volume are incomparable.
- Temporal: join/leave censoring, seasonality, incident bursts, window choice, and delayed replies.
- Construct: roles are not necessarily teams; messages are not work; co-presence is not collaboration; correlation is not influence. Homophily, influence, and shared causes are generically confounded in observational networks ([Shalizi & Thomas 2011, abstract and §§2–4](https://doi.org/10.1177/0049124111404820)).
- Behavioral reactivity: disclosed measurement may change use; covert measurement is outside this lane and unacceptable.

### Discriminating validation and negative controls

**SYN**

1. Relation-specific surveys: independently ask about communication, advice seeking, knowledge sharing, and collaboration; test dyadic precision/recall, calibration, and QAP association separately. Failure blocks the corresponding construct, not the trace description.
2. Owner-validated boundaries: compare inferred communities/mixing with canonical teams using ARI/AMI and permutation baselines. Discord roles alone are not gold truth.
3. Stratified blinded human coding: sample reply, mention, reaction, and thread events across channels, sizes, and roles; code interaction function and context with inter-rater reliability. Without legitimate content access, abstain rather than infer.
4. Time-respecting holdout: train on earlier windows, predict later interactions against sender-activity, receiver-popularity, channel, and recency baselines. Predictive success supports recurrence only, not construct validity.
5. Missingness sensitivity: simulate node/edge loss by permission/channel/member strata, not only random deletion; publish rank, community, density, and bridge stability envelopes.
6. Negative controls:
   - permute targets within sender/channel/time strata;
   - shuffle timestamps within actor-day while preserving volumes;
   - permute role labels while preserving role sizes;
   - compare bot/system-only and human-only layers;
   - test impossible future-to-past ordering;
   - test self-reactions and broadcast-only events separately.

   A purported bridge, temporal-flow, or role-mixing signal that survives the control designed to destroy that mechanism is non-discriminating. Negative controls are an established bias-detection device, though their application here is synthesis ([Lipsitch, Tchetgen Tchetgen & Cohen 2010, abstract and Fig. 1, pp. 383–388](https://doi.org/10.1097/EDE.0b013e3181d61eeb)).
7. Predeclare construct, graph, window, exclusions, denominator, null model, validation threshold, and abstention result before examining organizational outcomes.

### Hard abstention rules

- No **productivity/performance** claim without independently measured outcomes, a causal design, and an authorized decision owner.
- No **influence/knowledge-flow** claim from temporal association, PageRank, replies, mentions, or brokerage; observational influence is confounded.
- No **sentiment/endorsement** from reaction tokens without validated contextual coding.
- No **informal-leadership** claim from centrality, k-core, or brokerage without independent multi-method leadership measures.
- No person-level ranking or intervention when boundary coverage, systematic missingness, validation, or governance gates fail.
- A failed construct test leaves only a descriptive statement about observed Discord events.

```json
{
  "action_id": "spawn-0002",
  "status": "pass",
  "validation": "pass",
  "artifacts": [
    "ona_method_evidence_return",
    "discord_candidate_graph_binding_matrix",
    "metric_construct_misuse_matrix",
    "bias_register",
    "validation_negative_control_plan",
    "abstention_rules",
    "primary_source_registry"
  ],
  "blockers": [],
  "handoff": "Synthesis may use these bindings only after the API and governance explorers verify observability, authorization, completeness, and privacy; unsupported person-level organizational claims must abstain."
}
```

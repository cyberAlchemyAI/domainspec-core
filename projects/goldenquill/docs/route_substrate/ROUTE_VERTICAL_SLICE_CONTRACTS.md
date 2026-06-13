# Tilth Route-Resolution Contracts (Vertical Slice)

This document establishes the production-facing contracts for route resolution. It transitions the underlying logic established in the `agnostic_route_substrate` proof into stable API payloads, schemas, and state contracts. The chatbot and UI interact strictly with these affordances—they never parse the taxonomy or policy rules directly.

## 1. Route Evaluation Contract

This table defines the canonical route evaluation states in strict precedence order (highest to lowest priority). All logic belongs to the engine; the UI only reacts to these states.

| State | Meaning | Severity | Blocking | User/Input Resolution Action |
| :--- | :--- | :--- | :--- | :--- |
| **POLICY_CHANGED** | The hash of the current active policy differs from the hash recorded at the time this route was last evaluated. | CRITICAL | Yes | UI must prompt user to re-evaluate or re-affirm the route under current policy. |
| **SPLIT_ROUTE_COLLAPSE** | One binding collapses multiple route obligations, roles, fields, or entities that must be represented as separate bindings. | CRITICAL | Yes | User/system must split the route into one binding per distinct role/field/entity obligation before evaluation continues. |
| **SEPARATION_ERROR** | The proposed routing violates an anti-affinity rule (e.g., the same entity acting as independent reviewer and applicant). | CRITICAL | Yes | User must replace one of the conflicting entity bindings to restore separation of duties. |
| **FACT_CAPACITY_MISMATCH** | The entity's known factual attributes (e.g., lack of insurance) contradict the required facts for the candidate capacity. | CRITICAL | Yes | User must provide missing factual evidence for the entity or change the candidate capacity. |
| **DEFAULT_DENY** | The binding is malformed or incomplete in a way that is not an explicit unresolved placeholder. | CRITICAL | Yes | User/system must repair the malformed binding or convert it into an explicit `UNRESOLVED` placeholder before route evaluation continues. |
| **TAXONOMY_GAP** | The binding asks the engine to evaluate a role, capacity, or classification that does not yet exist in the taxonomy. | CRITICAL | Yes | User/system must add the missing taxonomy concept through governance or choose an already-defined role/capacity. |
| **RESOLVED_INADMISSIBLE** | The route is technically complete, but explicitly prohibited or rejected by higher-order policy (or lacks tier-1 evidence). | HIGH/CRITICAL | Yes | Route cannot proceed as configured. User must change the entity or escalate for an override. |
| **UNCONFIRMED** | A human decision is required to verify the capacity mapping, but the binding remains in DRAFT or the user has not clicked APPROVED. | HIGH/CRITICAL | Yes | A human operator must explicitly change the binding status to APPROVED. |
| **UNRESOLVED** | The system recognizes an entity exists but does not have enough information to categorize or evaluate it. | LOW/CRITICAL | Yes (if SUBMITTED) | User must supply the missing metadata (role, capacity, or entity mapping). |
| **PASS** | The route is fully resolved, confirmed, and mathematically valid under current policy. No conflicts exist. | NONE | No | None. Proceed. |

---

## 2. Affordance API Schema

This is the exact JSON payload the engine emits back to the chatbot/UI for a single route binding evaluation cycle. The UI acts entirely as a dumb rendering layer driven by the `affordance` hints.

```json
{
  "route_id": "PKT-004:[3].entity_route.entity_id",
  "state": "UNRESOLVED",
  "severity": "CRITICAL",
  "plain_reason": "This route is still unresolved. The system cannot evaluate admissibility until a route role is chosen.",
  "missing_input": "route_role",
  "allowed_next_choices": [
    "applies",
    "leads",
    "hosts",
    "receives_funds",
    "provides_service",
    "signs_agreement",
    "carries_liability"
  ],
  "next_action": "PROMPT_USER",
  "provenance_ref": "unresolved_route_table.json:person_named_route:seed/packet_registry.json:[3].entity_route.entity_id",
  "person_route": true,
  "current_binding": {
    "entity_id": "ENT-WILLIAM",
    "candidate_capacity": "",
    "route_role": "",
    "lifecycle_stage": "SUBMITTED",
    "status": "UNRESOLVED"
  }
}
```

---

## 3. Minimal One-Route Template Schema

This is the payload shape the Chatbot/UI sends back to the engine after collecting user input for one route loop.

```json
{
  "entity_id": "string",
  "candidate_capacity": "string",
  "route_role": "string",
  "lifecycle_stage": "string",
  "provenance_ref": "string",
  "person_route": "boolean",
  "human_approval": "string"
}
```

*Rule: If `route_role` is missing or changed, the engine will clear `candidate_capacity` and force the loop to start over, returning `UNRESOLVED` or `DEFAULT_DENY` with new `allowed_next_choices` depending on whether the binding is still an explicit unresolved placeholder or a malformed resolved binding.*

---

## 4. Concrete Vertical Slice Example

**Scenario:** MSC packet record `PKT-004` contains a person-route `[3].entity_route.entity_id` resolved to `ENT-WILLIAM`.

**Turn 1: Initial State**
- UI submits binding: `entity_id: ENT-WILLIAM`, `route_role: ""`, `candidate_capacity: ""`, `person_route: true`.
- **Engine Response:** `state: UNRESOLVED`. `missing_input: route_role`. `allowed_next_choices: ["applies", "leads", "hosts", "receives_funds", "provides_service", "signs_agreement", "carries_liability"]`.
- *Chatbot:* "William is listed on this packet. What role is he fulfilling?"

**Turn 2: Role Supplied**
- User selects: `provides_service`.
- UI submits binding: `route_role: "provides_service"`, `candidate_capacity: ""`.
- **Engine Response:** `state: UNRESOLVED`. `missing_input: candidate_capacity`. `allowed_next_choices: ["internal_service_provider", "commercial_operator", "individual_contributor"]`.
- *Chatbot:* "For this route, the selected role is provides service. Which capacity applies?" *(Note: The system does not assume `individual_contributor` just because `person_route` is true).*

**Turn 3: Capacity Supplied**
- User selects: `individual_contributor`.
- UI submits binding: `route_role: "provides_service"`, `candidate_capacity: "individual_contributor"`.
- **Engine Response:** `state: UNCONFIRMED`. `missing_input: human_approval`. `next_action: REQUEST_EXPLICIT_APPROVAL`.
- *Chatbot:* "William is admissible for the provides service role under the individual contributor capacity, but this is a person-route decision. Please explicitly confirm and approve this mapping to finalize the route."

**Turn 4: Final Approval**
- User clicks: [APPROVE]
- UI submits binding: `human_approval: "APPROVED"`.
- **Engine Response:** `state: PASS`. `next_action: NONE`.
- *Chatbot:* "Route resolved and saved."

---

## 5. Production Substrate Decision Note

To scale the prototype engine into production, three architectural substrates were evaluated:

1. **OPA (Open Policy Agent) + Rego**
   - *Pros:* Industry gold standard for policy decoupling. Highly performant. Portable.
   - *Cons:* Heavy learning curve for Rego syntax. Overkill for purely linear decision trees. Slower integration velocity.
2. **JSON Schema + Thin Evaluator**
   - *Pros:* Native to the existing JSON-heavy bundle ecosystem. Excellent open-source tooling.
   - *Cons:* JSON Schema is designed for data validation, not precedence-based business logic (e.g., `SPLIT_ROUTE_COLLAPSE` vs `SEPARATION_ERROR` is awkward to express in pure JSON schema).
3. **Custom Python Module (Current Substrate)**
   - *Pros:* Complete control over execution order, precedence, and error affordances. Fits seamlessly into existing Tilth validation scripts. 
   - *Cons:* Higher risk of building a bespoke, unmaintainable "shadow rules engine."

**Recommendation for Next Prototype:** 
**JSON Schema + Thin Evaluator.** 
Use JSON Schema strictly to validate the structure of the incoming `Minimal One-Route Template Schema` and the outgoing `Affordance API Schema`, but keep the route logic encapsulated in a tightly bounded, rigorously tested Python module (the thin evaluator). OPA/Rego is too heavyweight for the chatbot's latency and data requirements at this stage, while pure Python without JSON schema boundaries invites schema drift.

# FIT Farms MVP Operator Specification

## 1. Purpose
FIT Farms serves as the MVP operator proving ground. The goal is to successfully process one real opportunity and one real organization folder, ultimately producing an 8-point analyst output for the operator. This proves the end-to-end viability of the Scout system under realistic, governed conditions.

## 2. Customer-Facing Operator Spine
The overarching operator workflow follows a rigid six-step spine:
1. **Discover**: Identify and acquire relevant source artifacts.
2. **Draft**: Prepare initial opportunity insights and summaries.
3. **Review**: Evaluate the draft against operator criteria and constraints.
4. **Capture**: Secure evidence, provenance, and operator decisions.
5. **Report**: Produce the structured output for operator consumption.
6. **Remember**: Store the confirmed artifacts and context for future use.

## 3. The 8 Operator Pillars
The true MVP output is the operator-facing interface consisting of these 8 pillars:
1. **Opportunity summary**: A plain, factual overview of the opportunity.
2. **Fit rationale**: A grounded evaluation of how the opportunity aligns with the applicant.
3. **Missing-information list**: Explicit documentation of what facts remain unknown.
4. **Section map**: A structured breakdown of the required proposal sections.
5. **First draft section**: One grounded, evidence-backed draft of a core section.
6. **Evidence/provenance map**: Clear citations linking all claims back to the acquired source artifacts.
7. **Blocker list**: Hard constraints or missing prerequisites preventing immediate action.
8. **Next operator action**: The single most valuable next step the human operator must take.

## 4. Internal Telemetry Support
Internal system metrics exist solely to support the 8 Operator Pillars invisibly or via a dedicated evidence panel. They do not replace the operator-facing output. These include:
- `source_id`
- `retrieval_status`
- `payload_sha256`
- `local_artifact_path`
- Fetch ledger entries
- Freshness states
- Provenance/evidence references

## 5. Proposed Local Fixture Strategy
Local fixtures drive the MVP without requiring immediate live fetching.
We propose using the existing `tests/fixtures/funder_terrain/` convention or establishing a dedicated `tests/fixtures/mvp/` handoff directory in the future. We will avoid hardcoding absolute machine paths (e.g., `/Users/...`) as doctrine. The strategy remains entirely local, deterministic, and auditable.

## 6. FIT Farms Boundaries
FIT Farms may act as the applicant for FIT Farms-specific work. All third-party work must remain strictly in draft or handoff states unless explicit authorization exists. The system must never pretend FIT Farms is the applicant for another entity. The "Applied As" identity boundary remains absolute and explicitly governed.

## 7. Live Acquisition Posture
Live fetch is a product-critical capability. Governed acquisition retrieves source facts and artifacts accurately. However, the acquisition layer does NOT score, draft, alert, submit, export, or infer authority. It is strictly a retrieval and normalization mechanism.

## 8. Minimum MVP UI Behavior
The operator interface for the MVP must successfully:
- Load the organization context.
- Load or acquire one single opportunity.
- Show the source/retrieval state.
- Display the 8 Operator Pillars.
- Highlight blockers and the next valid action.
- Keep the operator's authority central to all decisions.

## 9. Definition of Done
The FIT Farms MVP is considered done when:
- One real opportunity is fully processed.
- One FIT Farms folder/context is utilized.
- The eight-point output is generated successfully.
- An accurate evidence/provenance map is displayed.
- One grounded first draft section is produced.
- No manual script stitching is required by the operator.

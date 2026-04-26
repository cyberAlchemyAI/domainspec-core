# DomainSpec Canonical Definitions

Purpose: authoritative source of DomainSpec research definitions.

This document is the normative definition contract for the DomainSpec evidence program. The paper is a condensed synthesis of these definitions plus experimental evidence.

## Authority and Precedence

1. `definitions/DEFINITIONS.md` is the canonical definition source.
2. `definitions/DEFINITIONS-INDEX.md` is the lookup/index layer that maps IDs to artifacts and examples.
3. `papers/domainspec-paper.md` is a narrative condensation for publication and discussion.

When wording differs across artifacts, this document is authoritative for definition semantics.

## Definition Families

- `DS-C*`: contribution-level definitions
- `DS-D*`: core architecture and ontology definitions
- `DS-P*`: structural properties
- `DS-COR-*`: corollaries
- `DS-F*`: formal constructs and equations
- `DS-M*`: research methodology and execution definitions

## Contribution-Level Definitions

### DS-C1: Meta-Architecture Contribution

DomainSpec defines a dual-track L0-L7 architecture where domain semantics, governance, and execution evidence are structurally traceable.

### DS-C2: Deterministic Derivation Contribution

Given fixed concept graph and fixed derivation rules, test and metric obligations are deterministic and reproducible.

### DS-C3: Governance Attenuation Contribution

Governance fidelity attenuates as governance density rises unless structural interventions are applied.

### DS-C4: Meta-Circular Self-Governance Contribution

Governance is itself governed through signal, threshold, and tuning-loop contracts.

## Core Architecture and Ontology Definitions

### DS-D1: Meta-Type System

Let:

$$
\mathcal{M} = \mathcal{M}_B \cup \mathcal{M}_U
$$

Paper baseline profile (24 types):

$$
\mathcal{M}_B^{24} = \{Entity, ValueObject, Enum, Operation, Query, Calculation, Rule, Policy, Workflow, Interface, Event, Mapping, StateMachine\}
$$

$$
\mathcal{M}_U = \{Page, Layout, Component, ViewModel, Hook, Form, Action, Guard, Binding, Adapter, StateIndicator\}
$$

Composition extension profile (25 types):

$$
\mathcal{M}_B^{25} = \mathcal{M}_B^{24} \cup \{Saga\}
$$

Use paper/profile-specific counts explicitly when reporting experiment evidence.

### DS-D2: Typed Relationship System

Let:

$$
\mathcal{R} = \mathcal{R}_B \cup \mathcal{R}_U \cup \mathcal{R}_X
$$

Paper baseline profile (26 edges):

$$
\mathcal{R}_B^{12} = \{performs, produces, enforces, calculates, transitions, exposes, orchestrates, applies, maps, contains, queries, emits\}
$$

$$
\mathcal{R}_U^{8} = \{renders, wraps, composes, consumes, submits, shapes, protects, displays\}
$$

$$
\mathcal{R}_X^{6} = \{fetches, mutates, reflects, derives, contracts, mirrors\}
$$

Composition extension profile (29 edges):

$$
\mathcal{R}_{CF}^{3} = \{produces\text{-}for, triggers\text{-}cross, enforces\text{-}cross\}
$$

$$
\mathcal{R}^{29} = \mathcal{R}_B^{12} \cup \mathcal{R}_U^{8} \cup \mathcal{R}_X^{6} \cup \mathcal{R}_{CF}^{3}
$$

### DS-D3: Concept Graph

A feature-level concept graph is:

$$
G = (V, E, \tau, \lambda)
$$

where:

- $V$ is concept vertices
- $E \subseteq V \times V$ is directed edges
- $\tau: V \rightarrow \mathcal{M}$ is meta-type assignment
- $\lambda: E \rightarrow \mathcal{R}$ is edge-type assignment

### DS-D4: Derivation Function

Test obligations are:

$$
T = f(G, \Delta) = \bigcup_{i=1}^{|\Delta|} \delta_i(G)
$$

where $\Delta$ is the derivation-rule set.

### DS-D5: Layer Set and Dual-Track Projection

Layer universe:

$$
\mathcal{L} = \{L_0, L_1, L_2, L_3, L_4, L_5, L_6, L_7\}
$$

Business projection:

$$
\mathcal{L}_B = \{L_0, L_1, L_2, L_{3B}, L_{4B}, L_5, L_{6B}, L_{7B}\}
$$

Operational projection:

$$
\mathcal{L}_O = \{L_0, L_1, L_2, L_{3O}, L_{4O}, L_5, L_{6O}, L_{7O}\}
$$

Shared layers are $L_0$-$L_2$.

### DS-D6: Layer-7 Orchestration Contract

Let:

- $S = \{s_1, ..., s_9\}$ be business stages
- $H \subseteq S \times S$ be stage handoffs
- $\Sigma$ be emitted signals
- $\Theta$ be threshold predicates
- $\Pi$ be tuning proposals/actions

Then:

$$
L_{7B} = (S, H), \quad L_{7O} = (\Sigma, \Theta, \Pi)
$$

with coupling:

$$
s_9 \Rightarrow \Sigma \xrightarrow{\Theta} \Pi \xrightarrow{apply} updates(S,H)
$$

### DS-D7: Edge-Family Partition

Relationship families are disjoint:

$$
\mathcal{R} = \mathcal{R}_B \uplus \mathcal{R}_U \uplus \mathcal{R}_X
$$

and in composition-enabled analyses may extend to:

$$
\mathcal{R}^{+} = \mathcal{R} \uplus \mathcal{R}_{CF}
$$

### DS-D8: Edge-Signature Operator

Let:

$$
\sigma: \mathcal{R} \rightarrow \mathcal{P}(\mathcal{M}) \times \mathcal{P}(\mathcal{M})
$$

A typed edge instance $e=(u,r,v)$ is valid iff:

$$
\tau(u) \in \pi_1(\sigma(r)) \land \tau(v) \in \pi_2(\sigma(r))
$$

### DS-D9: Governance Attenuation Function

Let $\phi(k)$ be observed per-rule governance fidelity with $k$ active governance constraints. Attenuation is:

$$
A(k) = 1 - \phi(k)
$$

Critical regime is defined by:

$$
\frac{\partial \phi}{\partial k} < 0 \quad \text{for} \quad k > k^*
$$

### DS-D10: Coverage-Status Taxonomy

Concept mapping status (E6 style):

- `covered`
- `strained`
- `uncovered`

Edge modeling status (E9 style):

- `works`
- `strained`
- `broken`

Cross-experiment synthesis must preserve these vocabularies without relabeling.

## Structural Properties and Corollary

### DS-P1: Type Safety Property

All edge instances satisfy signature constraints.

### DS-P2: Backend/UI Partition Property

$\mathcal{M}_B \cap \mathcal{M}_U = \emptyset$ for the selected profile.

### DS-P3: Cross-Layer Direction Property

Edges in $\mathcal{R}_X$ are directed UI -> backend.

### DS-COR-1: Critical Layer Corollary

There exists a critical governance density $k^*$ such that adding constraints beyond $k^*$ reduces effective governance fidelity.

## Formal Constructs

### DS-F1: Governance Derivation Chain

$$
L4 \xrightarrow{justifies} L3 \xrightarrow{implemented\ by} L6
$$

### DS-F2: Deterministic Derivation Construct

$$
T = f(G, \Delta)
$$

### DS-F3: Test Cardinality Construct

$$
|T| = \sum_{i=1}^{20} |\delta_i(G)|
$$

### DS-F4: Observability Cardinality Construct

$$
|O| = \sum_{j=1}^{16} |o_j(G)|
$$

### DS-F5: Channel-Capacity Governance Model

$$
C = B \cdot \log_2\left(1 + \frac{S}{N}\right)
$$

### DS-F6: Closed-Loop Tuning Construct

$$
Pipeline \rightarrow Signals \rightarrow Thresholds \rightarrow Proposals \rightarrow Updates
$$

### DS-F7: Cross-Feature Composition Algebra

$$
G_{A \oplus B} = (V_A \cup V_B, E_A \cup E_B \cup E_{AB}, \tau_A \cup \tau_B, \lambda_A \cup \lambda_B \cup \lambda_{AB})
$$

## Method and Execution Definitions

### DS-M1: Tier Policy

Two analysis tiers are valid: `foundation` and `full`.

### DS-M2: Claim Evidence Vocabulary

Evidence strength and status values are constrained by claim/evidence contracts.

### DS-M3: Protocol Quality Gate

Protocols must pass checklist criteria before execution.

### DS-M4: Reproducibility Metadata Contract

Each run row must include canonical metadata fields.

### DS-M5: Validity Threat Quartet

Internal, external, construct, and conclusion threats are mandatory analysis dimensions.

### DS-M6: Signal Envelope Vocabulary

Signals must conform to schema-defined types and required envelope fields.

### DS-M7: Definition Anchor Requirement

Protocols must list definition IDs used as authority.

### DS-M8: Context Bundle Minimum Contract

Context bundles must include claim scope, source-role matrix, terminology map, metric map, conflict log, and follow-ups.

### DS-M9: Reference Authority Taxonomy

Authority levels and normalization states:

- levels: `primary`, `supporting`, `fallback`
- states: `operationalized`, `waived`, `pending normalization`

### DS-M10: Claim Acceptance and Disconfirmation Semantics

Claim updates require explicit acceptance-rule evaluation and explicit disconfirming criteria checks.

### DS-M11: Evidence Update Semantics

Upgrades and downgrades must cite concrete experimental evidence.

### DS-M12: Emission-Rate Definition

$$
EmissionRate = \frac{actual\_signal\_count}{expected\_signal\_count}
$$

## Usage Rules

1. Reference definitions by ID (`DS-*`) in protocols, claims, and evidence updates.
2. Use `DEFINITIONS-INDEX.md` for discovery, and this file for authoritative semantics.
3. If paper wording conflicts with this file, update paper or annotate drift; do not silently reinterpret definitions.
4. Any new gate-critical term must be added here before becoming normative in protocols.

---
module: body-war-login-suggest-track-score-preview
version: current
status: design-validator-pass
updatedAt: 2026-07-28
docType: ux-plan
---

# UX Plan: Runner Login to Score Preview

## Experience Goal

The runner should always know:

1. which track they are helping;
2. which activity they selected;
3. what data Body War will retain or discard;
4. whether the data is fixture or real Strava;
5. why the preview has its displayed value;
6. what the preview does not prove.

## Information Architecture

```text
Anonymous
└── Entrar com Strava

Connected
├── Perfil conectado
├── Pistas sugeridas
│   ├── Criar sugestao
│   └── Ajudar esta pista
├── Confirmar atividade
│   ├── Pista selecionada
│   ├── Atividade selecionada
│   ├── Dados retidos e descartados
│   └── Consentimento desmarcado
└── Pontuacao preliminar
    ├── Total
    ├── Ritmo
    ├── Distancia
    ├── Frequencia
    ├── Politica e modo de evidencia
    └── Limitacoes
```

## Critical Flow

| Step | Surface | Required behavior | Recovery |
| --- | --- | --- | --- |
| U1 | Login | One primary `Entrar com Strava` action; explain connection purpose. | retry after typed OAuth error |
| U2 | Suggested tracks | Track card exposes status and candidate-geometry ceiling. | create or choose another track |
| U3 | Help | Preserve exact selected track and announce it above activities. | explicit “trocar pista” |
| U4 | Activity | Show name, date, distance, time, pace; choose exactly one. | reload activity list |
| U5 | Consent | Unchecked by default; exact retained/discarded data; selected track/activity repeated. | no request until checked |
| U6 | Calculation progress | Show durable stages without claiming all-or-nothing failure. | resume with same request selector |
| U7 | Score preview | Total, components, policy, evidence mode, geometry status, limitations. | recalculate only if inputs/policy change |

## Required Copy Posture

Candidate Portuguese copy:

- title: `Pontuacao preliminar`;
- authority: `Esta pontuacao nao define controle da pista.`;
- geometry: `Geometria candidata criada a partir da atividade selecionada.`;
- fixture mode: `Dados de teste — nao sao uma atividade real do Strava.`;
- real mode: `Atividade consultada no Strava com seu consentimento.`;
- sparse history: `Frequencia baseada apenas nos dias disponiveis nesta versao.`;
- pending policy: `A regra numerica ainda precisa ser confirmada antes do calculo.`;
- retained: activity summary, exact consent record, private simplified geometry,
  score inputs/components/digests;
- discarded: provider tokens, raw provider payload, notes, photos, raw geometry
  streams.

Final copy must use project typography and avoid unaccented Portuguese where
the current static implementation can render UTF-8 safely.

## Accessibility and Responsive Contract

- all controls have programmatic labels and visible focus;
- the consent checkbox is not preselected;
- status and score do not rely on color alone;
- progress and errors use an `aria-live` region without repeated announcements;
- score components are a semantic list or table;
- the track and activity selected labels remain visible at 320px and 390px;
- primary action remains within the viewport and has at least a 44px touch
  target;
- the critical path remains operable in short landscape-height viewports;
- 200% text scaling and representative long track/activity/consent copy do not
  hide identity, consent, primary action, or result state;
- portrait and landscape orientations retain the same exact binding;
- keyboard order follows track, activity, consent, submit, result;
- reduced-motion preference disables non-essential transitions.

## State Copy Matrix

| State | Primary message | Forbidden implication |
| --- | --- | --- |
| `anonymous` | connect Strava | account already linked |
| `track_selected` | named selected track | first track chosen implicitly |
| `activity_selected` | named/date activity selected | activity already submitted |
| `geometry_pending` | preparing candidate route | official route validation |
| `geometry_unavailable` | selected activity lacks usable route data | activity invalid in Strava generally |
| `score_policy_unavailable` | numeric rule awaiting owner confirmation | zero score |
| `score_available` | preliminary score and components | verified control/conquest |
| `fixture` | test data | real Strava evidence |

## Browser Witnesses

1. Non-first track Help remains bound through confirmation and result.
2. Unchecked consent sends zero POST requests.
3. Displayed, affirmed, transmitted, and persisted consent identities match.
4. A delayed double-click creates one journey result.
5. Accepted mutation plus failed refresh recovers the result without duplicate.
6. Missing geometry preserves evidence and renders an actionable state.
7. Stale/missing policy renders no fabricated numeric zero.
8. 320px and 390px complete flow retains all critical controls.
9. Short-height landscape flow retains identity, consent, action, and result.
10. 200% text scaling and long representative content retain every critical
    control without overlap or clipping.
11. Portrait-to-landscape rotation preserves the selected track/activity and
    unchecked-or-affirmed consent state.

The current critical path has no text-entry control, so a software-keyboard
witness is not required unless a later design adds text input.

## Moderated Test Boundary

After the code/browser gate passes, run exactly three supervised
fake-provider formative sessions. Observe task completion, confusion around
confirmation, understanding of “candidate geometry,” understanding of the
score breakdown, and whether participants can state that the preview does not
grant control.

This yields formative UX evidence only. It does not validate the score's
fairness, real Strava fit, conversion, retention, or production readiness.

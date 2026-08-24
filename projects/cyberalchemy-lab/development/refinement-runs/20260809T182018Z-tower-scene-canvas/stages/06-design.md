# 06 — Invoke Design

## Architecture

```text
locked L0 fixture -> loadResearchTowerL0 -> buildTowerSceneManifest
                                      |              |
                                      |              +-> rejects missing source/state/ceiling/axis
                                      v
                             existing Explorer API
                                      |
                                      v
                        Tower Scene Canvas page
                        - overview + tower list
                        - level strip (native buttons)
                        - evidence scene + detail dock
                        - unavailable-system panel
                        - decoration / motion control (separate)
```

## UI contract

- Root: `data-workbench="tower-scene-canvas"`.
- Tower controls: `[data-list="towers"] [data-tower-id]`.
- Scene controls: `[data-list="tower-levels"] [data-level-id]`.
- Status: `[data-panel="tower-scene-status"]` with polite announcement only for real selection/refusal changes.
- Refusal: `[data-panel="scene-unavailable"]`.
- Orientation: explicit `focus-tower` and `reset-camera` buttons; the first version may implement focus as a CSS state, not pan/zoom physics.

## Accessibility and motion

Native button activation, visible focus, selected state, keyboard and touch parity, 44px target minimum, text-order alternate navigation, and responsive reflow are required. Reduced motion disables visual transitions and all decoration; semantic state is immediate. The motion toggle controls decoration only.

## Data boundary

`buildTowerSceneManifest` performs no external work and accepts only a verified read model. It does not add a real-tower selector. The L0/L1/L2 evidence axis and the L1/L2/L3/Lphi/L4 system axis remain separate values.

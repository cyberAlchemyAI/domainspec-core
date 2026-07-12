# Cross-Task Decisions

| Decision | Selection | Source |
| --- | --- | --- |
| OV1-PD1 | Operations surfaces have separate identity and immutable blob authority. | OV1-D1/D2 and accepted architecture. |
| OV1-PD2 | `parse5` 8.0.1 is pinned behind `HtmlTransformEngine`; golden bytes define behavior. | OVG-001. |
| OV1-PD3 | Fixed budgets are 5 MiB HTTP, 4 MiB source, 512 KiB fragment, and 8 MiB result. | OVG-002. |
| OV1-PD4 | Blob write precedes event append; event projection remains metadata-only. | OV1-D2/D3 and architecture. |
| OV1-PD5 | Operation lookup precedes CAS: same id/same digest returns original; same id/different digest conflicts; stale fails. | OV1-D6. |
| OV1-PD6 | Keep `/api/canvas/current` V0-compatible and add a separate display projection for workbench selection. | OV1-D1/D7 compatibility consequence. |
| OV1-PD7 | Redirect/display target is durable; refresh and browser acknowledgement are transient. | OVG-004. |
| OV1-PD8 | Retention defaults are 1 GiB soft, 2 GiB hard, seven-day grace, reclaim below soft. | OVG-003 plan constants. |
| OV1-PD9 | Automatic reclaim removes proven orphans before oldest eligible committed revisions. | OVG-003. |
| OV1-PD10 | Prune tombstone is durable before body deletion; current/shared referenced bodies are protected. | OVG-003. |
| OV1-PD11 | V1 target kind is only `whole_document`; regions remain schema-incompatible until separate design approval. | OV1-D4 and deferred L3. |
| OV1-PD12 | Operations and navigation are trusted-local preview/display effects, not skill execution or protected-effect authority. | OV1-D8. |

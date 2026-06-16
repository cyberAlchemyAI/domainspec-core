# TASK-TTP-006 - Data Appendix And Result Tables

Status: `pending`
Layer: L2

## Objective

Create `DATA-APPENDIX.md` with validation, benchmark, and artifact tables.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/DATA-APPENDIX.md`
- optional copied/symlinked data under `data/`

## Implementation Detail

Extract tables from:

- `TRITON-BENCHMARK-REPORT.md`
- W7 benchmark `benchmark.json`
- W6/W7 task-session evidence
- final technical report status table
- `formal/FORMAL-VALIDATION-REPORT.md`

Do not alter benchmark values.

## Smallest Working Units

| SWU ID | Goal | Done Criteria | Verification |
| --- | --- | --- | --- |
| SWU-TTP-006A | Extract benchmark and validation tables. | Tables match raw JSON and reports. | `jq empty .../benchmark.json` |

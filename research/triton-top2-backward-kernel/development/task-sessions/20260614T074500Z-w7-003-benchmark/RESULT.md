# Task Session Result - TASK-W7-003

Result: `pass-runpod`

## Summary

Added `scripts/benchmark_triton_paths.py`, ran it on RunPod, copied benchmark
artifacts back into this task-session folder, and wrote
`TRITON-BENCHMARK-REPORT.md`.

## Validation

```sh
.venv/bin/python -m py_compile scripts/benchmark_triton_paths.py
.venv/bin/python -m pytest tests -q
POD_HOST=213.173.102.17 POD_PORT=43736 scripts/runpod_cuda_iteration.sh
ssh -p 43736 root@213.173.102.17 "cd /workspace/triton-top2-backward-kernel && /usr/local/bin/python scripts/benchmark_triton_paths.py --warmup 10 --iters 50 --json-out development/benchmarks/20260614T074500Z/benchmark.json --markdown-out development/benchmarks/20260614T074500Z/BENCHMARK.md"
```

Results:

- local suite: `54 passed, 14 skipped`;
- RunPod validation: focused Triton `15 passed`, full suite `68 passed`;
- benchmark artifacts copied to `artifacts/`.

## Benchmark Summary

| Size | Fixed Mask Median ms | CAP2 Median ms |
| --- | ---: | ---: |
| small | 0.1350 | 0.1739 |
| medium | 0.1378 | 0.1673 |

## Follow-Up

Next ready task: `TASK-W8-001`, final prior-art and novelty report.


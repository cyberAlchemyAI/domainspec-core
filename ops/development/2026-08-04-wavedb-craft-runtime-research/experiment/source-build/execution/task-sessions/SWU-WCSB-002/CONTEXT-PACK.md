# Context Pack: SWU-WCSB-002

- Mode: fresh Task Session, local Codex runtime.
- Work Pack: `plan/WORK-PACK.md`.
- Selected unit: `SWU-WCSB-002` / `TASK-WCSB-02`.
- Dependency: SWU-WCSB-001 terminal and Invoke Refresh owner receipts pass.
- Objective: execute one exact reviewed-source WaveDB build attempt and bind
  one loadable, upstream-tested addon to live evidence.
- Source: `https://github.com/vijayee/WaveDB.git`, commit
  `01c77e8b70f71de9b72480e73a3a179f6e93a009`.
- Attempt: `wcsb-20260804-01`; both attempt and evidence directories are
  absent and cannot be reused or cleaned.
- Dependencies: admitted lockfile SHA-256 only, installed with lifecycle
  scripts disabled.
- Toolchain: Node 22.12.0, npm 10.9.0, Python 3.12.3, GCC/G++ 13.3.0,
  Make 4.3, binutils 2.42, OpenSSL enabled at `/usr`.
- Outputs: the attempt directory, the source-build evidence directory, and the
  terminal Task Session receipt.
- Forbidden: alternate source/lock/toolchain, source repair, Craft access,
  workspace Git mutation, package publication, deployment, credentials, or
  destructive cleanup.
- Closeout owner: `invoke:refresh:apply-approved`, bookkeeping-only over the
  declared Work Pack, TASK-WCSB-02, and W0 targets.
- Claim ceiling: one local Linux x86_64 reviewed-source build observation.

All source, dependency, generated-source, build, load, test, canary, evidence,
and scope checks are acceptance-critical. There is no fallback attempt.


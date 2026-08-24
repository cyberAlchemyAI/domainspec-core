# Task Session Context Pack: SWU-WCP-001

## Selection

- Work Pack: `../../../plan/WORK-PACK.md`
- Work Pack digest: `36c994207a5bb2674bd3344b86cd574be0582075ea84b48fba9dbdf7b87a2adb`
- Task: `TASK-WCP-01`
- SWU: `SWU-WCP-001`
- Selection: explicit from Work Pack; exactly one selected unit
- Runtime: local, standalone non-mutating package audit
- Strict coverage: pass

## Objective

Decide whether `@vijayee/wavedb@0.15.8` has one exact, non-contradictory
registry-artifact/source correspondence. Stop before dependency resolution,
install scripts, native compile, or addon load on any mismatch.

## Controlling sources

| Source | SHA-256 | Control |
| --- | --- | --- |
| `../../../plan/WORK-PACK.md` | `36c994207a5bb2674bd3344b86cd574be0582075ea84b48fba9dbdf7b87a2adb` | selected unit, write scope, closeout |
| `../../../plan/work-pack/tasks/TASK-WCP-01-INPUT-CLOSURE.md` | `fba1f1d46e56755151f35660e3bdc2f918c7a8331d4515907b8051821084906c` | unit algorithm and acceptance |
| `../../../design/ARCHITECTURE.md` | `77421e9b8fc128dedec300783cae1b452a96f55e8c34615d956212c60ffd4d3f` | provenance architecture |
| `../../../design/DESIGN-SELECTION-RESULT.json` | `23922ffb2f5e448b29e72f5d35343ef2f10ebf413282a3f8d9367c345cc7b4b1` | design-validator-pass |
| `../../../../findings.md` | `958ed1ae74cfad7483a70f6ca7a78ba5a970a97e928da4d88e40979f680b53f0` | WP-0 stop rule and claim ceiling |

## Exact execution contract

- Inputs: npm registry metadata, exact tarball, SRI/SHA-1, declared gitHead
  `54832130f408c44637ad84f35cb93003b0f238c4`, reviewed source commit
  `01c77e8b70f71de9b72480e73a3a179f6e93a009`, local environment identities.
- Writes: `experiment/execution/wp0-provenance/**` and this session directory.
- Material writes: none.
- Execution outputs: metadata/comparison evidence, terminal receipt,
  continuation handoff, closeout receipt/cursor.
- Forbidden: `node_modules`, `.node` binaries, native build output, install
  scripts, package lock changes, Craft writes, Git, cleanup outside the exact
  temporary audit directory.
- Done: exact integrity and version/source comparison; stable verdict; proof no
  install/build/addon artifacts were created; one successor only if pass.
- Validation: tarball hashes, registry metadata, both source package versions,
  source comparison boundary, experiment-path artifact scan.

## Gate classification

The source/package contradiction is missing/contradictory evidence with no
safe automatic choice. Decision Gate is not invoked because zero currently
admissible native-execution options exist. The legal outcome is a terminal
Task Session BLOCK plus a package/security owner route.

## Closeout

Current Work Pack already names the blocker and expected stop. Closeout may be
receipt-backed no-op for the Work Pack if its bytes already represent the
terminal result; session evidence and the chain state remain separately owned.

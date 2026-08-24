# Execution Pack

## Route

```text
Invoke Plan
  -> task-session-until-blocker
    -> fresh Task Session: SWU-BWCN-001
    -> fresh Task Session: SWU-BWCN-002
    -> fresh Task Session: SWU-BWCN-003
    -> stop at completed frontier or first blocker
```

## Admission protocol

Every mutation-capable SWU must have, immediately before writing:

- one exact task contract;
- one exact work-pack control snapshot;
- one strict-coverage JSON context pack;
- one materialized Invoke package;
- one passing producer receipt;
- one current Task Session mutation-admission receipt; and
- one closeout preflight.

Material writes and execution outputs are disjoint. Generated outputs owned by
the material package are material writes; receipts and screenshots produced by
running admitted code are execution outputs.

## Validation order

1. validate the current material package;
2. verify current mutation admission;
3. apply only admitted writes;
4. run SWU-specific deterministic validation;
5. compare ontology semantic input digests;
6. write the Task Session execution receipt;
7. perform Invoke Refresh closeout synchronization;
8. admit the unique successor.

## Stop conditions

- any digest mismatch;
- stale or rejected material package;
- unexpected write;
- deterministic test failure;
- browser runtime cannot be pinned;
- browser assertion failure;
- closeout synchronization failure; or
- no unique ready successor.


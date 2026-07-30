# Staged Material Validation

- Target inventory: pass; 10 unique normalized paths, 6 updates, 4 creates.
- Terminal receipt schema JSON parse: pass.
- Command matrix JSON parse: pass.
- Command matrix coverage: pass; 29/29 units have exact argv contracts.
- Attempt coverage: pass; five attempt-producing units have deterministic ID,
  collision, retention, success teardown, and failure teardown contracts.
- Shared-write ownership: pass; four exact overlap contracts.
- Semantic validator Python compile: pass.
- Receipt adversarial suite: pass; 8/8.
- Staged whitespace checks: pass.
- Target UI/ontology execution: not run.
- Selected SWU: none.

Commands executed:

```bash
python3 -m json.tool <staged>/TASK-SESSION-RECEIPT.schema.json
python3 -m json.tool <staged>/work-pack/shared/COMMAND-MATRIX.json
python3 -m py_compile <staged>/work-pack/shared/validate-task-session-receipt.py
python3 <staged>/work-pack/shared/test-task-session-receipt.py
git diff --no-index --check /dev/null <each-staged-target>
```

This validates staged plan material only. The post-apply canonical readiness
audit remains required.

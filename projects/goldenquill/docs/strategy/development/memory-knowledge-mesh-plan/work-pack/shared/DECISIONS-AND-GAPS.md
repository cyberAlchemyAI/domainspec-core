# Decisions And Gaps

## Decisions

1. Start with a layer index, not a runtime rewrite.
2. Treat memory and knowledge as multiple authority classes, not one store.
3. Keep org contexts out of this task because no org was named.
4. Stop before code/test parity work if the test runner is unavailable.

## Gaps

1. No `docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md` existed before this work.
2. Runtime memory CLI reports 15 registers, while some docs/docstrings still mention 13.
3. Reflection Packet has blueprint/policy presence but is dormant as a runtime consumer.
4. `logfire` is not installed in this shell, so memory CLI observability is degraded but not failed.
5. `pytest` is not available through system Python and no usable project `.venv` was found in the prior validation pass.


"""Logician — deterministic Python + Cedar policy gates (fail-closed, zero-token).

Per architecture v7 LOCKED 2026-04-19 §A: Logician is the sixth seat — the only
seat without an LLM. Its predicates are deterministic Python + Cedar policy
gates that enforce the Five Operating Laws + Four Autonomy Rules as PRE/POST
gates around every other seat's invocation.

Gate-family modules live at `logician.gates.*`. Test suite at `logician.tests.*`.
"""

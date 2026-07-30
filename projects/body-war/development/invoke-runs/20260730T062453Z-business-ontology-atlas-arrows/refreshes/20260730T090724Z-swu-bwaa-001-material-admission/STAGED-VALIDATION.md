# Staged Validation — SWU-BWAA-001

- Isolation: current `projects/body-war/ontology/business/` copied to a fresh
  `/tmp` overlay; only the three staged outputs replaced their live preimages.
- Live target mutation: none.
- Projection tests: `8 passed`, `0 failed`.
- Coverage validator: pass.
- Coverage: 237 nodes, 231 relations, 122 internal relations, 109 portal
  relations, 13 directed lens flows carrying 109 relation IDs, 44 zero-degree
  nodes.
- Coverage receipt JSON: parsed.
- Staged whitespace: pass through three scoped `git diff --no-index --check`
  comparisons.
- Current semantic locks: unchanged from the Work Pack.

The staged result proves only the exact material bytes proposed for
`SWU-BWAA-001`. Task Session must still verify the live preimages, apply the
material, run the exact commands against live bytes, and emit its terminal
receipt.

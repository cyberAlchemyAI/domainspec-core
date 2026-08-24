# Verbatim Repair Revalidation Return Manifest

The two native agent returns are preserved as literal receipt artifacts rather
than copied into this file, so one canonical byte sequence backs each lane.

| Lane | Pooled identity | Verbatim return | SHA-256 |
| --- | --- | --- | --- |
| Proposer | Abramsky, Samson | [`receipts/PROPOSER.md`](receipts/PROPOSER.md) | `f8a3672ea8c1c69d634e13e2a09a1915a17561f0d107fbff3fdf694e7d4d7f64` |
| Balancer | Ashby, W. Ross | [`receipts/BALANCER.md`](receipts/BALANCER.md) | `228017fc83c1ee36851776d4a297e23fc1a6ffe18ae49f4701bedabb0e3dc529` |

Both returns bind:

- dispatch `2026-07-30-arcanum-addon-repair-revalidation`;
- run `arcanum-addon-repair-revalidation-a850483e`;
- source commit `80dcd79677ad73b21dbaded12e0e9cd47aace82b`;
- repaired corpus digest
  `5b5e79f5632b2e29e7a20e7ac4d9e92addef6f707e9525c71e7266c24349e4b0`;
- all 75 current files under `define/`, `design/`, and `plan/`; and
- read-only review scope.

The Proposer returned `validation: pass`. The Balancer returned
`validation: block` after finding a machine-route counter-example. Neither
return authorizes mutation.

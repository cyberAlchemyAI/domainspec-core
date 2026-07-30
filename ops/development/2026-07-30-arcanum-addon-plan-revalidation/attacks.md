# Verbatim Revalidation Return Manifest

The two native agent returns are preserved as literal receipt artifacts rather
than copied into this file, so one canonical byte sequence backs each lane.

| Lane | Pooled identity | Verbatim return | SHA-256 |
| --- | --- | --- | --- |
| Proposer | Artin, Emil | [`receipts/PROPOSER.md`](receipts/PROPOSER.md) | `8c9e750facd8713287eda23eabd463d4e4efa25ea8aaee9818bca24dcfbbc7e0` |
| Balancer | Capucci, Matteo | [`receipts/BALANCER.md`](receipts/BALANCER.md) | `e497ac0fee1bb141065ea2595c2587af7a82a7e9f1e712daf8eda105e2523a35` |

Both returns bind:

- dispatch `2026-07-30-arcanum-addon-plan-revalidation`;
- run `arcanum-addon-plan-revalidation-cc655251`;
- source commit `80dcd79677ad73b21dbaded12e0e9cd47aace82b`;
- corpus digest
  `bb0a6f31cf1142902693d30c53ecc2ee08b6747e14ea12f7dff5b81d08d64b14`;
- read-only review scope.

Neither return authorizes mutation. Both returned `validation: block`.

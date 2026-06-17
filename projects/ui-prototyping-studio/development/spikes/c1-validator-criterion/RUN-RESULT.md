# C-1 Validator Spike — RUN-RESULT
Criterion: `criterion.md` (FROZEN)
Canonicalizer: domainspec-html-canon v1.4.0 (sha256:c1a9f0e2b7)
TaskScope: {cta.primary, card.hint}
Out-of-scope: {card.title, card.footer}
fixtures.lock: `fixtures.lock`

## Per-fixture results

```
id       | category | expect      | v3          | match
-------------------------------------------------------
GOOD-1   | GOOD     | NOT_REJECT  | NOT_REJECT  | OK
GOOD-2   | GOOD     | NOT_REJECT  | NOT_REJECT  | OK
GOOD-3   | GOOD     | NOT_REJECT  | NOT_REJECT  | OK
BAD-1    | BAD      | REJECT      | REJECT      | OK
BAD-2    | BAD      | REJECT      | REJECT      | OK
BAD-3    | BAD      | REJECT      | REJECT      | OK
HELD-4   | HELD     | REJECT      | REJECT      | OK
HELD-5   | HELD     | NOT_REJECT  | NOT_REJECT  | OK
HELD-6   | HELD     | NOT_REJECT  | NOT_REJECT  | OK
HELD-7   | HELD     | NOT_REJECT  | NOT_REJECT  | OK
HELD-8   | HELD     | REJECT      | REJECT      | OK
```

## Verdict: **SURVIVED**

V3 matched every fixture on the closed set (incl. held-out). Generalization beyond this set is NOT established by this spike.

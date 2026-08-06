# States

The resolver is stateless. The lifecycle below describes admission evidence,
not a new runtime selection lifecycle.

```text
candidate-authored -> candidate-witnessed -> canonical-accepted
  -> generated-parity-passed -> consumer-admitted
```

Each arrow requires its named owner receipt. Failure or drift returns to
`candidate-authored`; no state grants execution authority.


# Validation-Driven Aggregate Report Repair

The first Experiment Harness profile validation returned `flag` because the
latest aggregate Invoke report omitted the already-canonical `invoke-live`
profile ID and `invoke` lifecycle owner.

The repair added exactly those two metadata rows to the report writer in the
already-admitted aggregate runner. The aggregate suite and Experiment Harness
profile validation were rerun and both passed. No selection behavior,
generated runtime surface, or lifecycle authority changed.

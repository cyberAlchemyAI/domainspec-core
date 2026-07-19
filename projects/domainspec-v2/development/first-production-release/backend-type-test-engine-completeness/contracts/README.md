# Candidate Backend Structural Verification Contract

This folder is a planning target for `SWU-BTE-005`, `SWU-BTE-009`, and
`SWU-BTE-010`. It is not current definition, profile, ledger, or release authority.

The planned catalogue must record:

- the selected profile ID/version/digest;
- the successor profile `feature-with-independent-node-and-edge-files@1` and
  its candidate posture;
- the exact 13 admitted backend kinds;
- the exact 16 admitted backend relationship signatures;
- one exact schema path and digest per kind;
- one shared edge schema, same-feature edge root, project-level cross-feature edge
  root, and resolver scope rules;
- one stable obligation ID per current criterion entry;
- criterion rule, expected source representation, and source anchor;
- expected positive and mutation fixture IDs;
- execution and mutation evidence requirements;
- causal node-to-pattern and edge-to-composition/removal requirements;
- IOLM and Body War consumer receipt identities, projection/redaction posture, and
  the integrated manifest binding;
- owner approval record and explicit `release_admission: not-granted`.

The catalogue is the independent `O_spec` denominator. Engine output may consume or compare against it, but engine output may not silently rewrite it. The exact comparator is `O_spec = O_gen = T_gen = E_run`; a consumer receipt never defines `O_spec` or grants profile/release authority.

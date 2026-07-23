# Cross-task Decisions

| ID | Decision | Consequence |
| --- | --- | --- |
| CTD-01 | Separate `validate-whisper-run-receipt.py` from `validate-whisper-draft.py`. | Existing document checks keep their conservative scope. |
| CTD-02 | Use exact SHA-256 digest binding for approval/comprehension/post-apply records. | Evidence cannot transfer across revisions without re-audition. |
| CTD-03 | Compute generation decision and final status separately. | A candidate trial may be generated but cannot claim pass. |
| CTD-04 | First surface is role-complete source order unless render evidence explicitly proves viewport membership. | Source review stays useful without browser overclaim. |
| CTD-05 | Local presets live under `.arcanum/spells/whisper/presets/`. | Generated runtime no longer carries host-private prose. |
| CTD-06 | Full validation ends in a Spellcraft receipt, not automatic promotion. | Human/lifecycle authority remains explicit. |

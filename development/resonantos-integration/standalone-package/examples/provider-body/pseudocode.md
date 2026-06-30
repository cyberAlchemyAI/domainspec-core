# Provider Body Pseudocode

```text
function promote_review_artifact_body(review_artifact, decision_receipt):
  require decision_receipt.action == "approve"
  require review_artifact.scope_tag in allowed_scope_tags
  require review_artifact.source_refs not empty
  require review_artifact.promotion_owner is authorized for target
  require review_artifact.validation.status == "pass"

  trusted_write_result = host.trusted_memory.write(review_artifact.target, review_artifact.payload)
  return audit_receipt(trusted_write_result, decision_receipt, review_artifact)
```

This body belongs behind the host-mediated trusted-write boundary.

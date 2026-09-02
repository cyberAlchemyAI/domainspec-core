# DomainSpec CLI candidate

Local-only AlchLang parser, compiler and guarded action runtime.

```bash
domainspec build customer-approval.md --out generated
domainspec run customer-approval.md ReleaseCredit \
  --actor CreditOperator \
  --facts '{"customerId":"c-1","riskScore":600,"status":"approved","amount":100}' \
  --grant credit-release-authority
```

Discover operation patterns before requesting generation:

```bash
domainspec patterns
domainspec patterns --available
domainspec patterns --blocked
domainspec pattern operation-port
```

Availability is derived from the registered meta-type, integration binding,
generator and conformance prerequisites. Blocked patterns remain visible but
`domainspec pattern <id>` fails closed for them. Pattern registration does not
make an architecture pattern stable; stability remains owner-controlled.

The CLI does not connect to external services. Programmatic consumers may inject
memory, SQLite or allowlisted HTTP adapters. Every action requires explicit
rules, permission, authority grant and adapter binding.

# Interfaces: Capital Logic Library

## CapitalLogicLibraryModule

The internal module contract through which downstream Tilth components (the
classification chain, Logician deterministic gates) consume the library. Read + validate
only; no `orgs/` data crosses this boundary (Law 3).

**Exposes:** [ValidateCard](operations.md#validatecard), [GetCardDefaults](queries.md#getcarddefaults)

| Method                         | Signature                                              | Maps To                                          |
| ------------------------------ | ------------------------------------------------------ | ------------------------------------------------ |
| validateCard                   | `(card, family) -> ValidationResult`                   | [ValidateCard](operations.md#validatecard)       |
| getCardDefaults                | `(cic_id) -> CardDefaults`                             | [GetCardDefaults](queries.md#getcarddefaults)    |
| validateRulePack               | `(pack) -> ValidationResult`                           | [ValidateRulePack](operations.md#validaterulepack) |
| registerRulePack               | `(pack, now) -> RegistrationResult`                    | [RegisterRulePack](operations.md#registerrulepack) |

### Contract Notes

- Validation methods are fail-closed: any anti-coupling, closed-set, or provenance
  violation rejects rather than degrades.
- The module never resolves canonical naming itself — `CLAUDE.md` is the owner-boundary
  source of truth for the closed sets; the module conforms to it.

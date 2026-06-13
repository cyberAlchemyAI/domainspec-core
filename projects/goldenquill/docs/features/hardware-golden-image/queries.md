# Queries: Hardware & Golden Image

Read models over per-unit receipts and reference specs. No side effects.

## GetUnitReceipt

Returns the per-unit [VerificationReceipt](domain.md#verificationreceipt) for a given unit serial.

### Reads From

- [VerificationReceipt](domain.md#verificationreceipt)

### Input

| Field      | Type   | Required | Description        |
| ---------- | ------ | -------- | ------------------ |
| unit_serial | string | yes      | Unit to look up    |

### Output

| Field      | Source                                                       |
| ---------- | ------------------------------------------------------------ |
| receipt    | [VerificationReceipt](domain.md#verificationreceipt) (full record) |

### Authorization

Operator / Field Tech. Reads only appliance-local receipts; no `orgs/` access (Law 3).

---

## GetReferenceSpec

Returns the [ReferenceWorkstationSpec](domain.md#referenceworkstationspec) and its [SpecStatus](domain.md#specstatus) for a SKU — the one source of truth for "what counts as a Golden Quill unit."

### Reads From

- [ReferenceWorkstationSpec](domain.md#referenceworkstationspec)

### Input

| Field    | Type   | Required | Description     |
| -------- | ------ | -------- | --------------- |
| sku_name | string | yes      | SKU to look up  |

### Output

| Field   | Source                                                          |
| ------- | --------------------------------------------------------------- |
| spec    | [ReferenceWorkstationSpec](domain.md#referenceworkstationspec)  |
| status  | [SpecStatus](domain.md#specstatus)                              |

### Authorization

Operator. Feeds the burn-in threshold table and procurement.

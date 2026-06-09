# Inventory Interface Indexing Fixtures

These fixtures support `TASK-BW-INV-004`.

The validator reads the positive examples from `../templates/*.example.json`
and reads negative fixtures from `invalid/`. Negative fixtures are intentionally
small because they prove specific failure classes without duplicating the whole
template package.

Required negative classes:

- bad source reference,
- unknown link edge,
- missing required gap.

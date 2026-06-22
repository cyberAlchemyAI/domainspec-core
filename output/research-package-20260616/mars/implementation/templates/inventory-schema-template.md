# Inventory Schema

Purpose: define the local inventory chain for a project.

## Required Chain

1. `sources/SOURCE-CATALOG.md`
2. `sources/REFERENCE-LEDGER.md`
3. `inventory/INVENTORY-INDEX.md`
4. `inventory/library/<source-id>.md`
5. `inventory/raw/<source-id>/...`

## Directory Layout

| Path                                      | Role                                                |
| ----------------------------------------- | --------------------------------------------------- |
| `inventory/INVENTORY-INDEX.md`            | lookup and coverage view                            |
| `inventory/INVENTORY-SCHEMA.md`           | local inventory contract                            |
| `inventory/library/<source-id>.md`        | per-source extracted knowledge                      |
| `inventory/raw/<source-id>/...`           | raw retrieved or user-provided provenance artifacts |
| `inventory/*-rollup.md` or thematic files | secondary synthesized views                         |

## Rules

1. The per-source library file is the content authority for extracted knowledge.
2. The raw directory is the provenance base for that extracted knowledge.
3. The inventory index must show library and raw coverage status for each source.
4. If web retrieval is not possible, request user-provided raw files and record that dependency explicitly.

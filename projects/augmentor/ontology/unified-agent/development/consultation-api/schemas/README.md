# Consultation contract families

This directory contains the original `0.1.0` fixture contracts used by the
candidate-local L0 harness. They are not accepted by the live ResonantOS
consultation route.

The neutral producer output and the ResonantOS consumer use the exact-match
`1.0.0` live family recorded in `contract-families.json`. There is no implicit
compatibility between the fixture and live families. A future extension must
declare a new live identity and update producer, consumer, fixtures, and drift
tests together.

The fixture schemas remain here until the rich contract unit introduces its
closed live schemas. Their location does not grant runtime authority.

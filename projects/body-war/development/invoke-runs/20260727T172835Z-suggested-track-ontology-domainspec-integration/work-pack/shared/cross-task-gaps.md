# Cross-Task Gaps

| Gap | Affects | Owner | Handling |
| --- | --- | --- | --- |
| GAP-BWOI-001 generic consumer runner | DomainSpec and integration | DomainSpec engine owner | import generic APIs; block before copying FS runner |
| GAP-BWOI-002 no promoted Body War ontology | integration/formal lane | Body War ontology owner | candidate experimental lane; promoted-required negative fixture |
| GAP-BWOI-003 bounded profile kinds | DomainSpec graph | DomainSpec profile owner | use only Rule, Operation, Event and admitted edges |

These gaps do not block SWU-BWOI-001. Any execution discovery that invalidates
an acceptance criterion blocks that SWU and routes through Refresh or a new
Plan; it is not silently repaired across scopes.


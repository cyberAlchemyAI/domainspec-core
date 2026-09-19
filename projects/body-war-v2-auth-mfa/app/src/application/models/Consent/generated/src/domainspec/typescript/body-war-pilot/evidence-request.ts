// domainspec-meta: {"baseline_digest":"bfbc335d151ab8b29150dc95f246c2bc0954cff179ece5ce51222b2d1455abda","baseline_id":"domainspec-meta-types-current-implemented@10","binding_sha256":"4c5b4d8f9e6febb255117a7a3e207b30dc369bfe61d8dc1933d792a7bbadb6e8","language":"typescript","meta_type_id":"DS-D1.1","meta_type_label":"Entity","provider_sha256":"b53128e807f734043019e75e6b892900b83c320b909d859644f6a820a9c960f1","source_sha256":"c174f82e19e72b30f9305f005809bf8a63b52d102e708a9739a3d898b704b197"}
// domainspec-body: {"description":"A synthetic or consenting runner request to attach candidate activity evidence, never verified geometry or score.","fields":["request_id","consent_acknowledged","activity_present","consent_text_present"],"identity_field":"","typed_contract":{"ontology_node":"BW2-EVIDENCE-REQUEST","properties":[{"cardinality":"one","identity":true,"meaning":"The candidate request identity.","name":"request_id","ontology_property":"BW2-EVIDENCE-REQUEST#requestId","type":{"kind":"scalar","name":"String"}},{"cardinality":"one","identity":false,"meaning":"Whether the caller explicitly supplied boolean true.","name":"consent_acknowledged","ontology_property":"BW2-EVIDENCE-REQUEST#consentAcknowledged","type":{"kind":"scalar","name":"Bool"}},{"cardinality":"one","identity":false,"meaning":"Whether the activity identifier passed the HTTP string adapter.","name":"activity_present","ontology_property":"BW2-EVIDENCE-REQUEST#activityPresent","type":{"kind":"scalar","name":"Bool"}},{"cardinality":"one","identity":false,"meaning":"Whether the consent explanation passed the HTTP string adapter.","name":"consent_text_present","ontology_property":"BW2-EVIDENCE-REQUEST#consentTextPresent","type":{"kind":"scalar","name":"Bool"}}],"schema_version":"domainspec.typed-record/v1"}}
// domainspec-relationships: []
// domainspec-record-semantics: "domainspec.typed-record/v1"
// domainspec-ontology-node: "BW2-EVIDENCE-REQUEST"
type DomainspecRef<Selector extends string> = string & { readonly __domainspecRef: Selector };
export interface EvidenceRequestFields {
  readonly request_id: string;
  readonly consent_acknowledged: boolean;
  readonly activity_present: boolean;
  readonly consent_text_present: boolean;
}
export class EvidenceRequest {
  constructor(private readonly fields: Readonly<EvidenceRequestFields>) { this.fields = Object.freeze({ ...fields }); }
  sameIdentity(other: EvidenceRequest): boolean { return Object.is(this.fields.request_id, other.fields.request_id); }
  snapshot(): Readonly<EvidenceRequestFields> { return this.fields; }
}

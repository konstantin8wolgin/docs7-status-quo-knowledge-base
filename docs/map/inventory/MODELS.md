# Model inventory

Generated; do not edit by hand.

| ID | Table | Foreign keys | Relationships | Tests |
| --- | --- | --- | --- | --- |
| model:AuditEvent | audit_events | 4 | 0 | 10 |
| model:AuditRun | audit_runs | 2 | 0 | 4 |
| model:AuthSession | sessions | 1 | 0 | 2 |
| model:AuthToken | auth_tokens | 1 | 0 | 2 |
| model:ChatRun | chat_runs | 4 | 0 | 2 |
| model:Document | documents | 3 | 2 | 22 |
| model:DocumentAmount | document_amounts | 1 | 0 | 2 |
| model:DocumentDate | document_dates | 1 | 0 | 2 |
| model:DocumentEntity | document_entities | 3 | 0 | 10 |
| model:DocumentTag | document_tags | 1 | 0 | 1 |
| model:DocumentTrustFlag | document_trust_flags | 1 | 0 | 1 |
| model:Entity | entities | 3 | 1 | 11 |
| model:EntityConstraint | entity_constraints | 3 | 0 | 6 |
| model:EntityEvent | entity_events | 3 | 0 | 5 |
| model:EntityIdentifier | entity_identifiers | 2 | 0 | 10 |
| model:EntityMention | entity_mentions | 4 | 0 | 10 |
| model:ExtractedFieldEvidence | extracted_field_evidence | 3 | 0 | 1 |
| model:ExtractionRun | extraction_runs | 2 | 0 | 7 |
| model:Fact | facts | 3 | 1 | 14 |
| model:FactCandidate | fact_candidates | 4 | 0 | 5 |
| model:FactProvenance | fact_provenance | 5 | 0 | 4 |
| model:FactRevision | fact_revisions | 3 | 0 | 4 |
| model:FileObject | file_objects | 2 | 0 | 7 |
| model:Message | messages | 2 | 0 | 1 |
| model:OcrEvidence | ocr_evidence | 2 | 0 | 3 |
| model:Person | persons | 1 | 0 | 11 |
| model:ProcessingJob | processing_jobs | 4 | 0 | 8 |
| model:ReviewItem | review_items | 3 | 0 | 9 |
| model:User | users | 0 | 0 | 26 |
| model:Vault | vaults | 1 | 0 | 15 |
| model:VaultKey | vault_keys | 1 | 0 | 1 |
| model:VaultMember | vault_members | 3 | 0 | 3 |

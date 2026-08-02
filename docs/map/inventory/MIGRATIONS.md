# Migration inventory

Generated; do not edit by hand.

| ID | Parent | Tables | File |
| --- | --- | --- | --- |
| migration:0001 | root | audit_events, document_amounts, document_dates, document_tags, document_trust_flags, documents, extracted_field_evidence, extraction_runs, fact_candidates, fact_provenance, fact_revisions, facts, file_objects, messages, ocr_evidence, persons, processing_jobs, users, vault_members, vaults | backend/alembic/versions/0001_baseline.py |
| migration:0002 | 0001 | auth_tokens, sessions, users | backend/alembic/versions/0002_auth.py |
| migration:0003 | 0002 | processing_jobs | backend/alembic/versions/0003_job_queue.py |
| migration:0004 | 0003 | file_objects, vault_keys | backend/alembic/versions/0004_encryption.py |
| migration:0005 | 0004 | ocr_evidence | backend/alembic/versions/0005_fts_search.py |
| migration:0006 | 0005 | document_entities, entities, entity_constraints, entity_events, entity_identifiers, entity_mentions, fact_candidates, facts, persons, review_items | backend/alembic/versions/0006_entities.py |
| migration:0007 | 0006 | entity_constraints | backend/alembic/versions/0007_constraint_pair_unique.py |
| migration:0008 | 0007 | audit_events, documents | backend/alembic/versions/0008_user_context.py |
| migration:0009 | 0008 | chat_runs, messages | backend/alembic/versions/0009_answer_ladder.py |
| migration:0010 | 0009 | audit_runs, entities, review_items | backend/alembic/versions/0010_auditor_integrity.py |
| migration:0011 | 0010 | chat_runs | backend/alembic/versions/0011_chat_run_jsonb.py |

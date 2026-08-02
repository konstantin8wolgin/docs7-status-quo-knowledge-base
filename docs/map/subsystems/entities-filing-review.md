---
id: subsystem:entities-filing-review
kind: subsystem
summary: Entity register and durable constraints preserve uncertain evidence as explicitly reviewable through merge and recovery.
read_when: ["entities filing review", "entity merge unlink", "manual cards review inbox", "durable entity constraint schema migration"]
sources: ["file:backend/app/models.py", "file:backend/alembic/versions/0010_auditor_integrity.py", "file:backend/alembic/versions/0011_chat_run_jsonb.py", "file:backend/app/queue.py", "file:backend/app/domain/jobs.py", "file:backend/app/domain/filing.py", "file:backend/app/domain/review.py", "file:backend/app/domain/review_identity.py", "file:backend/app/domain/audit.py", "file:backend/app/routers/entities.py", "file:backend/app/routers/review.py", "file:client/src/api.js", "file:client/src/views/Entities.jsx", "file:client/src/components/ReviewInbox.jsx", "file:client/src/components/EntityCardDetail.jsx"]
inventory_refs: ["route:GET:/api/entities", "route:GET:/api/entities/{entity_id}", "route:GET:/api/review-items", "route:POST:/api/entities", "route:POST:/api/entities/merge", "route:POST:/api/entities/{entity_id}/confirm", "route:POST:/api/entities/{entity_id}/facts", "route:POST:/api/entities/{entity_id}/unlink", "route:POST:/api/entities/{entity_id}/unmerge", "route:POST:/api/review-items/{item_id}/resolve", "model:DocumentEntity", "model:Entity", "model:EntityConstraint", "model:EntityEvent", "model:EntityIdentifier", "model:EntityMention", "model:ReviewItem", "migration:0006", "migration:0007", "migration:0010", "migration:0011", "clientapi:confirmEntity", "clientapi:createEntity", "clientapi:createEntityFact", "clientapi:entityCard", "clientapi:listEntities", "clientapi:listReviewItems", "clientapi:resolveReviewItem", "clientapi:unlinkEntity"]
related: ["flow:entity-filing-review-merge", "flow:upload-job-extraction-filing-polling"]
last_verified: 2026-08-02
status: active
---
# Entities, filing, and review

## Responsibility
Turn mentions into a vault register while preserving uncertainty, decisions, and reversible merges.
## Boundaries
Validated extraction mentions or user cards enter; entities, links, events, constraints, and review items leave.
## Interfaces
Filing engine/domain, entity card/register routes, review resolution, merge/unmerge, confirm, and unlink.
## Dependencies
Documents, facts, jobs, audit engine, client dialogs, and authorization.
## Data
Entities own identifiers and events; mentions/link rows preserve document evidence; constraints record decisions. Conflict reviews retain the current and competing fact values plus revision identity, while unfiled reviews retain the assignable document.
## Invariants
Uncertain evidence stays explicitly uncertain and reviewable. Conflict choices verify the selected current or competing value with available source provenance only while the fact, revision, candidate, and document snapshot is current; ordinary provenance is often document-only and deeper run/OCR/field links are optional. Stale choices remain open with refresh guidance. Legacy evidence-less conflicts are explicitly closable, but real two-value conflicts are not dismissible. An unfiled retry enqueues at most one active filing job. Queued filing writes remain lease-fenced. Ordinary `fail()` dead letter best-effort opens an unfiled item immediately through the same single-document detector the nightly lint uses; lease-reaper dead letter skips that hook and depends on a later audit. Confirmed cards resist unsafe mutation; constraints and merges remain vault-local; prohibited pairs are checked before repointing; merges are recoverable. Schema history stays one linear chain in SQLite and PostgreSQL.
## Change points
Change `models`, create the next linear revision after the current head (`migration:0011`) without editing history, then change filing/review, queue terminalization and audit recovery, entity and review routes, API adapter, Entities view, ReviewInbox, and EntityCardDetail together.
## Proof
`backend/app/domain/jobs.py` → `surface_filing_dead_letter` and its ordinary-failure test; `backend/app/queue.py` → `reap_expired_leases` (source inspection establishes that it does not call the filing hook); `backend/app/domain/audit.py` → unfiled detectors. Tests cover filing/lease-loss rollback, ordinary filing dead-letter surfacing, generic lease reaping, entity model/API/merge, conflict and unfiled actions, review concurrency, manual cards, unlink, auditor, security, client inbox/card, and both database migration gates; no focused test currently pins the reaper-specific filing-review gap.

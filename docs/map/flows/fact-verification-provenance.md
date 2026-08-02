---
id: flow:fact-verification-provenance
kind: flow
summary: Promote extracted or user facts through revisions while recording document provenance and optional deeper evidence links.
read_when: ["fact verification provenance", "canonical fact revision evidence"]
sources: ["file:backend/app/domain/facts.py", "file:backend/app/domain/extraction.py", "file:backend/app/domain/review.py", "file:backend/app/routers/facts.py", "file:backend/app/domain/serialization.py"]
inventory_refs: ["route:POST:/api/facts/{fact_id}/verify", "model:Fact", "model:FactRevision", "model:FactProvenance", "clientapi:verifyFact"]
related: ["subsystem:facts-summaries", "subsystem:ai-extraction-provenance", "subsystem:entities-filing-review"]
last_verified: 2026-08-02
status: active
---
# Fact verification and provenance

## Entry
A validated extraction candidate or member-supplied entity fact proposes a value.
## Sequence
Resolve the subject, create/update the canonical fact, append a revision and provenance row, and optionally verify. Ordinary extracted facts normally attach only the source document; their candidate and provenance rows usually have no extraction-run, OCR, or field-evidence IDs. Direct verification likewise records the current source document (or no document for user-entered facts). Conflict resolution locks and revalidates the snapshot, clones whatever provenance the selected revision actually has, or records the selected candidate's document and optional extraction-run ID; deeper OCR/field links remain optional rather than guaranteed.
## Failures and retries
Duplicate/current-key conflicts resolve transactionally; stale candidate/document snapshots, invalid subject/evidence, or cross-vault IDs fail without changing the fact or review item.
## Trust boundaries
Provider confidence and nullable evidence links are not authorization or proof of claim support; only domain code selects canonical/current state.
## Observability
Revision status, provenance rows, verification activity, and source-document links. Their presence does not imply page, quote, OCR, or field-level support.
## Change together
Fact domain/models/routes, candidate/run linkage, extraction/OCR/field evidence writes, conflict snapshot rules, entity subject rules, serialization/UI, and ordinary/deep-provenance verification tests.

## Proof
`backend/app/domain/facts.py` → `upsert_fact`, `verify`; `backend/app/domain/extraction.py` → `_insert_extracted_parts`; `backend/app/domain/review.py` → conflict resolution; fact, manual-entity-fact, extraction-evidence, stale-conflict, and provenance-propagation tests.

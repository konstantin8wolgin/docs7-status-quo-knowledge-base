---
id: subsystem:facts-summaries
kind: subsystem
summary: Canonical facts, immutable revisions, optional-depth provenance, verification, document facets, and summaries.
read_when: ["facts summaries verification", "fact provenance revisions", "document amounts dates tags"]
sources: ["file:backend/app/domain/facts.py", "file:backend/app/domain/extraction.py", "file:backend/app/domain/serialization.py", "file:backend/app/routers/summary.py"]
inventory_refs: ["route:GET:/api/summary", "route:POST:/api/facts/{fact_id}/verify", "model:DocumentAmount", "model:DocumentDate", "model:DocumentTag", "model:DocumentTrustFlag", "model:Fact", "model:FactProvenance", "model:FactRevision", "clientapi:summary", "clientapi:verifyFact"]
related: ["flow:fact-verification-provenance", "subsystem:entities-filing-review"]
last_verified: 2026-08-02
status: active
---
# Facts and summaries

## Responsibility
Maintain current facts with immutable revisions and provenance records of variable evidence depth, then shape summary projections.
## Boundaries
Validated candidates or user values enter; vault-scoped canonical facts and views leave.
## Interfaces
Fact acceptance/verification, serialization, summary route, and client facts views.
## Dependencies
Extraction evidence, entities, documents, request context, and database constraints.
## Data
Facts point to current revisions; revisions have provenance rows that may cite a document and may optionally cite extraction-run, OCR, or field evidence. Ordinary extraction and direct verification are usually document-only, while user-entered facts can have no document. Conflict resolution preserves only the evidence links actually available on the selected revision/candidate.
## Invariants
Canonical transitions remain vault-scoped and append a revision/provenance record; verified values resist machine overwrite, and stale conflict snapshots are rejected. A provenance row is not a guarantee that its source document, page, or quote supports the current value, and deeper evidence columns are commonly null.
## Change points
Change fact domain, models/evidence links, extraction and conflict writes, API shapes, serialization, client provenance views, and shallow/deep evidence proof together.
## Proof
`backend/app/domain/facts.py` → `upsert_fact`, `verify`; `backend/app/domain/extraction.py` → `_insert_extracted_parts`; `backend/app/domain/serialization.py` → fact/document projections; facts, verification, extraction-evidence, conflict provenance, contract-shape, state, and adversarial scope tests.

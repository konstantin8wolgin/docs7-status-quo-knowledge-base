---
id: flow:entity-filing-review-merge
kind: flow
summary: File extracted mentions into entities, surface uncertainty, resolve review, and preserve merge recovery.
read_when: ["entity filing review merge", "mention matching review inbox"]
sources: ["file:backend/app/models.py", "file:backend/app/domain/filing.py", "file:backend/app/domain/review.py", "file:backend/app/domain/audit.py", "file:backend/app/routers/entities.py", "file:backend/app/routers/review.py", "file:client/src/components/ReviewInbox.jsx"]
inventory_refs: ["job:document.file", "model:EntityMention", "model:ReviewItem", "route:POST:/api/entities/merge"]
related: ["subsystem:entities-filing-review", "subsystem:ai-extraction-provenance"]
last_verified: 2026-07-17
status: active
---
# Entity filing, review, and merge

## Entry
A completed extraction supplies validated entity mentions or a user creates a manual card.
## Sequence
Normalize identifiers, apply constraints and matching tiers, link or create, emit events, and ask a bounded review. Identity answers affect only the candidate named in the question; conflict answers verify one evidenced value with that value's provenance, and unfiled answers enqueue a fresh filing attempt before ordinary merge resolution. Legacy conflicts without competing evidence may be closed explicitly, while real two-value conflicts cannot be silently dismissed.
## Failures and retries
Invalid engine decisions, stale fact/candidate/document review evidence, or lease loss roll back. The inbox keeps stale items visible with German refresh/retry guidance. Filing domain writes share the lease-conditioned completion transaction, and retries must not duplicate authoritative links, questions, or active refile jobs.
## Trust boundaries
Uncertain engine evidence remains explicitly uncertain and reviewable; proposals cannot override confirmed cards, cross vaults, claim foreign identifiers, or inject review text.
## Observability
Entity events, typed review evidence/resolution, audit findings, refile job state, and activity history.
## Change together
Change models plus a new revision after the current migration head, filing/review domains and routes, auditor, client cards/inbox, and adversarial proof together; never treat historical revisions as writable change points.

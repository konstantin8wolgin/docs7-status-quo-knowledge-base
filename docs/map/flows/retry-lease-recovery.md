---
id: flow:retry-lease-recovery
kind: flow
summary: Claim due jobs with leases, fence completion, retry with backoff, and let workers recover expired leases.
read_when: ["retry lease recovery", "worker crash dead letter"]
sources: ["file:backend/app/models.py", "file:backend/alembic/versions/0003_job_queue.py", "file:backend/app/queue.py", "file:backend/app/worker.py", "file:backend/app/domain/jobs.py", "file:backend/app/routers/jobs.py", "file:backend/app/domain/serialization.py", "file:backend/app/observability.py", "file:client/src/api.js"]
inventory_refs: ["model:ProcessingJob", "migration:0003", "job:document.process", "job:document.reprocess", "job:document.file", "job:chat.answer", "job:auditor.nightly"]
related: ["subsystem:jobs-workers", "subsystem:data-migrations-testing-operations"]
last_verified: 2026-08-02
status: active
---
# Retry, lease, and recovery

## Entry
A worker can claim any due queued job. Automatic inline mode targets a newly scheduled job and drains immediately available chained filing work; it is not a general queue drainer or scheduler for future retries.
## Sequence
Select due work by creation time (persisted `priority` is ignored), atomically claim and lease it, execute one typed body without an internal commit, and apply lease-conditioned completion in the same transaction. Ordinary failure rolls body work back and either records terminal state or requeues with exponential backoff; successful extraction chains filing.
## Failures and retries
Exceptions roll back domain work. A stale completion predicate rolls back filing or auditor writes rather than publishing work from a lost lease. Workers reap expired leases; inline mode never reaps them. Ordinary failure below `max_attempts` becomes `queued` with future `run_after`, but the inline task returns without arranging a wake-up. Reaping can requeue without resetting stage/backoff or can dead-letter extraction/chat/audit projections; a reaper-dead-lettered filing job does not invoke the immediate unfiled-review hook used after ordinary `fail()`.
## Trust boundaries
Only the current lease owner may finalize; job payloads are server-created and handlers recheck sensitive gates.
## Observability
Attempts, run-after, lease owner/expiry, terminal error, and stage are durable. The job API reports backoff as `queued`, not `retrying`, and omits `run_after`. Worker event messages are emitted, but the JSON formatter drops extras such as job ID, attempt, reaped count, and error.
## Change together
Change queue SQL, `ProcessingJob`/a new migration if required, handlers, worker reaping/scheduling, targeted inline execution, dead-letter projections, job serialization, client polling, logging fields/formatter, and SQLite/PostgreSQL recovery tests together.

## Proof
`backend/app/queue.py` → `claim_next`, `fail`, `reap_expired_leases`; `backend/app/worker.py` → `run_worker_once`; `backend/app/domain/jobs.py` → `process_job`, `surface_filing_dead_letter`; `backend/app/domain/serialization.py` → `job_payload`; `backend/app/observability.py` → `JsonFormatter`; `backend/tests/test_queue.py` → backoff, lease reaping, filing dead-letter, inline, and dual-database concurrency cases.

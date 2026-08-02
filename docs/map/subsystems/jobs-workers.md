---
id: subsystem:jobs-workers
kind: subsystem
summary: Durable job dispatch, lease fencing, retries, worker-owned recovery, chaining, and targeted inline execution.
read_when: ["jobs worker queue", "lease retry recovery", "processing job polling", "expired lease backoff dead letter"]
sources: ["file:backend/app/models.py", "file:backend/alembic/versions/0003_job_queue.py", "file:backend/app/domain/jobs.py", "file:backend/app/queue.py", "file:backend/app/worker.py", "file:backend/app/routers/jobs.py", "file:backend/app/domain/serialization.py", "file:backend/app/observability.py", "file:client/src/api.js"]
inventory_refs: ["route:GET:/api/jobs/{job_id}", "model:ProcessingJob", "job:auditor.nightly", "job:chat.answer", "job:document.file", "job:document.process", "job:document.reprocess", "migration:0003", "clientapi:job"]
related: ["flow:retry-lease-recovery", "flow:upload-job-extraction-filing-polling"]
last_verified: 2026-08-02
status: active
---
# Jobs and workers

## Responsibility
Persist, claim, execute, fence, retry, and chain background work; external workers alone reap expired leases and wake future-due retries.
## Boundaries
Typed job payloads enter; committed domain transitions and terminal status leave.
## Interfaces
Queue primitives, closed `JOB_BODIES` dispatch, worker loop, targeted inline background task, and job polling.
## Dependencies
Database transactions, settings, domain handlers, consent checks, and structured logging.
## Data
Processing jobs carry type, status, attempt budget, lease owner/expiry, scheduling time, and priority. Claims order by creation time, so persisted priority currently has no effect.
## Invariants
Only the active lease may complete or fail work. Queued filing and auditor bodies flush but do not commit, so their writes commit only with lease-conditioned completion and roll back on lease loss. Ordinary body failure requeues below the attempt limit with backoff; APIs expose that state as `queued`, not `retrying`. Worker reaping makes expired leases reclaimable or terminal and closes extraction/chat/audit projections. Inline mode neither reaps nor schedules a wake for backoff. After ordinary `fail()` dead-letters filing, worker and inline executors best-effort open an unfiled review outside the lease; reaper terminalization does not call that hook.
## Change points
Change `ProcessingJob`/a new migration only if persistence changes, then queue ordering/state, job registry, worker reaper/scheduler, targeted inline execution, terminal projections, job route/serialization, client polling, and observability together.
## Proof
`backend/app/queue.py` → `claim_next`, `fail`, `reap_expired_leases`; `backend/app/domain/jobs.py` → `process_job`, `surface_filing_dead_letter`; `backend/app/worker.py` → `run_worker_once`; `backend/app/domain/serialization.py` → `job_payload`; queue and worker tests prove ordinary retry, worker reaping, stale-owner fencing, terminal projections, nonterminal polling, and SQLite/PostgreSQL concurrency; smoke, auditor, answer, and load-smoke gates cover consumers.

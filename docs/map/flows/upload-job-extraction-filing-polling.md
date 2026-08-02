---
id: flow:upload-job-extraction-filing-polling
kind: flow
summary: Move an authorized upload through encrypted storage, extraction, filing, and terminal client polling.
read_when: ["upload extraction filing polling", "document processing pipeline", "raster MIME file type client picker"]
sources: ["file:backend/app/routers/documents.py", "file:backend/app/domain/uploads.py", "file:backend/app/filetype.py", "file:backend/app/domain/files.py", "file:backend/app/crypto.py", "file:backend/app/queue.py", "file:backend/app/domain/jobs.py", "file:backend/app/domain/serialization.py", "file:backend/app/domain/extraction.py", "file:backend/app/domain/filing.py", "file:client/src/api.js", "file:client/src/views/Capture.jsx"]
inventory_refs: ["route:POST:/api/upload", "route:GET:/api/jobs/{job_id}", "job:document.process", "job:document.file", "clientapi:uploadAndWait"]
related: ["subsystem:capture-documents", "subsystem:jobs-workers", "subsystem:ai-extraction-provenance", "subsystem:entities-filing-review"]
last_verified: 2026-08-02
status: active
---
# Upload to extraction, filing, and polling

## Entry
A verified, consenting vault member uploads an accepted file and optional context.
## Sequence
Validate quota/type, encrypt/store, commit file and queued processing job, schedule the configured executor, extract and persist evidence, then chain filing. Upload returns the accepted job before execution; bounded client polling reaches a terminal capture state or exposes a still-processing card whose recheck continues the same job.
## Failures and retries
Media, signature, size, or quota validation fails before persistence. Filing writes flush into the lease-conditioned completion transaction and roll back on lease loss. Ordinary retry backoff is persisted and serialized as `queued` (the server does not emit `retrying`); inline mode has no future wake-up, while workers reclaim due work and reap expired leases. Polling exhaustion alone remains nonterminal. An ordinary filing `fail()` that reaches dead letter best-effort opens the unfiled item immediately; lease-reaper dead letter does not. Either terminal filing state is reported separately on the completed parent poll (`filing: "failed"`), leaving the extracted document usable.
## Trust boundaries
File bytes and model output are untrusted; context, schemas, leases, and filing validators enforce boundaries.
## Observability
Job status/stage, terminal error, request ID, run engine, and the client's still-processing/recheck state expose progress without secrets. Backoff appears as queued with an error and no public `run_after`; dead-letter is projected as failed by the poll payload.
## Change together
Change `routers.documents`, `domain.uploads`, `filetype`, encrypted file helpers, queue/worker and `domain.jobs`, `domain.serialization`, extraction/filing, `client/src/api.js`, and `views/Capture.jsx` together. Prove upload validation, encryption, ordinary/reaper failure paths, job lifecycle, security, client polling/build, and runtime smoke.

## Proof
`backend/app/domain/uploads.py` → `copy_upload_to_temp`, `upload`; `backend/app/domain/jobs.py` → `create_processing_job`, `process_job`, `surface_filing_dead_letter`; `backend/app/queue.py` → `fail`, `reap_expired_leases`; `backend/app/domain/serialization.py` → `job_payload`; `backend/tests/test_queue.py` and client API/Capture tests → acceptance, chaining, retries, terminal filing projection, polling timeout, and recheck.

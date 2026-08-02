---
id: flow:sample-import
kind: flow
summary: Import an allowlisted repository sample through the same durable capture and filing pipeline as uploads.
read_when: ["sample import", "demo capture sample"]
sources: ["file:backend/app/routers/samples.py", "file:backend/app/domain/documents.py", "file:backend/app/domain/jobs.py", "file:backend/app/domain/serialization.py", "file:docs/api/openapi.json", "file:client/src/api.js"]
inventory_refs: ["route:GET:/api/samples", "route:POST:/api/samples/import", "clientapi:importSampleAndWait"]
related: ["subsystem:capture-documents", "flow:upload-job-extraction-filing-polling"]
last_verified: 2026-08-02
status: active
---
# Sample import

## Entry
A verified, consenting member chooses a server-declared sample name.
## Sequence
Resolve the allowlisted file and either return an existing import or create a queued capture job. A new import responds `202` at runtime and schedules extraction/filing; duplicate queued, running, or completed imports respond `200`. The client boundedly polls the shared capture result, and a manual recheck continues the same job.
## Failures and retries
Traversal or missing samples fail; processing uses the normal durable attempt rules. Retry backoff remains server status `queued`; an inline failure has no future wake-up, whereas workers claim it when due and reap expired leases. A client polling timeout reports still-processing rather than converting a live queued or running job into a failure.
## Trust boundaries
Client names never become arbitrary filesystem paths; sample bytes still pass the extraction contract.
## Observability
Sample route status, job stage/error, engine, and final document state. The generated OpenAPI declares only the decorator's `200` success response and omits the runtime `202` branch.
## Change together
Sample fixtures/domain/route, declared `200`/`202` response contract and OpenAPI, queue/worker behavior, API helper, demo tests, and runtime proof.

## Proof
`backend/app/domain/documents.py` → `import_sample`; `backend/app/routers/samples.py` → `import_sample`; `backend/app/domain/serialization.py` → `existing_import_job_payload`; `docs/api/openapi.json` → `POST /api/samples/import`; `backend/tests/test_queue.py` → new, duplicate, retry, and completed-import status cases.

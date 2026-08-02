---
id: subsystem:capture-documents
kind: subsystem
summary: Document listing, upload and sample capture, durable processing creation, and polling contracts.
read_when: ["upload capture documents", "sample import polling", "document lifecycle"]
sources: ["file:backend/app/routers/documents.py", "file:backend/app/domain/uploads.py", "file:backend/app/routers/samples.py", "file:backend/app/domain/documents.py", "file:backend/app/domain/serialization.py", "file:docs/api/openapi.json", "file:client/src/api.js", "file:client/src/views/Capture.jsx"]
inventory_refs: ["route:GET:/api/documents", "route:GET:/api/documents/{document_id}", "route:GET:/api/samples", "route:GET:/api/samples/file/{name}", "route:POST:/api/samples/import", "route:POST:/api/upload", "model:Document", "model:ProcessingJob", "clientapi:document", "clientapi:importSample", "clientapi:importSampleAndWait", "clientapi:listDocuments", "clientapi:samples", "clientapi:upload", "clientapi:uploadAndWait"]
related: ["flow:upload-job-extraction-filing-polling", "flow:sample-import"]
last_verified: 2026-08-02
status: active
---
# Capture and documents

## Responsibility
Accept bounded files or trusted samples and expose vault-scoped document state.
## Boundaries
Multipart or sample names enter; encrypted files, documents, and durable jobs leave.
## Interfaces
Upload, sample import, paginated document list, document detail, bounded capture polling, and explicit status recheck.
## Dependencies
Auth gates, storage quota, file encryption, job scheduling, and serialization.
## Data
Documents reference encrypted file objects and optional user context.
## Invariants
Accepted media and size are validated before durable work; all reads stay vault-scoped. Retry backoff is serialized as `queued`, not `retrying`, and inline mode does not schedule its future wake. Only failed/error/dead-letter terminal projections render as capture failures; exhausting the polling budget returns a resumable still-processing state. The payload names chained filing separately (`filing`: running/completed/failed): any dead-lettered filing renders saved-needs-review with a Postfach hint, but only ordinary `fail()` best-effort opens that review immediately; reaper dead letter waits for later audit detection. New sample import returns runtime `202` although generated OpenAPI currently lists only `200` success.
## Change points
Change upload/sample routes and declared response statuses, OpenAPI, client polling, storage, queue/worker terminal paths, serializers/schemas, and upload/sample tests together.
## Proof
`backend/app/domain/uploads.py` → `upload`; `backend/app/domain/documents.py` and `backend/app/routers/samples.py` → `import_sample`; `backend/app/domain/serialization.py` → `job_payload`; `client/src/api.js` → `waitForJob`; upload, pagination, sample-status, slow/queued-backoff/dead-letter polling, Capture recheck, smoke-flow, and adversarial tests.

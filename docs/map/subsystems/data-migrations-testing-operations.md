---
id: subsystem:data-migrations-testing-operations
kind: subsystem
summary: SQLAlchemy models, a linear PostgreSQL migration path, divergent SQLite create-all tests, audit evidence, CI, and operations.
read_when: ["data migrations testing operations", "PostgreSQL SQLite schema", "auditor nightly CI deploy"]
sources: ["file:backend/app/models.py", "file:backend/app/settings.py", "file:backend/alembic/env.py", "file:backend/alembic/versions/0003_job_queue.py", "file:backend/alembic/versions/0011_chat_run_jsonb.py", "file:backend/tests/conftest.py", "file:.github/workflows/ci.yml"]
inventory_refs: ["model:AuditEvent", "model:AuditRun", "model:ChatRun", "migration:0001", "migration:0002", "migration:0003", "migration:0004", "migration:0005", "migration:0006", "migration:0007", "migration:0008", "migration:0009", "migration:0010", "migration:0011", "job:auditor.nightly"]
related: ["subsystem:runtime-configuration", "flow:retry-lease-recovery"]
last_verified: 2026-08-02
status: active
---
# Data, migrations, testing, and operations

## Responsibility
Keep runtime models, migrations, database lanes, audit evidence, CI, and operational recovery aligned.
## Boundaries
Schema/model changes enter; a linear migration history plus explicitly different PostgreSQL-migration and SQLite-create-all proof leaves.
## Interfaces
SQLAlchemy metadata, Alembic, fixtures, Docker services, CI, runbook, auditor schedule, and load smoke.
## Dependencies
Every domain model, PostgreSQL and SQLite semantics, object storage, settings, and deployment images.
## Data
Migrations form one root-to-head chain. PostgreSQL applies that chain; ordinary SQLite development/tests default to current ORM `Base.metadata.create_all`. Revision 0011 converts three `ChatRun` structured-payload columns from PostgreSQL JSON to JSONB while remaining a no-op on SQLite; audit runs/events preserve bounded application evidence, not external immutable telemetry.
## Invariants
The PostgreSQL lane migrates from an empty database and enforces foreign keys. Ordinary SQLite connections do not enable `PRAGMA foreign_keys`, and create-all misses migration-only indexes/defaults/extensions; a fresh SQLite Alembic walk currently fails at revision 0003. These are known dialect/schema drift, not parity. New migrations still append to one linear chain and both configured test lanes remain required.
## Change points
Change model, the next linear migration, SQLite create-all/runtime initialization, database-specific semantics and parity/drift tests, inventory evidence, OpenAPI if relevant, and runbook together.
## Proof
`backend/app/models.py` → `make_session_factory`; `backend/app/settings.py` → `Settings.apply_runtime_defaults`; `backend/alembic/versions/0003_job_queue.py`; `backend/tests/conftest.py`; migration/dialect tests plus full SQLite/PostgreSQL suites, adversarial tests, Ruff, OpenAPI, CI, and runtime gate.

---
id: subsystem:runtime-configuration
kind: subsystem
summary: Runtime assembly, environment validation, route wiring, and local or production startup.
read_when: ["runtime configuration startup", "settings environment routes"]
sources: ["file:backend/app/main.py", "file:backend/app/settings.py", "file:backend/app/routers/health.py", "file:backend/app/route_policy.py", "file:backend/app/observability.py", "file:start.sh"]
inventory_refs: ["route:GET:/api/health", "route:GET:/api/ready", "route:POST:/api/reset"]
related: ["subsystem:data-migrations-testing-operations", "flow:retry-lease-recovery"]
last_verified: 2026-08-02
status: active
---
# Runtime and configuration

## Responsibility
Assemble validated settings, dependencies, middleware, routers, and the supported demo startup.
## Boundaries
Environment enters through `Settings`; application wiring leaves through `create_app`.
## Interfaces
Health, readiness, development reset, worker entrypoint, and `start.sh`.
## Dependencies
Database sessions, object storage, email, AI providers, executable router dependencies, and non-enforcing route-policy metadata.
## Data
Configuration is environment-backed and never copied into the Map. `ROUTE_POLICIES` is a tested inventory/adversarial ledger; application dependencies remain the runtime enforcement path.
## Invariants
Production rejects development secrets and routes; startup does not silently weaken gates. `/api/health` is process liveness metadata, while `/api/ready` executes only `SELECT 1`: readiness does not prove schema currency, storage, email, AI, queue, or worker health.
## Change points
Change settings, app/router wiring, executable dependencies and matching route-policy metadata, health/readiness probes, runbooks, and lifecycle/adversarial tests together.
## Proof
`backend/app/main.py` → `create_app`; `backend/app/settings.py` → `Settings`; `backend/app/routers/health.py` → `health`, `ready`; `backend/app/route_policy.py` → `ROUTE_POLICIES`; `backend/app/observability.py` → `JsonFormatter`; settings, lifecycle, route-policy, smoke-flow, and runtime gates.

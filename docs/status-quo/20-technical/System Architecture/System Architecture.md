---
id: technical-family-system-architecture
title: System Architecture
kind: technical-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical-family
map_pages:
  - subsystem:runtime-configuration
  - subsystem:auth-vault-consent
  - subsystem:client-architecture
  - flow:auth-vault-context
inventory_refs:
  - route:GET:/api/health
  - route:GET:/api/ready
  - route:POST:/api/reset
feature_links:
  - AUTH-01
  - AUTH-04
  - AUTH-05
  - CAP-03
parent: "[[Technical Atlas]]"
related:
  - "[[Client Architecture]]"
  - "[[Runtime and Operations]]"
---

> [!info] Navigation
> Parent: [[Technical Atlas]]. Sibling hubs: [[Client Architecture]] · [[Backend and API]] · [[Data and Migrations]] · [[Jobs and AI]] · [[Security and Storage]] · [[Runtime and Operations]].

# System Architecture

This family owns the system topology and composition contract, component ownership and dependency direction, opaque-session request context, and the exact lifecycle of requests through middleware and error boundaries. It distinguishes the local Uvicorn/Vite/SQLite/inline-job demo from the four-worker API plus two-worker PostgreSQL/MinIO production Compose topology and records what that Compose file omits.

## Child index

| Leaf | Owned contract |
| --- | --- |
| [[System Topology and Composition]] | Development/production process topology, `create_app`, `Deps`, adapter construction, environment-only reset, opaque sessions and first-membership context |
| [[Component Ownership and Dependency Direction]] | Client/router/domain/infrastructure ownership, direct SQLAlchemy domain dependencies, explicit transaction boundaries and tested route-policy metadata |
| [[Request Lifecycle Errors and Middleware]] | Exact Starlette insertion/unwind order, origin/CORS/request IDs/security headers, exception normalization and OpenAPI error drift |

Read [[System Topology and Composition]] first for deployment or composition questions, [[Component Ownership and Dependency Direction]] before changing boundaries, and [[Request Lifecycle Errors and Middleware]] before changing cross-cutting HTTP behavior. [[Complete API Contract]] owns per-route details; later [[Runtime and Operations]] and [[Security and Storage]] leaves deepen deployment and trust-boundary proof without duplicating these contracts.

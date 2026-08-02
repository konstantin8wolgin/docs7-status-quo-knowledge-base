---
id: technical-family-backend-and-api
title: Backend and API
kind: technical-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical-family
map_pages:
  - subsystem:runtime-configuration
  - subsystem:auth-vault-consent
  - subsystem:capture-documents
  - subsystem:search-grounded-chat
  - flow:auth-vault-context
inventory_refs:
  - route:GET:/api/summary
  - route:POST:/api/upload
  - route:POST:/api/chat
  - route:POST:/api/entities
  - route:POST:/api/review-items/{item_id}/resolve
  - route:POST:/api/reset
feature_links:
  - AUTH-01
  - CAP-01
  - ASSIST-01
  - ENT-01
  - REVIEW-01
parent: "[[Technical Atlas]]"
related:
  - "[[Client Architecture]]"
  - "[[Data and Migrations]]"
---

> [!info] Navigation
> Parent: [[Technical Atlas]]. Sibling hubs: [[System Architecture]] · [[Client Architecture]] · [[Data and Migrations]] · [[Jobs and AI]] · [[Security and Storage]] · [[Runtime and Operations]].

# Backend and API

This family owns router, domain, and infrastructure boundaries and the complete current API contract, including authentication and authorization gates, validation, transactions, failures, replay/pagination behavior, client reachability, handlers, tests, and generated-contract drift. Development exposes 39 routes; production omits only reset and exposes 38.

## Child index

| Leaf | Owned contract |
| --- | --- |
| [[Router Domain and Infrastructure Boundaries]] | Router/domain/adaptor ownership, direct-session services, explicit commits, durable-before-background job scheduling and route-policy metadata versus runtime dependencies |
| [[Complete API Contract]] | Every development/production route, all 31 client methods, roles and gates, requests/results/statuses, replay/pagination, reachability, handlers, proof and OpenAPI/inventory limitations |

Use [[Complete API Contract]] as the route ledger, not generated OpenAPI alone: sample import has a runtime 202/200 split, shared dependency failures and dynamic binary responses are underdeclared, normalized 422 errors differ, and no OpenAPI auth security scheme exists. [[Client API Permissions and Failure Contract]] owns browser adaptation and missing affordance metadata; later data/jobs/security notes own deeper internal state machines.

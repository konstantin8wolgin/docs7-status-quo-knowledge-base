---
id: technical-family-data-and-migrations
title: Data and Migrations
kind: technical-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical-family
map_pages:
  - subsystem:data-migrations-testing-operations
  - subsystem:jobs-workers
  - subsystem:ai-extraction-provenance
  - subsystem:entities-filing-review
  - subsystem:search-grounded-chat
inventory_refs:
  - model:User
  - model:Vault
  - model:Document
  - model:ProcessingJob
  - model:ExtractionRun
  - model:Entity
  - model:Fact
  - model:ChatRun
  - model:AuditRun
  - migration:0001
  - migration:0006
  - migration:0011
feature_links:
  - AUTH-04
  - CAP-03
  - DOC-01
  - ENT-03
  - FACT-01
  - ASSIST-01
parent: "[[Technical Atlas]]"
related:
  - "[[Backend and API]]"
  - "[[Jobs and AI]]"
---

> [!info] Navigation
> Parent: [[Technical Atlas]]. Sibling hubs: [[System Architecture]] · [[Client Architecture]] · [[Backend and API]] · [[Jobs and AI]] · [[Security and Storage]] · [[Runtime and Operations]].

# Data and Migrations

This family owns the exact 32-model relational topology, the linear 11-revision schema history, material SQLite/PostgreSQL differences, and the distinct export, reset and account-deletion lifecycles. The database has 76 FK columns but only four ORM relationships, no FK cascade, no composite same-vault FK, and default SQLite connections leave FK enforcement off.

## Child index

| Leaf | Owned contract |
| --- | --- |
| [[Domain Model and Relationships]] | All 32 model IDs, exact FKs/logical references, four ORM relationships, uniqueness/check coverage, tenant-consistency and cascade gaps |
| [[Migration History and Database Dialects]] | migration:0001→migration:0011 history, backfills/refusing downgrade, PostgreSQL FTS/JSONB, fresh-SQLite failure and create-all drift |
| [[Data Lifecycle Reset Export and Deletion]] | Supported export subset, exact reset/account preserved and deleted sets, manual order, cryptographic erasure and best-effort physical cleanup |

Read the model ledger before changing persistence ownership, the migration leaf before changing schema or claiming database parity, and the lifecycle leaf before changing a delete, reset, export, encryption or storage-cleanup path. [[Jobs and AI]] owns the state machines that write these rows.

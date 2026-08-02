---
id: technical-family-runtime-and-operations
title: Runtime and Operations
kind: technical-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical-family
map_pages:
  - subsystem:runtime-configuration
  - subsystem:data-migrations-testing-operations
  - subsystem:jobs-workers
  - subsystem:files-crypto-storage
  - subsystem:gdpr-account
  - flow:retry-lease-recovery
  - flow:account-export-deletion
inventory_refs:
  - route:GET:/api/health
  - route:GET:/api/ready
  - route:POST:/api/reset
  - route:GET:/api/account/export
  - route:DELETE:/api/account
  - model:ProcessingJob
  - model:ExtractionRun
  - model:ChatRun
  - model:AuditRun
  - model:AuditEvent
  - model:FileObject
  - model:VaultKey
  - migration:0001
  - migration:0011
  - job:auditor.nightly
  - job:chat.answer
  - job:document.file
  - job:document.process
  - job:document.reprocess
feature_links:
  - AUTH-01
  - AUTH-03
  - AUTH-04
  - CAP-01
  - CAP-03
  - DOC-02
  - ASSIST-01
  - REVIEW-01
parent: "[[Technical Atlas]]"
related:
  - "[[Security and Storage]]"
  - "[[System Architecture]]"
---

> [!info] Navigation
> Parent: [[Technical Atlas]]. Sibling hubs: [[System Architecture]] · [[Client Architecture]] · [[Backend and API]] · [[Data and Migrations]] · [[Jobs and AI]] · [[Security and Storage]].

# Runtime and Operations

This family owns settings semantics, local and production runtime topology, readiness and observability, backup and restore, incident recovery, and test lanes, gates, and release proof.

## Child index

| Leaf | Owns |
| --- | --- |
| [[Settings and Environment Contract]] | Complete named configuration surface, defaults, validation and dependency-construction timing without deployment values |
| [[Local and Production Runtime Topology]] | Local launcher, production image/Compose graph, migration/bucket ordering, health/readiness and worker-health gaps |
| [[Observability Backup Restore and Incident Recovery]] | Request/process visibility, durable operational evidence, backup triad, restore/rotation and incident limitations |
| [[Test Lanes Gates and Release Proof]] | Configured repository gates, CI-executed subset, optional S3, manual runtime, synthetic fixtures and private golden boundary |

Read settings before topology to distinguish accepted configuration from a deployable dependency graph. Then use observability/recovery for live-state and recovery questions and proof for the exact difference between policy, CI, optional infrastructure, manual evidence and private release evidence.

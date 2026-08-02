---
id: technical-family-jobs-and-ai
title: Jobs and AI
kind: technical-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical-family
map_pages:
  - subsystem:jobs-workers
  - subsystem:ai-extraction-provenance
  - subsystem:entities-filing-review
  - subsystem:search-grounded-chat
  - flow:retry-lease-recovery
  - flow:upload-job-extraction-filing-polling
  - flow:entity-filing-review-merge
  - flow:search-grounded-chat
inventory_refs:
  - model:ProcessingJob
  - model:ExtractionRun
  - model:EntityMention
  - model:ChatRun
  - model:AuditRun
  - job:auditor.nightly
  - job:chat.answer
  - job:document.file
  - job:document.process
  - job:document.reprocess
feature_links:
  - AUTH-03
  - CAP-03
  - ENT-03
  - REVIEW-01
  - ASSIST-01
  - ASSIST-02
  - ASSIST-03
parent: "[[Technical Atlas]]"
related:
  - "[[Data and Migrations]]"
  - "[[Security and Storage]]"
---

> [!info] Navigation
> Parent: [[Technical Atlas]]. Sibling hubs: [[System Architecture]] · [[Client Architecture]] · [[Backend and API]] · [[Data and Migrations]] · [[Security and Storage]] · [[Runtime and Operations]].

# Jobs and AI

This family owns all five durable job types, exact lease fencing and recovery, loose-to-strict extraction envelopes and actual evidence depth, policy-limited filing/auditor automation, and dialect-qualified search plus four-rung answer internals. It records the places where runtime trust is deliberately narrower than the schema or UI: inline recovery gaps, shallow provenance, bounded review/automation, stateless questions and document-level citation guards.

## Child index

| Leaf | Owned contract |
| --- | --- |
| [[Durable Job State Lease Fencing and Recovery]] | Five-type registry, due/FIFO claims, ignored priority, exact lease ownership, rollback/backoff/reaper/chaining, inline gaps and dead-letter projections |
| [[Extraction Envelope Evidence and Provenance]] | `from_loose` normalization behind strict models, page rules, seed/Vertex retry/fallback, persisted normalized state, reprocess authority and shallow evidence links |
| [[Filing Auditor and Policy-Limited Automation]] | Mention filing, identifier/decision/question guards, per-vault serialization, auditor schedule/delta/lint/consent/caps and exact merge/refile/alias policy |
| [[Search and Answer Agent Internals]] | Latest-run PostgreSQL/SQLite retrieval, fixed tools and rung caps, selected original rendering, stateless chat, citation guard, mismatch/reprocess and `ChatRun` omissions |

Start with the durable-job leaf for concurrency or failure questions. Then follow the owning body: extraction before evidence/schema work, filing/auditor before entity automation, and search/answer before retrieval, tool, citation or chat-run changes. [[Domain Model and Relationships]] and [[Migration History and Database Dialects]] own the rows and schema beneath every state machine.

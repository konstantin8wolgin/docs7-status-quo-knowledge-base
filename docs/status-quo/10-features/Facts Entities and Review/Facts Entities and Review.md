---
id: feature-family-facts-entities-and-review
title: Facts Entities and Review
kind: feature-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/feature-family
capability_ids: []
delivery: partial
reachability: user-facing
persistence: durable
evidence: code-and-tests
parent: "[[Feature Atlas]]"
related:
  - "[[Documents and Knowledge]]"
  - "[[Assistant and Search]]"
  - "[[Entity Register and Manual Creation]]"
  - "[[Entity Cards and Facts]]"
  - "[[Filing and Identity Decisions]]"
  - "[[Unlink Reassign Merge and Unmerge]]"
  - "[[Review Inbox and Conflict Resolution]]"
---

> [!info] Navigation
> Parent: [[Feature Atlas]]. Sibling hubs: [[Account and Access]] · [[Shell and Navigation]] · [[Capture and Processing]] · [[Documents and Knowledge]] · [[Assistant and Search]] · [[Forms]] · [[Dashboards and Reporting]] · [[Historical Intent]].

# Facts Entities and Review

This family owns entity registration and canonical card facts, filing and identity decisions, unlink and reassignment, merge recovery, and review-inbox handling for conflicts, identity questions, and unfiled material. The family is `partial`: durable reads and mutations work, while fact projections diverge, direct merge/unmerge controls are missing, and several review failure and stale-state paths are confusing.

## Child index

| Capability | Feature | Delivery | Reachability | Summary |
| --- | --- | --- | --- | --- |
| `ENT-01` | [[Entity Register and Manual Creation]] | `partial` | `user-facing` | Kind-filtered live cards and confirmed manual creation are durable, but search/sort/status UI and metadata editing/deletion are absent. |
| `ENT-02` | [[Entity Cards and Facts]] | `partial` | `user-facing` | Live card sections and canonical fact mutation work, while card, canonical, and wallet projections diverge and direct edits can retain unsupported provenance. |
| `ENT-03` | [[Filing and Identity Decisions]] | `partial` | `user-facing` | Immutable mentions, validated filing, bounded questions, constraints, and subject links work; overflow and lease-reaper terminalization have review gaps. |
| `ENT-04`, `ENT-05` | [[Unlink Reassign Merge and Unmerge]] | `partial` | `user-facing` with indirect/backend-only exceptions | Unlink/reassign is directly user-facing; merge is indirect through review, and unmerge is backend-only and snapshot-limited. |
| `REVIEW-01` | [[Review Inbox and Conflict Resolution]] | `partial` | `user-facing` | Typed resolutions and stale locking are durable, but loading/error/refresh/busy/history/focus behavior is incomplete and resolved candidates can still look open. |

## Family boundary

[[Fact Wallet and Verification]] owns the document-snapshot-derived Fakten route; this family owns canonical entity-card facts and their mutation/review contracts. [[Family and Person Cards]] owns the family projection, not person creation or access membership. [[Durable Job State Lease Fencing and Recovery]] and [[Filing Auditor and Policy-Limited Automation]] explain job and auditor internals while preserving the user-visible caps, reachability, and failure gaps recorded here.

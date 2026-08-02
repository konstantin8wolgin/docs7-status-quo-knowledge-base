---
id: feature-atlas
title: Feature Atlas
kind: feature-atlas
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/feature-atlas
capability_ids: []
delivery: partial
reachability: not-applicable
persistence: none
evidence: source-only
parent: "[[INDEX]]"
related:
  - "[[Technical Atlas]]"
  - "[[Rebuild Atlas]]"
  - "[[Account and Access]]"
  - "[[Shell and Navigation]]"
  - "[[Capability Ledger]]"
  - "[[UI Surface Coverage]]"
  - "[[Feature-to-Code Matrix]]"
  - "[[Known Gaps and Non-Capabilities]]"
---

> [!info] Navigation
> Parent: [[INDEX]]. Sibling atlases: [[Technical Atlas]] · [[Rebuild Atlas]].

# Feature Atlas

This atlas organizes current, partial, prototype, absent, and historically planned behavior by the user or operator promise it serves. Family hubs are stable navigation points. All current feature families now link to verified leaves; Historical Intent separately contains narrowly scoped planned-only evidence that is not current behavior or a rebuild requirement.

| Feature family | Capability ownership | Delivery | Reachability | Scope |
| --- | --- | --- | --- | --- |
| [[Account and Access]] | `AUTH-01`–`AUTH-05` | `partial` | `user-facing` with backend/development-only exceptions | Sessions and recovery are user-facing; consent withdrawal, export/deletion UI, role administration, and vault switching remain partial or absent |
| [[Shell and Navigation]] | `SHELL-01`–`SHELL-03` | `partial` | `user-facing` | Twelve responsive hash routes are implemented; overlay/error handling is partial and permission-aware affordances are absent |
| [[Capture and Processing]] | `CAP-01`–`CAP-03` | `partial` | `user-facing` | One-file and sample capture reach durable validation, extraction, filing, bounded polling, saved-needs-review, and results; progress/resume and format/error disclosure remain partial |
| [[Documents and Knowledge]] | `DOC-01`–`DOC-02`, `TASK-01`, `FACT-01`, `DB-01`, `FAMILY-01` | `partial` | `user-facing` | Paginated documents and originals are durable; tasks, fact wallet, client tables, and family cards are constrained projections rather than full management systems |
| [[Facts Entities and Review]] | `ENT-01`–`ENT-05`, `REVIEW-01` | `partial` | `user-facing` with indirect/backend-only exceptions | Register/cards/facts, filing, unlink/reassign, and review are durable; merge is indirect, unmerge backend-only, and projection/review gaps remain |
| [[Assistant and Search]] | `ASSIST-01`–`ASSIST-03` | `partial` | `user-facing` with backend-only direct search | Durable stateless conversation, four-rung scoped answering, document-level citations, abstention, and explicit grounding/polling/recovery limits |
| [[Forms]] | `FORM-01`, `PDF-00` | `prototype` | `user-facing` | Four hardcoded memory-only autofill simulations with flawed counting/source semantics; no integrated PDF viewing, filling, modification, annotation, signature, or output |
| [[Dashboards and Reporting]] | `DASH-01`, `INSIGHT-01`, `HISTORY-01`, `UNDO-00` | `partial` | `user-facing` | Summary navigation, mixed-snapshot derived charts, durable selected activity feed, silent/misleading error states, and no generic undo |
| [[Historical Intent]] | `CIRCLE-00` planned-only | `planned-only` | `not-applicable` | Circles intent and plan-reading containment, explicitly absent from models, migrations, routes, client surface, runtime, and rebuild contract |

## Populated feature routes

- [[Account and Access]] → [[Authentication and Sessions]] · [[Email Verification and Password Reset]] · [[AI Consent]] · [[Account Export Deletion and Development Reset]] · [[Role and Vault Limitations]]
- [[Shell and Navigation]] → [[Navigation and Responsive Shell]] · [[Global Drawers Toasts and Loading]] · [[Permission-Aware Affordance Gaps]]
- [[Capture and Processing]] → [[Capture Inputs and Validation]] · [[Sample Import]] · [[Processing Polling and Capture Results]]
- [[Documents and Knowledge]] → [[Document Library]] · [[Document Detail and Original Files]] · [[Tasks and Deadlines]] · [[Fact Wallet and Verification]] · [[Database Tables]] · [[Family and Person Cards]]
- [[Facts Entities and Review]] → [[Entity Register and Manual Creation]] · [[Entity Cards and Facts]] · [[Filing and Identity Decisions]] · [[Unlink Reassign Merge and Unmerge]] · [[Review Inbox and Conflict Resolution]]
- [[Assistant and Search]] → [[Assistant Conversation and Progress]] · [[Search and Four-Rung Answer Ladder]] · [[Citations Provenance and Abstention]]
- [[Forms]] → [[Form Autofill Prototype]] · [[PDF Viewing Filling and Annotation Boundary]]
- [[Dashboards and Reporting]] → [[Dashboard]] · [[Insights and Derived Metrics]] · [[Activity History and No-Undo Boundary]]
- [[Historical Intent]] → [[Circles Planned Sharing]] · [[Historical Plans Usage Boundary]]

Each populated leaf owns its declared capability IDs and states delivery, reachability, persistence, evidence, limitations, and proof. Hubs and this atlas list capability IDs for navigation but own none in frontmatter. Planned-only leaves remain containment records rather than current implementation specifications.

## Traceability

- [[Capability Ledger]] is the exact 33-ID roll-up of feature-leaf status axes and primary proof.
- [[UI Surface Coverage]] accounts for every reachable destination, global surface, shared component, cache and backend-only or dead UI boundary.
- [[Feature-to-Code Matrix]] follows each capability through client, API, domain, job, schema, tests and current Codebase Map pages.
- [[Known Gaps and Non-Capabilities]] consolidates verified defects and explicit negative boundaries without promoting them to planned work.

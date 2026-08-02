---
id: feature-family-documents-and-knowledge
title: Documents and Knowledge
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
  - "[[Capture and Processing]]"
  - "[[Facts Entities and Review]]"
  - "[[Document Library]]"
  - "[[Document Detail and Original Files]]"
  - "[[Tasks and Deadlines]]"
  - "[[Fact Wallet and Verification]]"
  - "[[Database Tables]]"
  - "[[Family and Person Cards]]"
---

> [!info] Navigation
> Parent: [[Feature Atlas]]. Sibling hubs: [[Account and Access]] · [[Shell and Navigation]] · [[Capture and Processing]] · [[Facts Entities and Review]] · [[Assistant and Search]] · [[Forms]] · [[Dashboards and Reporting]] · [[Historical Intent]].

# Documents and Knowledge

This family owns document discovery and detail, original-file access, summaries and extracted knowledge, tasks and deadlines, fact-wallet behavior, database-style projections, and family and person surfaces. The family is `partial`: durable document reads and core projections exist, while loaded-page search semantics, snapshot/canonical fact divergence, read-only tasks, client-only tables, and family-management absences constrain the current promise.

## Child index

| Capability | Feature | Delivery | Reachability | Summary |
| --- | --- | --- | --- | --- |
| `DOC-01` | [[Document Library]] | `partial` | `user-facing` | The current subject gets a keyset-paginated folder library, but search and sorting cover loaded pages while counts cover the complete result set. |
| `DOC-02` | [[Document Detail and Original Files]] | `partial` | `user-facing` | Hash-addressed detail and authorized encrypted originals are available, with silent fetch gaps and no embedded PDF/TXT viewer or editing. |
| `TASK-01` | [[Tasks and Deadlines]] | `partial` | `user-facing` | Actions and deadlines are ephemeral read-only projections from document fields, not durable Task or Reminder records. |
| `FACT-01` | [[Fact Wallet and Verification]] | `partial` | `user-facing` | Snapshot-derived fact cards can copy, open a source, and durably verify canonical matches, but cards may diverge from canonical counts and values. |
| `DB-01` | [[Database Tables]] | `partial` | `user-facing` | Client-only document and amount/date tables support local search/sort; the facts branch is dead and no query, edit, saved-view, or export contract exists. |
| `FAMILY-01` | [[Family and Person Cards]] | `partial` | `user-facing` | Linked person entities and live cards are visible, including self, but the surface is not member, role, vault, or subject administration. |

## Family boundary

These notes own how durable document knowledge is projected and navigated. Fact/entity conflict resolution belongs to [[Facts Entities and Review]], fact consumption by form prototypes belongs to [[Forms]], and grounded search and citations belong to [[Assistant and Search]]. The links preserve those handoffs without duplicating their contracts here.

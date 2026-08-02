---
id: feature-family-dashboards-and-reporting
title: Dashboards and Reporting
kind: feature-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-01
tags:
  - status-quo/feature-family
capability_ids: []
delivery: partial
reachability: user-facing
persistence: durable
evidence: code-and-tests
parent: "[[Feature Atlas]]"
related:
  - "[[Forms]]"
  - "[[Historical Intent]]"
  - "[[Dashboard]]"
  - "[[Insights and Derived Metrics]]"
  - "[[Activity History and No-Undo Boundary]]"
---

> [!info] Navigation
> Parent: [[Feature Atlas]]. Sibling hubs: [[Account and Access]] · [[Shell and Navigation]] · [[Capture and Processing]] · [[Documents and Knowledge]] · [[Facts Entities and Review]] · [[Assistant and Search]] · [[Forms]] · [[Historical Intent]].

# Dashboards and Reporting

This family owns dashboard summaries, insights and derived metrics, activity history, and explicit current limits such as the absence of undo behavior. It is `partial`: the server summary and selected AuditEvent feed are durable, while dashboard handoff and analytics are client-derived, mixed-snapshot behavior is visible, errors can be silent or misleading, and there is no generic inverse control.

## Child index

| Capability | Feature | Delivery | Reachability | Summary |
| --- | --- | --- | --- | --- |
| `DASH-01` | [[Dashboard]] | `partial` | `user-facing` | Durable summary counts drive greeting, quick navigation, and recent documents; quick-question handoff exists only in memory. |
| `INSIGHT-01` | [[Insights and Derived Metrics]] | `partial` | `user-facing` | Server counts mix with progressively loaded document charts; date, snapshot, settlement, and currency semantics are deliberately limited. |
| `HISTORY-01` | [[Activity History and No-Undo Boundary]] | `implemented` | `user-facing` | A durable readonly, vault-scoped what/why feed supports stable keyset pagination and entity/document links, with client error gaps. |
| `UNDO-00` | [[Activity History and No-Undo Boundary]] | `absent` | `user-facing` | No generic undo/redo or History inverse exists; backend-only unmerge is a distinct narrow operation. |

## Family boundary

[[Dashboard]] owns the landing projection and navigation handoffs. [[Insights and Derived Metrics]] owns ephemeral calculations and chart truth. [[Activity History and No-Undo Boundary]] separately owns the durable selected feed and the explicit absence of generic reversal.

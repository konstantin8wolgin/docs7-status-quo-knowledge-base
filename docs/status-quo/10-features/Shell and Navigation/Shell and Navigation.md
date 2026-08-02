---
id: feature-family-shell-and-navigation
title: Shell and Navigation
kind: feature-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/feature-family
capability_ids: []
delivery: partial
reachability: user-facing
persistence: session-memory
evidence: code-and-tests
parent: "[[Feature Atlas]]"
related:
  - "[[Account and Access]]"
  - "[[Capture and Processing]]"
  - "[[Navigation and Responsive Shell]]"
  - "[[Global Drawers Toasts and Loading]]"
  - "[[Permission-Aware Affordance Gaps]]"
---

> [!info] Navigation
> Parent: [[Feature Atlas]]. Sibling hubs: [[Account and Access]] · [[Capture and Processing]] · [[Documents and Knowledge]] · [[Facts Entities and Review]] · [[Assistant and Search]] · [[Forms]] · [[Dashboards and Reporting]] · [[Historical Intent]].

# Shell and Navigation

This family owns the responsive application shell, hash and browser navigation, global drawers and review surfaces, toasts and loading states, and gaps between visible affordances and effective permissions. Navigation is implemented; the family remains `partial` because global failure/accessibility handling is incomplete and client affordances are not permission-aware.

## Child index

| Capability | Feature | Delivery | Reachability | Summary |
| --- | --- | --- | --- | --- |
| `SHELL-01` | [[Navigation and Responsive Shell]] | `implemented` | `user-facing` | Twelve hash-routed destinations stay Back/Forward safe across desktop, tablet rail, and mobile tab-bar layouts. |
| `SHELL-02` | [[Global Drawers Toasts and Loading]] | `partial` | `user-facing` | Document and review drawers, transient toasts, and blocking loaders exist, with silent error and accessibility gaps. |
| `SHELL-03` | [[Permission-Aware Affordance Gaps]] | `absent` | `user-facing` | The client has no role/capability projection, so readonly and production users see controls the backend rejects. |

## Family boundary

`StoreProvider` owns navigation, summary state, document cache coordination, global overlays, and transient feedback after [[Authentication and Sessions]] admits a user. Individual feature views own their local workflow state and are documented under their respective families.

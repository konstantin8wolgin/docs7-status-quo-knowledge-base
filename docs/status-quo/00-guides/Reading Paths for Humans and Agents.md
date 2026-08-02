---
id: guide-reading-paths
title: Reading Paths for Humans and Agents
kind: guide
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/guide
parent: "[[INDEX]]"
related:
  - "[[How to Use This Knowledge Base]]"
  - "[[Truth and Status Model]]"
  - "[[Snapshot and Evidence Manifest]]"
---

> [!info] Navigation
> Parent: [[INDEX]]. Siblings: [[How to Use This Knowledge Base]] · [[Truth and Status Model]] · [[Snapshot and Evidence Manifest]].

# Reading Paths for Humans and Agents

Use the shortest path that reaches evidence appropriate to the task.

| Task | Short reading path | Stop condition |
| --- | --- | --- |
| Discover a product capability | [[INDEX]] → [[Feature Atlas]] → feature-family hub → populated feature leaf | The leaf names behavior, status, limitations, and proof |
| Explain an implementation boundary | [[INDEX]] → [[Technical Atlas]] → technical-family hub → populated technical leaf → Codebase Map page → source symbol | Ownership, control flow, and relevant tests are explicit |
| Prepare a clean-room rebuild | [[INDEX]] → [[Rebuild Atlas]] → [[Cross-Layer Invariants]] → [[Dependency-Ordered Rebuild Sequence]] → [[Acceptance and Equivalence Proof]] | Dependencies, preserved behavior, approved divergences, and proof are named |
| Audit coverage | [[INDEX]] → [[Snapshot and Evidence Manifest]] → [[Capability Ledger]] / [[UI Surface Coverage]] / [[Contract Coverage]] / [[Feature-to-Code Matrix]] | Every capability, surface, current inventory ID and explicit gap is accounted for |

## Focused agent routes

- To document a user control, enter through the owning feature family and follow only the client component, API method, route, model or job, and tests named by that leaf.
- To trace an API request, enter through the owning technical family, then follow the route inventory ID into its Map subsystem or flow and exact symbols.
- To investigate persistence, pair the relevant feature leaf with [[Data and Migrations]] and the subsystem that owns the write.
- To verify a limitation, find both the visible or callable boundary and the absence proof; do not substitute a plan describing future behavior.

All feature and technical family hubs now link to their verified leaves. Use [[Known Gaps and Non-Capabilities]] for negative-space review and the strict checker in [[Snapshot and Evidence Manifest]] for structural completeness.

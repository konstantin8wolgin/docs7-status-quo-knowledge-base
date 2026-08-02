---
id: feature-family-assistant-and-search
title: Assistant and Search
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
  - "[[Facts Entities and Review]]"
  - "[[Forms]]"
  - "[[Assistant Conversation and Progress]]"
  - "[[Search and Four-Rung Answer Ladder]]"
  - "[[Citations Provenance and Abstention]]"
---

> [!info] Navigation
> Parent: [[Feature Atlas]]. Sibling hubs: [[Account and Access]] · [[Shell and Navigation]] · [[Capture and Processing]] · [[Documents and Knowledge]] · [[Facts Entities and Review]] · [[Forms]] · [[Dashboards and Reporting]] · [[Historical Intent]].

# Assistant and Search

This family owns assistant conversation and progress, search and the four-rung answer ladder, read-only tool use, citations and provenance, abstention, and observable limits in memory and conversation management. It is `partial`: messages/runs are durable and answers are scoped, but prior turns are not answer context, direct search has no client surface, polling is locally unbounded, and document-level citations do not prove claim grounding.

## Child index

| Capability | Feature | Delivery | Reachability | Summary |
| --- | --- | --- | --- | --- |
| `ASSIST-01` | [[Assistant Conversation and Progress]] | `partial` | `user-facing` | Durable per-person messages and jobs expose progress, while answers are stateless across turns and polling/concurrency/consent recovery retain lossy edges. |
| `ASSIST-02` | [[Search and Four-Rung Answer Ladder]] | `partial` | `user-facing` with backend-only direct search | Cards, four fixed tools, transcript search, and original inspection are scoped rungs; PostgreSQL and SQLite differ and no direct search UI exists. |
| `ASSIST-03` | [[Citations Provenance and Abstention]] | `partial` | `user-facing` | Citation IDs are scope-guarded and titles canonicalized, but evidence membership, claim support, page/quote anchors, and nonempty citations are not enforced. |

## Family boundary

[[Assistant Conversation and Progress]] owns submission, durable message/job state, polling, and access-gate recovery. [[Search and Four-Rung Answer Ladder]] owns retrieval and tool execution. [[Citations Provenance and Abstention]] owns what the resulting source metadata and outcomes do—and do not—prove. Historical Circle search intent remains isolated in [[Circles Planned Sharing]].

---
id: guide-how-to-use-status-quo
title: How to Use This Knowledge Base
kind: guide
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-01
tags:
  - status-quo/guide
parent: "[[INDEX]]"
related:
  - "[[Truth and Status Model]]"
  - "[[Reading Paths for Humans and Agents]]"
  - "[[Snapshot and Evidence Manifest]]"
---

> [!info] Navigation
> Parent: [[INDEX]]. Siblings: [[Truth and Status Model]] · [[Reading Paths for Humans and Agents]] · [[Snapshot and Evidence Manifest]].

# How to Use This Knowledge Base

Use this corpus as a navigation and reconstruction aid, not as an authority that outranks the repository. Begin with the reader path matching the question, follow links until a note names exact evidence, and stop when the claim is proven at the required depth.

## Evidence citations

Name repository-relative paths and stable symbols, never line numbers. A useful citation identifies both the claim source and the proof boundary:

- implementation: `backend/app/main.py` → `create_app`;
- behavior proof: `backend/tests/test_security_adversarial.py` → the relevant named test;
- generated contract: `docs/api/openapi.json` → the operation or schema name;
- structural inventory: `docs/map/inventory/inventory.json` → the exact inventory ID.

Do not copy credentials, environment values, raw transcripts, private documents, plaintext keys, sensitive prompt content, or golden-corpus material into a note. Configuration notes name variables and semantics only.

## Common note template

```yaml
---
id: stable-kebab-case-id
title: Human-readable unique title
kind: guide
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: YYYY-MM-DD
tags:
  - status-quo/guide
parent: "[[Parent Note]]"
related:
  - "[[Sibling Note]]"
---
```

Every note opens with explicit parent and sibling navigation. Keep every basename, `id`, and human-readable `title` unique across the corpus. Use Obsidian wikilinks for relationships between status-quo notes.

## Feature-note additions

```yaml
capability_ids:
  - FAMILY-01
delivery: implemented
reachability: user-facing
persistence: durable
evidence: code-and-tests
```

A feature leaf states the promise, entry point, preconditions, controls, transitions, persistence, failures, trust boundaries, limitations, rebuild obligations, and exact proof. Control-heavy behavior uses a table with `Control`, `Visible when`, `Input`, `Action`, `Result`, `Persistence`, and `Failure behavior` columns. Use a Mermaid state diagram when prose would hide a transition.

## Technical-note additions

```yaml
map_pages:
  - subsystem:example
inventory_refs:
  - route:GET:/api/example
feature_links:
  - FAMILY-01
```

A technical leaf states ownership, entry points, dependencies, stored state, control flow, trust boundaries, concurrency and rollback behavior, configuration semantics, failure and recovery, deployment differences, tests, known drift, and rebuild ordering. Cite symbols rather than line numbers.

## Authoring discipline

Keep one claim in one owning note and link to it elsewhere. Use tables for exact mappings and Mermaid for relationships or state transitions that become harder to scan as prose. Keep indexes concise: summaries and links belong there; detailed implementation evidence belongs in leaf notes.

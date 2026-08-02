---
id: guide-truth-and-status-model
title: Truth and Status Model
kind: guide
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-01
tags:
  - status-quo/guide
parent: "[[INDEX]]"
related:
  - "[[How to Use This Knowledge Base]]"
  - "[[Reading Paths for Humans and Agents]]"
  - "[[Snapshot and Evidence Manifest]]"
---

> [!info] Navigation
> Parent: [[INDEX]]. Siblings: [[How to Use This Knowledge Base]] · [[Reading Paths for Humans and Agents]] · [[Snapshot and Evidence Manifest]].

# Truth and Status Model

## Truth order

When sources disagree, use this order and correct stale lower layers in the same documentation change:

1. executable code, tests, migrations, configuration, and generated contracts;
2. deterministic inventory generated from those sources;
3. curated Codebase Map pages;
4. architecture decision records;
5. progress notes and plans as historical evidence only.

The snapshot commit fixes which executable behavior this corpus describes. A prose assertion without source or proof never outranks the executable layer.

## Four independent status axes

No single label is allowed to hide delivery, access, state lifetime, or evidence strength.

| Axis | Exact values | Question answered |
| --- | --- | --- |
| Delivery | `implemented`, `partial`, `prototype`, `planned-only`, `absent` | How much behavior actually exists? |
| Reachability | `user-facing`, `development-only`, `backend-only`, `dead-or-unreachable`, `not-applicable` | Who or what can reach it today? |
| Persistence | `durable`, `session-memory`, `ephemeral`, `none` | Where and for how long does its state survive? |
| Evidence | `runtime-code-tests`, `code-and-tests`, `source-only`, `historical-only` | How strongly is the claim proven? |

These axes are orthogonal. For example, a user-visible prototype can be session-only and source-only, while a backend-only capability can be durable and covered by code and tests. Explain mixed status in prose rather than selecting a falsely reassuring value.

## Historical isolation

> [!danger] Historical intent is not the rebuild contract
> Planned-only behavior belongs under [[Historical Intent]] with a prominent warning. It must not be described as current, silently included in clean-room requirements, or used to override executable evidence.

Circles and every other planned-only idea remain historical. Forms remain a client-only prototype: the current workflow does not generate, change, sign, annotate, print, or download a PDF. Undo, drawing or annotation, integrated PDF editing, and other verified absences are current non-capabilities and must be stated explicitly rather than omitted.

## Resolving uncertainty

Record what is known, label the evidence level honestly, and cite the symbol or test that would settle the remaining question. Never promote a historical plan to current behavior merely because executable evidence is incomplete.

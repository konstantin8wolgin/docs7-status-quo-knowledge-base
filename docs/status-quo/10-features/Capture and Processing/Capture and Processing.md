---
id: feature-family-capture-and-processing
title: Capture and Processing
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
  - "[[Shell and Navigation]]"
  - "[[Documents and Knowledge]]"
  - "[[Capture Inputs and Validation]]"
  - "[[Sample Import]]"
  - "[[Processing Polling and Capture Results]]"
---

> [!info] Navigation
> Parent: [[Feature Atlas]]. Sibling hubs: [[Account and Access]] · [[Shell and Navigation]] · [[Documents and Knowledge]] · [[Facts Entities and Review]] · [[Assistant and Search]] · [[Forms]] · [[Dashboards and Reporting]] · [[Historical Intent]].

# Capture and Processing

This family owns capture inputs and validation, bundled sample import, upload and trust gates, processing and filing progress, polling and retry behavior, and the handoff from a capture result into durable knowledge surfaces. The family is `partial`: durable upload, sample, job, and filing behavior works, while format disclosure, progress truthfulness, resume discovery, and several failure states remain incomplete.

## Child index

| Capability | Feature | Delivery | Reachability | Summary |
| --- | --- | --- | --- | --- |
| `CAP-01` | [[Capture Inputs and Validation]] | `partial` | `user-facing` | One-file drop, native, and camera capture reach hardened server validation, but picker/visible format promises do not match the backend allowlist. |
| `CAP-02` | [[Sample Import]] | `implemented` | `user-facing` | Vault-scoped repository samples are enumerated, validated, deduplicated, and imported through the normal durable pipeline. |
| `CAP-03` | [[Processing Polling and Capture Results]] | `partial` | `user-facing` | Durable extraction/filing jobs, bounded polling, same-job recheck, failures, saved-needs-review, and result handoff work, while visible stages and resume state remain client-only. |

## Family boundary

This family ends when Capture hands a completed document ID or derived preview to another route. [[Document Detail and Original Files]] owns the durable document/original surface, [[Fact Wallet and Verification]] owns later fact confirmation, and [[Tasks and Deadlines]] owns the read-only action/deadline projection. Filing conflicts and saved-needs-review questions link to the existing Postfach rather than creating a fourth capture capability.

---
id: feature-family-account-and-access
title: Account and Access
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
  - "[[Historical Intent]]"
  - "[[Authentication and Sessions]]"
  - "[[Email Verification and Password Reset]]"
  - "[[AI Consent]]"
  - "[[Account Export Deletion and Development Reset]]"
  - "[[Role and Vault Limitations]]"
---

> [!info] Navigation
> Parent: [[Feature Atlas]]. Sibling hubs: [[Shell and Navigation]] · [[Capture and Processing]] · [[Documents and Knowledge]] · [[Facts Entities and Review]] · [[Assistant and Search]] · [[Forms]] · [[Dashboards and Reporting]] · [[Historical Intent]].

# Account and Access

This family owns the product-facing account lifecycle and its trust gates: authentication and sessions, email verification and password recovery, verified AI consent, backend account export and deletion, and the observable limits of roles and vault membership. The family is `partial`: sign-up, sign-in, recovery, and consent grant are user-facing, while account administration, consent withdrawal, role management, and vault switching have no client surface.

## Child index

| Capability | Feature | Delivery | Reachability | Summary |
| --- | --- | --- | --- | --- |
| `AUTH-01` | [[Authentication and Sessions]] | `implemented` | `user-facing` | Credential forms create or resume a durable cookie session; development builds may auto-login configured demo credentials. |
| `AUTH-02` | [[Email Verification and Password Reset]] | `implemented` | `user-facing` | Fragment-token verification and atomic password recovery use expiring, single-use server records. |
| `AUTH-03` | [[AI Consent]] | `partial` | `user-facing` | Capture and Assistant can grant per-user consent and preserve pending work; withdrawal is backend-only. |
| `AUTH-04` | [[Account Export Deletion and Development Reset]] | `partial` | `backend-only` | Export and deletion are complete APIs without settings UI; reset is a development-only owner operation exposed by an unconditional shell button. |
| `AUTH-05` | [[Role and Vault Limitations]] | `partial` | `backend-only` | Server-side roles and tenant isolation work, but the client receives neither role nor vault-choice state. |

## Family boundary

Authentication establishes identity; `resolve_context` then selects one membership and supplies vault, subject, and role to product routes. [[Shell and Navigation]] owns what the client exposes after that boundary, including the permission-awareness gaps documented in [[Permission-Aware Affordance Gaps]].

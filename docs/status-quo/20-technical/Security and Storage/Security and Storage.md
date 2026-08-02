---
id: technical-family-security-and-storage
title: Security and Storage
kind: technical-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical-family
map_pages:
  - subsystem:auth-vault-consent
  - flow:auth-vault-context
  - flow:consent-provider-fallback
  - subsystem:files-crypto-storage
  - flow:encrypted-file-read
  - subsystem:gdpr-account
  - flow:account-export-deletion
inventory_refs:
  - route:POST:/api/auth/login
  - route:GET:/api/auth/me
  - route:POST:/api/upload
  - route:GET:/api/file/{document_id}
  - route:GET:/api/account/export
  - route:DELETE:/api/account
  - model:AuthSession
  - model:VaultMember
  - model:VaultKey
  - model:FileObject
  - migration:0002
  - migration:0004
feature_links:
  - AUTH-01
  - AUTH-02
  - AUTH-03
  - AUTH-04
  - AUTH-05
  - CAP-01
  - CAP-02
  - CAP-03
  - DOC-01
  - DOC-02
parent: "[[Technical Atlas]]"
related:
  - "[[Jobs and AI]]"
  - "[[Runtime and Operations]]"
---

> [!info] Navigation
> Parent: [[Technical Atlas]]. Sibling hubs: [[System Architecture]] · [[Client Architecture]] · [[Backend and API]] · [[Data and Migrations]] · [[Jobs and AI]] · [[Runtime and Operations]].

# Security and Storage

This family owns identity, session, membership, consent, and vault-scope boundaries; encryption key hierarchy and object storage; and upload, download, quota, serving, and erasure behavior.

## Child index

| Leaf | Owns |
| --- | --- |
| [[Identity Sessions Membership and Vault Scope]] | Opaque sessions, implicit membership context, role enforcement, browser request defenses, consent and plaintext-derived-data limits |
| [[Encryption Key Hierarchy and Object Storage]] | AES-GCM envelope hierarchy, local/S3 adapters, integrity semantics, provider metadata drift and key rotation limits |
| [[Upload Download Quota and Erasure]] | Validated intake, plaintext/ciphertext buffering, quota races, safe serving, split DB/object transactions and physical-erasure gaps |

Read the three leaves together for a trust review: identity establishes who and which vault may act; encryption explains how original bytes and keys cross persistence boundaries; upload/download/erasure explains lifecycle, concurrency and recovery behavior. [[Runtime and Operations]] owns configuration, deployment, readiness, observability and release proof around those controls.

---
id: traceability-contract-coverage
title: Contract Coverage
kind: traceability
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/traceability
  - status-quo/contracts
parent: "[[INDEX]]"
related:
  - "[[Capability Ledger]]"
  - "[[UI Surface Coverage]]"
  - "[[Feature-to-Code Matrix]]"
  - "[[Known Gaps and Non-Capabilities]]"
  - "[[Dependency-Ordered Rebuild Sequence]]"
---

> [!info] Navigation
> Parent: [[INDEX]]. Siblings: [[Capability Ledger]] · [[UI Surface Coverage]] · [[Feature-to-Code Matrix]] · [[Known Gaps and Non-Capabilities]].

# Contract Coverage

This ledger adds semantic ownership and rebuild relevance to every raw ID currently present in `docs/map/inventory/inventory.json`. Its first column contains exactly 185 unique inventory IDs: 39 routes, 31 client methods, 32 models, 5 jobs, 11 migrations, 2 classified unknowns and 65 tests.

The generated inventory has no generation timestamp or source-commit field, so none is inferred here. The 65 tests are 47 backend files plus 18 client files. The product snapshot had 63; `test:backend/tests/test_status_quo.py` and `test:client/src/status-quo-mermaid.test.mjs` are later corpus-proof tests that bring the documentation branch inventory to 65.

Rebuild stages refer to [[Dependency-Ordered Rebuild Sequence]]. Missing generated relations are not treated as absence: clientapi:listEntities is manually paired with the entity-list route, `fileUrl` and sample `thumbUrl` account for the two indirect binary routes, and the generic DELETE-account test call is manually associated with account deletion.

## Routes — 39

| Inventory ID | Semantic ownership | Feature consumer or reachability | Technical note | Rebuild stage and relevance |
| --- | --- | --- | --- | --- |
| route:DELETE:/api/account | password-confirmed account erasure | `AUTH-04`; backend-only | [[Data Lifecycle Reset Export and Deletion]] | 11 — preserve owned/shared-vault split and cryptographic-before-physical erasure |
| route:DELETE:/api/auth/ai-consent | per-user AI-consent withdrawal | `AUTH-03`; backend-only | [[Identity Sessions Membership and Vault Scope]] | 3 — revoke before future provider work without forging another user |
| route:GET:/api/account/export | owner-scoped portable export subset | `AUTH-04`; backend-only | [[Data Lifecycle Reset Export and Deletion]] | 11 — version the supported subset and retain owner authorization |
| route:GET:/api/activity | selected readonly audit-event feed | `HISTORY-01` | [[Complete API Contract]] | 8 — preserve vault scope and stable keyset order |
| route:GET:/api/auth/me | session restoration and user projection | `AUTH-01` | [[Identity Sessions Membership and Vault Scope]] | 3 — server derives identity and active subject context |
| route:GET:/api/documents | scoped document library | `DOC-01`; also Dashboard/Fakten/Database/Forms/Insights | [[Complete API Contract]] | 5 — preserve current/all scope, failed exclusion and keyset paging |
| route:GET:/api/documents/{document_id} | scoped document detail projection | `DOC-02` | [[Complete API Contract]] | 5 — preserve vault-hiding lookup and stored extraction projection |
| route:GET:/api/entities | live entity register and filters | `ENT-01`, `FAMILY-01`; manual client relation | [[Complete API Contract]] | 8 — preserve vault/person filtering and stable ordering |
| route:GET:/api/entities/{entity_id} | canonical survivor card | `ENT-02`, `FAMILY-01` | [[Complete API Contract]] | 8 — preserve redirect, facts, documents and conflict projection |
| route:GET:/api/file/{document_id} | authorized decrypted original | `DOC-02`, `PDF-00`; indirect `fileUrl` | [[Upload Download Quota and Erasure]] | 4 — authorize before storage access and authenticate ciphertext |
| route:GET:/api/health | process liveness | backend-only operations | [[Local and Production Runtime Topology]] | 12 — retain liveness distinction; do not confuse it with dependency readiness |
| route:GET:/api/jobs/{job_id} | scoped durable-job status | `CAP-03`; composite capture methods | [[Durable Job State Lease Fencing and Recovery]] | 6 — expose durable stage/terminal state without mutating on poll |
| route:GET:/api/messages | durable person transcript | `ASSIST-01`, `ASSIST-03` | [[Search and Answer Agent Internals]] | 9 — preserve person/vault scope and pending/completed/failed rows |
| route:GET:/api/ready | API database readiness probe | backend-only operations | [[Local and Production Runtime Topology]] | 12 — current `SELECT 1` check must be strengthened deliberately |
| route:GET:/api/review-items | open typed review work | `REVIEW-01` | [[Filing Auditor and Policy-Limited Automation]] | 8 — preserve stable finding identities and vault scope |
| route:GET:/api/samples | allowlisted sample catalog | `CAP-02` | [[Complete API Contract]] | 5 — separate empty, error and safe catalog semantics |
| route:GET:/api/samples/file/{name} | allowlisted sample bytes | `CAP-02`; indirect returned `thumbUrl` | [[Complete API Contract]] | 5 — preserve basename isolation and truthful media response |
| route:GET:/api/search | latest-run scoped transcript retrieval | `ASSIST-02`; backend-only direct search | [[Search and Answer Agent Internals]] | 9 — retain dialect-qualified, person/vault-scoped retrieval |
| route:GET:/api/summary | account/person summary projection | `DASH-01`, `TASK-01`, shell badges, `INSIGHT-01` | [[Complete API Contract]] | 8 — preserve exact action/deadline/count semantics |
| route:POST:/api/auth/ai-consent | per-user consent grant | `AUTH-03` | [[Identity Sessions Membership and Vault Scope]] | 3 — prerequisite for provider-dependent work only |
| route:POST:/api/auth/login | credential authentication and session mint | `AUTH-01` | [[Identity Sessions Membership and Vault Scope]] | 3 — generic failure, rate limit and opaque session contract |
| route:POST:/api/auth/logout | current-session revocation | `AUTH-01` | [[Identity Sessions Membership and Vault Scope]] | 3 — replay-safe revocation and cookie clearing |
| route:POST:/api/auth/password-reset/confirm | atomic reset-token claim and password change | `AUTH-02` | [[Identity Sessions Membership and Vault Scope]] | 3 — single use, sibling invalidation and all-session revocation |
| route:POST:/api/auth/password-reset/request | privacy-preserving reset request | `AUTH-02` | [[Complete API Contract]] | 3 — keep account existence and delivery failure indistinguishable |
| route:POST:/api/auth/signup | transactional account/vault/session bootstrap | `AUTH-01` | [[Router Domain and Infrastructure Boundaries]] | 3 — preserve atomic identity graph and rollback on mail failure |
| route:POST:/api/auth/verify-email | atomic verification-token claim | `AUTH-02` | [[Complete API Contract]] | 3 — preserve purpose, expiry, locking and latest-link semantics |
| route:POST:/api/auth/verify-email/request | authenticated verification resend | `AUTH-02` | [[Complete API Contract]] | 3 — preserve per-user scope and rate/delivery contract |
| route:POST:/api/chat | durable asynchronous question admission | `ASSIST-01`–`ASSIST-03` | [[Search and Answer Agent Internals]] | 9 — commit user/pending rows and job before background work |
| route:POST:/api/entities | confirmed manual entity creation | `ENT-01` | [[Complete API Contract]] | 8 — preserve normalized identifiers and owner-conflict recovery |
| route:POST:/api/entities/merge | atomic direct merge | `ENT-05`; backend-only direct path | [[Filing Auditor and Policy-Limited Automation]] | 8 — preserve survivor, constraints, moved rows and snapshot event |
| route:POST:/api/entities/{entity_id}/confirm | entity confirmation | `ENT-02` | [[Complete API Contract]] | 8 — preserve vault scope and replay-safe status transition |
| route:POST:/api/entities/{entity_id}/facts | manual canonical fact/revision creation | `ENT-02` | [[Extraction Envelope Evidence and Provenance]] | 8 — preserve revision/provenance and uniqueness authority |
| route:POST:/api/entities/{entity_id}/unlink | pair-wide unlink or reassignment | `ENT-04` | [[Filing Auditor and Policy-Limited Automation]] | 8 — retain canonical-subject block and durable removed-pair guard |
| route:POST:/api/entities/{entity_id}/unmerge | LIFO merge recovery | `ENT-05`; backend-only | [[Filing Auditor and Policy-Limited Automation]] | 8 — preserve exact snapshot restoration limits |
| route:POST:/api/facts/{fact_id}/verify | canonical fact verification/revision | `FACT-01`, `ENT-02` | [[Extraction Envelope Evidence and Provenance]] | 8 — protect verified values from machine overwrite |
| route:POST:/api/reset | development-only vault content reset | `AUTH-04`; visible only in development route set | [[Data Lifecycle Reset Export and Deletion]] | 11 — preserve environment exclusion and exact retained identity shell |
| route:POST:/api/review-items/{item_id}/resolve | typed conflict/identity/unfiled resolution | `REVIEW-01`; indirect `ENT-05` merge | [[Filing Auditor and Policy-Limited Automation]] | 8 — preserve evidence revalidation and single-winner mutation |
| route:POST:/api/samples/import | idempotent sample admission | `CAP-02`, `CAP-03` | [[Complete API Contract]] | 5 — preserve 200 reuse versus 202 created job semantics |
| route:POST:/api/upload | validated encrypted upload and durable job admission | `CAP-01`, `CAP-03` | [[Upload Download Quota and Erasure]] | 5 — validate, encrypt and commit job with compensation boundaries |

## Client methods — 31

| Inventory ID | Semantic ownership | Feature consumer or reachability | Technical note | Rebuild stage and relevance |
| --- | --- | --- | --- | --- |
| clientapi:activity | paged activity adapter | `HISTORY-01` | [[Client API Permissions and Failure Contract]] | 10 — preserve cursor/query and normalized failure behavior |
| clientapi:chat | question admission adapter | `ASSIST-01`–`ASSIST-03` | [[Client API Permissions and Failure Contract]] | 10 — distinguish accepted durable work from ambiguous failure |
| clientapi:confirmEntity | entity confirmation adapter | `ENT-02` | [[Client API Permissions and Failure Contract]] | 10 — mutation is replay-safe but still authorization-gated |
| clientapi:confirmPasswordReset | reset-token mutation adapter | `AUTH-02` | [[Client API Permissions and Failure Contract]] | 10 — fragment token becomes request data only at explicit submit |
| clientapi:createEntity | manual entity-create adapter | `ENT-01` | [[Client API Permissions and Failure Contract]] | 10 — preserve full normalized request contract and conflict detail |
| clientapi:createEntityFact | manual fact-create adapter | `ENT-02` | [[Client API Permissions and Failure Contract]] | 10 — carry typed value/source into canonical revision flow |
| clientapi:document | detail fetch adapter | `DOC-02` and global drawer | [[Client API Permissions and Failure Contract]] | 10 — add explicit load/error recovery without weakening scoping |
| clientapi:entityCard | entity card fetch adapter | `ENT-02`, `FAMILY-01` | [[Client API Permissions and Failure Contract]] | 10 — preserve selected-card live refresh and survivor redirect |
| clientapi:importSample | primitive sample mutation | `CAP-02` | [[Client API Permissions and Failure Contract]] | 10 — expose both reuse and created-job responses |
| clientapi:importSampleAndWait | composite sample admission plus bounded polling | `CAP-02`, `CAP-03` | [[Client State Navigation and Cache]] | 10 — client composite; no separate server route |
| clientapi:job | job-status poll adapter | `CAP-03`; composite capture methods | [[Client API Permissions and Failure Contract]] | 10 — poll is scoped, readonly and nonmutating |
| clientapi:listDocuments | current/all paged document adapter | `DOC-01`, Dashboard/Fakten/Database/Forms/Insights | [[Client State Navigation and Cache]] | 10 — preserve scope parameter, cursor and cache compatibility |
| clientapi:listEntities | entity list adapter with optional query | `ENT-01`, `FAMILY-01`; manual route reconciliation | [[Client API Permissions and Failure Contract]] | 10 — generated relation is a false negative, not backend absence |
| clientapi:listReviewItems | review-list adapter | `REVIEW-01` | [[Client API Permissions and Failure Contract]] | 10 — loading/error states need separation in rebuilt drawer |
| clientapi:login | login adapter | `AUTH-01` | [[Client API Permissions and Failure Contract]] | 10 — credentialed same-origin request and typed machine errors |
| clientapi:logout | logout adapter | `AUTH-01` | [[Client API Permissions and Failure Contract]] | 10 — clear identity on confirmed or global unauthorized transition |
| clientapi:me | account bootstrap adapter | `AUTH-01` | [[Client API Permissions and Failure Contract]] | 10 — single source for signed-in identity, not role inference |
| clientapi:messages | whole-list transcript adapter | `ASSIST-01`, `ASSIST-03` | [[Client State Navigation and Cache]] | 10 — rebuild should correlate polling without inventing context memory |
| clientapi:requestEmailVerification | resend adapter | `AUTH-02` | [[Client API Permissions and Failure Contract]] | 10 — surface real delivery outcome deliberately |
| clientapi:requestPasswordReset | privacy-preserving request adapter | `AUTH-02` | [[Client API Permissions and Failure Contract]] | 10 — retain generic success copy for account-existence privacy |
| clientapi:reset | development reset adapter | `AUTH-04`; shell control | [[Client API Permissions and Failure Contract]] | 10 — environment-only mutation with visible failure handling |
| clientapi:resolveReviewItem | typed review mutation adapter | `REVIEW-01`, indirect `ENT-05` | [[Client API Permissions and Failure Contract]] | 10 — prevent duplicate submits and refresh stale work explicitly |
| clientapi:samples | sample catalog adapter | `CAP-02` | [[Client API Permissions and Failure Contract]] | 10 — distinguish empty from failed and retain safe returned URLs |
| clientapi:setAiConsent | grant-only consent adapter | `AUTH-03` | [[Client API Permissions and Failure Contract]] | 10 — preserved blocked operation retries only after confirmed grant |
| clientapi:signup | signup adapter | `AUTH-01` | [[Client API Permissions and Failure Contract]] | 10 — normalized conflict/delivery errors and credential transition |
| clientapi:summary | shared summary adapter | `DASH-01`, `TASK-01`, shell, `INSIGHT-01` | [[Client State Navigation and Cache]] | 10 — one provider-owned snapshot with explicit failure/staleness |
| clientapi:unlinkEntity | unlink/reassign adapter | `ENT-04` | [[Client API Permissions and Failure Contract]] | 10 — disclose pair-wide effect and preserve structured errors |
| clientapi:upload | primitive multipart upload | `CAP-01`, `CAP-03` | [[Client API Permissions and Failure Contract]] | 10 — do not replay ambiguous writes automatically |
| clientapi:uploadAndWait | composite upload plus bounded polling | `CAP-01`, `CAP-03` | [[Client State Navigation and Cache]] | 10 — client composite; preserve timeout as nonmutating outcome |
| clientapi:verifyEmail | verification-token claim adapter | `AUTH-02` | [[Client API Permissions and Failure Contract]] | 10 — token route owns pending/success/error presentation |
| clientapi:verifyFact | canonical verification adapter | `FACT-01`, `ENT-02`; dead Database caller is invalid | [[Client API Permissions and Failure Contract]] | 10 — require explicit value and serialize duplicate clicks |

## Models — 32

| Inventory ID | Semantic ownership | Feature consumer or classification | Technical note | Rebuild stage and relevance |
| --- | --- | --- | --- | --- |
| model:AuditEvent | selected product history and security/business audit facts | `HISTORY-01`; cross-cutting structural record | [[Domain Model and Relationships]] | 1 — retain vault/time ordering and nullable actor/subject/document links |
| model:AuditRun | one nightly auditor execution and budgets/outcomes | `REVIEW-01`; backend automation | [[Filing Auditor and Policy-Limited Automation]] | 1 — retain per-vault/day state and terminal failure evidence |
| model:AuthSession | opaque browser session digest and fixed expiry | `AUTH-01` | [[Identity Sessions Membership and Vault Scope]] | 1 — preserve hash-only secret storage, revocation and non-sliding expiry |
| model:AuthToken | purpose-scoped verification/reset token digest | `AUTH-02` | [[Identity Sessions Membership and Vault Scope]] | 1 — preserve expiry, single-use claim and sibling invalidation data |
| model:ChatRun | durable answer-ladder run/provenance | `ASSIST-01`–`ASSIST-03` | [[Search and Answer Agent Internals]] | 1 — retain rung/outcome/tool metadata while strengthening evidence membership |
| model:Document | extracted document projection and subject context | `CAP-01`–`CAP-03`, `DOC-01`, `DOC-02`; many readonly views | [[Domain Model and Relationships]] | 1 — aggregate root for file, runs, snapshots and filing |
| model:DocumentAmount | immutable current-envelope amount projection | `TASK-01`, Database, Insights, Assistant tools | [[Extraction Envelope Evidence and Provenance]] | 1 — preserve document-owned typed value/label/currency fields |
| model:DocumentDate | immutable current-envelope date projection | `TASK-01`, Database, Insights, Assistant tools | [[Extraction Envelope Evidence and Provenance]] | 1 — preserve document-owned date/label projection, not a task record |
| model:DocumentEntity | durable document/entity/role association | `FAMILY-01`, `ENT-02`–`ENT-05` | [[Domain Model and Relationships]] | 1 — preserve vault, pair and role semantics plus unlink/reassignment scope |
| model:DocumentTag | current extraction tag projection | document detail and search context | [[Extraction Envelope Evidence and Provenance]] | 1 — replace on successful authoritative extraction only |
| model:DocumentTrustFlag | current extraction trust-warning projection | document detail/review evidence | [[Extraction Envelope Evidence and Provenance]] | 1 — retain severity/label/explanation projection |
| model:Entity | canonical knowledge card and survivor redirect | `ENT-01`–`ENT-05`, `FAMILY-01`, `REVIEW-01` | [[Domain Model and Relationships]] | 1 — preserve kind/origin/status and redirect/no-self invariant |
| model:EntityConstraint | directed durable identity decision | `ENT-03`–`ENT-05`, `REVIEW-01` | [[Filing Auditor and Policy-Limited Automation]] | 1 — retain `not_same` and removed-link guards with unique directed pairs |
| model:EntityEvent | merge/unmerge and entity mutation evidence | `ENT-04`, `ENT-05`; not generic undo | [[Domain Model and Relationships]] | 1 — retain exact snapshots needed for narrow LIFO recovery |
| model:EntityIdentifier | normalized vault-scoped identifier ownership | `ENT-01`, `ENT-03`, `ENT-05` | [[Filing Auditor and Policy-Limited Automation]] | 1 — preserve unique normalized ownership and merge collision rules |
| model:EntityMention | immutable run/document mention evidence and assignment | `ENT-03`, `ENT-04`, `REVIEW-01` | [[Filing Auditor and Policy-Limited Automation]] | 1 — add completeness/idempotency without erasing evidence |
| model:ExtractedFieldEvidence | amount/date extraction evidence stub | `FACT-01`, `ENT-02`; structural provenance | [[Extraction Envelope Evidence and Provenance]] | 1 — current shallow label evidence should become value-linked if strengthened |
| model:ExtractionRun | immutable extraction authority/history | `CAP-03`, `DOC-02`, `ENT-03`, `ASSIST-02` | [[Extraction Envelope Evidence and Provenance]] | 1 — latest completed run controls search/filing while history remains |
| model:Fact | canonical entity/key value and current revision pointer | `FACT-01`, `ENT-02` | [[Domain Model and Relationships]] | 1 — preserve unique canonical fact and verified-value protection |
| model:FactCandidate | competing extracted values and conflict state | `FACT-01`, `ENT-02`, `REVIEW-01` | [[Extraction Envelope Evidence and Provenance]] | 1 — reconcile candidate closure with review resolution |
| model:FactProvenance | revision-to-source provenance edge | `FACT-01`, `ENT-02`, `ASSIST-03` relevance | [[Extraction Envelope Evidence and Provenance]] | 1 — current document-level links must not be overstated as claim proof |
| model:FactRevision | immutable canonical fact value history | `FACT-01`, `ENT-02` | [[Domain Model and Relationships]] | 1 — preserve revision authorship/source and current-edge authority |
| model:FileObject | encrypted object metadata and wrapped per-file key | `CAP-01`, `DOC-02`, account lifecycle | [[Encryption Key Hierarchy and Object Storage]] | 1 — preserve ciphertext/key graph while repairing provider/hash metadata drift |
| model:Message | durable user/assistant transcript row | `ASSIST-01`, `ASSIST-03` | [[Search and Answer Agent Internals]] | 1 — keep pending/completed/failed lifecycle and person scope |
| model:OcrEvidence | whole-page transcript evidence | `ASSIST-02`, extraction/search | [[Extraction Envelope Evidence and Provenance]] | 1 — latest completed run search source; current evidence has no spans/boxes |
| model:Person | vault subject/user-linked person | `AUTH-05`, `FAMILY-01`, fact/chat/document scope | [[Identity Sessions Membership and Vault Scope]] | 1 — keep knowledge subject distinct from user/membership administration |
| model:ProcessingJob | durable queue admission, retry and lease state | `CAP-03`, `REVIEW-01`, `ASSIST-01`; backend operations | [[Durable Job State Lease Fencing and Recovery]] | 1 — constrain the closed state/type vocabulary and preserve lease fields |
| model:ReviewItem | durable typed human decision work | `REVIEW-01`, indirect entity work | [[Filing Auditor and Policy-Limited Automation]] | 1 — retain finding identity, status and single-winner resolution fields |
| model:User | login identity, password and verification/consent state | `AUTH-01`–`AUTH-04` | [[Identity Sessions Membership and Vault Scope]] | 1 — separate identity from vault/person scope and preserve per-user gates |
| model:Vault | tenant and owner boundary | `AUTH-01`, `AUTH-04`, `AUTH-05`; structural across all data | [[Domain Model and Relationships]] | 1 — top-level isolation/lifecycle aggregate |
| model:VaultKey | one wrapped vault KEK | storage/security structural owner | [[Encryption Key Hierarchy and Object Storage]] | 1 — fail closed on absence and support versioned resumable rotation |
| model:VaultMember | user/person/vault role membership | `AUTH-05`; no administration UI | [[Identity Sessions Membership and Vault Scope]] | 1 — preserve ordered authorization while strengthening same-vault consistency |

## Jobs — 5

| Inventory ID | Semantic ownership | Feature consumer or reachability | Technical note | Rebuild stage and relevance |
| --- | --- | --- | --- | --- |
| job:auditor.nightly | per-vault deterministic and optional semantic audit | `REVIEW-01`; backend-only automation | [[Filing Auditor and Policy-Limited Automation]] | 6→8 — serialize with filing, enforce consent/budgets and close terminal run state |
| job:chat.answer | asynchronous four-rung answer generation | `ASSIST-01`–`ASSIST-03` | [[Search and Answer Agent Internals]] | 6→9 — retain progress exception, final lease fence and pending-message closure |
| job:document.file | latest-run entity filing | `ENT-03`, `REVIEW-01`; indirect from capture/review/auditor | [[Filing Auditor and Policy-Limited Automation]] | 6→8 — per-vault serialization, idempotency and dead-letter review projection |
| job:document.process | first encrypted-original extraction | `CAP-01`–`CAP-03`, `DOC-02` | [[Extraction Envelope Evidence and Provenance]] | 6→7 — terminal completion must atomically publish extraction and chain filing |
| job:document.reprocess | authoritative re-extraction of an existing document | `ENT-02`, `REVIEW-01`; backend automation/indirect | [[Extraction Envelope Evidence and Provenance]] | 6→7 — lock subject/file/run agreement and protect prior usable transcripts |

## Migrations — 11

| Inventory ID | Semantic ownership | Feature consumer or classification | Technical note | Rebuild stage and relevance |
| --- | --- | --- | --- | --- |
| migration:0001 | twenty-table baseline for identity, documents, extraction, facts, jobs, messages and audit | structural foundation for most capabilities | [[Migration History and Database Dialects]] | 1 — root history; reproduce conceptual baseline without rewriting deployed revision |
| migration:0002 | sessions, auth tokens, password, verification and consent | `AUTH-01`–`AUTH-03` | [[Migration History and Database Dialects]] | 1 — auth lifecycle schema and token/session separation |
| migration:0003 | durable retry, due-time and lease columns | `CAP-03`, `ASSIST-01`, `REVIEW-01` | [[Migration History and Database Dialects]] | 1 — preserve max-attempt backfill; current DDL breaks fresh SQLite chain |
| migration:0004 | vault keys and wrapped file DEKs | `CAP-01`, `DOC-02`, lifecycle/security | [[Migration History and Database Dialects]] | 1 — establish envelope hierarchy and PostgreSQL migration proof |
| migration:0005 | PostgreSQL unaccent/trigram/FTS function and OCR indexes | `ASSIST-02` | [[Migration History and Database Dialects]] | 1 — retain dialect-qualified search objects; SQLite is deliberate no-op |
| migration:0006 | entity/review graph and person-to-entity fact backfill | `ENT-01`–`ENT-05`, `REVIEW-01`, `FAMILY-01` | [[Migration History and Database Dialects]] | 1 — preserve refusal-before-loss and complete backfill invariants |
| migration:0007 | directed entity-constraint dedupe and uniqueness | `ENT-03`–`ENT-05` | [[Migration History and Database Dialects]] | 1 — retain deterministic survivor; downgrade cannot restore deleted duplicates |
| migration:0008 | document user context and composite activity index | `CAP-01`, `HISTORY-01` | [[Migration History and Database Dialects]] | 1 — preserve capture context and migration-only index |
| migration:0009 | message progress/status and durable chat runs | `ASSIST-01`–`ASSIST-03` | [[Migration History and Database Dialects]] | 1 — durable asynchronous answer state |
| migration:0010 | audit runs, stable review finding key/index and no-self redirect check | `REVIEW-01`, `ENT-05` | [[Migration History and Database Dialects]] | 1 — preserve auditor/review identity and entity integrity |
| migration:0011 | PostgreSQL ChatRun JSON-to-JSONB conversion | `ASSIST-01`–`ASSIST-03`; structural dialect parity | [[Migration History and Database Dialects]] | 1 — head revision; SQLite no-op does not prove the full chain |

## Classified unknown probes — 2

| Inventory ID | Semantic ownership | Feature consumer or classification | Technical note | Rebuild stage and relevance |
| --- | --- | --- | --- | --- |
| unknown:a90bc6bb56ab3b82 | intentional negative probe: GET `/api/auth/login` proves 405 method rejection | structural-only contract test; not a missing route | [[Complete API Contract]] | 12 — retain normalized method-not-allowed behavior |
| unknown:e470ad1bdabee4f7 | intentional negative probe: GET `/api/does-not-exist` proves 404 not-found behavior | structural-only contract test; not a planned endpoint | [[Complete API Contract]] | 12 — retain normalized unknown-route behavior |

## Backend test files — 47

| Inventory ID | Semantic ownership | Feature or contract coverage | Technical note | Rebuild stage and relevance |
| --- | --- | --- | --- | --- |
| test:backend/tests/test_account.py | account export/deletion and lifecycle rollback proof | `AUTH-04`; owned/shared-vault, ZIP omissions, storage-failure success | [[Data Lifecycle Reset Export and Deletion]] | 12 — prove destructive scope and cryptographic/physical split |
| test:backend/tests/test_activity.py | activity feed vocabulary and pagination proof | `HISTORY-01` | [[Test Lanes Gates and Release Proof]] | 12 — preserve selected event rendering, scope and keyset order |
| test:backend/tests/test_agent_transcript_skill.py | optional PR-transcript skill safety proof | structural-only repository tooling | [[Test Lanes Gates and Release Proof]] | 12 — keep sanitized optional tooling separate from product acceptance |
| test:backend/tests/test_ai.py | extraction/filing/answer provider and schema proof | `CAP-03`, `ENT-03`, `ASSIST-02`, `ASSIST-03`, `REVIEW-01` | [[Extraction Envelope Evidence and Provenance]] | 12 — prove normalization, timeout/retry/fallback and synthetic fixtures |
| test:backend/tests/test_answer.py | answer ladder, tools, citations and failure-closure proof | `ASSIST-01`–`ASSIST-03` | [[Search and Answer Agent Internals]] | 12 — preserve rung caps, scope, provenance and abstention semantics |
| test:backend/tests/test_answer_migration.py | ChatRun JSON/JSONB migration parity proof | `ASSIST-01`–`ASSIST-03`; structural migration | [[Migration History and Database Dialects]] | 12 — prove PostgreSQL conversion and isolated SQLite no-op boundary |
| test:backend/tests/test_audit.py | nightly auditor, lint, policy, caps and serialization proof | `REVIEW-01`, `ENT-03`–`ENT-05` | [[Filing Auditor and Policy-Limited Automation]] | 12 — preserve policy-limited actions and terminal AuditRun state |
| test:backend/tests/test_auth.py | signup/login/session/token/rate-limit/email transaction proof | `AUTH-01`, `AUTH-02` | [[Identity Sessions Membership and Vault Scope]] | 12 — prove privacy, concurrency, rollback and cookie behavior |
| test:backend/tests/test_authz.py | ordered-role and scoped authorization proof | `AUTH-05`, `SHELL-03` | [[Identity Sessions Membership and Vault Scope]] | 12 — retain server authority and readonly denials |
| test:backend/tests/test_cbmap_ci.py | Codebase Map CI wrapper proof | structural-only Map tooling | [[Test Lanes Gates and Release Proof]] | 12 — preserve architecture-maintenance gate, not product behavior |
| test:backend/tests/test_cbmap_cli.py | Codebase Map command contract proof | structural-only Map tooling | [[Test Lanes Gates and Release Proof]] | 12 — prove deterministic CLI routing and exit behavior |
| test:backend/tests/test_cbmap_curated.py | curated Map page/schema validation proof | structural-only Map tooling | [[Test Lanes Gates and Release Proof]] | 12 — keep curated explanation consistent with sources |
| test:backend/tests/test_cbmap_fingerprints.py | Map source-fingerprint proof | structural-only Map tooling | [[Test Lanes Gates and Release Proof]] | 12 — detect stale source-backed projections |
| test:backend/tests/test_cbmap_gold.py | deterministic Map golden-output proof | structural-only Map tooling | [[Test Lanes Gates and Release Proof]] | 12 — preserve reproducible generated inventory behavior |
| test:backend/tests/test_cbmap_hooks.py | Map hook installation/invocation proof | structural-only Map tooling | [[Test Lanes Gates and Release Proof]] | 12 — enforce the pre-commit maintenance boundary |
| test:backend/tests/test_cbmap_impact.py | source-to-page impact analysis proof | structural-only Map tooling | [[Test Lanes Gates and Release Proof]] | 12 — preserve bounded review-scope calculation |
| test:backend/tests/test_cbmap_inventory.py | route/client/model/job/migration/test inventory extraction proof | structural-only inventory; underpins this ledger | [[Test Lanes Gates and Release Proof]] | 12 — keep exact deterministic IDs and known relation limits |
| test:backend/tests/test_cbmap_source_mutations.py | Map detection under representative source changes | structural-only Map tooling | [[Test Lanes Gates and Release Proof]] | 12 — ensure architecture drift becomes visible |
| test:backend/tests/test_cbmap_validation.py | Map structural/checker validation proof | structural-only Map tooling | [[Test Lanes Gates and Release Proof]] | 12 — preserve source-lock and page-integrity gates |
| test:backend/tests/test_compat_api.py | compatibility API shapes and representative vertical flows | `CAP-02`, `FACT-01`, Dashboard/documents and API contracts | [[Complete API Contract]] | 12 — retain exact response semantics including sample reuse/create |
| test:backend/tests/test_contract_shapes.py | normalized HTTP error/validation/negative-probe proof | cross-cutting API; owns both unknown inventory rows | [[Request Lifecycle Errors and Middleware]] | 12 — preserve machine codes, 404, 405 and validation envelope |
| test:backend/tests/test_crypto.py | key hierarchy, ciphertext integrity and migration proof | `CAP-01`, `DOC-02`, lifecycle/security | [[Encryption Key Hierarchy and Object Storage]] | 12 — prove fail-closed keys, races, tamper and round trip |
| test:backend/tests/test_entities_api.py | entity route scoping, detail and mutation contract proof | `ENT-01`, `ENT-02`, `AUTH-04` reset interactions | [[Domain Model and Relationships]] | 12 — preserve survivor/card and lifecycle semantics |
| test:backend/tests/test_entities_merge.py | merge/unmerge transaction and restoration proof | `ENT-05` | [[Filing Auditor and Policy-Limited Automation]] | 12 — preserve collisions, redirects, subject survivor and LIFO snapshot |
| test:backend/tests/test_entities_migration.py | entity-graph backfill/downgrade-refusal proof | `ENT-01`–`ENT-05`; migration structural | [[Migration History and Database Dialects]] | 12 — prevent lossy 0006 transitions |
| test:backend/tests/test_entities_model.py | entity constraints and relational model proof | `ENT-01`–`ENT-05` | [[Domain Model and Relationships]] | 12 — prove identifiers, redirects and directed constraint invariants |
| test:backend/tests/test_filing.py | mention, prematch, decision, constraint and question-budget proof | `ENT-03`, `ENT-04`, `REVIEW-01` | [[Filing Auditor and Policy-Limited Automation]] | 12 — preserve immutable evidence and bounded policy behavior |
| test:backend/tests/test_lifecycle.py | application construction, health/readiness, CORS, headers and reset proof | cross-cutting runtime; `AUTH-04` | [[Local and Production Runtime Topology]] | 12 — separate liveness/readiness and environment-specific composition |
| test:backend/tests/test_load_smoke.py | bounded live/in-process load-smoke harness proof | cross-cutting operations | [[Test Lanes Gates and Release Proof]] | 12 — prove tool behavior, not production capacity by itself |
| test:backend/tests/test_manual_cards.py | manual entity/fact creation and conflict recovery proof | `ENT-01`, `ENT-02` | [[Domain Model and Relationships]] | 12 — preserve confirmed origin, normalized identifiers and revisions |
| test:backend/tests/test_pagination.py | deterministic document/activity cursor proof | `DOC-01`, `HISTORY-01` | [[Test Lanes Gates and Release Proof]] | 12 — preserve stable keysets and page traversal |
| test:backend/tests/test_postgres_parity.py | selected PostgreSQL-versus-SQLite semantic parity proof | cross-cutting data/concurrency | [[Migration History and Database Dialects]] | 12 — qualify dialect differences rather than infer equivalence |
| test:backend/tests/test_queue.py | claim/backoff/fencing/reaping/chaining/inline-worker proof | `CAP-03`, `ASSIST-01`, `REVIEW-01` | [[Durable Job State Lease Fencing and Recovery]] | 12 — core concurrency and rollback acceptance lane |
| test:backend/tests/test_reprocess.py | authoritative re-extraction and supersession proof | `ENT-02`, `ENT-03`, `REVIEW-01`, `ASSIST-02` | [[Extraction Envelope Evidence and Provenance]] | 12 — preserve prior-transcript guard and latest-run authority |
| test:backend/tests/test_review.py | typed review resolution and SQLite serialization proof | `REVIEW-01`, `ENT-03`–`ENT-05`, `FACT-01` | [[Filing Auditor and Policy-Limited Automation]] | 12 — prove evidence locks, stale conflict and single-winner mutation |
| test:backend/tests/test_review_identity.py | stable finding identity/repeat-policy proof | `REVIEW-01` | [[Filing Auditor and Policy-Limited Automation]] | 12 — keep distinct recurrence semantics per finding kind |
| test:backend/tests/test_route_policy.py | development/production route set and policy metadata proof | `AUTH-05`; cross-cutting API | [[Router Domain and Infrastructure Boundaries]] | 12 — keep reset environment distinction and exact policy catalog |
| test:backend/tests/test_search.py | latest-run scoped retrieval and dialect behavior proof | `ASSIST-02` | [[Search and Answer Agent Internals]] | 12 — prove PostgreSQL/SQLite qualified contracts |
| test:backend/tests/test_security_adversarial.py | live-route bijection, role, consent and cross-tenant attack matrix | `AUTH-03`, `AUTH-05`, `SHELL-03`; all protected routes | [[Identity Sessions Membership and Vault Scope]] | 12 — mandatory trust-boundary acceptance proof |
| test:backend/tests/test_serialization_perf.py | bounded serialization/performance regression proof | cross-cutting API/client payload concerns | [[Test Lanes Gates and Release Proof]] | 12 — retain proportional payload/performance guard without claiming load capacity |
| test:backend/tests/test_settings.py | environment parsing, aliases/defaults and validation proof | structural runtime | [[Settings and Environment Contract]] | 12 — preserve deterministic resolution and strengthen missing validations |
| test:backend/tests/test_smoke_flows.py | end-to-end representative user flow proof | `AUTH-01`, Capture, documents, facts, entities, Assistant | [[Test Lanes Gates and Release Proof]] | 12 — vertical equivalence across HTTP, domain and persistence |
| test:backend/tests/test_state.py | summary/actions/deadline computation proof | `DASH-01`, `TASK-01`, `INSIGHT-01` | [[Complete API Contract]] | 12 — preserve projection rules without inventing tasks |
| test:backend/tests/test_status_quo.py | handbook schema/link/inventory parity checker proof | structural-only status-quo corpus; first post-snapshot corpus test | [[Test Lanes Gates and Release Proof]] | 12 — prove strict documentation contract and exact current inventory coverage |
| test:backend/tests/test_storage.py | local and optional S3 adapter proof | `CAP-01`, `DOC-02`; storage structural | [[Encryption Key Hierarchy and Object Storage]] | 12 — adapter round trip is not full production S3 acceptance |
| test:backend/tests/test_unlink.py | pair-wide unlink/reassign and guard proof | `ENT-04` | [[Filing Auditor and Policy-Limited Automation]] | 12 — preserve canonical-subject block and durable removed-pair decisions |
| test:backend/tests/test_uploads.py | filename/MIME/signature/size/quota/serving-header proof | `CAP-01`, `DOC-02` | [[Upload Download Quota and Erasure]] | 12 — retain hardened intake and scoped original responses |

## Client test files — 18

| Inventory ID | Semantic ownership | Feature or contract coverage | Technical note | Rebuild stage and relevance |
| --- | --- | --- | --- | --- |
| test:client/src/api-auth.test.mjs | auth adapter request/error/credential proof | `AUTH-01`, `AUTH-02` | [[Client API Permissions and Failure Contract]] | 12 — preserve same-origin credentials and normalized auth transitions |
| test:client/src/api-documents.test.mjs | document adapter scope/cursor/URL proof | `DOC-01`, `DOC-02` | [[Client State Navigation and Cache]] | 12 — preserve current/all and encoded detail behavior |
| test:client/src/api-job.test.mjs | bounded `waitForJob` state-machine proof | `CAP-03` | [[Client API Permissions and Failure Contract]] | 12 — timeout remains nonmutating; terminal states remain distinct |
| test:client/src/assistant-consent.test.mjs | Assistant verification/consent gate and retry proof | `AUTH-02`, `AUTH-03`, `ASSIST-01` | [[Client State Navigation and Cache]] | 12 — preserve draft/operation through resolved prerequisites |
| test:client/src/capture-consent.test.mjs | Capture verification/consent gate proof | `AUTH-02`, `AUTH-03`, `CAP-01` | [[Client State Navigation and Cache]] | 12 — no provider work before verified consent |
| test:client/src/capture-context.test.mjs | optional filing-context request proof | `CAP-01`, `ENT-03` | [[Client API Permissions and Failure Contract]] | 12 — keep note/context separate from file validation and subject identity |
| test:client/src/capture-polling.test.mjs | capture polling, recheck and result-state proof | `CAP-03` | [[Client State Navigation and Cache]] | 12 — preserve same-job recheck and saved-needs-review distinction |
| test:client/src/cbmap-inventory.test.mjs | client-method inventory fixture proof | structural-only inventory | [[Test Lanes Gates and Release Proof]] | 12 — preserve exact 31 method IDs and static-relation qualifications |
| test:client/src/chat-progress.test.mjs | Assistant message polling/progress/failure proof | `ASSIST-01` | [[Client State Navigation and Cache]] | 12 — retain pending stages and terminal closure while improving recovery |
| test:client/src/document-drawer.test.mjs | drawer detail/original/language helper proof | `DOC-02`, `SHELL-02` | [[UI Reachability Accessibility and Responsive Behavior]] | 12 — preserve deep-link handoff; add missing load/error/a11y proof |
| test:client/src/email-verification-banner.test.mjs | reactive resend banner state proof | `AUTH-02`, `SHELL-02` | [[UI Reachability Accessibility and Responsive Behavior]] | 12 — preserve gate-triggered appearance and rate/delivery states |
| test:client/src/entities.test.mjs | entity register/card/unlink client behavior proof | `ENT-01`–`ENT-05`, `FAMILY-01` | [[Client State Navigation and Cache]] | 12 — retain live-card and mutation handoffs with explicit failures |
| test:client/src/entity-create.test.mjs | manual create payload and owner-conflict recovery proof | `ENT-01` | [[Client API Permissions and Failure Contract]] | 12 — preserve normalized identifiers and recovery choice |
| test:client/src/history-feed.test.mjs | rendered feed, links, paging and no-undo proof | `HISTORY-01`, `UNDO-00` | [[UI Reachability Accessibility and Responsive Behavior]] | 12 — preserve readonly event handoff and explicit absence of undo |
| test:client/src/review-inbox.test.mjs | typed review actions and document handoff proof | `REVIEW-01`, `SHELL-02`, indirect `ENT-05` | [[UI Reachability Accessibility and Responsive Behavior]] | 12 — retain action bodies while adding load/busy/focus coverage |
| test:client/src/status-quo-mermaid.test.mjs | pinned Mermaid syntax proof for every diagram in the status-quo corpus | structural-only corpus proof | [[Snapshot and Evidence Manifest]] | 12 — keep every diagram parseable as the corpus evolves |
| test:client/src/token-link.test.mjs | fragment-token route extraction proof | `AUTH-02` | [[Client State Navigation and Cache]] | 12 — keep secrets out of server-visible query strings |
| test:client/src/view-regressions.test.mjs | twelve hashes, responsive/source reachability and shared cache proof | `SHELL-01`, document/fact/family/entity/insight/history views | [[UI Reachability Accessibility and Responsive Behavior]] | 12 — exact destination and cache regression lane; source checks are not full a11y proof |

## Ledger boundary

The tables above describe the current inventory, not a generated call graph. Semantic associations remain authoritative where static extraction is intentionally incomplete. Rebuild acceptance requires both exact ID parity and the behavior/invariant proof described by the linked notes; preserving 185 names without their failure, authorization, transaction and recovery semantics is not equivalence.

---
id: technical-complete-api-contract
title: Complete API Contract
kind: technical
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical
  - status-quo/backend-api
map_pages:
  - subsystem:runtime-configuration
  - subsystem:auth-vault-consent
  - subsystem:capture-documents
  - subsystem:client-architecture
  - subsystem:search-grounded-chat
  - flow:auth-vault-context
inventory_refs:
  - route:DELETE:/api/account
  - route:DELETE:/api/auth/ai-consent
  - route:GET:/api/account/export
  - route:GET:/api/activity
  - route:GET:/api/auth/me
  - route:GET:/api/documents
  - route:GET:/api/documents/{document_id}
  - route:GET:/api/entities
  - route:GET:/api/entities/{entity_id}
  - route:GET:/api/file/{document_id}
  - route:GET:/api/health
  - route:GET:/api/jobs/{job_id}
  - route:GET:/api/messages
  - route:GET:/api/ready
  - route:GET:/api/review-items
  - route:GET:/api/samples
  - route:GET:/api/samples/file/{name}
  - route:GET:/api/search
  - route:GET:/api/summary
  - route:POST:/api/auth/ai-consent
  - route:POST:/api/auth/login
  - route:POST:/api/auth/logout
  - route:POST:/api/auth/password-reset/confirm
  - route:POST:/api/auth/password-reset/request
  - route:POST:/api/auth/signup
  - route:POST:/api/auth/verify-email
  - route:POST:/api/auth/verify-email/request
  - route:POST:/api/chat
  - route:POST:/api/entities
  - route:POST:/api/entities/merge
  - route:POST:/api/entities/{entity_id}/confirm
  - route:POST:/api/entities/{entity_id}/facts
  - route:POST:/api/entities/{entity_id}/unlink
  - route:POST:/api/entities/{entity_id}/unmerge
  - route:POST:/api/facts/{fact_id}/verify
  - route:POST:/api/reset
  - route:POST:/api/review-items/{item_id}/resolve
  - route:POST:/api/samples/import
  - route:POST:/api/upload
  - clientapi:activity
  - clientapi:chat
  - clientapi:confirmEntity
  - clientapi:confirmPasswordReset
  - clientapi:createEntity
  - clientapi:createEntityFact
  - clientapi:document
  - clientapi:entityCard
  - clientapi:importSample
  - clientapi:importSampleAndWait
  - clientapi:job
  - clientapi:listDocuments
  - clientapi:listEntities
  - clientapi:listReviewItems
  - clientapi:login
  - clientapi:logout
  - clientapi:me
  - clientapi:messages
  - clientapi:requestEmailVerification
  - clientapi:requestPasswordReset
  - clientapi:reset
  - clientapi:resolveReviewItem
  - clientapi:samples
  - clientapi:setAiConsent
  - clientapi:signup
  - clientapi:summary
  - clientapi:unlinkEntity
  - clientapi:upload
  - clientapi:uploadAndWait
  - clientapi:verifyEmail
  - clientapi:verifyFact
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
  - FACT-01
  - ENT-01
  - ENT-02
  - ENT-04
  - ENT-05
  - REVIEW-01
  - ASSIST-01
  - ASSIST-02
  - HISTORY-01
  - DASH-01
parent: "[[Backend and API]]"
related:
  - "[[Router Domain and Infrastructure Boundaries]]"
  - "[[Client API Permissions and Failure Contract]]"
  - "[[Snapshot and Evidence Manifest]]"
---

> [!info] Navigation
> Parent: [[Backend and API]]. Sibling: [[Router Domain and Infrastructure Boundaries]]. Related client contract: [[Client API Permissions and Failure Contract]].

# Complete API Contract

The frozen development application has exactly **39** product routes. Production has exactly **38** because route:POST:/api/reset is not mounted. Every path is under `/api`; no `/api/state`, forms, PDF-editing, undo, circle-sharing, or generic admin API exists.

Access abbreviations below are executable dependency levels: **public** has no session requirement; **auth** requires a live user cookie but not vault context; **RO** resolves the first membership/vault/person and requires the readonly floor; **member** and **owner** require those ordered roles. **EV** means verified email and **AI** means current consent when the configured provider is not seed. These gates are per-route dependencies/calls, not middleware derived from `ROUTE_POLICIES`.

Common protected-route failures are normalized `401 unauthenticated`, `404 not_found` when vault/subject or a foreign object is hidden, and `403 forbidden` for role failure. EV and AI failures are `403 email_verification_required` and `403 ai_consent_required`. Tables emphasize additional or operation-defining statuses.

## Authentication and account routes (12)

| Method/path and inventory ID | Access/gates | Runtime request | Success and important statuses | Replay / page | Client reachability | Handler | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `POST /api/auth/signup` — route:POST:/api/auth/signup | public | JSON `email` 3–320 and email-shaped, `password` 10–1024, trimmed `displayName` 1–120 | `201 {ok:true}` plus new opaque session cookie; `400 conflict` duplicate, `422`, `429`; adapter/email exception can become 500 and roll back | Creates account/vault/person/token/session; no idempotency key | clientapi:signup → Auth screen | `app.authn.signup` | AUTH, CONTRACT |
| `POST /api/auth/login` — route:POST:/api/auth/login | public | JSON `email` length 3–320 and `password` length 1–1024 | `200 {ok:true}` plus new session cookie; `401` generic credentials, `429`, `422` | Each success creates a session; failed attempts share a process-local bucket | clientapi:login → Auth/AuthProvider | `app.authn.login` | AUTH, SECURITY |
| `POST /api/auth/logout` — route:POST:/api/auth/logout | public | Optional session cookie; no body | `200 {ok:true}`, clears cookie; live matching session revoked | Server-idempotent; replay/absent cookie still succeeds and clears | clientapi:logout → AuthProvider | `app.authn.logout` | AUTH, SECURITY |
| `GET /api/auth/me` — route:GET:/api/auth/me | auth | Cookie only | `200` ID/email/display name plus EV/AI flags; `401` | Read updates session `last_seen_at`; no paging | clientapi:me → AuthProvider | `app.authn.me` | AUTH, CONTRACT |
| `POST /api/auth/ai-consent` — route:POST:/api/auth/ai-consent | auth | Cookie only | `200 {ok:true}`; `401` | Re-grant is semantically idempotent but refreshes timestamp | clientapi:setAiConsent → Capture/Assistant | `app.authn.grant_ai_consent` | AI, SECURITY |
| `DELETE /api/auth/ai-consent` — route:DELETE:/api/auth/ai-consent | auth | Cookie only | `200 {ok:true}`; `401` | Idempotently clears timestamp | No client method/UI | `app.authn.withdraw_ai_consent` | AI, SECURITY |
| `POST /api/auth/verify-email/request` — route:POST:/api/auth/verify-email/request | auth | Cookie only | Generic `200 {ok:true}` when already verified or even send failure; `401`, `429` | Success replaces prior unused link; send failure rolls back replacement | clientapi:requestEmailVerification → banner | `app.authn.request_verification_email` | AUTH |
| `POST /api/auth/verify-email` — route:POST:/api/auth/verify-email | public | JSON nonempty `token` max 512 | `200 {ok:true}`; `400` invalid/expired/used token; `422` | Token is single-use | clientapi:verifyEmail → token screen | `app.authn.verify_email` | AUTH, SECURITY |
| `POST /api/auth/password-reset/request` — route:POST:/api/auth/password-reset/request | public | JSON email 3–320 | Generic `200 {ok:true}` for known/unknown/send failure; `429`, `422` | Eligible replay replaces older unused reset token; externally enumeration-safe | clientapi:requestPasswordReset → Auth screen | `app.authn.password_reset_request` | AUTH, SECURITY |
| `POST /api/auth/password-reset/confirm` — route:POST:/api/auth/password-reset/confirm | public | JSON token 1–512, password 10–1024 | `200 {ok:true}` changes password and revokes all live sessions; `400` invalid/raced token, `422` | Exact token atomically single-use; replay is 400 | clientapi:confirmPasswordReset → token screen | `app.authn.password_reset_confirm` | AUTH, SECURITY |
| `GET /api/account/export` — route:GET:/api/account/export | owner-of-vault-data | Cookie only | `200 application/zip`, attachment, `Cache-Control:no-store`; `401`, `403` | Read snapshot, no paging | No client method/UI | `app.routers.account.account_export` | ACCOUNT |
| `DELETE /api/account` — route:DELETE:/api/account | auth | JSON nonempty `password` max 1024 | `200 {ok:true}` and clears cookie; `403` wrong password, `422`; domain erases owned data/session/token state | Destructive; replay normally becomes 401 | No client method/UI | `app.routers.account.account_delete` | ACCOUNT, SECURITY |

## Documents, jobs, assistant, reporting, and operations (15)

| Method/path and inventory ID | Access/gates | Runtime request | Success and important statuses | Replay / page | Client reachability | Handler | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GET /api/activity` — route:GET:/api/activity | RO | Query `cursor?`; integer `limit=30` accepts any integer at the query/schema layer, then `feed_page` clamps it to 1–100 | `200 {items,nextCursor}`; `400` malformed cursor, `422` only when `limit` is not parseable as an integer | Stable cursor page using the clamped size | clientapi:activity → History | `app.routers.activity.activity` | ACTIVITY |
| `GET /api/documents` — route:GET:/api/documents | RO | `scope=current\|all`, `limit>=1` default 50 and capped at 200, `cursor?` | `200 {items,nextCursor}`; `400` invalid cursor, `422` bad scope/limit | Keyset cursor; reads are repeatable only relative to changing data | clientapi:listDocuments → shared cache | `app.routers.documents.documents` | CAPTURE, PAGING |
| `GET /api/documents/{document_id}` — route:GET:/api/documents/{document_id} | RO | Path ID | `200 DocumentOut`; `404` missing/foreign | Read, no paging | clientapi:document → drawer | `app.routers.documents.document` | CAPTURE, SECURITY |
| `POST /api/upload` — route:POST:/api/upload | member + EV + AI | Multipart required `file`, optional `user_context` trimmed/capped 2000 | `202 JobPayloadOut`; `400` malformed upload, `403` gates/role, `413` size/quota, `415` type/content mismatch, `422` | New durable file/job per accepted request; no idempotency key | clientapi:upload; composite clientapi:uploadAndWait → Capture | `app.routers.documents.upload` | CAPTURE, QUEUE, SECURITY |
| `GET /api/jobs/{job_id}` — route:GET:/api/jobs/{job_id} | RO | Path ID | `200 JobPayloadOut`; `404` missing/foreign | Read poll projection, no page | clientapi:job → capture composites | `app.routers.jobs.job` | QUEUE, SECURITY |
| `GET /api/samples` — route:GET:/api/samples | RO | None | `200 [{name,label,thumbUrl}]` | Read allowlisted catalog | clientapi:samples → Capture | `app.routers.samples.samples` | CAPTURE |
| `GET /api/samples/file/{name}` — route:GET:/api/samples/file/{name} | RO | Basename path | `200` dynamic bytes/MIME/disposition/CSP; `404` | Read | Indirect returned `thumbUrl`, no method | `app.routers.samples.sample_file` | UPLOADS, SECURITY |
| `POST /api/samples/import` — route:POST:/api/samples/import | member + EV + AI | JSON basename `name` 1–255, optional `user_context` trimmed/capped 2000 | **`202` for new job, `200` for reused active/completed import**; `403`, `404`, `422` | Sequential dedupe reuses active/completed work and dead-letter permits a fresh attempt; only PostgreSQL serializes concurrent same-vault/filename imports with an advisory transaction lock, while SQLite retains a check-then-create race | clientapi:importSample; composite clientapi:importSampleAndWait → Capture | `app.routers.samples.import_sample` | CAPTURE, QUEUE |
| `POST /api/chat` — route:POST:/api/chat | member + EV + AI | JSON trimmed `question` 1–2000 | `200 ChatOut` with user/pending assistant messages and engine; `403`, `422` | Creates new messages/run/job; no idempotency key | clientapi:chat → Assistant | `app.routers.chat.chat` | ANSWER, SECURITY |
| `GET /api/messages` — route:GET:/api/messages | RO | None | `200 [MessageOut]` including pending/progress/citations | Full current-person history; no cursor | clientapi:messages → Assistant | `app.routers.chat.messages` | ANSWER |
| `GET /api/search` — route:GET:/api/search | RO | `q` default empty/max 500, `limit` 1–100 default 20 | `200 {items}`; `422` bad query constraints | Bounded result, no cursor | No client method/UI; Assistant uses internal ladder instead | `app.routers.search.search` | SEARCH, SECURITY |
| `GET /api/summary` — route:GET:/api/summary | RO | None | `200 SummaryOut` slim current-person projection | Read snapshot, no cursor | clientapi:summary → StoreProvider | `app.routers.summary.summary` | CONTRACT, AUTHZ |
| `GET /api/file/{document_id}` — route:GET:/api/file/{document_id} | RO | Path ID | `200` decrypted dynamic bytes; inline for image/PDF, attachment otherwise; `404` doc/blob missing | Read; integrity/storage failure can become 500 | Indirect `fileUrl`, no inventory method | `app.routers.files.file` | UPLOADS, SECURITY |
| `GET /api/health` — route:GET:/api/health | public | None | `200 {ok,backend,database}` | Liveness read; no dependency probe | No client method/UI | `app.routers.health.health` | LIFECYCLE, CONTRACT |
| `GET /api/ready` — route:GET:/api/ready | public | None | `200 {ok:true}` after `SELECT 1`; `503 service_unavailable` | Database-only readiness | No client method/UI | `app.routers.health.ready` | LIFECYCLE, CONTRACT |

## Entity, fact, review, and development routes (12)

| Method/path and inventory ID | Access/gates | Runtime request | Success and important statuses | Replay / page | Client reachability | Handler | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GET /api/entities` — route:GET:/api/entities | RO | Optional unvalidated-string `kind`, `status` query | `200 [EntitySummaryOut]` | Full filtered register, no cursor | clientapi:listEntities → Entities/Familie/Unlink | `app.routers.entities.list_entities` | ENTITY, SECURITY |
| `POST /api/entities` — route:POST:/api/entities | member | JSON with one of six exact kinds, trimmed nonempty `name<=200`, at most 10 normalized/deduped aliases and at most 10 typed/normalized identifiers; exact contract below | `200 EntityCardOut`; `409 identifier_owned`, `422` | Creates card; normalized identifier uniqueness may reject replay | clientapi:createEntity → create dialog | `app.routers.entities.create_user_card` | MANUAL |
| `GET /api/entities/{entity_id}` — route:GET:/api/entities/{entity_id} | RO | Path ID | `200 EntityCardOut`; `404` missing/foreign | Read live card, follows supported merge redirect | clientapi:entityCard → entity/family card | `app.routers.entities.entity_card` | ENTITY, SECURITY |
| `POST /api/entities/{entity_id}/confirm` — route:POST:/api/entities/{entity_id}/confirm | member | Path ID, no body | `200 EntitySummaryOut`; `404` | Idempotent confirmation; activity recorded once | clientapi:confirmEntity → card | `app.routers.entities.confirm` | MERGE |
| `POST /api/entities/{entity_id}/facts` — route:POST:/api/entities/{entity_id}/facts | member | JSON trimmed nonempty `label<=120`, `value<=2000` | `200 FactOut`; `404`, `409` merged/duplicate, `422` | Creates verified user fact; no idempotency key | clientapi:createEntityFact → card | `app.routers.entities.add_user_fact` | MANUAL |
| `POST /api/entities/{entity_id}/unlink` — route:POST:/api/entities/{entity_id}/unlink | member | JSON `document_id`, reason `reassign\|not_related\|other`, optional exact field `target_entity_id`, optional `note<=500` | `204` empty; `404`, `409`, `422` | Guarded mutation; replay is not a success guarantee | clientapi:unlinkEntity → unlink dialog | `app.routers.entities.unlink_entity` | UNLINK, SECURITY |
| `POST /api/entities/merge` — route:POST:/api/entities/merge | member | JSON nonempty `sourceId`, `targetId` | `200 EntitySummaryOut`; `404`, `409` blocked/invalid | Transactional mutation; no idempotency key | No direct method/UI; review may merge indirectly | `app.routers.entities.merge_entities` | MERGE, SECURITY |
| `POST /api/entities/{entity_id}/unmerge` — route:POST:/api/entities/{entity_id}/unmerge | member | Path source ID, no body | `200 EntitySummaryOut`; `404`, `409 not_merged` | Restores recorded snapshot; replay becomes 409 | No client method/UI | `app.routers.entities.unmerge_entity` | MERGE, SECURITY |
| `POST /api/facts/{fact_id}/verify` — route:POST:/api/facts/{fact_id}/verify | member | JSON trimmed nonempty `value` 1–2000 | `200 FactOut`; `404`, `422`; separate best-effort security audit | Mutation has no request idempotency key | clientapi:verifyFact → Fakten/entity card; dead Database branch calls it without the required value | `app.routers.facts.verify_fact` | FACT, AUTHZ |
| `GET /api/review-items` — route:GET:/api/review-items | RO | `status=open` string query | `200 {items}` | Full status-filtered list, no cursor | clientapi:listReviewItems → Postfach | `app.routers.review.review_items` | REVIEW |
| `POST /api/review-items/{item_id}/resolve` — route:POST:/api/review-items/{item_id}/resolve | member | JSON answer `same\|different\|unsure`, optional `entityIds` | `200 ReviewItemOut`; `404`, `409` stale/conflict | Atomic single winner; competing/replay request receives 409 | clientapi:resolveReviewItem → Postfach | `app.routers.review.resolve_review` | REVIEW |
| `POST /api/reset` — route:POST:/api/reset | owner + **dev-only** | None | `200` refreshed summary after vault reset/reseed; common auth/role failures | Destructive; no idempotency promise; absent in production | clientapi:reset → always-visible shell icon | `app.routers.dev.reset` | LIFECYCLE, AUTHZ, SECURITY |

The tables contain 12 + 15 + 12 = **39** distinct development routes. Removing only route:POST:/api/reset leaves the exact **38** production routes.

## Exact manual entity-create request contract

route:POST:/api/entities accepts an `EntityCreateIn` object with extra keys forbidden. Its source contract is:

| Field | Exact accepted shape | Normalization and dedupe |
| --- | --- | --- |
| `kind` | Exactly `person`, `organization`, `property`, `vehicle`, `contract`, or `other` | No coercion to another kind |
| `name` | String, maximum 200 characters; must remain nonempty after trimming | Leading/trailing whitespace is removed; the trimmed value is stored |
| `aliases` | Optional list, at most 10 strings; every alias must be nonempty after trimming and at most 120 characters | Each value is Unicode NFC-normalized and trimmed, then duplicates are removed case-insensitively with `casefold`, preserving the first normalized spelling and order |
| `identifiers` | Optional list, at most 10 objects; each `value` is at most 120 characters and must remain nonempty after trimming | Each object is normalized and duplicates by `(kind, normalized value)` are removed, preserving the first |
| `identifiers[].kind` | Exactly `iban`, `license_plate`, `vin`, `insurance_number`, `customer_number`, `tax_id`, `meter_number`, or `other` | Kind remains part of the dedupe/uniqueness key |

Identifier value normalization is Unicode NFKC, uppercase, then removal of all whitespace. License plates additionally remove ASCII hyphen and Unicode hyphen/dash/minus variants. The resulting `(kind, normalized value)` must be nonempty and is unique per vault across entity cards; an existing owner produces `409 identifier_owned`. Alias casefold dedupe is request-local and does not establish cross-entity alias uniqueness.

## All 31 generated client methods

The method inventory counts exported API operations and composites, not URL helpers. Every ID is accounted for here independently of relation-extractor edges.

| Inventory ID | Adapter behavior | Consumer / reachability |
| --- | --- | --- |
| clientapi:activity | GET activity, optional cursor | `History` |
| clientapi:chat | POST question | `Assistant` |
| clientapi:confirmEntity | POST entity confirm | `EntityCardDetail` |
| clientapi:confirmPasswordReset | POST token/password | `TokenScreen` |
| clientapi:createEntity | POST entity body | `EntityCreateDialog` |
| clientapi:createEntityFact | POST entity fact body | `EntityCardDetail` |
| clientapi:document | GET document ID | `DocumentDrawer` |
| clientapi:entityCard | GET encoded entity ID | `EntityCardDetail` |
| clientapi:importSample | POST sample/context | Internal primitive used by composite |
| clientapi:importSampleAndWait | Import then bounded job poll | `Capture` |
| clientapi:job | GET job ID | Internal polling primitive |
| clientapi:listDocuments | GET scope plus optional cursor | Shared document cache in `lib.jsx` |
| clientapi:listEntities | GET optional kind/status query | `Entities`, `Familie`, `UnlinkDialog` |
| clientapi:listReviewItems | GET status query | `ReviewInbox` |
| clientapi:login | POST credentials | `AuthProvider`, `AuthScreen` |
| clientapi:logout | POST no body | `AuthProvider` |
| clientapi:me | GET current user | `AuthProvider` |
| clientapi:messages | GET message history | `Assistant` |
| clientapi:requestEmailVerification | POST no body | verification banner |
| clientapi:requestPasswordReset | POST email | `AuthScreen` |
| clientapi:reset | POST no body | shell reset control |
| clientapi:resolveReviewItem | POST answer/entity IDs | `ReviewInbox` |
| clientapi:samples | GET catalog | `Capture` |
| clientapi:setAiConsent | POST grant | `Assistant`, `Capture` |
| clientapi:signup | POST account fields | `AuthScreen` |
| clientapi:summary | GET summary | `StoreProvider` |
| clientapi:unlinkEntity | POST unlink body | `UnlinkDialog` |
| clientapi:upload | multipart upload | Internal primitive used by composite |
| clientapi:uploadAndWait | Upload then bounded job poll | `Capture` |
| clientapi:verifyEmail | POST token | `TokenScreen` |
| clientapi:verifyFact | POST fact value | `Fakten`, `EntityCardDetail`; dead Database branch calls it incorrectly without a value |

There is intentionally no client method for account export/delete, consent withdrawal, direct merge/unmerge, health/readiness, raw search, original-file bytes, or sample-file bytes. The last two are indirect browser URLs rather than absence of user access.

## OpenAPI and inventory qualifications

The committed OpenAPI has all **39 development operations across 37 unique paths**, but it is not the complete runtime contract:

- Sample import declares only success `200`; runtime returns `202` when it creates a new job and `200` when an active/completed import is reused.
- Shared cookie/context/role/EV/AI dependency failures are underdeclared on many operations. Cookie parameters appear optional and there is no OpenAPI authentication `securityScheme` or operation security requirement.
- Account export declares ZIP content, but document and sample file operations do not fully declare their dynamic binary media/disposition responses or runtime 404s.
- Generated 422 response schemas commonly describe FastAPI's default validation shape, while runtime exception handling returns normalized `{error:"invalid request", code:"validation_error", detail:[...]}`.
- Duplicate signup is HTTP 400 with machine code `conflict`, an intentional runtime oddity that status-only generated clients can mishandle.

Inventory relations also have known static false negatives: optional-query clientapi:listEntities does call route:GET:/api/entities; indirect `fileUrl`/sample `thumbUrl` reach the two binary routes; generic DELETE-account test calls can evade test relation extraction. These are inventory limitations, not missing source behavior.

## Focused proof key

Each route row names at least one proof group. Exact evidence is:

- **AUTH** — `backend/tests/test_auth.py` → `test_signup_login_me_logout`, duplicate-signup, verification resend, password-reset flow/concurrency/rate-limit tests.
- **AI** — `backend/tests/test_ai.py` and `test_reprocess.py` → consent grant/withdraw and provider gates.
- **SECURITY** — `backend/tests/test_security_adversarial.py` → `test_every_product_route_is_attacked`, no-cookie, gate, forged/tampered cookie, readonly/member, production reset, and cross-tenant tests.
- **AUTHZ** — `backend/tests/test_authz.py` → role enforcement, reset, fact-audit, tenant-preserving reset.
- **CONTRACT** — `backend/tests/test_contract_shapes.py` → real response round trips, normalized errors, health/ready, upload codes.
- **ACCOUNT** — `backend/tests/test_account.py` → owner/nonowner export and password-confirmed deletion/erasure/failure isolation.
- **ACTIVITY** — `backend/tests/test_activity.py` → stable pagination, vault isolation and authentication.
- **CAPTURE** — `backend/tests/test_compat_api.py` → documents/detail/upload/job/sample compatibility, validation and sample idempotency.
- **PAGING** — `backend/tests/test_pagination.py` → cursor traversal, no gaps/duplicates, limit cap and invalid cursor.
- **QUEUE** — `backend/tests/test_queue.py` → polling states, inline/worker behavior, retry/dead letter and concurrent sample dedupe.
- **UPLOADS** — `backend/tests/test_uploads.py` and `test_crypto.py` → media validation, quota, safe names, sample/document bytes, CSP and decryption.
- **ANSWER** — `backend/tests/test_answer.py` → pending chat, durable completion, failure closure and message polling; smoke flows cover request integration.
- **SEARCH** — `backend/tests/test_search.py` → route query behavior, dialects, scoping and edge cases.
- **ENTITY** — `backend/tests/test_entities_api.py` → filtered register, live cards, sections and 404.
- **MANUAL** — `backend/tests/test_manual_cards.py` → entity/fact validation, identifier conflict, provenance and concurrency.
- **MERGE** — `backend/tests/test_entities_merge.py` → confirm idempotency and merge/unmerge locking/round trips.
- **UNLINK** — `backend/tests/test_unlink.py` → unlink/reassign validation, concurrency and vault isolation.
- **FACT** — `backend/tests/test_compat_api.py` and `test_authz.py` → sticky verification, validation and audit.
- **REVIEW** — `backend/tests/test_review.py` → list filtering, all answer types, stale evidence, single winner and refile behavior.
- **LIFECYCLE** — `backend/tests/test_lifecycle.py` → route mounting, health/readiness, headers/CORS/request IDs and reset behavior.

## Rebuild obligations

Treat these 39 rows, their environment/gate distinctions, normalized failures, per-operation replay semantics, and 31 client methods as one change-together contract. Generate an accurate production OpenAPI with reusable cookie security and common errors, represent 202 sample creation, model dynamic files explicitly, and retain adversarial live-route bijection so documentation metadata cannot replace executable authorization.

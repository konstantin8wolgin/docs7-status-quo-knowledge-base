---
id: traceability-known-gaps-and-non-capabilities
title: Known Gaps and Non-Capabilities
kind: traceability
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/traceability
  - status-quo/gaps
parent: "[[INDEX]]"
related:
  - "[[Capability Ledger]]"
  - "[[UI Surface Coverage]]"
  - "[[Contract Coverage]]"
  - "[[Feature-to-Code Matrix]]"
  - "[[Acceptance and Equivalence Proof]]"
---

> [!info] Navigation
> Parent: [[INDEX]]. Siblings: [[Capability Ledger]] · [[UI Surface Coverage]] · [[Contract Coverage]] · [[Feature-to-Code Matrix]].

# Known Gaps and Non-Capabilities

This is the negative-space register for the snapshot. It separates current defects and proof gaps from deliberate boundaries and genuinely absent capabilities. A clean rebuild must not silently reproduce a verified defect, but it also must not turn an absence into scope without an explicit product and security decision.

| Classification | Rebuild treatment |
| --- | --- |
| verified defect | Repair deliberately, retain a regression test for the old failure, and record the behavior divergence. |
| technical limitation | Preserve only when required for external compatibility; otherwise replace it while proving the surrounding invariant. |
| proof gap | Add the missing proof before claiming equivalence or production readiness. |
| backend-only or indirect | Keep the reachability classification unless a separately authorized UI/API change exposes it. |
| explicit non-capability | Exclude from equivalence. Adding it is new product scope. |
| planned-only or historical-only | Exclude entirely from the rebuild contract. |

## Cross-layer and contract gaps

| ID | Verified gap or limitation | Current effect | Clean-rebuild disposition | Primary evidence |
| --- | --- | --- | --- | --- |
| `GAP-API-01` | `ROUTE_POLICIES` is sorted/tested metadata, not executable middleware enforcement. | A route can be secure only through its actual dependency/domain predicates; policy labels alone grant or deny nothing. | Preserve explicit server gates and the live-route/role parity tests; centralize only with equivalent executable proof. | [[Router Domain and Infrastructure Boundaries]] |
| `GAP-API-02` | Generated OpenAPI underdeclares cookie security, common dependency failures, normalized 422 bodies and dynamic binary responses; sample import omits its runtime `202` creation response. | Generated consumers can infer the wrong authentication, error, status or content contract. | Generate a production-accurate contract with reusable cookie security/errors, both sample outcomes and explicit binary responses. | [[Complete API Contract]]; [[Request Lifecycle Errors and Middleware]] |
| `GAP-API-03` | Duplicate signup returns HTTP 400 with machine code `conflict`; idempotency is operation-specific and no general idempotency key exists. | Status-only clients can misclassify conflicts; automatic replay of writes is unsafe. | Preserve machine codes and per-operation replay semantics or version an intentional change. | [[Complete API Contract]]; [[Router Domain and Infrastructure Boundaries]] |
| `GAP-API-04` | Static relation extraction misses optional entity-query URLs, indirect original/sample URLs and some generic DELETE-account calls. | A missing generated edge is not absence evidence. | Maintain the manual edges in [[Contract Coverage]] and improve extraction separately. | [[Client API Permissions and Failure Contract]] |
| `GAP-ARCH-01` | Domain code imports SQLAlchemy models and accepts `Session`; there is no repository port, and some routers retain orchestration. | Module names do not form a strict clean-architecture boundary. | Rebuild bottom-up and preserve transaction ownership; deepen a boundary only when it makes the module more coherent. | [[Component Ownership and Dependency Direction]] |
| `GAP-ARCH-02` | Reads can mutate session `last_seen_at`; audit writes are sometimes best-effort second transactions. | “Read-only request” and “audit is atomic with business write” are not universal truths. | Keep commit/rollback placement explicit and classify audit guarantees per operation. | [[Router Domain and Infrastructure Boundaries]] |
| `GAP-CLIENT-01` | API errors are thrown as plain objects; non-204 success is assumed JSON; ordinary calls have no timeout, abort, retry, backoff, idempotency key or offline queue. | Consumers use inconsistent message fields and cannot safely replay arbitrary failures or add binary methods naively. | Introduce typed results/errors, explicit binary handling and operation-specific recovery. | [[Client API Permissions and Failure Contract]] |
| `GAP-CLIENT-02` | The client receives no role, active-vault, membership or capability projection. | Every role sees write affordances; denial is discovered only after a server request. | Add a server-authorized projection before hiding/disabling controls; backend enforcement remains authoritative. | [[Permission-Aware Affordance Gaps]] |

## Identity, privacy, and storage gaps

| ID | Verified gap or limitation | Current effect | Clean-rebuild disposition | Primary evidence |
| --- | --- | --- | --- | --- |
| `GAP-SEC-01` | Sessions have fixed non-sliding 30-day expiry, independent concurrent login rows and no rotation, inventory, device management, revoke-other-sessions, remember-me, MFA, bearer mode or cluster revocation cache. | The session contract is secure but administratively narrow; exact non-sliding behavior lacks dedicated proof. | Preserve opaque hash-stored cookies, fixed expiry and password-reset revocation; add management only as explicit scope and test exact renewal behavior. | [[Identity Sessions Membership and Vault Scope]] |
| `GAP-SEC-02` | Login throttling is process-local and there is no shared edge limiter. | Limits vary across processes/replicas and reset on restart. | Retain key separation while moving enforcement to a cluster-aware edge/store. | [[Authentication and Sessions]]; [[Local and Production Runtime Topology]] |
| `GAP-SEC-03` | Membership/person/vault agreement is application-enforced; the database has no composite same-vault constraints. | Corrupt or future direct writes can create cross-vault references that individual FKs accept. | Add enforceable tenant-consistency invariants and corrupted-link adversarial tests. | [[Domain Model and Relationships]] |
| `GAP-SEC-04` | AES-GCM uses no authenticated associated data and stored wrap/encryption labels do not dispatch a version. | Ciphertext is authenticated, but its envelope is not bound to vault/file metadata and there is no algorithm migration path. | Bind stable context as AAD and version the envelope without weakening fail-closed reads. | [[Encryption Key Hierarchy and Object Storage]] |
| `GAP-SEC-05` | `FileObject.sha256` records plaintext SHA-256 but reads never compare it. | The hash is metadata, not the integrity guard; AES-GCM is the actual integrity proof. | Define the digest's purpose and either verify it or remove claims that it is checked. | [[Encryption Key Hierarchy and Object Storage]] |
| `GAP-SEC-06` | `storage_provider` remains `local` under S3; reads ignore it and use one process-global adapter. | Metadata is untruthful and cannot route a mixed-provider migration. | Persist truthful provider/location/version data or delete the field; prove backend switching. | [[Encryption Key Hierarchy and Object Storage]] |
| `GAP-SEC-07` | File read scopes the `Document` but trusts its linked `FileObject.vault_id`; tests use valid links. | A corrupted cross-vault link is not explicitly rejected at that boundary. | Constrain the relationship and add corrupted-row tests. | [[Encryption Key Hierarchy and Object Storage]] |
| `GAP-SEC-08` | Upload, object adapters, download and export buffer whole plaintext/ciphertext; downloads lack ranges, ETag/conditional policy and `Cache-Control: no-store`. | Memory amplification and browser/intermediary caching behavior are undeclared. | Add bounded authenticated streaming/chunking and an intentional serving/cache policy. | [[Upload Download Quota and Erasure]] |
| `GAP-SEC-09` | Quota is a nonlocking `SUM` of live metadata and ignores ciphertext expansion, temp files and orphan objects. | Concurrent admissions can exceed the configured limit; logical and physical usage diverge. | Use atomic reservation/accounting plus storage reconciliation. | [[Upload Download Quota and Erasure]] |
| `GAP-SEC-10` | Database/key erasure commits before best-effort object deletion; failures still return success and there is no cleanup outbox/reconciler. | Cryptographic inaccessibility can be complete while ciphertext remains physically present. | Preserve the distinction, make cleanup durable/retryable, and report confirmed physical state separately. | [[Data Lifecycle Reset Export and Deletion]] |
| `GAP-SEC-11` | CORS/origin and security headers are code-owned but no complete deployment edge policy exists; exact no-Origin/CSRF semantics lack dedicated proof. | Proxy/TLS/header behavior can differ from the in-process application boundary. | Specify and test browser, proxy and deployment controls together. | [[Identity Sessions Membership and Vault Scope]]; [[Test Lanes Gates and Release Proof]] |

## Data, migration, and lifecycle gaps

| ID | Verified gap or limitation | Current effect | Clean-rebuild disposition | Primary evidence |
| --- | --- | --- | --- | --- |
| `GAP-DATA-01` | The 32-model schema has 76 FK columns but only four ORM relationships, no FK cascade, no composite same-vault FK and mostly unconstrained state/kind/role strings. | Integrity and deletion order depend heavily on application convention. | Preserve conceptual records while adding deliberate tenant, state and lifecycle constraints; do not add blind cascades. | [[Domain Model and Relationships]] |
| `GAP-DATA-02` | Default SQLite connections do not enable FK enforcement. | SQLite tests can pass deletion/write orders PostgreSQL rejects. | Enable FK proof or treat SQLite as an explicitly weaker development dialect; retain PostgreSQL proof. | [[Domain Model and Relationships]] |
| `GAP-DATA-03` | Fresh SQLite `alembic upgrade head` fails at migration 0003; the isolated 0011 test is not a full-chain test. | SQLite create-all works, but SQLite historical migration support is false. | Choose one supported schema path and test real upgrades; do not claim full SQLite migration support. | [[Migration History and Database Dialects]] |
| `GAP-DATA-04` | `create_all` neither migrates nor stamps and omits migration-only indexes/extensions/server defaults. | ORM-created SQLite and migrated PostgreSQL are observably different even at the nominal same model shape. | Make schema equivalence explicit or remove create-all from authoritative runtime paths. | [[Migration History and Database Dialects]] |
| `GAP-DATA-05` | Mention/idempotency and active refiling jobs rely on select-then-insert conventions without complete database uniqueness. | Concurrency can create incomplete mention sets or duplicate active work. | Add enforceable completeness/idempotency or serialized ownership. | [[Filing Auditor and Policy-Limited Automation]] |
| `GAP-LIFE-01` | Account export is a selected, unversioned subset assembled in memory, not a database dump. It includes reviews, chat/audit runs, entity mentions/events/constraints and activity events, but omits auth/tenancy/key material; processing jobs and extraction evidence; fact candidates/history/provenance; document amount/date/tag/trust rows and raw envelopes; non-activity audit events and full audit detail; file-object metadata plus unreferenced/deleted objects; and other records outside its explicit DTO projection. | “Export” cannot reconstruct the account or prove full data portability; one missing key/object aborts the entire ZIP, and exported rows can retain IDs for omitted rows. | Publish a versioned projection and its exact exclusions; stream if needed and never call it a complete backup. | [[Data Lifecycle Reset Export and Deletion]] |
| `GAP-LIFE-02` | Reset reseeding happens after the destructive commit. | A reseed failure leaves an already-reset vault empty or partial. | Expose this non-atomic postcondition or move to a durable, observable workflow. | [[Data Lifecycle Reset Export and Deletion]] |
| `GAP-LIFE-03` | There is no product document retention, deletion, archive or physical-object reconciliation workflow. | `deleted_at` is effectively unused and orphan/missing sets are undiscoverable. | Define retention and reconcile logical/physical state before claiming erasure completeness. | [[Upload Download Quota and Erasure]] |

## Jobs, extraction, filing, search, and answer gaps

| ID | Verified gap or limitation | Current effect | Clean-rebuild disposition | Primary evidence |
| --- | --- | --- | --- | --- |
| `GAP-JOB-01` | Persisted job `priority` is ignored; due claims sort only by creation time, with no ID tie-break for equal timestamps. | Auditor `-10` priority has no runtime meaning and equal-time ordering is under-specified. | Remove/rename the field or implement a deterministic priority/FIFO contract. | [[Durable Job State Lease Fencing and Recovery]] |
| `GAP-JOB-02` | Inline execution neither reaps abandoned leases nor wakes for future `run_after`, and never schedules nightly audits. | Durable jobs can remain stranded until a worker or explicit invocation appears. | Repair inline recovery or require a worker as an enforceable deployment dependency. | [[Durable Job State Lease Fencing and Recovery]] |
| `GAP-JOB-03` | Lease reaping requeues immediately without normal backoff/stage reset/error and does not surface the filing dead-letter review item. | Recovered jobs behave differently from ordinary failures; a terminal filing problem can be temporarily invisible. | Unify recovery semantics and dependent-state closure while retaining lease fencing. | [[Durable Job State Lease Fencing and Recovery]] |
| `GAP-JOB-04` | Job type/status vocabularies lack database checks; `failed` is modeled but active failure paths use queued or dead-letter. | Invalid strings can persist and the declared state machine is broader than runtime. | Constrain the closed registry and align modeled/runtime states. | [[Durable Job State Lease Fencing and Recovery]] |
| `GAP-EXT-01` | `Envelope.from_loose` drops/defaults provider data before strict validation; a first unknown non-text extraction can complete without pages. | “Strict envelope” does not mean verbatim strict input, and a degraded first run can become authoritative. | Decide compatibility versus defect explicitly; preserve prior-transcript protection until authority is stronger. | [[Extraction Envelope Evidence and Provenance]] |
| `GAP-EXT-02` | `raw_output_json` and normalized envelope store the same normalized object; provider failure details and dropped fields are not retained. | The original model response and fallback cause cannot be reconstructed. | Define safe raw/normalized retention and redaction rather than implying raw evidence exists. | [[Extraction Envelope Evidence and Provenance]] |
| `GAP-EXT-03` | OCR evidence is page text only; extracted-field evidence uses labels, no value quote/OCR link/box; ordinary fact provenance is document-only. | Claim-level/page-span support is shallow despite nullable schema capacity. | Store real OCR links/spans/quotes and tie current values to their actual evidence. | [[Extraction Envelope Evidence and Provenance]] |
| `GAP-FILE-01` | Mention discovery completeness, same-kind matching and custom-engine decision completeness are not fully enforced; the two-question cap is per invocation and overflow silently proposes cards. | Filing can record incomplete or overly permissive identity decisions without observable overflow. | Enforce completeness/kind rules and surface cap/overflow outcomes. | [[Filing Auditor and Policy-Limited Automation]] |
| `GAP-AUDIT-01` | Default seed audit has no semantic findings; unknown/recorded-only findings are not actionable, and budgets are not surfaced. | “Auditor coverage” is narrower than stored finding vocabularies suggest. | Preserve the policy matrix and make actual action coverage/budgets observable. | [[Filing Auditor and Policy-Limited Automation]] |
| `GAP-SEARCH-01` | PostgreSQL uses German FTS/trigram behavior while SQLite uses accent-folded substring logic; SQLite representative-page ordering is not fully equivalent. | Result/rank/page behavior differs by dialect. | Test both as intentionally qualified contracts or choose one authoritative search implementation. | [[Search and Answer Agent Internals]] |
| `GAP-CHAT-01` | Conversation history is durable but intentionally absent from answer context. | Each question is stateless; adding memory would change answer behavior and privacy scope. | Preserve stateless equivalence unless conversation memory is explicitly designed and authorized. | [[Search and Answer Agent Internals]] |
| `GAP-CHAT-02` | `ChatRun` omits the candidate snippets/pages actually supplied to the model; mismatch provenance can be null or fall back to the first page. | A later reviewer cannot reconstruct the exact answer evidence set. | Persist the bounded candidate evidence and exact mismatch source safely. | [[Search and Answer Agent Internals]] |
| `GAP-CITE-01` | Citation guard proves only current vault/person scope, stored title and dedupe—not evidence-set membership, claim support, page/quote/span or nonempty citations. | An answered result can display document chips without proving the claim, or have zero citations. | Bind citations to supplied evidence and claims; label unsourced results honestly. | [[Citations Provenance and Abstention]]; [[Search and Answer Agent Internals]] |

## Runtime, operations, and proof gaps

| ID | Verified gap or limitation | Current effect | Clean-rebuild disposition | Primary evidence |
| --- | --- | --- | --- | --- |
| `GAP-OPS-01` | Health is unconditional; readiness only runs `SELECT 1` and ignores schema head, storage, workers/queue, SMTP, AI provider and key decryption. | An empty/stale or dependency-broken deployment can report ready. | Add dependency-aware readiness with safe representative checks. | [[Local and Production Runtime Topology]] |
| `GAP-OPS-02` | Worker services inherit an HTTP `/api/ready` image healthcheck even though they run no HTTP server; there is no heartbeat or queue-lag health. | Healthy workers appear unhealthy, and wedged workers are not detected. | Add worker-specific command/heartbeat health and graceful drain. | [[Local and Production Runtime Topology]] |
| `GAP-OPS-03` | Production topology has no owned client/TLS/proxy edge, shared throttle, immutable secret injection, migration/bucket init job, HA/failover or production-graph acceptance test. | Critical deployment ordering and edge security remain operator conventions. | Make deployment dependencies explicit and automatically exercised. | [[Local and Production Runtime Topology]] |
| `GAP-OPS-04` | JSON logging drops most extras and traceback structure; exception logging is split and request/job correlation, metrics, traces, alerts and error aggregation are absent. | Durable rows carry some evidence, but operational diagnosis is fragmented. | Preserve request IDs/body safety while adding one structured telemetry contract. | [[Observability Backup Restore and Incident Recovery]] |
| `GAP-OPS-05` | Backup is a manual, uncoordinated database/object/master-key triad with no script, manifest, retention, PITR, scheduler, RPO/RTO, continuous restore test or reconciler. | Database/object snapshots can disagree and mere connectivity is not recovery proof. | Automate coordinated capture and prove restore by authenticated decryption. | [[Observability Backup Restore and Incident Recovery]] |
| `GAP-OPS-06` | Master-key rotation is a manual one-row primitive with no batch command, key version, resume, dual read, audit, rollback or drill. | Partial rotation can split vaults between unreadable key states. | Implement a fenced, resumable, versioned, audited rotation workflow and recovery drill. | [[Observability Backup Restore and Incident Recovery]] |
| `GAP-OPS-07` | Settings allow unknown keys and do not validate positive numeric bounds, safe paths, URLs/origins/emails, paired S3/SMTP credentials, fixture existence or usable Vertex configuration; several failures occur only during app construction or first use. | Misconfiguration fails at inconsistent and sometimes late lifecycle points. | Validate configuration and dependency readiness deliberately without exposing secrets. | [[Settings and Environment Contract]] |
| `GAP-PROOF-01` | CI omits the local runtime smoke, production image/Compose acceptance, required S3 end-to-end lane and private golden backtest. | Repository green does not prove production startup/storage/recovery or private release quality. | Retain public gates, automate safe runtime/deployment proof and require a separately authorized sanitized golden attestation. | [[Test Lanes Gates and Release Proof]] |
| `GAP-PROOF-02` | Focused proof is absent for concurrent quota admission, corrupted cross-vault relationships, plaintext-hash mismatch, ranges/no-store, exact non-sliding sessions, no-Origin/CSRF, structured tracebacks, stale-schema readiness, worker health, restore/rotation and orphan reconciliation. | These invariants or defects cannot be claimed from current tests. | Add targeted adversarial/integration/operational lanes before equivalence claims. | [[Test Lanes Gates and Release Proof]] |

## User-surface defects by capability

| Capability | Verified current defects and limitations | Clean-rebuild disposition |
| --- | --- | --- |
| `AUTH-01` | Client login demands ten characters while backend login accepts any nonempty password; rejected logout retains identity with no busy/error state; development auto-login failure is silent; tabs/loaders/errors lack full semantics. | Align validation with the server contract, make logout/recovery visible, and add accessible auth state without weakening generic credential failure. |
| `AUTH-02` | Reset-request failures intentionally look successful; resend may say sent after mail failure; the banner is reactive and not globally discoverable; verification/consent gate ordering differs between Capture and Assistant. | Preserve request privacy and atomic token rules; correct false delivery/status copy as a recorded divergence. |
| `AUTH-03` | Consent withdrawal is backend-only; there is no settings/history/provider explanation surface. | Preserve provider-dependent per-user gating; expose withdrawal only as authorized new UI scope. |
| `AUTH-04` | Export/deletion are backend-only; reset is development-only, uses native confirmation and hides failure. | Keep lifecycle distinctions; any settings UI must disclose export subset and physical-erasure semantics. |
| `AUTH-05`, `SHELL-03` | No vault switcher/admin/capability projection; all roles see upload/chat/fact/entity/review/reset controls and receive generic denial. | Add server-derived capability state and direct denial proof; do not infer role client-side. |
| `SHELL-01` | Invalid hashes can render Dashboard without canonicalizing; active mobile tab does not auto-scroll; static readiness/privacy copy is not live status; navigation lacks label, `aria-current`, semantic links, skip/focus movement and expanded badge names. | Preserve labels/hashes/breakpoints while making routing and navigation semantic. |
| `SHELL-02` | Summary failure can leave a blank view and false persona fallback; drawer failures render nothing or stale data; language leaks between documents; review failure looks empty; drawers can stack; warning/error styling is inconsistent; toasts lack announcement/history/close; modals lack labeling, Escape, focus trap/return and inert background. | Add explicit load/error/retry, deterministic severity and one accessible overlay primitive. |
| `CAP-01` | Input is not reset; picker/copy/backend type allowlists disagree; extra drops are ignored; no preflight/progress; HTTP error field mismatch yields `Unbekannter Fehler`; preview trusts browser MIME and lacks PDF/TXT/error/edit tools; drop target is not keyboard-operable. | Publish one format/limit contract, clear inputs, classify errors and make intake accessible while retaining hardened server validation. |
| `CAP-02` | Empty and failed catalogs are indistinguishable; every preview is an image; filename dedupe is not content dedupe; SQLite retains a concurrent duplicate window; WebP samples and administration are absent. | Preserve vault/idempotency semantics and add media-aware empty/error/dedupe treatment. |
| `CAP-03` | Progress labels are timer animation; active job/recheck is memory-only; polling timeout is nonrecovering; no recent-upload recovery/cancel/attempt/backoff/dead-letter UI; terminal retry resubmits; result correction/verification/completion/undo is absent; saved-needs-review can promise a missing item. | Rediscover durable jobs, expose truthful stage/failure/review state and repair the filing-reaper gap. |
| `DOC-01` | Full counts accompany only locally loaded search/sort results; no loaded-count disclosure, scope-all selector or snapshot token; first-page failure looks empty; no archive/failed/person filters or document mutations/bulk/export/saved views. | Move full-set operations server-side or label partial state; make initial errors recoverable. |
| `DOC-02` | Drawer ignores document cache fallback; uncached/failure can render nothing; stale/language/default-confidence/storage labels can mislead; PDF/TXT are filename-only; original failures leave the app; no detail mutations or integrated PDF behavior. | Preserve encrypted original reads/deep links and add truthful, recoverable presentation. |
| `TASK-01` | Actions/deadlines are projections with conflicting badges and no persistence; past/future/date parsing/dedupe rules can mislead; there is no local error/retry or midnight refresh. | Preserve exact readonly projection only; a real task system is new scope. |
| `FACT-01` | Canonical counts and document snapshots diverge; manual/corrected facts can disappear; verified page includes proposed cards; provenance is shallow; progressive failure is silent; no correction/unverify/revert/delete/bulk flow; copy lacks feedback and readonly controls remain visible. | Define one canonical wallet and truthful provenance; design reversal/correction explicitly. |
| `DB-01` | Tables are silent partial client projections; “Beträge & Fristen” contains every date; dead facts branch would issue an invalid verification; no server table/export/edit/bulk/paging/grouping contract. | Preserve reachable columns/handoffs, delete the dead branch or revive it as an explicit new contract. |
| `FAMILY-01` | Surface is linked knowledge, not user/family administration; manually created unlinked persons are filtered; failures look empty/null; selection is memory-only; date and native fact-edit semantics are loose. | Name the domain accurately, preserve linkage behavior and add explicit recovery/capabilities. |
| `ENT-01` | No search/sort/status/paging/refresh; load failure looks empty; selected card has no address; manual entities lack metadata/identifier lifecycle; a manual person creates no `Person` or access. | Preserve normalized ownership and confirmed origin; make lifecycle/reachability explicit. |
| `ENT-02` | Card, canonical fact and snapshot projections differ; reprocess replaces the envelope but retains run history; current value can retain stale evidence; resolved candidates remain conflict; failed fetch has no inline recovery; metadata/identifiers cannot be edited/deleted. | Add canonical listing, evidence tied to current revision and normalized conflict/history rules. |
| `ENT-03` | Mention completeness/same-kind decisions are underconstrained; only one candidate is retained, two-question overflow silently proposes cards, and removed subject links can block restoration. | Strengthen validation/idempotency and surface overflow/reaper outcomes. |
| `ENT-04` | Target-list failure becomes empty; one clicked role performs pair-wide unlink; no restore/history/undo/bulk path exists. | Disclose pair-wide scope and preserve durable guards; recovery is a new contract. |
| `ENT-05` | Direct merge and all unmerge are backend-only; core merge does not require equal kinds; unmerge is LIFO/snapshot-limited and can leave post-merge edits on survivor with no preview/conflict UI. | Preserve atomic survivor/snapshot invariants; do not call this generic undo. |
| `REVIEW-01` | Loading/error look empty; buttons permit duplicate submits; stale copy asks for nonexistent refresh; some action copy is inaccurate; focus IDs are ignored; no filter/search/paging/history/undo/bulk/keyboard flow; readonly mutations remain visible; duplicate refiling can enqueue. | Add observable loading/busy/refresh/focus/history, accurate copy and active-job uniqueness. |
| `ASSIST-01` | Durable history is not answer context; no threads/retention controls; ordering lacks ID tie-break; polling is unbounded whole-list fixed-rate; concurrent sends, stale responses and gate/network ambiguity can strand/duplicate/erase optimistic rows; initial failure looks empty. | Preserve durable job/message closure and explicit statelessness; bound, correlate and recover polling/submission. |
| `ASSIST-02` | Direct search is backend-only; dialect results differ; corrupt/missing originals can fail rather than abstain; no user-selected source/tool/filter/saved query or conversation scope. | Preserve fixed scoped ladder and qualify dialects; classify original failures honestly. |
| `ASSIST-03` | Citations are scope-only, can be empty and lack page/quote/claim support; chips are nonkeyboard spans; title linking is separate; abstention and activity copy can overstate evidence. | Bind/display structured evidence and use semantic controls/copy. |
| `FORM-01` | Prototype treats unverified facts as usable, has naive name/source/completion logic, cosmetic progress, stale counts, always-enabled mock export and no validation/persistence/draft/audit/undo/API/generated bytes. | Retain only as a client prototype reference; real forms are new scope. |
| `PDF-00` | No integrated viewer, thumbnails, zoom/rotation/text layer, AcroForm mapping/fill/flatten, annotation, signature, print/download output, derivative/version/history or undo. | Keep absent for equivalence; any implementation needs a new threat model and encrypted artifact contract. |
| `DASH-01` | Browser/server dates can disagree; missing person falls back to `Ilja`; “fine” can coexist with overdue deadlines; quick ask is memory-only; summary failure/staleness is invisible; counts mix semantics. | Remove false identity/status, surface failures/staleness and define handoff lifetime. |
| `INSIGHT-01` | Summary/documents lack one snapshot; partial failure is silent; totals ignore settlement/currency and always render EUR; document date is labeled capture month; hardcoded fallback date exists; no scope/range/drilldown/retry/export/accounting policy. | Use an explicit snapshot/partial marker, honest date/currency/settlement semantics and recovery. |
| `HISTORY-01` | First-page failure looks empty; load-more has no busy/error guard and can append duplicates; relative time does not update; no refresh/exact time/actor/detail/filter/export/retry. | Preserve readonly selected vocabulary/keyset order and add recovery/concurrency guards. |
| `UNDO-00` | No generic inverse API, undo/redo stack, History reversal, snapshot selection or event replay. | Exclude from equivalence; future reversal is mutation-specific new design. |
| `CIRCLE-00` | No current model, migration, route, client method, navigation, view, test, persistence or runtime. | Exclude entirely; historical sharing intent is not evidence or a rebuild obligation. |

## Explicit non-capabilities

The following must stay visibly classified as absent, backend-only, prototype, or planned-only. They are not hidden acceptance requirements:

- no durable task/reminder model, creation, assignment, completion, recurrence, notification, calendar or snooze;
- no generic undo/redo, arbitrary inverse mutation, History replay or reversible event log;
- no integrated PDF viewing/editing/filling/annotation/signature/output/versioning;
- no Circles sharing, invitation, lens, switcher or cross-vault sharing runtime;
- no vault creation/switch/archive, membership invite/accept/change/remove/leave, ownership transfer or client role administration;
- no signed-in email/password/profile management, session/device list, revoke-other-sessions, remember-me or MFA;
- no client account export/deletion, AI-consent withdrawal, direct search, direct entity merge or unmerge;
- no document rename/move/tag/archive/delete/refile/bulk mutation, saved search or full-set table query UI;
- no conversation memory, threads, picker, edit/regenerate, archive/delete or retention controls;
- no real form draft, persistence, validation, API, audit trail, generated artifact or download;
- no claim-level citation/provenance guarantee, cross-person/vault search scope, arbitrary SQL or user-selected answer tools;
- no user-facing worker/dead-letter/operator retry, queue health, backup, restore, key rotation or object reconciliation control;
- no complete audit/security-event replay: Verlauf is a selected readonly product feed;
- no production claim from the sample OpenAPI, optional S3 adapter test, local runtime smoke, synthetic fixtures or public golden-script tests alone.

## Decisions a clean rebuild must make explicitly

| Decision | Current truth that prevents an implicit choice |
| --- | --- |
| repair versus compatibility | Login validation, false empty/loading states, dead Database facts, ignored priority, inline recovery, readiness, metadata/hash drift and misleading copy are verified defects/limitations, not desirable equivalence targets. |
| one authoritative schema path | PostgreSQL migrates fully; SQLite create-all works but fresh SQLite Alembic does not. |
| evidence depth | The schema can hold more than the application records; current citations/provenance are document/page-shallow. |
| physical erasure | Database/key deletion can succeed while object deletion fails; cryptographic and physical completion need separate statuses. |
| storage migration | Current rows cannot truthfully route mixed local/S3 objects. |
| conversation context | Durable transcript exists, but answer generation is stateless by design. |
| task/form/PDF/Circle scope | These are projection, prototype, absent and planned-only respectively; implementing them is product expansion. |
| accessibility divergence | Semantic routing, focus management, announcements and permission-aware controls improve the product and must be documented as intentional repairs. |
| release claim | Repository gates, production deployment/storage/recovery proof and the separately authorized private golden attestation are distinct layers. |

Use [[Acceptance and Equivalence Proof]] to turn each retained invariant and approved repair into executable acceptance evidence. Use [[Dependency-Ordered Rebuild Sequence]] to place the repair at the earliest layer that owns it.

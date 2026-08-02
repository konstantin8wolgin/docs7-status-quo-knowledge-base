---
id: rebuild-acceptance-equivalence-proof
title: Acceptance and Equivalence Proof
kind: rebuild
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/rebuild
  - status-quo/acceptance
parent: "[[Rebuild Atlas]]"
related:
  - "[[Cross-Layer Invariants]]"
  - "[[Dependency-Ordered Rebuild Sequence]]"
  - "[[Capability Ledger]]"
  - "[[Contract Coverage]]"
  - "[[Known Gaps and Non-Capabilities]]"
---

> [!info] Navigation
> Parent: [[Rebuild Atlas]]. Siblings: [[Cross-Layer Invariants]] · [[Dependency-Ordered Rebuild Sequence]]. Coverage: [[Capability Ledger]] · [[Contract Coverage]] · [[Known Gaps and Non-Capabilities]].

# Acceptance and Equivalence Proof

Equivalence means that the rebuilt system preserves the frozen snapshot's trusted and user-observable contract, including qualified failure behavior and reachability. It does not mean identical source layout, accidental implementation details, or silent reproduction of every defect.

## Acceptance policy

| Contract class | Acceptance rule | Divergence rule |
| --- | --- | --- |
| Exact security and trust invariants | Every applicable `SQI-*` scope, authorization, consent, encryption, rollback, fencing, secret-handling, and erasure rule must pass equivalent or stronger negative proof. | A stronger control is allowed only when it does not remove required user semantics or broaden access. A weaker control is never equivalent. |
| User semantics | Preserve the owning feature note's entry points, German labels when contract-significant, transitions, status distinctions, and durable-versus-memory lifetime. | Copy/layout may improve. A changed result, reachability, or lifetime is a documented product divergence and needs explicit acceptance. |
| Observable current defects | First reproduce the snapshot result in an end-user-shaped scenario. Then either retain it as compatibility behavior or record an explicit corrected result and proof. | A defect may be corrected in a clean rebuild; it may not disappear from the comparison or be silently relabeled as current behavior. |
| Backend-only, development-only, indirect, and dead paths | Preserve the interface and its reachability classification when it belongs to the structural contract. Do not promote it to a user-facing promise. | Removing dead code or adding a UI are separate decisions. The dead Database facts branch may be deleted; direct merge/unmerge, search, consent withdrawal, export/deletion, and health/readiness remain classified until intentionally changed. |
| Prototype behavior | Preserve it only as a clearly labelled prototype when compatibility requires it. Mock output must not pass acceptance as real output. | A production feature needs a new durable contract; it is not equivalent merely because it resembles the prototype UI. |
| Absent and planned-only behavior | Exclude from the implementation and equivalence gates. Maintain negative tests or inventory checks where confusion is likely. | Adding Circles, generic undo, integrated PDF editing/annotation/signature/output, task persistence, or other explicit non-capabilities is new product scope. |

> [!warning] Defect corrections are explicit divergences
> A divergence record must name the snapshot scenario and result, the replacement result, affected `SQI-*` and capability IDs, migration/compatibility impact, automated proof, manual proof, and approval. “Cleaner implementation” is not a sufficient reason or record.

## Equivalence scenario matrix

Proof is layered. “Automated proof” names the current closest executable evidence and the equivalent rebuild test to retain. “Manual proof” is required where browser interaction, deployment topology, or recovery cannot be established by the named test alone.

### Happy paths and user semantics

| Scenario | Current expected result | Capabilities / invariants | Automated proof | Manual proof | Qualifier |
| --- | --- | --- | --- | --- | --- |
| Sign up, restore, and log out | Sign-up atomically creates user/vault/self person/person entity/owner membership/token/session; cookie restores the shell; logout revokes and clears it. | `AUTH-01`; `SQI-ID-01`, `SQI-SCOPE-01` | Auth signup/login/me/logout and session lifecycle tests; client credential/401 tests | Complete German auth modes and reload/logout flow in a browser | Initial verification email send is part of signup transaction. |
| Verify email and reset password | Fragment token is single-use; verification marks the user; reset changes password and revokes all sessions. | `AUTH-02`; `SQI-TOKEN-01` | Auth token TTL/replay/concurrency/rollback tests; token-link client test | Follow both fragment links, confirm URL replacement and signed-out result | Request endpoints intentionally hide account existence; resend may claim success after send failure. |
| Capture one valid upload | Member + gates accepts one file, encrypts original, creates durable processing work, polls to a document, and hands off to detail/facts/tasks. | `CAP-01`, `CAP-03`, `DOC-01`, `DOC-02`; `SQI-GATE-01`, `SQI-FILE-01`, `SQI-JOB-01` | Upload compatibility/validation/crypto/queue tests; client capture polling tests | Drop/picker/camera path, result content, original open, and navigation handoff | Visible format copy and ordinary backend error presentation are current defects. |
| Import a sample twice | Catalog is vault-scoped; a valid import uses the same pipeline; PostgreSQL concurrent/sequential duplicate requests converge on active/completed work. | `CAP-02`, `CAP-03`; `SQI-FILE-01`, `SQI-JOB-01` | Sample import/path/content/idempotency tests | Catalog loading, media preview, disappearance after success | SQLite retains a check-then-create race; PDF/TXT sample previews are misleading. |
| Browse and deep-link documents | Current-subject keyset pages have stable continuation; a document hash opens detail and authorized original; closing replaces the hash. | `DOC-01`, `DOC-02`, `SHELL-01`; `SQI-FILE-READ-01`, `SQI-CLIENT-01` | Pagination, route/hash/cache, drawer, crypto/file-response tests | Back/Forward, direct deep link, cached-then-fresh and media behavior | Search/sort cover loaded pages while counts cover the complete summary. |
| Verify a fact and inspect a card | Matching canonical fact becomes verified with revision/provenance and resists later machine overwrite; live entity card reflects canonical current value. | `FACT-01`, `ENT-02`; `SQI-FACT-01` | Fact stickiness, manual cards, review provenance tests | Wallet source/copy/verify and card edit/source display | Wallet snapshot and canonical/card projections can diverge; direct-edit source may not support the new value. |
| File and review an ambiguous mention | Filing asks at most two new questions in a pass; a user resolution assigns/creates/constrains atomically and refreshes Postfach/summary. | `ENT-03`, `REVIEW-01`; `SQI-FILING-01`, `SQI-REVIEW-01` | Filing decision/budget/idempotency and review action tests | Exact German choices/feedback and card/document handoffs | Overflow silently creates proposed cards; one-candidate `gleich` copy overstates merge behavior. |
| Ask a question with source navigation | One question creates durable user/pending-assistant messages and run/job; scoped ladder completes or abstains; citations open current-person documents. | `ASSIST-01`–`ASSIST-03`; `SQI-SEARCH-01`, `SQI-CITE-01` | Answer rung/tool/citation/chat closure tests; client polling/progress tests | Suggestion/composer, progress text, abstention, citation keyboard/pointer behavior | Conversation is stateless; citation guards scope/title only, not claim support. |
| Navigate every destination responsively | All 12 hashes remain available on desktop, 72 px rail, and mobile horizontal tab bar; view changes preserve global store and discard view-local state. | `SHELL-01`, `SHELL-02`; `SQI-CLIENT-01` | View/hash regressions and source contract tests | Exercise above 920, 721–920, ≤720, and ≤640 widths with Back/Forward and overlays | Active mobile tab is not auto-scrolled; accessibility gaps are divergence candidates. |
| Read dashboard, insights, and history | Summary counts/links render; Insights derives mixed snapshot charts; History pages durable selected events and links to entity/document. | `DASH-01`, `INSIGHT-01`, `HISTORY-01` | Summary, activity pagination/vault, and client view tests | Verify current labels, links, changing chart inputs, and history relative times | Insights is not accounting; History is not undo; first-request failures can look empty/blank. |

### Failures and degraded states

| Scenario | Current expected result | Capabilities / invariants | Automated proof | Manual proof | Qualifier |
| --- | --- | --- | --- | --- | --- |
| Invalid upload metadata/content/quota | Reject before durable job with structured `413` or `415`; temporary file is removed. | `CAP-01`; `SQI-FILE-01` | Upload validation, magic mismatch, oversize, quota tests | Observe Capture's generic `Unbekannter Fehler` defect versus corrected disclosure | Concurrent quota admission is not hard-bounded. |
| Summary or list request fails | Global summary can leave a blank/null view; several lists collapse failure into empty or partial state. | `SHELL-02`, `DOC-01`, `DB-01`, `FAMILY-01`, `REVIEW-01`, `ASSIST-01`, `HISTORY-01`; `SQI-CLIENT-01` | Client source/regression tests where present | Inject summary/documents/entities/review/messages/activity failure and record exact visible state | A clean rebuild should correct these only as explicit UI divergences. |
| Processing exceeds client poll budget | Durable job continues; client returns `processing_timeout` with same job ID; `Status erneut prüfen` starts another bounded poll without resubmitting bytes. | `CAP-03`; `SQI-JOB-01`, `SQI-RETRY-01` | API job and capture polling tests | Leave/reload to demonstrate that current resume handle is lost | Rediscovery is a preferred explicit divergence, not current behavior. |
| Filing dead-letters after extraction | Document remains usable; Capture reports saved-needs-review and filing failure separately. | `CAP-03`, `ENT-03`, `REVIEW-01`; `SQI-RETRY-01` | Queue filing dead-letter/poll/review tests | Verify result copy and Postfach presence/absence for normal-fail versus reaper path | Reaper terminalization may create no immediate review item. |
| Provider/tool/storage failure during chat | Infrastructure exceptions fail the one-attempt job and close its own pending bubble; expected tool errors stay bounded and ladder continues. | `ASSIST-01`, `ASSIST-02`; `SQI-LEASE-01`, `SQI-SEARCH-01` | Chat failure/dead-letter/lost-lease and tool validation tests | Observe fixed German failure bubble and polling stop | Provider judgment degradation can look like evidence abstention and is weakly recorded. |
| Account object cleanup fails after commit | Deletion/reset still succeeds after database/key erasure; each object deletion is attempted; orphan ciphertext may remain. | `AUTH-04`; `SQI-ERASURE-01` | Account/reset storage-delete failure tests | Inspect operational signal and communicate cryptographic versus physical result | Current logging drops useful extras; no reconciler proves cleanup. |

### Security and privacy

| Scenario | Current expected result | Capabilities / invariants | Automated proof | Manual proof | Qualifier |
| --- | --- | --- | --- | --- | --- |
| No cookie, forged cookie, or legacy identity header | Protected route rejects; caller cannot assert user/vault/consent through old headers. | `AUTH-01`, `AUTH-05`; `SQI-ID-01`, `SQI-SCOPE-01`, `SQI-AUTHZ-01` | Adversarial all-route, forged/tampered cookie, legacy-header tests in both DB lanes | Inspect browser request identity and `401` transition | Public routes and logout have their declared exceptions. |
| Cross-tenant ID probing | Foreign documents/files/jobs/entities/facts/reviews are indistinguishable from absent through `404`-style behavior. | All durable user-facing capabilities; `SQI-SCOPE-01` | Cross-tenant adversarial matrix in both lanes | Attempt representative foreign deep link and original URL | Corrupted cross-row same-vault consistency is not fully tested. |
| Readonly/member/owner mismatch | Server rejects unauthorized writes/reset regardless of visible controls. | `AUTH-05`, `SHELL-03`; `SQI-AUTHZ-01` | Authz and declared-role adversarial tests | Verify currently visible-but-rejected controls and any rebuilt capability projection | UI permission awareness is absent and should be corrected explicitly. |
| Unsafe cross-origin request | Present unapproved Origin on POST/PUT/PATCH/DELETE gets normalized `403` with request/security headers. | `AUTH-01`; `SQI-HTTP-01` | Cross-origin, CORS preflight, security-header lifecycle tests | Browser/proxy-origin exercise at the real edge | Missing Origin passes; no CSRF token or complete edge policy exists. |
| Tampered ciphertext or lost key | No plaintext is returned; AES-GCM/key unwrap fails closed. | `CAP-01`, `DOC-02`; `SQI-CRYPTO-01`, `SQI-FILE-READ-01` | Crypto tamper/wrong/missing-key tests | Restore a known encrypted object and download through authorization | No AAD or stored-hash comparison; corrupted cross-vault file link lacks dedicated proof. |
| Consent revoked before provider use | Future live-provider upload/import/chat is blocked; queued chat recheck can fail its pending bubble without provider work. | `AUTH-03`, `CAP-01`, `ASSIST-01`; `SQI-GATE-01` | Consent withdrawal/adversarial and job recheck tests | Grant, queue, revoke, and inspect user-visible recovery | No withdrawal UI; revocation after the one start check does not cancel an in-flight call. |

### Concurrency and transactionality

| Scenario | Current expected result | Capabilities / invariants | Automated proof | Manual proof | Qualifier |
| --- | --- | --- | --- | --- | --- |
| Duplicate signup/token claim | One durable winner; loser receives stable conflict/invalid result, not 500 or partial account/token state. | `AUTH-01`, `AUTH-02`; `SQI-TOKEN-01` | Signup race and token single-use tests on both DB lanes | None beyond response/error copy | Duplicate signup is HTTP 400 with code `conflict`. |
| Two workers claim/finish one job | One live lease owner publishes; stale/expired owner rolls its body back and cannot overwrite the winner. | `CAP-03`, `ASSIST-01`; `SQI-LEASE-01` | Claim/fence/lost-lease tests | Inspect durable attempt/owner/stage during a controlled run | Chat progress commits are the bounded exception. |
| Filing and auditor overlap | Same-vault filing/auditor jobs serialize; other types, including chat, may run concurrently. | `ENT-03`, `REVIEW-01`, `ASSIST-01`; `SQI-LEASE-01` | Queue/auditor serialization tests, including PostgreSQL locks | Run two workers and inspect job order | SQLite relies on writer behavior rather than PostgreSQL advisory locks. |
| Two resolutions of one review item | Exactly one transaction applies its mutation and resolves; loser rolls back and receives `409`. | `REVIEW-01`; `SQI-REVIEW-01` | Same-item concurrency tests on SQLite and applicable PostgreSQL path | Rapid double-click demonstrates client stale feedback gap | Buttons are not locally disabled; distinct refile producers can still duplicate jobs. |
| Opposite merge attempts | Atomic source claim and canonical locking prevent redirect cycles; unmerge obeys LIFO and compatibility snapshot. | `ENT-05`; `SQI-MUTATION-01` | Entity merge race, no-cycle, LIFO and edited-fact tests | Backend-only direct route exercise if retained | Direct merge/unmerge have no current UI. |
| Concurrent quota admission | Both requests may pass an unlocked sum and exceed the configured vault limit. | `CAP-01`; `SQI-FILE-01` | Add an explicit reproduction if compatibility is considered | Load two near-limit uploads and measure accepted total | Preferred rebuild behavior is atomic accounting; correcting it is an explicit divergence. |

### Recovery and operations

| Scenario | Current expected result | Capabilities / invariants | Automated proof | Manual proof | Qualifier |
| --- | --- | --- | --- | --- | --- |
| Ordinary retry and dead letter | Failure below max requeues with persisted due time; final failure closes the applicable projection; dead letters are terminal. | `CAP-03`, `ASSIST-01`; `SQI-RETRY-01` | Queue retry/backoff/dead-letter tests | Inspect client status and operator-visible job row | No generic retry endpoint; feature actions create new work. |
| Expired worker lease | Worker reaper requeues or dead-letters and closes extraction/chat/audit projections as implemented. | `CAP-03`, `ASSIST-01`, `REVIEW-01`; `SQI-RETRY-01` | Reaper tests for each dependent type | Stop a worker mid-job and observe another worker recover | Inline mode has no reaper; filing review projection is incomplete. |
| Production start ordering | Schema and bucket must be initialized before API/workers; production reset route is absent. | `AUTH-04`, all backend capabilities; `SQI-SCHEMA-01`, `SQI-JOB-01` | Production settings/route tests and migration lane | Start the actual production graph after init jobs; probe API and workers | Current Compose does not encode migrations/bucket init and workers inherit an invalid API healthcheck. |
| Readiness under partial dependency failure | `/ready` proves only `SELECT 1`; it can be green with stale schema, broken storage, no workers, provider/email failure, or unusable keys. | Backend/operations only; `SQI-OPERATE-01` | Lifecycle readiness tests | Fail each dependency and compare `/health`, `/ready`, job/file behavior | A stronger readiness contract is an explicit, desirable divergence. |
| Restore a backup | Database + ciphertext + matching master key restore, migrate, start, then authorized download/decryption of a known file. | `DOC-02`, `AUTH-04`; `SQI-OPERATE-01` | Crypto/storage primitives only | Required isolated restore-by-decryption drill | Current repository has no automated backup/restore or recorded drill. |
| Rotate the master key | One-blob rewrap primitive works, but no safe batch/resume/dual-key/version workflow exists. | Operations only; `SQI-CRYPTO-01`, `SQI-OPERATE-01` | `rewrap_vault_kek` unit proof | Required stop-writers/full-vault rotation and download verification if current procedure is retained | A production rebuild should implement and drill a resumable versioned process. |
| Release quality proof | Both database lanes, client, static, OpenAPI, structural, runtime, and applicable private quality evidence are separately green. | All current capabilities | Commands below | Local runtime, production graph, recovery, provider/storage and private attestation as applicable | CI presently omits several manual/optional lanes. |

## Exact repository acceptance commands

The configured major-change gate is:

```bash
cd backend && .venv/bin/python -m pytest
cd backend && TEST_DATABASE_URL=postgresql+psycopg://docs7:docs7@127.0.0.1:5433/docs7 .venv/bin/python -m pytest
cd client && node --test src/*.test.mjs && npm run build
ruff check backend
ruff format --check backend
backend/.venv/bin/python backend/scripts/export_openapi.py --check
./cbmap check --base origin/main
bash start.sh
```

The status-quo contract itself additionally requires:

```bash
backend/.venv/bin/python backend/scripts/check_status_quo.py --repo-root .
backend/.venv/bin/python -m pytest backend/tests/test_status_quo.py
```

The first command proves strict frontmatter, status, links, parent backlinks, planned-only isolation, exact 33-capability parity across the owning feature notes and both capability ledgers, exact 185-ID parity between [[Contract Coverage]] and the generated inventory, technical reciprocity for current capabilities, inventory-ID mentions, and exact UI view-key/hash parity. It is structural proof only: the behavioral, security, concurrency, recovery, database, browser, and operational gates below remain separate requirements.

## Final acceptance record

A rebuild acceptance record must state:

- snapshot revision and rebuild revision;
- exact capability and inventory set comparison;
- every applicable `SQI-*` result;
- commands, exit codes, and skipped/optional lanes;
- each accepted defect reproduction and each explicit corrected divergence;
- manual browser, production, storage, restore, rotation, and incident evidence;
- separately authorized, sanitized private-golden pass/fail attestation when required;
- remaining operational qualifications.

No green subset may be summarized as full equivalence when a required lane, failure class, or recovery proof is missing.

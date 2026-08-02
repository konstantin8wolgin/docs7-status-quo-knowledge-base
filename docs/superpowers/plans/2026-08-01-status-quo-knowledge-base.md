# docs7 Status-Quo Knowledge Base Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the finished, reconstruction-grade `docs/status-quo/` corpus that describes every current docs7 feature and technical subsystem, separates historical intent, and proves complete source-to-feature traceability.

**Architecture:** `docs/status-quo/` is the human and rebuild specification; `docs/map/` remains the canonical source router and generated inventory. Feature notes describe observable behavior, technical notes explain implementation and invariants, rebuild notes define dependency order, and traceability notes prove coverage. A small repository checker validates links, frontmatter, capability identities, and generated-inventory coverage.

**Tech Stack:** Obsidian Flavored Markdown, Mermaid, Python 3.12 standard library, pytest, the repository Codebase Map, React/Vite source evidence, FastAPI/SQLAlchemy source evidence.

## Global Constraints

- Snapshot truth is based on commit `5448cf335e2cb25d74d6c0e6c476b72d1e14e803`; later documentation-only commits do not alter product behavior.
- Executable code, tests, migrations, configuration, and generated contracts outrank curated prose and historical plans.
- Never read or reproduce root `.env`, credentials, raw transcripts, private documents, plaintext keys, sensitive prompt content, or private golden corpus/output.
- Product documentation is English; exact user-visible German labels are quoted when they are part of the behavior contract. Code and comments remain English.
- Every status-quo note has YAML frontmatter with a unique `id`, unique human-readable `title`, `kind`, `status`, `snapshot_commit`, `last_verified`, and `tags`.
- Feature notes also declare `capability_ids`, `delivery`, `reachability`, `persistence`, and `evidence`; technical notes declare `map_pages`, `inventory_refs`, and `feature_links` when applicable.
- Internal note relationships use Obsidian wikilinks. Every note basename is unique across `docs/status-quo/` so wikilinks resolve unambiguously.
- Source evidence uses repository-relative paths and symbols, never fragile line numbers.
- Delivery values are exactly `implemented`, `partial`, `prototype`, `planned-only`, or `absent`.
- Reachability values are exactly `user-facing`, `development-only`, `backend-only`, `dead-or-unreachable`, or `not-applicable`.
- Persistence values are exactly `durable`, `session-memory`, `ephemeral`, or `none`.
- Evidence values are exactly `runtime-code-tests`, `code-and-tests`, `source-only`, or `historical-only`.
- Circles and every other planned-only idea live under Historical Intent with a prominent warning and never enter the current rebuild contract.
- Forms must be described as a client-only prototype: no PDF is generated, changed, signed, annotated, printed, or downloaded by the current workflow.
- Undo, annotation/drawing, integrated PDF editing, and other checked absences are explicit current non-capabilities, not silently omitted.
- Mermaid is required for relationships and state transitions where it reduces reading effort; diagrams must be accompanied by precise prose.
- Do not hand-edit `docs/map/inventory/*` or `docs/map/source-lock.json`; regenerate and reconcile through `cbmap`.
- Do not change product behavior. Only the knowledge-base checker, its tests, the status-quo corpus, and verified stale documentation are in scope.
- Preserve unrelated user changes. Never inspect historical plans broadly; read a plan only when a status-quo note needs to distinguish a specific historical capability.

---

## File Structure

### Validation

- `backend/scripts/check_status_quo.py` — validates the corpus without external libraries.
- `backend/tests/test_status_quo.py` — focused tests for link, frontmatter, ID, status-value, and inventory-coverage failures.

### Entry and guides

- `docs/status-quo/INDEX.md`
- `docs/status-quo/00-guides/How to Use This Knowledge Base.md`
- `docs/status-quo/00-guides/Truth and Status Model.md`
- `docs/status-quo/00-guides/Reading Paths for Humans and Agents.md`
- `docs/status-quo/00-guides/Snapshot and Evidence Manifest.md`

### Features

- `docs/status-quo/10-features/Feature Atlas.md`
- Account and Access: hub plus Authentication and Sessions; Email Verification and Password Reset; AI Consent; Account Export Deletion and Development Reset; Role and Vault Limitations.
- Shell and Navigation: hub plus Navigation and Responsive Shell; Global Drawers Toasts and Loading; Permission-Aware Affordance Gaps.
- Capture and Processing: hub plus Capture Inputs and Validation; Sample Import; Processing Polling and Capture Results.
- Documents and Knowledge: hub plus Document Library; Document Detail and Original Files; Tasks and Deadlines; Fact Wallet and Verification; Database Tables; Family and Person Cards.
- Facts Entities and Review: hub plus Entity Register and Manual Creation; Entity Cards and Facts; Filing and Identity Decisions; Unlink Reassign Merge and Unmerge; Review Inbox and Conflict Resolution.
- Assistant and Search: hub plus Assistant Conversation and Progress; Search and Four-Rung Answer Ladder; Citations Provenance and Abstention.
- Forms: hub plus Form Autofill Prototype; PDF Viewing Filling and Annotation Boundary.
- Dashboards and Reporting: hub plus Dashboard; Insights and Derived Metrics; Activity History and No-Undo Boundary.
- Historical Intent: hub plus Circles Planned Sharing; Historical Plans Usage Boundary.

### Technical

- `docs/status-quo/20-technical/Technical Atlas.md`
- System Architecture: System Topology and Composition; Component Ownership and Dependency Direction; Request Lifecycle Errors and Middleware.
- Client Architecture: Client State Navigation and Cache; Client API Permissions and Failure Contract; UI Reachability Accessibility and Responsive Behavior.
- Backend and API: Router Domain and Infrastructure Boundaries; Complete API Contract.
- Data and Migrations: Domain Model and Relationships; Migration History and Database Dialects; Data Lifecycle Reset Export and Deletion.
- Jobs and AI: Durable Job State Lease Fencing and Recovery; Extraction Envelope Evidence and Provenance; Filing Auditor and Policy-Limited Automation; Search and Answer Agent Internals.
- Security and Storage: Identity Sessions Membership and Vault Scope; Encryption Key Hierarchy and Object Storage; Upload Download Quota and Erasure.
- Runtime and Operations: Settings and Environment Contract; Local and Production Runtime Topology; Observability Backup Restore and Incident Recovery; Test Lanes Gates and Release Proof.

### Rebuild and traceability

- Rebuild Atlas; Cross-Layer Invariants; Dependency-Ordered Rebuild Sequence; Acceptance and Equivalence Proof.
- Capability Ledger; UI Surface Coverage; Contract Coverage; Feature-to-Code Matrix; Known Gaps and Non-Capabilities.

---

### Task 1: Corpus contract, skeleton, and validator

**Files:**

- Create: `backend/scripts/check_status_quo.py`
- Create: `backend/tests/test_status_quo.py`
- Create: `docs/status-quo/INDEX.md`
- Create: all four files under `docs/status-quo/00-guides/`
- Create: `docs/status-quo/10-features/Feature Atlas.md` and its nine feature-family hub notes
- Create: `docs/status-quo/20-technical/Technical Atlas.md` and its seven technical-family hub notes
- Create: `docs/status-quo/30-rebuild/Rebuild Atlas.md`
- Do not create leaf or traceability notes owned by later tasks

**Interfaces:**

- Consumes: committed inventory at `docs/map/inventory/inventory.json` and the exact frontmatter/status contract from Global Constraints.
- Produces: `check_corpus(repo_root: Path) -> list[str]`, a CLI returning 0 on success and 1 with one diagnostic per line on failure; the root navigation contract consumed by every later note; stable hub links for later tasks.

- [ ] **Step 1: Write failing validator tests**

Create tests using temporary repositories that prove diagnostics for: missing frontmatter; duplicate `id`; duplicate note basename; unresolved wikilink; invalid delivery/reachability/persistence/evidence value; duplicate capability ID ownership; missing required inventory reference; and a passing minimal corpus. Import the checker module through `importlib.util` so no package change is needed.

- [ ] **Step 2: Run the focused tests and verify failure**

Run: `cd backend && .venv/bin/python -m pytest tests/test_status_quo.py -q`

Expected: collection or assertion failure because `check_status_quo.py` does not exist.

- [ ] **Step 3: Implement the validator**

Use only `argparse`, `json`, `pathlib`, `re`, and `sys`. Parse the simple frontmatter subset line-by-line; collect scalar values and YAML list entries. Resolve wikilinks by exact relative path without `.md` or by unique basename. Ignore fenced code blocks when scanning wikilinks and inventory IDs. Require every current route, model, job, migration, and client-method ID in `inventory.json` to occur outside code fences somewhere in the finished corpus. Permit incomplete coverage only when `--allow-incomplete` is passed, which later writing tasks use before the ledgers exist.

- [ ] **Step 4: Run focused tests until green**

Run: `cd backend && .venv/bin/python -m pytest tests/test_status_quo.py -q`

Expected: all validator tests pass.

- [ ] **Step 5: Create the entry guides and atlas hubs**

`INDEX.md` must contain a concise reader choice table for feature discovery, technical understanding, clean-room rebuild, and coverage audit; a Mermaid navigation graph; snapshot warning; and links to every top-level atlas. Guides must define truth order, four status axes, source citation style, note templates, historical isolation, and short task-specific reading paths. Hub notes must explain their scope and link only to existing parent/sibling hubs until leaf tasks populate their child indexes.

- [ ] **Step 6: Validate the initial skeleton**

Run: `backend/.venv/bin/python backend/scripts/check_status_quo.py --repo-root . --allow-incomplete`

Expected: exit 0 with no structural/link/frontmatter error.

- [ ] **Step 7: Commit**

```bash
git add backend/scripts/check_status_quo.py backend/tests/test_status_quo.py docs/status-quo
git commit -m "docs: establish status quo knowledge base"
```

### Task 2: Account, access, shell, and navigation feature notes

**Files:**

- Modify: `docs/status-quo/10-features/Account and Access/Account and Access.md`
- Create: the five Account and Access leaf notes from File Structure
- Modify: `docs/status-quo/10-features/Shell and Navigation/Shell and Navigation.md`
- Create: the three Shell and Navigation leaf notes from File Structure
- Modify: `docs/status-quo/10-features/Feature Atlas.md`

**Interfaces:**

- Consumes: note/frontmatter contract from Task 1; `client/src/auth/*`, `client/src/App.jsx`, `client/src/lib.jsx`, `client/src/api.js`, authentication/context/authorization backend modules and tests.
- Produces: capability IDs `AUTH-01` through `AUTH-05` and `SHELL-01` through `SHELL-03`, with links later consumed by technical and traceability notes.

- [ ] **Step 1: Orient and collect authoritative evidence**

Run focused `cbmap orient` queries for auth/vault/consent and client shell/navigation. Inspect the returned Map pages, then the listed source symbols and focused auth/client tests. Do not read root `.env`.

- [ ] **Step 2: Write Account and Access leaves**

Document exact form controls, validation, German errors, development auto-login, session-cookie behavior, token fragments, password reset atomicity, resend/rate-limit states, consent ordering and retry preservation, backend-only withdrawal, export/delete behavior, and missing account settings UI. Include authentication-to-vault Mermaid flow and control/state tables.

- [ ] **Step 3: Write Shell and Navigation leaves**

Document all twelve reachable destinations, exact hashes, fallback routing, Back/Forward behavior, desktop/tablet/mobile transitions, sidebar/mobile badges, top-bar buttons, review/document overlays, toasts, summary blocking/error behavior, reset role/dev mismatch, memory-only state, accessibility gaps, and controls exposed to readonly users. Include the client state-ownership/navigation graph.

- [ ] **Step 4: Reconcile indexes and links**

Populate both family hubs and Feature Atlas with concise child summaries, capability IDs, delivery/reachability badges, and bidirectional related links.

- [ ] **Step 5: Validate**

Run: `backend/.venv/bin/python backend/scripts/check_status_quo.py --repo-root . --allow-incomplete`

Expected: exit 0.

- [ ] **Step 6: Commit**

```bash
git add docs/status-quo/10-features
git commit -m "docs: explain access and navigation features"
```

### Task 3: Capture, document, knowledge, task, and family feature notes

**Files:**

- Modify: Capture and Processing hub and create its three leaves
- Modify: Documents and Knowledge hub and create its six leaves
- Modify: `docs/status-quo/10-features/Feature Atlas.md`

**Interfaces:**

- Consumes: `Capture.jsx`, document cache/API, Documents, DocumentDrawer, Aufgaben, Fakten, DatabaseView, Familie, upload/sample/job/file/fact backend routes and focused tests.
- Produces: `CAP-01` through `CAP-03`, `DOC-01` through `DOC-02`, `TASK-01`, `FACT-01`, `DB-01`, and `FAMILY-01` feature contracts.

- [ ] **Step 1: Orient and inspect current evidence**

Use Map projections for capture/documents, upload-to-filing polling, files/crypto, facts/summaries, and client architecture. Inspect exact consuming components, API methods, domain symbols, and tests.

- [ ] **Step 2: Write capture leaves**

Cover optional context, drag/drop, first-file behavior, native and camera pickers, visible-versus-actual accepted formats, size/quota and content sniffing, preview lifecycle, sample enumeration/import/dedup, verification/consent gates, retry closures, cosmetic versus server progress, 126-second default polling budget, still-processing recheck, failure retry, filing dead-letter projection, result panels, and all loading/error limitations. Include capture and upload pipeline state diagrams.

- [ ] **Step 3: Write document and knowledge leaves**

Cover folder rail, current/all scope distinction, loaded-page search, sorting, keyset pagination, cache single-flight/epoch invalidation, drawer hash behavior, summary/fallback/fetch errors, original-file serving, image versus PDF/TXT presentation, summary translation, facts/amounts/dates/trust/tags, task/deadline read-only projections, fact normalization/verification/copy/provenance, database tabs and dead facts tab, and family person-card behavior.

- [ ] **Step 4: Update family hubs and Feature Atlas**

Every child gets a one-sentence scope and status. Cross-link capture result → document drawer/facts/tasks and document facts → forms/entities/assistant without duplicating their content.

- [ ] **Step 5: Validate and commit**

Run the checker with `--allow-incomplete`; then commit as:

```bash
git add docs/status-quo/10-features
git commit -m "docs: explain capture and document knowledge features"
```

### Task 4: Entity, fact, filing, and review feature notes

**Files:**

- Modify: `docs/status-quo/10-features/Facts Entities and Review/Facts Entities and Review.md`
- Create: the five Facts Entities and Review leaves from File Structure
- Modify: `docs/status-quo/10-features/Feature Atlas.md`

**Interfaces:**

- Consumes: entity/review client components; entities, facts, filing, review, review identity, auditor domains; entity routes/models/migrations and focused tests.
- Produces: `ENT-01` through `ENT-05` and `REVIEW-01`, with entity/fact/review terminology shared by later technical notes.

- [ ] **Step 1: Collect evidence through focused Map projections**

Read the entities/filing/review subsystem and flow, then exact symbols and focused tests for manual creation, identity filing, facts, conflict resolution, merge/unmerge, unlink/reassign, audit lint, stale evidence, concurrency, and lease rollback.

- [ ] **Step 2: Write register, card, and fact leaves**

Document kind filters, card statuses, aliases, identifier kinds and uniqueness conflicts, manual creation controls, confirmation, optional card sections, manual facts, native-prompt editing, verification-state inconsistencies, source links, and person/family relationships.

- [ ] **Step 3: Write filing and mutation leaves**

Explain mention persistence, unique-identifier prematch boundary, provider decision validation, question budget, confirmed-card immutability, subject links, constraints, unlink reasons/reassignment, merge survivor rules, snapshot restoration, unmerge limits, and which operations are backend-only. Use state and relationship diagrams.

- [ ] **Step 4: Write review leaf**

Explain identity, conflict, and unfiled types; every available resolution; stale-evidence checks; single-winner locking; client feedback; retry creation; missing refresh/busy/error behavior; and auditor-opened work.

- [ ] **Step 5: Update indexes, validate, and commit**

Run the checker with `--allow-incomplete`; commit as:

```bash
git add docs/status-quo/10-features
git commit -m "docs: explain entity filing and review features"
```

### Task 5: Assistant, forms, reporting, absence, and historical-intent feature notes

**Files:**

- Modify: Assistant and Search, Forms, Dashboards and Reporting, and Historical Intent hubs
- Create: the nine corresponding leaf notes from File Structure
- Modify: `docs/status-quo/10-features/Feature Atlas.md`

**Interfaces:**

- Consumes: Assistant/chat progress, Dashboard, Formulare, Einblicke, History; search/chat/answer/audit backend; targeted `docs/plans/knowledge-base/09-circles.md` as historical-only evidence.
- Produces: `ASSIST-01` through `ASSIST-03`, `FORM-01`, `PDF-00`, `DASH-01`, `INSIGHT-01`, `HISTORY-01`, `UNDO-00`, and `CIRCLE-00`.

- [ ] **Step 1: Orient and inspect current assistant/search/reporting evidence**

Use Map projections for search-grounded chat, facts/summaries, client architecture, and activity. Inspect the current source/tests. Read only the targeted Circles plan to preserve its intent without treating it as executable evidence.

- [ ] **Step 2: Write assistant and search leaves**

Cover message persistence, pending bubbles, one-second polling, progress stages, submission/concurrency, consent recovery, network fallback, limited rich-text parsing, citation UI/accessibility, no conversation memory, search normalization/dialect differences, four answer rungs, fixed tools, original-page rasterization, citation guard limitations, abstention reasons, and job failure closure. Include the answer-ladder graph.

- [ ] **Step 3: Write forms and PDF-boundary leaves**

Enumerate all four templates and fields, fact-key resolution, naive first/last name derivation, 200 ms cascade, every field and phase state, confirm/reject/edit/confirm-all/reset/source/export controls, loss on unmount, person/verification filtering defects, blank/manual counting defects, and mock success claims. State unequivocally that no PDF editing/filling/export, AcroForm handling, annotation, signature, thumbnail, or integrated PDF viewer exists.

- [ ] **Step 4: Write dashboard/reporting/history leaves**

Cover greeting and quick-question handoff, nav stats/recent documents, task/fact/family/insight navigation, client-derived charts and temporary partial data, hardcoded date fallback, currency aggregation limitations, activity pagination/link precedence/errors, and explicit test-backed absence of undo.

- [ ] **Step 5: Write historical-intent leaves**

Summarize Circles as planned sharing visibility only: invitations, memberships, live-card versus frozen selection, read-only cross-vault lens, inbox, context switcher, and crypto deferral. Begin with a warning that no circle models, migrations, routes, client methods, UI, or runtime behavior exist. Explain how future agents may consult historical plans without upgrading them to current status.

- [ ] **Step 6: Update indexes, validate, and commit**

Run the checker with `--allow-incomplete`; commit as:

```bash
git add docs/status-quo/10-features
git commit -m "docs: explain assistant forms and reporting features"
```

### Task 6: System, client, backend, and API technical reconstruction notes

**Files:**

- Modify: `docs/status-quo/20-technical/Technical Atlas.md`
- Create/modify: all System Architecture, Client Architecture, and Backend and API notes from File Structure

**Interfaces:**

- Consumes: current feature notes; `main.py`, `deps.py`, routers, domain packages, infrastructure adapters, App/lib/api/client components, route policy, OpenAPI, generated route/client inventories, focused tests.
- Produces: technical ownership map and exact contracts consumed by rebuild and traceability notes.

- [ ] **Step 1: Orient system/client/API boundaries**

Use focused Map projections and generated inventory instead of broad source loading. Verify composition, middleware order, route mounting, development-only reset, relative `/api`, cookies, hash routing, cache ownership, and router/domain boundaries against source/tests.

- [ ] **Step 2: Write system architecture notes**

Explain process topology, `create_app` and `Deps`, adapter construction, dependency direction, router/domain/infrastructure ownership, middleware/error lifecycle, request IDs, CORS/origin behavior, and exception normalization. Include topology and request-flow Mermaid graphs.

- [ ] **Step 3: Write client architecture notes**

Explain AuthProvider/StoreProvider/view-local state, URL-persisted versus memory state, document cache scopes/single-flight/epochs, API request/error behavior, global 401 handling, permissions unavailable to UI, dead/unreachable components, responsive breakpoints, modal/drawer keyboard/focus limitations, and tests.

- [ ] **Step 4: Write backend/API notes**

Explain thin routers and direct-session domain services. The Complete API Contract must contain all 39 development routes, method/path, access role, email/consent/dev gates, request shape, response behavior, important status codes, idempotency/pagination, client reachability, handler symbol, and focused test evidence. Qualify the sample-import 200/202 OpenAPI mismatch.

- [ ] **Step 5: Update atlas, validate, and commit**

Run the checker with `--allow-incomplete`; commit as:

```bash
git add docs/status-quo/20-technical
git commit -m "docs: reconstruct system client and API architecture"
```

### Task 7: Data, migrations, jobs, extraction, filing, auditor, and answer-agent technical notes

**Files:**

- Create/modify: all Data and Migrations and Jobs and AI notes from File Structure
- Modify: `docs/status-quo/20-technical/Technical Atlas.md`

**Interfaces:**

- Consumes: all 32 models, 11 migrations, queue/worker/jobs, AI engines/schema, extraction/facts/entities/filing/review/audit/search/answer domains, generated inventories, focused SQLite/PostgreSQL tests.
- Produces: complete persistence/state-machine reconstruction and technical graph edges used by rebuild/traceability.

- [ ] **Step 1: Map the current data model and migration chain**

Use model/migration inventories, then inspect exact constraints, foreign keys, JSON variants, manual deletion order, SQLite foreign-key behavior, PostgreSQL FTS/JSONB differences, create-all versus Alembic, and migration tests.

- [ ] **Step 2: Write data and migration notes**

Catalog every model grouped by identity/tenancy, files/documents, processing/evidence, entities/review, facts/provenance, conversation/audit. Explain relationships, missing database constraints, domain-enforced tenant consistency, lifecycle deletion, exact 0001→0011 history, and dialect differences. Include relationship graphs.

- [ ] **Step 3: Write job and recovery note**

Document queued/running/completed/dead-letter transitions, claim ordering, attempt increment, exact lease fencing, rollback, backoff, expired lease reaping, per-vault filing/auditor serialization, chaining, chat progress exception, filing projection, worker versus inline differences, missing inline retry wake-up/reaper, ignored priority, and dead-letter recovery. Include state diagram.

- [ ] **Step 4: Write extraction/evidence and filing/auditor notes**

Document envelope fields and strictness, page invariants, seed/Vertex paths, provider retry/timeout/fallback, stored normalized/raw behavior, actual OCR/field/fact provenance depth, reprocess transcript guard, mention filing validation, constraints/questions, auditor schedule/lint/semantic consent, caps, and policy-limited actions.

- [ ] **Step 5: Write search/answer internals note**

Document latest-run search, PostgreSQL/SQLite retrieval, tools, answer rung transitions, selected original rendering, stateless questions, candidate and citation guards, mismatch events/reprocessing, pending message closure, and stored ChatRun evidence.

- [ ] **Step 6: Update atlas, validate, and commit**

Run the checker with `--allow-incomplete`; commit as:

```bash
git add docs/status-quo/20-technical
git commit -m "docs: reconstruct data jobs and AI internals"
```

### Task 8: Security, storage, runtime, operations, and proof technical notes

**Files:**

- Create/modify: all Security and Storage and Runtime and Operations notes from File Structure
- Modify: `docs/status-quo/20-technical/Technical Atlas.md`

**Interfaces:**

- Consumes: auth/context/authz, crypto/files/uploads/storage, settings/main/start/compose/Docker/runbook, observability/rate limit/account/reset, repository gates and focused tests.
- Produces: trust-boundary, deployment, recovery, configuration, and proof contracts consumed by rebuild notes.

- [ ] **Step 1: Orient security/storage/runtime evidence**

Use Map projections for auth/vault/consent, files/crypto/storage, GDPR account, runtime/configuration, and data/testing/operations. Never inspect environment values.

- [ ] **Step 2: Write identity and storage security notes**

Explain opaque hashed sessions, cookies, membership context, roles, application-level tenant scoping, Origin/SameSite boundary, in-memory rate limits, consent timing, AES-GCM DEK/KEK/master-key hierarchy, local/S3 adapters, SHA/storage-provider/AAD limitations, streaming intake, quota races, safe serving, caching/range limitations, and erasure ordering. Include trust and key graphs.

- [ ] **Step 3: Write settings/runtime/deployment notes**

Catalog every current environment-variable name and semantics without values. Explain local start/seed/archive behavior, SQLite/create-all, production image/API/workers/Postgres/MinIO topology, missing frontend/TLS/reverse proxy, migration-first order, health/readiness scope, worker health gap, and secure-cookie deployment needs. Include deployment graph.

- [ ] **Step 4: Write observability/recovery/proof notes**

Explain request IDs/access logs, dropped worker fields and missing exception logging, durable operational records, backup triad, restore-by-decryption proof, key rotation limitation, object cleanup/orphans, account/export/reset lifecycle, SQLite/PostgreSQL/client/Ruff/OpenAPI/Map/runtime gates, optional S3 proof, and private golden boundary.

- [ ] **Step 5: Update atlas, validate, and commit**

Run the checker with `--allow-incomplete`; commit as:

```bash
git add docs/status-quo/20-technical
git commit -m "docs: reconstruct security storage and operations"
```

### Task 9: Rebuild handbook and complete traceability ledgers

**Files:**

- Create/modify: all four `docs/status-quo/30-rebuild/` notes
- Create/modify: all five `docs/status-quo/40-traceability/` notes
- Modify: `docs/status-quo/INDEX.md`
- Modify: Feature Atlas and Technical Atlas only for missing cross-links discovered during ledger construction

**Interfaces:**

- Consumes: every finished feature/technical note and the committed route/model/job/migration/client inventories.
- Produces: exhaustive capability, UI, contract, and feature-to-code coverage; dependency-ordered rebuild specification; final zero-error validator input.

- [ ] **Step 1: Build the capability ledger**

Create one stable row for every feature capability, including backend-only, dead/unreachable, prototype, planned-only, and absent items. Columns: ID, exact capability, delivery, reachability, persistence, evidence, feature note, technical notes, primary proof. Capability IDs must have exactly one owning feature note.

- [ ] **Step 2: Build UI Surface Coverage**

Account for all twelve main destinations, auth/token screens, banners, every shared drawer/dialog, reusable feature component, meaningful control group, dead components, scope cache, and backend capabilities without UI. Record entry point, controls, states, feature note, and test status.

- [ ] **Step 3: Build Contract Coverage**

List every generated route, client method, model, job, migration, and classified unknown exactly as identified in `inventory.json`; link each to its technical note and feature consumer or state `backend-only`/`structural-only`. Do not copy generated prose; add semantic ownership and rebuild relevance.

- [ ] **Step 4: Build Feature-to-Code Matrix and known-gaps register**

Map each capability to client symbols, API method/route, domain symbols, job, models/migrations, focused tests, and Map pages. Known Gaps must include every verified drift from the design spec plus UI accessibility/error gaps, contract mismatches, dead code, non-capabilities, and current-defect-versus-clean-rebuild guidance.

- [ ] **Step 5: Write rebuild handbook**

Define immutable cross-layer invariants; dependency order from domain/schema through runtime; vertical slice sequencing; explicit choices for reproducing versus correcting current defects; and acceptance commands. Include the full dependency graph and an equivalence matrix for happy paths, failures, security, concurrency, recovery, and operations.

- [ ] **Step 6: Run the strict validator**

Run: `backend/.venv/bin/python backend/scripts/check_status_quo.py --repo-root .`

Expected: exit 0, proving all internal links/frontmatter/status values/capability IDs and every generated route/model/job/migration/client method are covered.

- [ ] **Step 7: Commit**

```bash
git add docs/status-quo
git commit -m "docs: complete rebuild and traceability handbook"
```

### Task 10: Reconcile Codebase Map drift and run final proof

**Files:**

- Modify only current curated Map pages whose executable claims are verified stale
- Regenerate: `docs/map/inventory/*` through `./cbmap inventory build`
- Modify: `docs/status-quo/00-guides/Snapshot and Evidence Manifest.md`

**Interfaces:**

- Consumes: verified drift register, finished corpus, all repository gates.
- Produces: synchronized current Map, exact proof manifest, clean branch ready for AutoReview.

- [ ] **Step 1: Determine Map impacts**

Run `./cbmap inventory build` and `./cbmap impact --base 5448cf335e2cb25d74d6c0e6c476b72d1e14e803`. For each impacted page, update verified claims or prepare a page-specific attestation. Never change generated inventory by hand.

- [ ] **Step 2: Correct verified stale Map claims**

At minimum inspect and correct the signed-cookie claim, inline lease-recovery claim, observability claim for dropped worker fields, S3 storage-provider metadata, unread SHA-256 semantics, readiness scope, route-policy runtime role, SQLite foreign-key behavior, export completeness, and provenance depth wherever the current Map overstates them. Update `last_verified` and relationships/proof when the semantic page changes.

- [ ] **Step 3: Reconcile Map maintenance**

Run `./cbmap maintain --base 5448cf335e2cb25d74d6c0e6c476b72d1e14e803` with concrete attestations for byte-identical impacted pages, then `./cbmap check --base ...` and `./cbmap audit --max-findings 20`.

- [ ] **Step 4: Run documentation and focused gates**

Run the strict status-quo checker, its pytest file, all client Node tests, client build, Ruff check/format check, and OpenAPI check. Repair every failure.

- [ ] **Step 5: Run broad repository proof**

Run the full backend SQLite suite. Run the PostgreSQL lane when its configured database is available. Run a bounded local runtime smoke and representative browser walkthrough without opening protected data. Record every exact command/result and every unavailable external lane in Snapshot and Evidence Manifest.

- [ ] **Step 6: Commit**

```bash
git add docs/map docs/status-quo/00-guides/Snapshot\ and\ Evidence\ Manifest.md
git commit -m "docs: reconcile status quo evidence"
```

- [ ] **Step 7: Prepare final review**

Generate the complete branch review package and hand it to the most capable independent reviewer. Apply one bounded fix wave for verified findings, re-run affected proof, and leave no load-bearing finding unresolved.

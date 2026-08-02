---
id: traceability-ui-surface-coverage
title: UI Surface Coverage
kind: traceability
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/traceability
  - status-quo/ui
parent: "[[INDEX]]"
related:
  - "[[Capability Ledger]]"
  - "[[Feature-to-Code Matrix]]"
  - "[[Contract Coverage]]"
  - "[[Known Gaps and Non-Capabilities]]"
  - "[[Acceptance and Equivalence Proof]]"
---

> [!info] Navigation
> Parent: [[INDEX]]. Siblings: [[Capability Ledger]] · [[Feature-to-Code Matrix]] · [[Contract Coverage]] · [[Known Gaps and Non-Capabilities]].

# UI Surface Coverage

This register accounts for every reachable destination, global overlay, authentication/token surface, reusable interaction group, cache, and intentionally unreachable or backend-only surface in the snapshot. Proof classifications mean:

- **focused** — a direct behavioral test exercises the rendered state, navigation, or adapter interaction;
- **indirect** — a helper, adapter, or backend contract is tested, but the complete rendered state is not;
- **source-only** — implementation or deliberate absence is visible in source, with no focused behavior test identified;
- **absent** — the inventory and current source contain no such UI.

## Twelve destinations and hashes

| Destination | View key | Hash | Entry and meaningful control groups | Material states and handoffs | Capability owner | Proof |
| --- | --- | --- | --- | --- | --- | --- |
| Übersicht | `dashboard` | `#/uebersicht` | `Dashboard`; quick question, suggestion chips, four navigation stats, recent-document cards, all-documents and capture actions | summary or null; question hands off through memory to Assistant; document cards open the global drawer | `DASH-01` | hash focused; view indirect |
| Aufnehmen | `capture` | `#/aufnehmen` | `Capture`; note, drop target, file picker, camera input, sample cards | idle, working, cosmetic progress, still-processing, failed, generic error, done, saved-needs-review; result can open document or Postfach | `CAP-01`, `CAP-02`, `CAP-03` | focused |
| Formulare | `forms` | `#/formulare` | `Formulare`; four template cards, cascade, edit/confirm/reject fields, confirm-all, refill, mock export | ready, cascading, filled, done; local edits vanish on unmount | `FORM-01`, `PDF-00` | source-only |
| Assistent | `assistant` | `#/assistent` | `Assistant`; intro suggestions, composer, retry banner, consent gate, pending progress, answer rows and citation chips | loading/history, optimistic send, pending stages, completed, abstained, failed; document citations open the drawer | `ASSIST-01`, `ASSIST-02`, `ASSIST-03` | focused core; citation accessibility source-only |
| Aufgaben | `tasks` | `#/aufgaben` | `Aufgaben`; `ActionCard` and `DeadlineCard` groups | summary or null; overdue/upcoming rows open source documents | `TASK-01` | backend focused; UI indirect |
| Dokumente | `documents` | `#/dokumente` | `Documents`; folder rail, local search, local sort, rows, load-more | first load, failed-as-empty, empty, partial page, later-page error/retry; row opens drawer | `DOC-01` | cache/paging focused; first-load failure indirect |
| Fakten | `facts` | `#/fakten` | `Fakten`, `PersonFacts`, `FactCard`; local search, category groups, source, verify and copy controls | progressive current-scope pages, partial cache, verification busy/error, document handoff | `FACT-01` | focused core |
| Datenbank | `database` | `#/datenbank` | `DatabaseView`; reachable `Tabelle` and `Beträge & Fristen` tabs, local search/sort, row handoff | progressive current-scope pages; an unreachable `facts` branch remains in source | `DB-01` | indirect; dead branch source-proven |
| Familie | `family` | `#/familie` | `Familie`; linked-person grid, selected `EntityCardDetail`, back control | loading, empty, failure presented as empty, selected card, detail failure presented as null | `FAMILY-01`, shared `ENT-02`, `ENT-04` | focused core |
| Personen & Objekte | `entities` | `#/personen-objekte` | `Entities`; kind chips, entity grid, create dialog, live card, unlink dialog | loading, empty, failure presented as empty, selected card; review handoff is global | `ENT-01`–`ENT-05`, `REVIEW-01` | focused core |
| Einblicke | `insights` | `#/einblicke` | `Einblicke`; statistic and chart panels with document handoff | null without summary; progressive documents create mixed/partial snapshots | `INSIGHT-01` | limited focused proof |
| Verlauf | `history` | `#/verlauf` | `History`; activity rows and load-more | loading, feed, empty, first-load error presented as empty, later pages | `HISTORY-01`, `UNDO-00` | focused core |

`client/src/view-regressions.test.mjs` directly covers every hash-to-view mapping. The strict corpus checker independently compares the exact view-key/hash pairs above with `VIEW_HASH_PATHS`, so a value-preserving swap does not pass. `#/dokumente/<encoded-id>` is the only deeper client route; it opens the global document drawer and preserves encoded IDs through browser history.

## Authentication, tokens, global overlays, and dialogs

| Surface | Entry and controls | States and current behavior | Capability owner | Proof |
| --- | --- | --- | --- | --- |
| Account bootstrap | `AuthProvider` | `Konto wird geprüft…`, session restore, development auto-login, signed-out fallback, global `401` clearing | `AUTH-01` | auth/adapter focused; loader accessibility untested |
| Login and signup | `AuthScreen`; tabs, name, email, password, forgot-password entry, submit | login/signup/reset-request, busy and error states | `AUTH-01`, `AUTH-02` | focused |
| Email verification token | `/verify-email#token=…`; automatic claim and return-to-login control | pending, success, error | `AUTH-02` | focused token parsing and backend claim |
| Password reset token | `/password-reset#token=…`; password and save controls | pending form, busy, success, error, return to login | `AUTH-02` | focused token parsing and backend atomicity |
| Verification banner | `EmailVerificationBanner`; resend control | appears reactively after Capture/Assistant gate; sending, sent, rate-limit, generic error | `AUTH-02` | focused |
| AI consent modal | `ConsentModal`; close, cancel, accept | submitting and error states; preserves the blocked Capture/Assistant retry | `AUTH-03` | gates focused; focus behavior source-only |
| Responsive shell | `Shell`, `MobileTabBar`; destinations, Postfach, reset, logout, new document | desktop sidebar, tablet rail, mobile tabs; uniform controls regardless of role | `SHELL-01`, `SHELL-03` | routing focused; permission/a11y source-only |
| Summary loader | active view area inside the still-visible shell | `Lade deine Dokumente…`; rejection can leave the selected view blank | `SHELL-02` | indirect |
| Toast stack | `StoreProvider.toast` and App renderer | stacked 2.6-second messages; only exact `err` is red; no history or close control | `SHELL-02` | source-only |
| Document drawer | `DocumentDrawer`; scrim, close, open-original, language toggle | cached-then-fresh detail; uncached load has no visible drawer; stale cache survives fetch failure | `DOC-02`, `SHELL-02` | narrow focused; failure/a11y source-only |
| Review drawer | `ReviewInbox`; scrim, close, typed resolution buttons and document handoff | loading looks empty; feedback/error; can stack with document drawer | `REVIEW-01`, `SHELL-02` | actions focused; loading/stacking/a11y source-only |
| Entity creation | `EntityCreateDialog`; kind, name, optional aliases and identifiers | submit/error plus owner-conflict recovery | `ENT-01` | focused |
| Unlink/reassign | `UnlinkDialog`; reason, optional target and note | target-loading failure becomes empty list; submit/error | `ENT-04` | body/error helpers focused |
| Development reset | native `window.confirm` from shell reset icon | success refresh; failure is not presented | `AUTH-04`, `SHELL-03` | source-only |
| Entity fact edit | native `window.prompt` in `EntityCardDetail` | untyped value replacement with no field-level validation | `ENT-02` | source/indirect |

## Visible responsive shell projections

| Surface | Source and responsive visibility | State and persistence | Gates | Capability owner | Proof |
| --- | --- | --- | --- | --- | --- |
| `Lokal & privat` trust claim | `client/src/App.jsx::Shell` renders `Lokal & privat` plus `Deine Dateien sind verschlüsselt. Live-KI nutzt Vertex AI (EU).` in the sidebar above 920 px; trust text is hidden in the 72 px rail and mobile shell | Static bundled copy with no runtime state or persistence; it does not change with the configured seed/Vertex provider, storage adapter, dependency health, or the fact that derived database knowledge is plaintext | Any authenticated shell; no role, verification, consent, provider, storage, health, or readiness gate | `SHELL-01`, `SHELL-03` | source-only; [[Navigation and Responsive Shell]] and [[Identity Sessions Membership and Vault Scope]] qualify the responsive/static and plaintext-derived-state boundaries |
| Persona name and email projection | `client/src/App.jsx::Shell` reads `state?.person` for name/avatar initials and `user?.email` for the email line; name/email metadata is visible above 920 px and hidden in rail/mobile regimes | `state.person` is summary-backed StoreProvider memory and `user.email` is `/me`-backed AuthProvider memory; missing values render `Ilja Stehle` and `Konto`; state clears on reload/sign-out and is refreshed from durable backend projections | Any authenticated shell after account/summary loading; no role/capability gate and the displayed person is not a vault/person selector | `AUTH-01`, `SHELL-01`, `SHELL-02` | indirect for `/me`/summary state; responsive/fallback rendering is source-only; [[Navigation and Responsive Shell]], [[Global Drawers Toasts and Loading]], [[Permission-Aware Affordance Gaps]] |
| Unconditional `KI bereit` badge | `client/src/App.jsx::Shell` renders a static green badge in the top bar above 720 px; it is hidden on mobile | Literal source text with no state or persistence; always says ready while visible and is not connected to provider, network, worker, queue, health, or readiness, so it may misrepresent the active provider and actual readiness | Any authenticated shell; no role, email-verification, AI-consent, provider, route-availability, `/api/health`, or `/api/ready` gate | `SHELL-01`, `SHELL-03` | source-only; [[Permission-Aware Affordance Gaps]] records the unconditional claim, while [[Local and Production Runtime Topology]] proves that liveness/readiness do not establish AI/provider/worker readiness |

## Reusable components and local control groups

| Group | Consumers | Contract carried | Proof |
| --- | --- | --- | --- |
| `AuthProvider` | entire client | account bootstrap, in-memory `/me`, auth mutations, shared unauthorized clearing | focused |
| `EmailVerificationBanner` | shell after gated actions | resend state and verification feedback | focused |
| `ConsentModal` | Capture, Assistant | shared AI consent grant and preserved retry | focused |
| `DocumentDrawer` | hash deep link, Dashboard, Documents, Fakten, Aufgaben, Database, Insights, History, review | detail projection and authorized original handoff | narrow focused |
| `ReviewInbox` | shell Postfach and capability handoffs | open review list and typed mutation actions | focused core |
| `EntityCardDetail` | Entities, Familie | canonical card projection, fact edit/verify, documents, unlink | focused core |
| `PersonFacts` / `FactCard` | Fakten and card projections | snapshot facts, source navigation, canonical verification call | focused core |
| `EntityCreateDialog` / `UnlinkDialog` | Entities/card | confirmed manual creation and pair-wide unlink/reassign request bodies | focused |
| Capture result group | `SampleCard`, `Processing`, `StillProcessingCard`, `ErrorCard`, `Result`, `SavedNeedsReviewHeader` | local pipeline state and handoff copy | focused core; accessibility source-only |
| Dashboard/task/form groups | `AskHero`, `NavStat`, `ActionCard`, `DeadlineCard`, `FieldRow`, `SummaryBanner`, `SuccessCard` | view-local navigation and prototype state | mostly source/indirect |

## Scope caches and shared memory

| State owner | Exact scope and lifetime | Consumers and caveats | Proof |
| --- | --- | --- | --- |
| `AuthProvider.user` | in-memory `/me`; cleared on successful logout or shared `401` | all signed-in surfaces; rejected logout retains identity | focused auth tests |
| `StoreProvider.state` | slim summary, shell load state, badges/persona/recent documents; replaced by refresh | shell and summary-derived destinations; failed refresh is not surfaced | indirect |
| `createDocumentCache.current` | current-person pages, cursor, loading/error, single-flight promise and epoch | Documents, Fakten, Database, Forms, Insights; capture/refresh invalidates this cache | focused cache tests |
| `createDocumentCache.all` | all-vault pages with the same state machine | adapter/backend support it, but no current/all UI selector exists; capture/refresh invalidates it too | focused adapter/cache; UI absence source-only |
| Drawer fallback | summary `recentDocuments` and `actions` only | does not consult the shared paginated cache, so a loaded document can still reopen blank | source-only defect |
| Shell memory | pending Assistant question, active entity ID, review-open flag, toast stack, drawer language | survives destination changes, not reload or sign-out; drawer language leaks between documents | source/indirect |
| Assistant local list | wholesale copy of durable messages plus optimistic rows and polling state | optimistic/pending state can be lost or overwritten by stale list responses | focused progress tests |
| View-local state | samples, entity/family lists, History pages, Forms entries, filters, sorts, selected cards | resets when the view unmounts | mostly source/indirect |

## Dead, backend-only, indirect, and absent surfaces

| Classification | Surface | Current proof and reachability |
| --- | --- | --- |
| dead/unreachable | `DatabaseView.jsx::{FactsTab,FactWalletCard}` and `tab === "facts"` | `TABS` never offers `facts`; a forced call would omit the verification value. Source-proven defect, not a hidden capability. |
| compatibility-only | client recognition of job status `retrying` | queue code never persists or emits it in the snapshot. |
| backend-only | AI-consent withdrawal | route exists; adapter/control does not. |
| backend-only | account export and account deletion | routes exist; settings/adapters/controls do not. Development reset is a separate visible action. |
| backend without UI | GET `/api/health` — route:GET:/api/health | Public liveness only: after application construction it returns `200 {ok, backend, database}` without dependency I/O. There is no client method, destination, control, badge binding, or other UI consumer. [[Complete API Contract]] records the route contract; [[Local and Production Runtime Topology]] and `backend/tests/test_lifecycle.py` provide runtime/focused proof. |
| backend without UI | GET `/api/ready` — route:GET:/api/ready | Public database-only readiness: it executes `SELECT 1`, returns `200 {ok:true}` on success and `503 service_unavailable` only for a SQLAlchemy database error. It does not prove schema head, storage, workers/queue, email, AI provider, or key usability, and has no client method, destination, control, badge binding, or other UI consumer. [[Complete API Contract]] records the route contract; [[Local and Production Runtime Topology]] and `backend/tests/test_lifecycle.py` provide runtime/focused proof. |
| backend-only | role, vault, and membership state | enforcement exists; `/me` has no role/capability projection and no administration or switcher exists. |
| backend capability without UI | document `scope=all` | client adapter and route accept it; no selector exposes it. |
| backend capability without UI | direct `/api/search` | no adapter, search destination, or direct search control. Assistant uses it indirectly. |
| indirect/backend-only | entity merge and unmerge | review can merge two cards indirectly; direct merge and every unmerge lack client adapters/controls. |
| backend option without UI | review statuses beyond `open`, and unfiled `unsure` dismissal | server contract exists; drawer exposes neither option. |
| backend option without UI | entity `status` filter | client loads all statuses allowed by its adapter and filters only by kind locally. |
| backend-only automation | nightly deterministic/optional semantic audit, auto-merge/refile/alias work, original-page rasterization | worker paths only; effects surface through durable data/review or answers. |
| absent | durable task/reminder creation, mutation, completion, assignment, recurrence, or notifications | `TASK-01`; no model, route, adapter, or control. |
| absent | permission-aware affordances | `SHELL-03`; all roles see write controls and learn denial only after the request. |
| absent | integrated PDF view/fill/output/annotation/signature | `PDF-00`; browser original opening and worker rasterization do not satisfy this surface. |
| absent | generic undo/redo | `UNDO-00`; backend entity unmerge is a narrow recovery interface. |
| planned-only | Circles sharing | `CIRCLE-00`; no current model, route, adapter, view, or rebuild obligation. |

The exact defects and clean-rebuild dispositions behind these rows live in [[Known Gaps and Non-Capabilities]]. The rebuilt UI is equivalent only when each retained surface also satisfies the corresponding failure, accessibility, authorization, cache, and recovery checks in [[Acceptance and Equivalence Proof]].

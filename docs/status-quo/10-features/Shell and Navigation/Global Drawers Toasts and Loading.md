---
id: feature-global-drawers-toasts-and-loading
title: Global Drawers Toasts and Loading
kind: feature
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/feature
  - status-quo/shell-navigation
capability_ids:
  - SHELL-02
delivery: partial
reachability: user-facing
persistence: session-memory
evidence: code-and-tests
parent: "[[Shell and Navigation]]"
related:
  - "[[Navigation and Responsive Shell]]"
  - "[[Permission-Aware Affordance Gaps]]"
  - "[[Email Verification and Password Reset]]"
---

> [!info] Navigation
> Parent: [[Shell and Navigation]]. Related: [[Navigation and Responsive Shell]] · [[Permission-Aware Affordance Gaps]] · [[Email Verification and Password Reset]].

# Global Drawers Toasts and Loading

The shell provides global document and review drawers, transient toasts, and two blocking startup loaders. Delivery is `partial`: happy paths are implemented, but several failures collapse into empty content or disappear, and global overlays lack complete dialog/focus semantics. Drawer and feedback state is predominantly session-memory; document identity also lives in the URL, toasts are ephemeral for 2.6 seconds, and displayed content comes from durable server records.

## Global control map

| Control | Visible when | Input | Action | Result | Persistence | Failure behavior |
| --- | --- | --- | --- | --- | --- | --- |
| Any document card/source | A view has a document ID | Click | `openDoc(id)` navigates to Documents deep link | Global document drawer opens | ID in hash; drawer content/language in memory | Missing ID does nothing |
| Document scrim | Document drawer rendered | Click | `closeDoc()` | Replaces deep link with `#/dokumente` | URL replacement | No keyboard equivalent |
| Document close icon | Document drawer rendered | Click | Same close action | Drawer closes | URL replacement | No accessible name or Escape handler |
| `Öffnen` | Document drawer has a document | Click | Opens `fileUrl` in a new tab | Browser renders/downloads original according to response | External tab only | Browser/server handles error |
| `Translate to English` / `Auf Deutsch zeigen` | Document drawer summary | Click | Toggles between `summary_de` and `summary_en` | Summary language changes | Memory-only and persists across document changes while component remains mounted | No translation request; missing text renders empty |
| `Postfach` top-bar icon | Authenticated shell | Click | Sets review drawer open | Loads open review items | Memory-only open/items state | Load rejection is converted to an empty list |
| Review scrim or close icon | Review drawer open | Click | Closes Postfach | Drawer disappears | Memory-only | No keyboard equivalent or Escape handler |
| Review answer buttons | Item supplies actions | Answer plus server-provided entity IDs | Resolves item, removes it locally, shows feedback, then refreshes summary | Review mutation is durable; feedback is memory-only | `409` gets stale-item message; other rejection gets generic save message |
| Toast | A caller invokes `toast(message, kind)` | Message and kind | Appends to fixed stack, schedules removal | Colored dot plus message | Ephemeral, 2.6 seconds | No pause, close, retry, history, or announcement |

## Document drawer states

`DocumentDrawer` first looks in `state.recentDocuments` and `state.actions`, then fetches `/api/documents/{id}`. A cached summary can render immediately and is replaced by the fresh detail. On fetch failure, the cached fallback remains with no warning. If the deep-linked document has no cached fallback, there is no spinner, empty-state card, or error drawer: the component returns nothing while the document hash remains active.

The drawer shows folder/type/title/issuer/date, action status and due date, original preview/link, German or already-stored English summary, amounts/dates, extracted facts, trust flags, tags, and a confidence footer. It is a read surface; the language toggle changes only which existing summary field is displayed. Images render inline; other types render filename and rely on `Öffnen` for the original.

Document state is hash-addressable, but the selected summary language is not. The drawer's local language choice survives switching document IDs while the global component stays mounted and resets only on unmount/reload.

## Review drawer states

Opening Postfach fetches `GET /api/review-items?status=open`. There is no loading state, so the initial render can show stale items from a prior opening or `Nichts zu klären` while the request is pending. A rejected list request also becomes the same empty state: `Dein Archiv ist auf dem neuesten Stand.` can therefore mean either success with zero items or failure.

Action sets depend on item type:

| Review item | Buttons | Success feedback |
| --- | --- | --- |
| Conflict with both values | `Aktuellen Wert behalten`, `Neuen Wert übernehmen` | `Aktueller Wert bestätigt.` or `Neuer Wert übernommen.` |
| Conflict without usable conflicting value | `Hinweis schließen` | `Hinweis geschlossen.` |
| Unfiled | `Erneut einsortieren` | `Dokument wird erneut einsortiert.` |
| Other/entity match | `gleich`, `verschieden`, `unsicher` | `Zusammengeführt.`, `Gemerkt — das wird nicht mehr gefragt.`, or `Weggelegt — beide Karten bleiben bestehen.` |

A stale resolution gets `Diese Rückfrage ist nicht mehr aktuell. Bitte aktualisiere das Postfach und versuche es erneut.` Other rejected writes show `Die Rückfrage konnte nicht gespeichert werden. Bitte versuche es erneut.` The error has `role=alert`, but shares the green `review-feedback` styling used for success. A successful mutation awaits global summary refresh after changing local state; refresh failure is not caught or surfaced.

`Dokument öffnen` inside Postfach calls `openDoc` without closing Postfach. The independent global states can therefore render both drawers and scrims at once; because ReviewInbox appears later in the app tree with the same drawer z-index, it remains over the document drawer until closed.

## Toast semantics

`StoreProvider.toast` generates a random ID, appends without deduplication, and removes each item after 2600 ms. Rendering recognizes only exact kind `err` as red; every other kind is green. Callers that pass `warn` for a failure therefore receive success-colored feedback. Toasts have no `role=status`, `role=alert`, or `aria-live`, and pointer interaction does not pause expiration.

On mobile, the stack moves above the fixed tab bar and narrows to viewport width. It uses the same z-index as the consent modal, so source order determines overlap.

## Blocking startup and summary failure

There are two sequential global waits:

1. `AuthProvider` blocks the entire app with `Konto wird geprüft…` while `/api/auth/me` resolves. A `401` leads to login or development auto-login; other failures also end at the auth screen.
2. Once authenticated, `StoreProvider` calls `/api/summary`. The shell, sidebar, and top bar render, but the view area is replaced with `Lade deine Dokumente…` until the promise settles.

The summary effect uses `refresh().finally(() => setLoading(false))` without a catch. A non-`401` rejection clears the loader but leaves `state=null`, emits no retry or explanation, and can leave the active view blank; Dashboard explicitly returns null. During loading/null state the sidebar persona can fall back to `Ilja Stehle`, even though only the authenticated email is known. A summary `401` also triggers the global unauthorized handler, which removes the authenticated shell.

Neither loader is an ARIA live region. The spinner is purely visual and there is no timeout, cancel, or manual retry control.

## Overlay accessibility gaps

The drawers are `aside` elements, not modal dialogs. They do not declare `role=dialog`, `aria-modal`, or a labelled title relationship; ReviewInbox has only `aria-label=Postfach`. Scrims are clickable `div` elements with no keyboard activation. Neither drawer traps/restores focus, focuses its heading/close action, hides background content from assistive technology, or handles Escape. Drawer close icons lack `title` and `aria-label`.

The consent modal in [[AI Consent]] has dialog semantics but shares the focus-management gaps. The verification banner in [[Email Verification and Password Reset]] is the only relevant global-style surface here with `role=status`.

## Rebuild obligations

Preserve document deep links and cached-then-fresh rendering, review action copy and conflict handling, summary refresh after review mutation, toast lifetime/stacking unless intentionally changed, and responsive full-width drawers. Add explicit loading/error/retry states, deterministic severity semantics, live-region behavior, proper modal labelling, Escape handling, and focus containment/restoration. Opening a document from Postfach must have an intentional single- or stacked-drawer policy.

## Evidence

- `client/src/lib.jsx` → `StoreProvider`, `refresh`, `toast`, `openDoc`, `closeDoc`, `openReviewInbox`, `closeReviewInbox`
- `client/src/App.jsx` → `Shell`, global loading branch, toast stack, `DocumentDrawer`, `ReviewInbox`
- `client/src/components/DocumentDrawer.jsx` → `cachedDocument`, `DocumentDrawer`
- `client/src/components/ReviewInbox.jsx` → `reviewActions`, `reviewResolutionCopy`, `ReviewInbox`
- `client/src/styles.css` → `.scrim`, `.drawer`, `.toast-stack`, `.review-feedback`, mobile drawer/toast rules
- `client/src/api.js` → `handle`, `api.summary`, `api.document`, `api.listReviewItems`, `api.resolveReviewItem`
- `client/src/document-drawer.test.mjs` → `DocumentDrawer renders explicit zero confidence as 0 percent`, `DocumentDrawer keeps fallback confidence for missing values`
- `client/src/review-inbox.test.mjs` → `review API lists and resolves each answer with entity ids`, `inbox pins calm badge, evidence, removal and exact feedback copy`
- `client/src/api-auth.test.mjs` → `401 invokes unauthorized handler and throws structured error`

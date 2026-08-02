---
id: technical-ui-reachability-accessibility-and-responsive-behavior
title: UI Reachability Accessibility and Responsive Behavior
kind: technical
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical
  - status-quo/client-architecture
map_pages:
  - subsystem:client-architecture
inventory_refs:
  - clientapi:summary
  - clientapi:document
  - clientapi:listReviewItems
  - clientapi:resolveReviewItem
  - clientapi:listEntities
feature_links:
  - SHELL-01
  - SHELL-02
  - SHELL-03
  - DB-01
  - FORM-01
parent: "[[Client Architecture]]"
related:
  - "[[Client State Navigation and Cache]]"
  - "[[Client API Permissions and Failure Contract]]"
  - "[[Navigation and Responsive Shell]]"
---

> [!info] Navigation
> Parent: [[Client Architecture]]. Siblings: [[Client State Navigation and Cache]] · [[Client API Permissions and Failure Contract]].

# UI Reachability Accessibility and Responsive Behavior

The shell mounts one of twelve view components and exposes every view in both desktop `NAV` and the flattened mobile tab bar. Responsive changes alter layout and labeling, not route availability. The one verified dead branch is inside Database, not a missing top-level destination.

## Reachability matrix

| View component | Label / hash | Primary data ownership | Reachability |
| --- | --- | --- | --- |
| `Dashboard` | `Übersicht` / `#/uebersicht` | global summary; memory-only quick-question handoff | Desktop and mobile navigation |
| `Capture` | `Aufnehmen` / `#/aufnehmen` | view-local file/sample/context/progress/result plus durable job | Desktop and mobile navigation |
| `Formulare` | `Formulare` / `#/formulare` | client-only template/field/phase memory | Desktop and mobile navigation |
| `Assistant` | `Assistent` / `#/assistent` | durable messages plus view-local draft/poll/consent recovery | Desktop and mobile navigation |
| `Aufgaben` | `Aufgaben` / `#/aufgaben` | global summary projection | Desktop and mobile navigation |
| `Documents` | `Dokumente` / `#/dokumente` | current document-cache scope plus local filter/sort | Desktop/mobile; only view with ID deep link |
| `Fakten` | `Fakten` / `#/fakten` | current document cache and local search/filter | Desktop and mobile navigation |
| `DatabaseView` | `Datenbank` / `#/datenbank` | current document cache and local table state | Desktop and mobile navigation; one internal dead tab |
| `Familie` | `Familie` / `#/familie` | entity API plus active-entity memory | Desktop and mobile navigation |
| `Entities` | `Personen & Objekte` / `#/personen-objekte` | entity API, filters, create/card memory | Desktop and mobile navigation |
| `Einblicke` | `Einblicke` / `#/einblicke` | global summary/current documents and local chart selection | Desktop and mobile navigation |
| `History` | `Verlauf` / `#/verlauf` | paginated activity held locally | Desktop and mobile navigation |

The mobile tab bar is horizontally scrollable and contains all twelve items; there is no collapsed subset or menu. The active item is not automatically scrolled into view.

## Dead and unreachable code

`DatabaseView.jsx` contains `FactsTab`, `FactWalletCard`, and a `tab === "facts"` render branch. `TABS` exposes only `table` and `values`, initial state is `table`, and every setter comes from those two tab controls. No URL or external state can select `facts`. The branch is dead/unreachable. If forced by developer manipulation, its verification call omits the required fact value and would receive 422. It is not a second delivered fact-wallet surface.

All source files under current `views/` otherwise have a path from `App.VIEWS`; global `DocumentDrawer` and `ReviewInbox` are always mounted under the authenticated shell and become visible through store state. Entity create/unlink dialogs are reachable from the entity surfaces. Token screens are pathname-gated before the authenticated store.

## Exact responsive breakpoints

The shared CSS has three behavior boundaries, applied cumulatively:

| Width | Exact behavior |
| --- | --- |
| Above 920 px | 246 px sidebar with brand/navigation text, section labels, trust copy and persona metadata; multi-column grids use desktop rules |
| 721–920 px | Sidebar becomes a 72 px icon rail; brand/navigation labels, section labels, trust text and persona metadata hide; four-column grids become two, three-column grids become one, entity grid becomes two |
| At or below 720 px | Sidebar disappears; `100dvh` column shell and fixed safe-area-aware horizontally scrollable bottom bar appear; subtitle and static `KI bereit` hide; add-document button becomes icon-only; grids collapse, document rows reflow, tables scroll, drawers become full viewport width |
| At or below 640 px | Entity kind picker drops from three to two columns; entity identifier rows and entity fact forms become one column, layered on top of the 720 px mobile shell |

The 640 px rule is component-level, not a fourth navigation regime. At every width, all twelve destinations remain reachable. Drawer/toast sizing and safe-area offsets change, but route/state semantics do not.

## Mixed overlay semantics

| Surface | Current semantics | Keyboard/focus boundary |
| --- | --- | --- |
| AI consent | Inner element has `role=dialog`, `aria-modal=true`, labelled title; outer layer uses presentation role | No initial focus, trap, focus return, background inerting, or Escape handling; the overlay supplies no keyboard-close behavior |
| Entity create | `role=dialog`, `aria-modal=true`, labelled title | Same missing focus/Escape/inert behavior; pointer scrim closes; close button is labelled |
| Unlink/reassign | `role=dialog`, `aria-modal=true`, labelled title | Same missing focus/Escape/inert behavior; pointer scrim closes; close button is labelled |
| Document drawer | Semantic `aside` only | No dialog role/name, trap, focus return, inert background or Escape; scrim is a click-only `div`; close icon has no accessible name |
| Review drawer | `aside` with `aria-label=Postfach` | No dialog/modal semantics, trap, focus return, inert background or Escape; scrim is pointer-only; close icon has no accessible name |

Both global drawers can be open simultaneously, producing stacked scrims; source order places ReviewInbox over DocumentDrawer. No overlay coordinates focus or restores it to its opener. The document hash can remain active while a failed uncached detail fetch renders no drawer at all.

## Other accessibility boundaries

- Mobile navigation has an accessible label; desktop navigation does not. Active buttons use color/class only and omit `aria-current`. They are buttons rather than links, despite stable hashes.
- Top-bar icon controls rely mostly on `title`; numeric badges have no expanded label. There is no skip link or focus movement after view navigation.
- Assistant inline citation chips and the separate citation list use clickable `span` elements without button/link role, `tabIndex`, or key handling. They are not keyboard-operable. Some entity document rows independently implement Enter handling; that does not repair citations or scrims.
- Drawers' initial/loading/empty/error states are not consistently announced. Toasts have no `role` or `aria-live` and disappear after 2.6 seconds without pause/close.
- Auth/summary loaders are visual text/spinners, not live regions. Review mutation errors use `role=alert`; the verification banner uses `role=status`; these isolated uses do not establish a global announcement policy.
- Charts expose image roles/labels, but many icon-only and visually encoded states remain only partially named.

## Test boundary

Client tests cover hash parsing, all-view mapping, document drawer data fallbacks, auth 401 behavior, review request/copy behavior, capture polling, and several source regressions. They do not run a browser accessibility engine and do not prove tab order, focus containment/return, Escape, scrim keyboard activation, screen-reader announcement, mobile overflow discoverability, or viewport interaction at 920/720/640. Accessibility claims here therefore combine executable markup/CSS with limited source-oriented tests.

## Rebuild obligations

Preserve all twelve labels/hashes at every breakpoint, the exact responsive regimes, and explicit identification of the dead Database facts branch. A clean rebuild should use semantic links or route-aware controls, `aria-current`, labelled navigation, keyboard-operable citations, and one coherent modal/drawer primitive with initial focus, trap, Escape, background inerting, and focus return. These improvements must not accidentally make dead behavior current or hide server-authorized actions without a real permission projection.

## Evidence

- `client/src/App.jsx` → `NAV`, `MOBILE_NAV`, `VIEWS`, `Shell`, `MobileTabBar`
- `client/src/styles.css` → media queries at 920 px, 720 px, and 640 px; drawer/scrim/citation rules
- `client/src/components/DocumentDrawer.jsx`, `ReviewInbox.jsx`, `EntityCreateDialog.jsx`, `UnlinkDialog.jsx` → overlay semantics
- `client/src/auth/ConsentModal.jsx` → consent dialog semantics
- `client/src/views/Assistant.jsx` → clickable citation spans
- `client/src/views/DatabaseView.jsx` → `TABS`, `FactsTab`, dead conditional branch
- `client/src/view-regressions.test.mjs` → all-view and hash-routing source regressions
- `client/src/document-drawer.test.mjs`, `review-inbox.test.mjs`, `api-auth.test.mjs` → limited behavior proof

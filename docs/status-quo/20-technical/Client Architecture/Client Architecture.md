---
id: technical-family-client-architecture
title: Client Architecture
kind: technical-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical-family
map_pages:
  - subsystem:client-architecture
  - subsystem:auth-vault-consent
  - subsystem:capture-documents
  - subsystem:search-grounded-chat
inventory_refs:
  - clientapi:me
  - clientapi:summary
  - clientapi:listDocuments
  - clientapi:uploadAndWait
  - clientapi:messages
  - clientapi:reset
feature_links:
  - SHELL-01
  - SHELL-02
  - SHELL-03
  - DOC-01
  - CAP-03
  - ASSIST-01
parent: "[[Technical Atlas]]"
related:
  - "[[System Architecture]]"
  - "[[Backend and API]]"
---

> [!info] Navigation
> Parent: [[Technical Atlas]]. Sibling hubs: [[System Architecture]] · [[Backend and API]] · [[Data and Migrations]] · [[Jobs and AI]] · [[Security and Storage]] · [[Runtime and Operations]].

# Client Architecture

This family owns client state and navigation, scope-aware caching and polling, API/error adaptation and permission gaps, and exact UI reachability, accessibility, and responsive behavior. The client is a browser-memory React application: the hash persists only view/document identity, while server projections and most workflow state are fetched or held locally with no local/session storage.

## Child index

| Leaf | Owned contract |
| --- | --- |
| [[Client State Navigation and Cache]] | AuthProvider/StoreProvider/view-local ownership, hash routing, current/all document cache, single flight, cursor merge, epochs and capture/Assistant polling |
| [[Client API Permissions and Failure Contract]] | Relative credentialed fetch adapter, global 401, two error shapes, missing role metadata, absent client methods and inventory relation limits |
| [[UI Reachability Accessibility and Responsive Behavior]] | Twelve reachable views, dead Database facts branch, 920/720/640 breakpoints, mixed dialog/drawer semantics and keyboard/focus limits |

All 31 generated client methods are accounted for in [[Complete API Contract]]. Feature leaves own user-visible copy and workflow defects; these leaves own the shared state, transport, reachability and accessibility mechanisms that cross those features.

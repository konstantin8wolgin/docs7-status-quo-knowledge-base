---
id: technical-client-api-permissions-and-failure-contract
title: Client API Permissions and Failure Contract
kind: technical
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical
  - status-quo/client-architecture
map_pages:
  - subsystem:client-architecture
  - subsystem:auth-vault-consent
  - flow:auth-vault-context
inventory_refs:
  - clientapi:me
  - clientapi:login
  - clientapi:logout
  - clientapi:setAiConsent
  - clientapi:reset
  - route:DELETE:/api/account
  - route:GET:/api/account/export
  - route:GET:/api/search
feature_links:
  - AUTH-01
  - AUTH-03
  - AUTH-04
  - AUTH-05
  - SHELL-03
parent: "[[Client Architecture]]"
related:
  - "[[Client State Navigation and Cache]]"
  - "[[UI Reachability Accessibility and Responsive Behavior]]"
  - "[[Complete API Contract]]"
---

> [!info] Navigation
> Parent: [[Client Architecture]]. Siblings: [[Client State Navigation and Cache]] · [[UI Reachability Accessibility and Responsive Behavior]].

# Client API Permissions and Failure Contract

`client/src/api.js` is one small fetch adapter over relative `/api` URLs. It includes cookies on every adapter request, parses successful JSON except for 204, normalizes failed JSON into a thrown plain object, and has one global unauthorized callback. It has no generated types, cancellation, retry policy for ordinary requests, auth-header support, or permission model.

## Request and error adaptation

| Concern | Current behavior |
| --- | --- |
| Base URL | Every method uses relative `/api`; Vite proxies it in development and production requires same-origin or separately configured edge routing |
| Credentials | `fetch(..., {credentials: "include"})`; identity is the HttpOnly cookie, unavailable to JavaScript |
| JSON writes | `jsonRequest` always uses POST with `Content-Type: application/json`; special methods construct their own POST or multipart options |
| Success | `204` becomes `null`; every other successful adapter response must be JSON and is parsed with `res.json()` |
| Failure | Best-effort JSON parse, then throw `{...body, status, code, error}` where `error` falls back to status text |
| Global 401 | Call the current unauthorized handler before throwing; `AuthProvider` installs a handler that sets `user=null`, unmounting the authenticated store |
| Binary access | `fileUrl(id)` and server-provided sample thumbnail URLs bypass `handle`; the browser directly renders/downloads their dynamic response |

A network-level `fetch` rejection remains a native `Error`, not the normalized object. Consumers therefore see two error shapes. Many views catch and suppress errors into an empty/partial state; upload's generic card reads `error.message`, while normalized HTTP errors normally expose `error.error`, producing the known `Unbekannter Fehler` path.

The 401 callback is global mutable module state. It affects protected reads and writes alike, but not direct browser navigations to a file/sample URL. Login's own 401 also invokes it before the auth screen catches the error; setting an already-null user is harmless. There is no refresh-token or retry-after-login mechanism.

## Permission visibility gap

`GET /api/auth/me` returns ID, email, display name, email-verification state, AI-consent state, and whether provider configuration requires consent. It does not return role, vault ID, selected person ID, route permissions, or environment capabilities. The summary also omits them. Client code therefore cannot reliably hide or disable member/owner actions.

Readonly users can still see upload/sample/chat entry points, fact/entity/review mutation controls, unlink/create controls, and the reset icon; the server rejects disallowed calls with 403. Members can see the owner-only reset control. A separately deployed production client can still render reset even though production `create_app` omits its route, yielding 404. This is server-enforced authorization with non-permission-aware affordances, not a client security bypass.

Email verification and AI consent are the only gates surfaced to the UI. Capture and Assistant check the `me` flags and also recover from matching 403 machine codes. The server remains authoritative because local state may be stale.

## Methods absent from the client surface

There is no generated client method or reachable UI for:

- account ZIP export or account deletion: route:GET:/api/account/export and route:DELETE:/api/account;
- AI-consent withdrawal: route:DELETE:/api/auth/ai-consent (the client can only grant through clientapi:setAiConsent);
- direct entity merge or unmerge: route:POST:/api/entities/merge and route:POST:/api/entities/{entity_id}/unmerge;
- liveness or readiness: route:GET:/api/health and route:GET:/api/ready;
- raw transcript search: route:GET:/api/search.

Merge can still happen indirectly when clientapi:resolveReviewItem resolves an eligible review item as `same`; that does not make the direct merge/unmerge routes client-reachable. Original document and sample bytes are reachable through URL helpers, not API methods.

## Inventory relation limitations

The generated client inventory correctly contains 31 method IDs, but relation extraction has three known blind spots that must not be interpreted as missing behavior:

- clientapi:listEntities constructs an optional query suffix, so its recorded structural path `/api/entities{param}` does not match route:GET:/api/entities and the `calls_route` edge is a false negative;
- file and sample URLs are indirect (`fileUrl` and returned `thumbUrl`), not `api` object methods, so route:GET:/api/file/{document_id} and route:GET:/api/samples/file/{name} have no generated client-method edge despite user reachability;
- generic test-client calls to DELETE account are not always recognized by the test-relation extractor, despite executable account-deletion tests.

These are limitations of static relation extraction, not absence proof. [[Complete API Contract]] accounts for the runtime routes and all method IDs separately.

## Recovery boundaries

Ordinary adapter calls have no automatic retry, timeout, abort, backoff, idempotency key, or offline queue. Capture adds its own bounded polling above `job`; Assistant adds locally unbounded one-second message polling above `messages`. Auth development auto-login is the only automatic request replay: after initial `me` returns 401, `AuthProvider` may use build-time demo credentials in Vite development and then fetch `me` again.

Because successful non-204 responses are assumed JSON, adding a binary endpoint to `api` without a specialized handler would fail. Because errors are thrown as plain objects, consumers cannot rely on `instanceof Error`. Rebuild code should make these contracts explicit rather than preserving accidental ambiguity.

## Rebuild obligations

Preserve same-origin credential behavior, stable server error codes, global session-expiry transition, and server-side authorization. Add an explicit permission/environment projection before making affordances role-aware; never infer role from a failed mutation. Keep binary URL handling deliberate, and classify retry/idempotency by operation rather than globally replaying writes.

## Evidence

- `client/src/api.js` → `handle`, `request`, `jsonRequest`, `setUnauthorizedHandler`, `api`, `fileUrl`
- `client/src/auth/AuthProvider.jsx` → unauthorized handler and development auto-login
- `backend/app/schemas.py` → `MeOut`
- `backend/app/route_policy.py` → complete access metadata and absent direct client surfaces
- `client/src/api-auth.test.mjs` → `401 invokes unauthorized handler and throws structured error`
- `client/src/cbmap-inventory.test.mjs` → client-method extraction
- `backend/tests/test_authz.py` → readonly/member enforcement
- `backend/tests/test_security_adversarial.py` → role/gate enforcement and account self-service boundary

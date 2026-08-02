---
id: feature-permission-aware-affordance-gaps
title: Permission-Aware Affordance Gaps
kind: feature
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/feature
  - status-quo/shell-navigation
capability_ids:
  - SHELL-03
delivery: absent
reachability: user-facing
persistence: none
evidence: code-and-tests
parent: "[[Shell and Navigation]]"
related:
  - "[[Role and Vault Limitations]]"
  - "[[Navigation and Responsive Shell]]"
  - "[[Account Export Deletion and Development Reset]]"
  - "[[AI Consent]]"
  - "[[Global Drawers Toasts and Loading]]"
---

> [!info] Navigation
> Parent: [[Shell and Navigation]]. Related: [[Role and Vault Limitations]] · [[Navigation and Responsive Shell]] · [[Account Export Deletion and Development Reset]] · [[AI Consent]] · [[Global Drawers Toasts and Loading]].

# Permission-Aware Affordance Gaps

Permission-aware client affordances are a current non-capability: delivery is `absent`. Backend authorization and tenant isolation are implemented and remain the final guard, but the user-facing shell renders the same destinations and mutation controls for owner, member, and readonly users and in development or production. There is no permission state to persist because `/me` supplies neither role, active vault, nor capability flags.

> [!warning] Scope of the absence
> `delivery: absent` describes client permission awareness, not server protection. Unauthorized writes are rejected by `ctx_with`, route-specific gates, and vault-scoped queries; they are not silently accepted.

## Why the client cannot adapt

`AuthProvider` stores the `/me` projection: user ID, email, display name, email-verification state, consent state, and whether consent is required. `StoreProvider` stores summary data but no role/capability projection. `NAV`, `VIEWS`, top-bar actions, and global drawers have no role condition. The backend's `Role` and route policy are never imported or mirrored in client state.

The consequence is both over-exposure and under-exposure: users see actions they cannot perform, while owners have no UI for valid export and deletion operations and no user has a consent-withdrawal UI.

## Visible controls versus effective authorization

| Control | Visible when | Input | Action | Result | Persistence | Failure behavior |
| --- | --- | --- | --- | --- | --- | --- |
| All twelve navigation destinations | Any authenticated role | Click/tap | Mounts the selected view | Read surfaces generally load for readonly users; write surfaces still render | Route in URL; view state in memory | No route guard or explanatory disabled state |
| `Dokument` top-bar action and `Aufnehmen` navigation | Any authenticated role | File, camera image, or sample | Attempts upload/import | Requires `MEMBER`, verified email, and live-provider consent | Successful document is durable | Readonly `403 insufficient role` is not a recognized gate; Capture falls back to `Unbekannter Fehler` because the structured error has no JavaScript `message` |
| Assistant composer and suggestions | Any authenticated role | Question | Attempts chat | Requires `MEMBER`, verified email, and live-provider consent | Successful messages/runs are durable | Readonly denial becomes `Der Assistent ist gerade nicht erreichbar.` rather than a permission explanation |
| Fact verification controls | Wherever fact views render them | Proposed value | Attempts verification | Requires `MEMBER` | Durable on success | Surface-specific generic feedback; a `warn` toast is rendered success-green because toast severity recognizes only `err` |
| Entity create/confirm/fact/unlink or reassignment actions | Entity surfaces expose them | Entity/fact choices | Attempts mutation | Requires `MEMBER` | Durable on success | Backend `403`; no shell-level disablement or role guidance |
| Direct entity merge/unmerge routes | Never exposed by the client | Direct API request | Merges or unmerges entities | Requires `MEMBER` | Durable on success | These are backend-only operations; there is no client control to disable, explain, or report failure |
| Postfach resolution buttons | Review drawer has items | Answer and entity IDs | Attempts resolution; `gleich` on certain two-entity review items can invoke a merge indirectly | Listing requires readonly; resolving requires `MEMBER` | Durable on success | Readonly gets `Die Rückfrage konnte nicht gespeichert werden. Bitte versuche es erneut.`; this is not a general merge control and never exposes unmerge |
| Reset icon | Every authenticated role and every client build | Native confirmation | Calls `/api/reset` | Requires `OWNER` and route exists only outside production | Durable reset on success | Member/readonly gets unshown `403`; production gets unshown `404`; no catch or toast |
| Static `KI bereit` badge | Desktop/tablet shell | None | No action | Always reports ready | None | Does not reflect role, verification, consent, provider health, or route availability |

The `Formulare` destination is also visible to every role, but its current flow is a client-only, memory-only prototype and does not perform a protected PDF/server mutation. Visibility there should not be mistaken for authorization to generate, change, sign, annotate, print, or download a PDF.

## Reset environment and role mismatch

The reset icon is the sharpest shell mismatch. `App.jsx` always renders it and asks `Demo auf die Beispieldaten zurücksetzen? Eigene Uploads werden entfernt.` The backend mounts the route only when `APP_ENV != prod`, then requires owner context. The client neither checks availability nor catches rejection. Even the nearby source comment is stale: it claims reset revokes sessions, while executable reset code and tests preserve the user, session, and auth tokens. [[Account Export Deletion and Development Reset]] owns the actual reset lifecycle.

## Readonly experience

A readonly member can legitimately view summary, documents and originals, entities, messages, search, jobs, activity, samples, and open review items within the selected vault. The same user also sees upload, chat, fact/entity mutation, review-resolution, and reset controls. Backend `403` is therefore expected defense, not an exceptional tenant leak, but the client translates it into generic workflow failure rather than explaining `Nur Mitglieder` or `Nur Eigentümer`.

There is no owner/member/readonly badge, no tooltip explaining unavailable actions, no disabled control with a reason, and no accessible announcement of permission prerequisites. Hiding controls alone would not replace backend checks; current server enforcement must remain authoritative.

## Missing authorized affordances

- Owners can call account export but have no `Daten exportieren` control.
- Every authenticated user can self-delete with password confirmation but has no account-deletion control.
- Every authenticated user can withdraw AI consent through the backend but has no client adapter method or settings control.
- The data model supports multiple memberships, but there is no vault switcher or member/role administration.
- Direct entity merge and unmerge routes are backend-only. The only client-reachable merge path is the indirect consequence of answering `gleich` on certain two-entity review items; no direct merge or unmerge control exists.
- Verification resend is shown reactively only after a protected workflow is attempted, not as a global account-status action.

These are current absent surfaces, not hidden menu items or planned behavior.

## Rebuild obligations

Keep backend authorization and tenant scope as the security boundary. Add a server-derived capability projection or equivalent authorized action model; do not infer permissions from email, client routes, or caller-provided role/vault values. Use it to hide or disable actions consistently, explain prerequisites in German, and distinguish role, verification, consent, environment availability, and transient failure. Prove that UI adaptation never broadens server access and that direct unauthorized calls still receive `403` or cross-tenant `404`.

## Evidence

- `client/src/auth/AuthProvider.jsx` → `AuthProvider` user projection
- `client/src/App.jsx` → `NAV`, `Shell`, unconditional Postfach/reset/logout/Capture controls
- `client/src/lib.jsx` → `StoreProvider` state projection
- `client/src/views/Capture.jsx` → `run` error classification
- `client/src/views/Assistant.jsx` → `send` gate/error classification
- `client/src/components/ReviewInbox.jsx` → `resolve`
- `client/src/views/Entities.jsx` → exposed entity-list controls and absence of merge/unmerge controls
- `client/src/components/EntityCardDetail.jsx` → exposed entity-detail controls and absence of merge/unmerge controls
- `client/src/api.js` → `handle`, auth/summary/mutation methods and absence of merge/unmerge adapter methods
- `backend/app/authn.py` → `_me_payload`
- `backend/app/authz.py` → `Role`, `require_role`
- `backend/app/context.py` → `ctx_with`
- `backend/app/domain/entities.py` → `merge`, `unmerge`
- `backend/app/domain/review.py` → `resolve_review_item` indirect merge path
- `backend/app/route_policy.py` → `ROUTE_POLICIES`
- `backend/app/main.py` → conditional development-router mount
- `backend/tests/test_authz.py` → `test_readonly_member_gets_403_on_member_and_owner_routes`, `test_member_gets_403_on_reset`
- `backend/tests/test_security_adversarial.py` → `test_readonly_cannot_write`, `test_member_cannot_reset`, `test_reset_absent_in_prod`, `test_declared_role_matches_enforcement`
- `backend/tests/test_account.py` → `test_non_owner_cannot_export_account_zip`

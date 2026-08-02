---
id: flow:auth-vault-context
kind: flow
summary: Resolve an opaque bearer session through user and membership records into one dependency-enforced vault context.
read_when: ["authentication to vault context", "session cookie request context"]
sources: ["file:backend/app/authn.py", "file:backend/app/context.py", "file:backend/app/route_policy.py"]
inventory_refs: ["route:POST:/api/auth/login", "route:GET:/api/auth/me", "model:AuthSession", "model:VaultMember"]
related: ["subsystem:auth-vault-consent", "subsystem:client-architecture"]
last_verified: 2026-08-02
status: active
---
# Authentication to vault context

## Entry
A credentialed request carries an opaque random bearer cookie. The cookie is not signed, encrypted, or self-describing; only its SHA-256 digest is stored in `AuthSession`.
## Sequence
Hash the cookie, load the live session and user, resolve the first ordered membership plus current person, then let the route's FastAPI dependency enforce its role. `ROUTE_POLICIES` mirrors that access contract for inventory and tests but is not runtime middleware.
## Failures and retries
Missing, expired, revoked, or insufficient sessions fail without selecting a fallback vault.
## Trust boundaries
Headers never choose identity or vault; database membership is authoritative.
## Observability
Request IDs and status are logged without cookies or tokens.
## Change together
Change session minting/resolution, context dependencies, each route's executable dependency, route-policy metadata, client credential handling, and authz/adversarial tests together.

## Proof
`backend/app/authn.py` → `mint_token`, `create_session`, `user_for_session`, `_set_session_cookie`; `backend/app/context.py` → `get_current_user`, `resolve_context`, `ctx_with`; `backend/app/route_policy.py` → `ROUTE_POLICIES`; `backend/tests/test_auth.py` and `backend/tests/test_security_adversarial.py` → session lifecycle, live-route bijection, and declared-role enforcement.

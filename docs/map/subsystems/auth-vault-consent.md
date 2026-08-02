---
id: subsystem:auth-vault-consent
kind: subsystem
summary: Cookie authentication, verified-email gates, vault isolation, roles, and explicit AI consent.
read_when: ["auth vault consent", "login signup permissions", "email verification password reset"]
sources: ["file:backend/app/authn.py", "file:backend/app/context.py", "file:backend/app/routers/__init__.py", "file:backend/app/route_policy.py"]
inventory_refs: ["route:DELETE:/api/auth/ai-consent", "route:GET:/api/auth/me", "route:POST:/api/auth/ai-consent", "route:POST:/api/auth/login", "route:POST:/api/auth/logout", "route:POST:/api/auth/password-reset/confirm", "route:POST:/api/auth/password-reset/request", "route:POST:/api/auth/signup", "route:POST:/api/auth/verify-email", "route:POST:/api/auth/verify-email/request", "model:AuthSession", "model:AuthToken", "model:Person", "model:User", "model:Vault", "model:VaultMember", "migration:0002", "clientapi:confirmPasswordReset", "clientapi:login", "clientapi:logout", "clientapi:me", "clientapi:requestEmailVerification", "clientapi:requestPasswordReset", "clientapi:setAiConsent", "clientapi:signup", "clientapi:verifyEmail"]
related: ["flow:auth-vault-context", "flow:consent-provider-fallback"]
last_verified: 2026-08-02
status: active
---
# Authentication, vault scope, and consent

## Responsibility
Resolve an authenticated user into one vault-scoped request context and enforce consent gates.
## Boundaries
Opaque bearer session cookies and purpose-bound auth tokens enter; a dependency-enforced, role-bearing `RequestContext` leaves. Neither token type contains decodable identity claims.
## Interfaces
Signup, login, logout, verification, password reset, consent, and context dependencies.
## Dependencies
Users, sessions, tokens, vault membership, email delivery, executable route dependencies, and tested route-policy metadata.
## Data
Tokens are hashed, purpose-bound, expiring, single-use records; password-reset issuance and confirmation serialize on the user row, and consent is timestamped on users.
## Invariants
No caller selects another vault; route dependencies and domain predicates, not `ROUTE_POLICIES`, enforce access. Non-seed AI work requires verified email and current consent. A reset confirmation atomically claims its token, changes the password, invalidates sibling reset tokens, and revokes live sessions in one transaction.
## Change points
Change auth routes, context dependencies, verified-email/consent gates, route-policy metadata, client auth, and adversarial tests together.
## Proof
`backend/app/authn.py` → `mint_token`, `user_for_session`, password-reset confirmation; `backend/app/context.py` → `resolve_context`, `ctx_with`; `backend/app/routers/__init__.py` → `require_verified_email`, `require_ai_consent`; `backend/app/route_policy.py` → `ROUTE_POLICIES`; authentication concurrency on both database lanes plus authorization, settings, and security-adversarial suites.

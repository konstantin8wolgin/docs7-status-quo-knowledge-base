---
id: flow:consent-provider-fallback
kind: flow
summary: Enforce verified consent before provider work and select only configured, allowed fallback behavior.
read_when: ["consent provider fallback", "AI provider seed vertex", "provider configuration client consent"]
sources: ["file:backend/app/authn.py", "file:backend/app/context.py", "file:backend/app/routers/__init__.py", "file:backend/app/settings.py", "file:backend/app/ai/base.py", "file:backend/app/ai/seed_engine.py", "file:backend/app/ai/vertex_engine.py", "file:backend/app/domain/jobs.py", "file:client/src/api.js", "file:client/src/auth/ConsentModal.jsx", "file:client/src/assistant-consent.js", "file:client/src/views/Assistant.jsx"]
inventory_refs: ["route:POST:/api/auth/ai-consent", "route:DELETE:/api/auth/ai-consent", "model:User"]
related: ["subsystem:auth-vault-consent", "subsystem:ai-extraction-provenance", "subsystem:data-migrations-testing-operations"]
last_verified: 2026-07-17
status: active
---
# Consent and provider fallback

## Entry
Upload, sample import, chat, filing, answer, or auditor work reaches an AI boundary.
## Sequence
Resolve user/vault, require verified email and consent, select the configured provider, validate its output, and use explicit fallback policy. The Assistant detects both local auth state and API denial, preserves the question, grants consent through the shared modal, refreshes auth, and retries once.
## Failures and retries
Missing/revoked consent fails before provider use. Declining or failing the grant keeps the question recoverable; an accepted grant never duplicates an already appended user message. Provider/schema failures enter durable retry or bounded ladder behavior.
## Trust boundaries
Headers never select identity or vault. Configuration selects providers; model output never changes consent, provider policy, permissions, or durable truth directly. Private prompt/document content never enters logs.
## Observability
Engine identifiers, job/run status, consent denial codes, and audit records; never prompts with private content in logs.
## Change together
Change `authn` grant/revoke routes, request context/dependencies, settings and engine factory/adapters, durable jobs, `client/src/api.js`, shared consent gate/modal, and consuming views together. Prove provider failures, consent withdrawal at admission and worker time, Assistant recovery without duplicate messages, private-log safety, adversarial isolation, and client behavior.

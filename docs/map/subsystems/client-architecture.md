---
id: subsystem:client-architecture
kind: subsystem
summary: React application shell, API adapter, authentication state, views, dialogs, and polling helpers.
read_when: ["client architecture React", "API adapter views polling", "frontend auth dialogs"]
sources: ["file:client/src/App.jsx", "file:client/src/api.js", "file:client/src/lib.jsx", "file:client/src/assistant-consent.js", "file:client/src/views/Assistant.jsx", "file:client/src/views/Capture.jsx"]
inventory_refs: ["clientapi:reset"]
related: ["flow:upload-job-extraction-filing-polling", "flow:auth-vault-context"]
last_verified: 2026-07-18
status: active
---
# Client architecture

## Responsibility
Render German product workflows over one credentialed API adapter with explicit async state.
## Boundaries
User events, URL hashes, and API payloads enter components; views, dialogs, polling, and navigation leave.
## Interfaces
`api.js`, auth provider/screens, hash-synchronized application shell, shared scope-aware document cache, Assistant consent recovery, Capture polling/recheck, reusable cards/dialogs, and Vite.
## Dependencies
Backend contracts, error shape, route gates, polling states, and build-time demo credentials.
## Data
Server state stays authoritative; document views share single-flight paginated cache entries for current/all scopes, while helpers normalize display and pending/completed transitions.
## Invariants
Credentials remain included, German UI copy is intentional, hash navigation remains Back/Forward safe, document mutations invalidate shared cache state, and pending work eventually stops polling. A polling budget ending is a recoverable nonterminal state, not a processing failure; consent recovery preserves the pending chat question and avoids duplicate user messages.
## Change points
Change API method, consuming view/helper, node tests, and build proof together.
## Proof
All `client/src/*.test.mjs`, including polling-timeout and Assistant-consent regressions, Vite build, and runtime browser/API smoke.

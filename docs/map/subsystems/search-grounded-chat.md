---
id: subsystem:search-grounded-chat
kind: subsystem
summary: Vault/person-scoped search, stateless-per-question chat jobs, answer ladder, scope-only citation guards, and activity history.
read_when: ["search grounded chat", "answer ladder citations", "messages activity", "citation metadata API client rendering"]
sources: ["file:backend/app/models.py", "file:backend/app/schemas.py", "file:backend/alembic/versions/0011_chat_run_jsonb.py", "file:backend/app/domain/search.py", "file:backend/app/domain/answer.py", "file:backend/app/domain/chat.py", "file:backend/app/domain/jobs.py", "file:backend/app/routers/search.py", "file:backend/app/routers/chat.py", "file:client/src/api.js", "file:client/src/views/Assistant.jsx", "file:client/src/assistant-consent.js", "file:client/src/chat-progress.js"]
inventory_refs: ["route:GET:/api/activity", "route:GET:/api/messages", "route:GET:/api/search", "route:POST:/api/chat", "model:ChatRun", "model:Message", "migration:0009", "migration:0011", "job:chat.answer", "clientapi:activity", "clientapi:chat", "clientapi:messages"]
related: ["flow:search-grounded-chat", "flow:retry-lease-recovery"]
last_verified: 2026-08-02
status: active
---
# Search and grounded chat

## Responsibility
Retrieve vault/person-scoped candidates for one current question and produce deterministic or provider answers with document-scope-guarded citations.
## Boundaries
Normalized queries enter; ranked snippets, durable messages, progress, and grounded answers leave.
## Interfaces
Search route/domain, chat enqueue/job, answer ladder, messages, activity, and client polling.
## Dependencies
Documents, facts, extraction evidence, encrypted originals, jobs, consent, and PostgreSQL FTS fallback.
## Data
Messages expose user/assistant state; chat runs record the current question, ladder outcome, tools, model/token metadata, and mismatch fields, but not the search/card/page candidate set or conversation history supplied to the model. Structured payloads use PostgreSQL JSONB after migration 0011 and portable JSON on SQLite.
## Invariants
No cross-vault/person search row or citation survives domain scoping; model output cannot self-escalate tools or write knowledge state; failed jobs close pending messages. Citation guarding deduplicates visible document IDs and normalizes titles only—it does not enforce ladder-candidate membership, evidence support, page/quote accuracy, entailment, or nonempty citations. Each job answers only its stored current question. Consent recovery preserves that question and never appends its user message twice.
## Change points
Change search candidates, conversation-context inputs, evidence-set persistence, citation guard/ladder, `ChatRun`/Message persistence, schemas/serializers, chat job/routes, `client/src/api.js`, Assistant rendering, and polling together.
## Proof
`backend/app/domain/search.py` → `search_documents`; `backend/app/domain/answer.py` → `build_card_context`, `walk_ladder`, `guard_citations`; `backend/app/domain/chat.py` → `chat`; `backend/app/domain/jobs.py` → `run_chat_answer_job_body`; SQLite/PostgreSQL search, stateless current-question ladder, citation scope/title, job failure closure, chat/messages API, Assistant recovery/rendering/polling, activity, and adversarial isolation tests.

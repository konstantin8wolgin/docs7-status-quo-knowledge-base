---
id: flow:search-grounded-chat
kind: flow
summary: Run one current question through a vault/person-scoped answer ladder and return scope-guarded document citations.
read_when: ["search to grounded chat", "answer ladder citation"]
sources: ["file:backend/app/models.py", "file:backend/app/schemas.py", "file:backend/alembic/versions/0011_chat_run_jsonb.py", "file:backend/app/domain/search.py", "file:backend/app/domain/answer.py", "file:backend/app/domain/chat.py", "file:backend/app/domain/jobs.py", "file:backend/app/routers/search.py", "file:backend/app/routers/chat.py", "file:client/src/api.js", "file:client/src/views/Assistant.jsx", "file:client/src/assistant-consent.js", "file:client/src/chat-progress.js"]
inventory_refs: ["route:GET:/api/search", "route:POST:/api/chat", "job:chat.answer", "model:ChatRun", "migration:0011", "clientapi:chat"]
related: ["subsystem:search-grounded-chat", "subsystem:facts-summaries"]
last_verified: 2026-08-02
status: active
---
# Search to grounded chat

## Entry
A verified, consenting member submits a normalized search query or chat question; the Assistant gates missing consent before submission and also handles a server-side consent denial.
## Sequence
Preserve the pending question, collect consent when required, refresh auth, and retry without duplicating an already appended user message. The server persists that question and passes only it—not prior messages—through entity cards, bounded read-only tools, transcript search, and original-page inspection before closing the message.
## Failures and retries
Declined or failed consent leaves the question recoverable without provider work; empty/hostile queries fail safely, unavailable evidence advances rungs, and job failures clear citations and close user-visible pending state.
## Trust boundaries
Search/tool reads are code-scoped to vault/person and model output cannot select arbitrary tools. The citation guard only drops duplicate or invisible document IDs and replaces model-supplied titles with stored titles; it does not require membership in the rung's candidate set or prove claim support, page/quote truth, or entailment.
## Observability
Search scores/snippets are transient inputs. Durable message/chat-run state records the current question, progress, rung/outcome, tool calls, model/token metadata, attempts, and final citation IDs/count, but not the candidate evidence set used for an answer.
## Change together
Change search parity, current-question/conversation context, candidate-set persistence, citation scope/support guard, answer ladder, `ChatRun`/Message schema and serializers, chat job/routes, API adapter, Assistant rendering and polling together; prove deterministic, stateless-history, citation-scope/support, failure-closure, and adversarial cases.

## Proof
`backend/app/domain/chat.py` → `chat`; `backend/app/domain/jobs.py` → `run_chat_answer_job_body`; `backend/app/domain/answer.py` → `walk_ladder`, `guard_citations`; `backend/app/domain/search.py` → `search_documents`; answer/search/chat tests plus Assistant consent/polling tests.

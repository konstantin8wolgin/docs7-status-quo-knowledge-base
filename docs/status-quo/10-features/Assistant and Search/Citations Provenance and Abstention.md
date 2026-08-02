---
id: feature-citations-provenance-and-abstention
title: Citations Provenance and Abstention
kind: feature
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/feature
  - status-quo/assistant-search
capability_ids:
  - ASSIST-03
delivery: partial
reachability: user-facing
persistence: durable
evidence: code-and-tests
parent: "[[Assistant and Search]]"
related:
  - "[[Assistant Conversation and Progress]]"
  - "[[Search and Four-Rung Answer Ladder]]"
  - "[[Document Detail and Original Files]]"
  - "[[PDF Viewing Filling and Annotation Boundary]]"
---

> [!info] Navigation
> Parent: [[Assistant and Search]]. Related: [[Assistant Conversation and Progress]] · [[Search and Four-Rung Answer Ladder]] · [[Document Detail and Original Files]] · [[PDF Viewing Filling and Annotation Boundary]].

# Citations Provenance and Abstention

`ASSIST-03` gives completed assistant messages durable document-level citation metadata and records ladder provenance in `ChatRun`. Its trust boundary is narrower than the UI promise “jede Antwort kommt mit Quelle”: citation guards prove current vault/person visibility and replace model titles with stored titles, but they do not prove that a cited document supports a claim, belonged to the evidence supplied at that rung, contains a cited page or quote, or that an answered message has any citation at all.

## Scope guard versus grounding guard

`guard_citations` takes the model's requested `doc_id` values, queries documents under both current vault and current person, discards missing/foreign IDs and duplicates, preserves requested order, and emits only `{doc_id, stored_title}`. The focused ladder test proves that an invented title is replaced and an unknown sentinel ID is removed; it does not create a real foreign document. The adversarial search test proves `/api/search` tenant isolation, not cross-tenant chat-citation filtering. The citation scope claim therefore comes from the explicit vault/person predicates in `guard_citations`, while a dedicated real-foreign-document citation test is absent.

| Property | Enforced? | Exact meaning |
| --- | --- | --- |
| Current vault visibility | Yes | Foreign-vault IDs are filtered out |
| Current person visibility | Yes | Same-vault other-person IDs are filtered out |
| Stored title truth | Yes | Model-provided title is ignored; database title is returned |
| Duplicate document removal | Yes | First visible occurrence wins by `doc_id` |
| Citation belongs to card/tool/search/page evidence set | No | Any current-person document ID requested by the engine can survive, even if not supplied at that rung |
| Citation supports the answer's claim | No | No entailment, quote comparison, or field/value check occurs |
| Page, span, quote, or snippet presence | No | Durable/API citation schema has only document ID and title |
| At least one citation for `status=answered` | No | `_answered` accepts missing/empty citations and remains answered |

Filtering all proposed citations to an empty list does not change the answer to an abstention. A trustworthy-looking title chip therefore establishes navigable source scope, not claim-level grounding.

## Provenance that is stored

The assistant message stores guarded document citations. The associated `ChatRun` stores question, engine/model names, status, `unanswered_reason`, rung reached, whether rung 3+ was reached, fixed-tool call name/params/row count, optional `transcript_mismatch` text, token usage, duration, and finish time. It does **not** store a mismatch document or page, card context, transcript snippets, rasterized original bytes, full provider prompt/response, or a claim-to-evidence mapping as a user-facing citation object.

At rung 4, original PDFs are rasterized only for AI inspection. A model-reported transcript mismatch can produce a separate `AuditEvent`: its `document_id` column holds the selected document, while `payload_json` holds `document_id`, `page_number`, and the mismatch `note`. Those source fields belong to the audit event, not `ChatRun`. Normal answer citations still omit page number and quote, and the mismatch record does not create an integrated user PDF viewer.

The generic engine/parser shape permits `transcript_mismatch` on an answer from any rung. Only rung 4 assigns candidate document/page provenance; an earlier-rung mismatch can therefore produce an audit event with null document/page fields. At rung 4, if no guarded cited ID matches the candidate pages, audit-event provenance falls back to the first page rather than proving which page supports the mismatch.

## Citation presentation and accessibility

Completed, non-abstaining messages with citations render `Quelle:` followed by chips deduplicated again by `doc_id` or title. Clicking a chip with `doc_id` navigates to the global document drawer. The chip is a `<span onClick>` rather than a button or link and has no keyboard handler, `tabIndex`, or explicit accessible label; keyboard-only users cannot reliably activate it.

Answer body tokens of the form <code>&#91;&#91;Title&#93;&#93;</code> are a second, client-only linking mechanism. They search the currently loaded documents by exact title, then first substring match, and open that document. They are not derived from the guarded citation array, are not evidence-set checked, and become plain unbracketed text when unmatched. Because the loaded list remains current-person scoped, this mechanism does not intentionally broaden scope, but it is even less a grounding proof.

The content renderer otherwise understands only `**bold**`; line breaks survive via preformatted whitespace. It does not render general Markdown, web links, code, lists, tables, or citation page details.

## Abstention and failure states

| Outcome | Durable text/status | Machine-readable reason | Meaning |
| --- | --- | --- | --- |
| Search has no candidates | `Das steht nicht in deinen Dokumenten.` / `unanswered` | `no_candidates`, rung 3 | Retrieval found no current scoped transcript candidate for generated terms |
| Search had candidates but original stage cannot answer | Same text/status | `originals_checked`, rung 4 | Candidates existed; no renderable original page or page-stage answer was available |
| Answer at any rung | Engine text / `answered` | null; rung 1–4 | Citation list may still be empty or only scope-guarded |
| Job exception/dead letter | `Entschuldige — diese Antwort ist fehlgeschlagen. Bitte stell die Frage noch einmal.` / completed message, failed run | Run `failed`; citations cleared | Infrastructure/provider/job failure, not evidence absence |
| Client POST/network/permission error outside recognized gates | Local `Der Assistent ist gerade nicht erreichbar.` | Not a durable ladder reason | Request failure; may coexist with an accepted server job after ambiguous network loss |

The UI also treats exact German or English `Das steht nicht …` strings as abstention styling and hides citation chips for them. The backend currently emits the German string. Abstention distinguishes no candidate from a pipeline that reached originals, but the same user-facing sentence conceals that distinction; only `ChatRun.unanswered_reason` retains it, and the client does not expose it.

Provider-specific malformed/timeout judgments can degrade to `kind=insufficient` rather than throw. At the final search/page stages that may surface as the same “not in your documents” abstention even though provider quality—not the user's evidence—was the limiting condition; the provider fallback reason is not preserved in `ChatRun`.

## Limitations and trust boundary

- The marketing copy says answers come only from documents and with sources, but the guard cannot prove either claim at statement level.
- After every normally completed ladder run, including an abstention or an answer with zero citations, the backend writes activity detail `Assistent hat mit Quellenangabe geantwortet`; this reporting copy is not conditioned on a citation existing.
- Stored tool-call provenance includes row counts, not the full returned rows, and is not displayed to the user.
- Citation title chips open a document, not a page or supporting excerpt.
- A deleted/inaccessible destination later can leave durable citation metadata whose drawer read fails under current authorization.
- No citation copy/export, citation details dialog, source ordering explanation, confidence, or user feedback/correction control exists.
- Original-page rasterization reads authorized bytes transiently for the model; it must not be described as a user preview, saved annotation, or generated document.

## Rebuild obligations

Preserve fail-closed vault/person citation scope, stored-title replacement, durable outcome/rung/abstention provenance, and the no-citation failure closure. To fulfill the visible grounding promise, a rebuild must additionally bind citations to the exact evidence set, require support for answered claims, store/display page or structured-field provenance where available, enforce a nonempty citation policy or label unsourced answers, and use semantic keyboard-accessible source controls.

## Evidence

- `backend/app/domain/answer.py` → `LadderResult`, `guard_citations`, `_answered`, `_unanswered`, `_page_payloads`, `walk_ladder`
- `backend/app/ai/base.py` → `AnswerAttempt`, `SearchStageInput`, `PageStageInput`
- `backend/app/models.py` → `Message`, `ChatRun`
- `backend/app/domain/chat.py` → `message_to_json`
- `backend/app/domain/jobs.py` → `run_chat_answer_job_body`, `_close_failed_chat_bubble`, `CHAT_FAILURE_MESSAGE`
- `backend/app/schemas.py` → `CitationOut`, `MessageOut`
- `client/src/views/Assistant.jsx` → `ABSTAIN`, `BotRow`, `findDoc`, `renderInline`, `renderContent`, `dedupeCitations`
- `backend/tests/test_answer.py` → `test_ladder_nachzahlung_uses_rung_two_and_guarded_citations`, `test_ladder_candidate_gate_and_cross_vault_citation_guard`, `test_unrenderable_originals_report_originals_checked_not_no_candidates`, `test_chat_job_failure_never_strands_pending_message`
- `backend/tests/test_security_adversarial.py` → `test_search_never_returns_another_tenants_transcript` (search tenant isolation only; no real-foreign-document chat-citation fixture)

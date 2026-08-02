---
id: subsystem:ai-extraction-provenance
kind: subsystem
summary: Provider selection, loose-to-typed extraction normalization, shallow evidence capture, and immutable runs.
read_when: ["AI extraction provenance", "vision provider fallback", "OCR evidence transcript"]
sources: ["file:backend/app/ai/base.py", "file:backend/app/ai/schema.py", "file:backend/app/domain/jobs.py", "file:backend/app/domain/extraction.py", "file:backend/app/domain/facts.py"]
inventory_refs: ["model:ExtractedFieldEvidence", "model:ExtractionRun", "model:FactCandidate", "model:OcrEvidence", "migration:0005", "job:document.process", "job:document.reprocess"]
related: ["flow:consent-provider-fallback", "flow:fact-verification-provenance"]
last_verified: 2026-08-02
status: active
---
# AI extraction and provenance

## Responsibility
Select an allowed engine, normalize its loose output into typed data, validate any present transcript pages, and persist a document projection plus shallow extraction evidence.
## Boundaries
Authorized original bytes enter providers; `Envelope.from_loose` defaults, stringifies, normalizes, and drops unknown/malformed values before strict Pydantic validation. A page-less first extraction is accepted, so a completed run need not contain a usable transcript.
## Interfaces
Extraction engines, loose normalizer/typed schema, transcript validation, processing/reprocess bodies, projection persistence, and evidence serialization. Raw provider output is not retained separately from the normalized envelope.
## Dependencies
Consent, encrypted files, provider settings, jobs, facts, and filing.
## Data
Runs store engine/model/prompt/status metadata and one whole-page `OcrEvidence` row per present page. Amount/date field evidence uses labels as quotes and normally has no OCR/box link. Ordinary fact candidates/revisions/provenance cite the document but normally leave extraction-run/OCR/field evidence IDs null; schema capacity does not imply populated depth.
## Invariants
Provider output is untrusted until loose normalization plus typed/domain validation. Present pages must be contiguous, one-based, and nonblank. A page-less reprocess cannot supersede an existing completed transcript, but page-less first processing can complete; previous completed runs stay historical and remain authoritative when reprocess fails.
## Change points
Change input rendering, prompts/model IDs, loose normalizer and typed schema, transcript authority rules, provider/fallback metadata, run/raw-output retention, OCR/field/fact provenance writes, serialization, synthetic fixtures, and adversarial/reprocess tests together.
## Proof
`backend/app/ai/schema.py` → `Envelope.from_loose`, `require_complete_transcript`; `backend/app/domain/jobs.py` → `_extract_normalized_envelope`, `_has_completed_transcript`; `backend/app/domain/extraction.py` → `_insert_extracted_parts`, `apply_envelope_to_document`; `backend/app/domain/facts.py` → `upsert_fact`; AI normalization, extraction-evidence, reprocess-authority, prompt-injection, provenance, and serialization tests.

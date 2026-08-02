---
id: feature-pdf-viewing-filling-annotation-boundary
title: PDF Viewing Filling and Annotation Boundary
kind: feature
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/feature
  - status-quo/forms
  - status-quo/absence
capability_ids:
  - PDF-00
delivery: absent
reachability: user-facing
persistence: none
evidence: source-only
parent: "[[Forms]]"
related:
  - "[[Form Autofill Prototype]]"
  - "[[Document Detail and Original Files]]"
  - "[[Citations Provenance and Abstention]]"
---

> [!info] Navigation
> Parent: [[Forms]]. Related: [[Form Autofill Prototype]] · [[Document Detail and Original Files]] · [[Citations Provenance and Abstention]].

# PDF Viewing Filling and Annotation Boundary

`PDF-00` is an explicit current non-capability. The product can accept a PDF as an original document and an authorized user can ask the browser to open that unchanged original in a new tab. It has no integrated PDF viewer, page navigator, thumbnails, AcroForm reader or filler, field mapper, PDF generator or modifier, annotation/drawing/highlighting tool, signature workflow, saved output, or completed-PDF record.

> [!danger] No PDF leaves the Forms workflow
> `Formular exportieren` in [[Form Autofill Prototype]] creates no bytes, sends no request, opens no print dialog, supplies no download, and stores no record. Its toast, printer icon, `done` phase, and “ready to print” language are mock presentation only.

## What exists versus what does not

| Surface or capability | Current status | Exact boundary |
| --- | --- | --- |
| Upload PDF original | Implemented outside Forms | Capture accepts validated `application/pdf` input for extraction; this is ingestion, not editing or filling. |
| Document drawer PDF presentation | Partial outside Forms | Shows a filename tile rather than embedded pages. |
| `Original` / `Öffnen` | Implemented outside Forms | Opens `GET /api/file/{document_id}` in a new browser tab; the server returns the decrypted, unchanged original with inline disposition and the browser decides how to present it. |
| AI original-page inspection | Backend-only outside Forms | The answer ladder can rasterize selected original PDF pages for model evidence inspection. No rasterized page is exposed as a user viewer, editor, or saved derivative. |
| Integrated viewer and page controls | Absent | No canvas/iframe/PDF component, page navigation, thumbnails, zoom, rotation, text layer, or viewer state. |
| AcroForm handling and field binding | Absent | No parsing, discovery, mapping, filling, flattening, or validation of PDF form fields. The four UI templates are React data, not PDF schemas. |
| PDF generation or modification | Absent | No route, client method, document/file write, render pipeline, or output bytes. |
| Annotation, drawing, or highlighting | Absent | No tool, annotation model, coordinate/page state, save action, or persisted layer. |
| Signature | Absent | No typed, drawn, cryptographic, certificate, placement, consent, or audit workflow. |
| Print or download completed form | Absent | Forms invokes neither browser print nor a link/download response. |
| Saved output and history | Absent | No draft/output model, new `Document`, `FileObject`, audit event, version, or undo target is created. |

## Checked boundary

At the snapshot, the form component imports no API adapter or file URL and its export handler only calls `toast` and `setPhase`. The client adapter and server route policy contain no form-fill, PDF-export, annotation, signature, or generated-document contract. `DocumentDrawer` deliberately renders only images inline; PDF and TXT originals get a filename tile. The file route is a read of encrypted stored bytes, not an output writer.

This absence must not be confused with two uses of PDF libraries elsewhere: capture/extraction reads uploaded PDFs, and assistant evidence inspection can turn an original page into a raster for a model. Neither provides user-visible integrated viewing or mutates the source.

## Rebuild obligations

A clean-room equivalent of the current product must preserve authorized access to unchanged originals without claiming an editor. Any future viewer, AcroForm, annotation, signature, or output feature requires an explicit threat model, vault/person authorization, immutable-original policy, encrypted output storage, provenance/version semantics, failure recovery, and tests. It is an additive future capability, not a hidden requirement inferred from the current mock.

## Evidence

- `client/src/views/Formulare.jsx` → `exportForm`, `SuccessCard`; absence of API/file/print/download behavior
- `client/src/components/DocumentDrawer.jsx` → `DocumentDrawer` image-only inline preview and original link
- `client/src/api.js` → `api`, `fileUrl`; absence of form/PDF-output methods
- `backend/app/routers/files.py` → `file`
- `backend/app/domain/files.py` → `read_file_bytes`
- `backend/app/routers/documents.py` → `upload`, `documents`, `document`; absence of generated-output routes
- `backend/app/domain/answer.py` → `_page_payloads`
- `backend/app/route_policy.py` → `ROUTE_POLICIES`
- `backend/tests/test_uploads.py` → `test_served_document_files_include_csp_header`, `test_served_text_document_is_attachment`
- `backend/tests/test_crypto.py` → `test_file_round_trips_and_stored_object_is_ciphertext`

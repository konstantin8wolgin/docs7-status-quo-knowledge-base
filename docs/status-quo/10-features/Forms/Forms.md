---
id: feature-family-forms
title: Forms
kind: feature-family
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-01
tags:
  - status-quo/feature-family
capability_ids: []
delivery: prototype
reachability: user-facing
persistence: session-memory
evidence: source-only
parent: "[[Feature Atlas]]"
related:
  - "[[Assistant and Search]]"
  - "[[Dashboards and Reporting]]"
  - "[[Form Autofill Prototype]]"
  - "[[PDF Viewing Filling and Annotation Boundary]]"
---

> [!info] Navigation
> Parent: [[Feature Atlas]]. Sibling hubs: [[Account and Access]] · [[Shell and Navigation]] · [[Capture and Processing]] · [[Documents and Knowledge]] · [[Facts Entities and Review]] · [[Assistant and Search]] · [[Dashboards and Reporting]] · [[Historical Intent]].

# Forms

This family owns the client-only form-autofill prototype and its explicit PDF boundary. The current workflow does not generate, modify, sign, annotate, print, or download a PDF.

## Child index

| Capability | Feature | Delivery | Reachability | Summary |
| --- | --- | --- | --- | --- |
| `FORM-01` | [[Form Autofill Prototype]] | `prototype` | `user-facing` | Four hardcoded templates animate document-snapshot facts through client-memory states; verification/source/counting defects and a mock export constrain the promise. |
| `PDF-00` | [[PDF Viewing Filling and Annotation Boundary]] | `absent` | `user-facing` | Originals can open unchanged in a browser tab, but integrated viewing, AcroForm fill, modification, annotation, signature, and saved output do not exist. |

## Family boundary

The prototype may consume document facts and open a source drawer, but it never writes canonical facts or files. [[Form Autofill Prototype]] owns its simulated fields and controls; [[PDF Viewing Filling and Annotation Boundary]] prevents mock wording, original-file access, extraction, or AI rasterization from being mistaken for delivered PDF work.

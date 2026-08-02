---
id: technical-atlas
title: Technical Atlas
kind: technical-atlas
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/technical-atlas
map_pages:
  - subsystem:runtime-configuration
  - subsystem:client-architecture
  - subsystem:auth-vault-consent
  - subsystem:capture-documents
  - subsystem:data-migrations-testing-operations
  - subsystem:jobs-workers
  - subsystem:ai-extraction-provenance
  - subsystem:entities-filing-review
  - subsystem:search-grounded-chat
  - subsystem:files-crypto-storage
  - subsystem:gdpr-account
  - flow:auth-vault-context
  - flow:consent-provider-fallback
  - flow:encrypted-file-read
  - flow:account-export-deletion
  - flow:retry-lease-recovery
  - flow:upload-job-extraction-filing-polling
  - flow:entity-filing-review-merge
  - flow:search-grounded-chat
inventory_refs:
  - route:GET:/api/health
  - route:GET:/api/ready
  - route:POST:/api/auth/login
  - route:GET:/api/summary
  - route:POST:/api/upload
  - route:GET:/api/file/{document_id}
  - route:GET:/api/account/export
  - route:DELETE:/api/account
  - route:POST:/api/reset
  - clientapi:me
  - clientapi:listDocuments
  - clientapi:uploadAndWait
  - clientapi:messages
  - model:Document
  - model:AuthSession
  - model:VaultMember
  - model:VaultKey
  - model:FileObject
  - model:ProcessingJob
  - model:ExtractionRun
  - model:Entity
  - model:ChatRun
  - migration:0001
  - migration:0011
  - job:auditor.nightly
  - job:chat.answer
  - job:document.file
  - job:document.process
  - job:document.reprocess
feature_links:
  - AUTH-01
  - AUTH-04
  - AUTH-03
  - AUTH-05
  - SHELL-01
  - CAP-01
  - CAP-03
  - DOC-01
  - DOC-02
  - ASSIST-01
  - ASSIST-02
  - ASSIST-03
  - ENT-03
  - REVIEW-01
parent: "[[INDEX]]"
related:
  - "[[Feature Atlas]]"
  - "[[Rebuild Atlas]]"
  - "[[Contract Coverage]]"
  - "[[Feature-to-Code Matrix]]"
  - "[[Known Gaps and Non-Capabilities]]"
---

> [!info] Navigation
> Parent: [[INDEX]]. Sibling atlases: [[Feature Atlas]] · [[Rebuild Atlas]].

# Technical Atlas

This atlas organizes the current system by responsibility, ownership, state, control flow, trust boundary, failure behavior, operational proof, and rebuild dependency. Family hubs are stable entry points. All seven technical families are reconstructed at this snapshot; every family links to verified leaves rather than leaving security, storage or operations implicit.

| Technical family | Scope |
| --- | --- |
| [[System Architecture]] | Three leaves: local/production topology and composition; component/dependency ownership; exact middleware, request-ID and error lifecycle |
| [[Client Architecture]] | Three leaves: provider/view/cache state; API permission/failure adaptation; twelve-view reachability, 920/720/640 responsive and accessibility behavior |
| [[Backend and API]] | Two leaves: router/domain/infrastructure boundaries and the exact 39-development/38-production route plus 31-client-method contract |
| [[Data and Migrations]] | Three leaves: exact 32-model topology; 11-revision history and dialect drift; export/reset/account-deletion lifecycle |
| [[Jobs and AI]] | Four leaves: five-type durable queue; extraction/provenance; filing/auditor policy; search and answer-agent internals |
| [[Security and Storage]] | Three leaves: identity/session/vault scope; encryption/key hierarchy/object storage; upload/download/quota/erasure |
| [[Runtime and Operations]] | Four leaves: settings/environment; local/production topology; observability/backup/restore/incidents; test/release proof |

## Current reconstruction path

```mermaid
flowchart LR
    T["[[System Topology and Composition]]"] --> O["[[Component Ownership and Dependency Direction]]"]
    O --> R["[[Request Lifecycle Errors and Middleware]]"]
    R --> B["[[Router Domain and Infrastructure Boundaries]]"]
    B --> A["[[Complete API Contract]]"]
    C["[[Client State Navigation and Cache]]"] --> P["[[Client API Permissions and Failure Contract]]"]
    P --> U["[[UI Reachability Accessibility and Responsive Behavior]]"]
    A --> P
    T --> C
    T --> D["[[Domain Model and Relationships]]"]
    D --> M["[[Migration History and Database Dialects]]"]
    D --> L["[[Data Lifecycle Reset Export and Deletion]]"]
    D --> J["[[Durable Job State Lease Fencing and Recovery]]"]
    J --> E["[[Extraction Envelope Evidence and Provenance]]"]
    E --> F["[[Filing Auditor and Policy-Limited Automation]]"]
    J --> S["[[Search and Answer Agent Internals]]"]
    R --> I["[[Identity Sessions Membership and Vault Scope]]"]
    I --> K["[[Encryption Key Hierarchy and Object Storage]]"]
    K --> X["[[Upload Download Quota and Erasure]]"]
    T --> G["[[Settings and Environment Contract]]"]
    G --> Y["[[Local and Production Runtime Topology]]"]
    Y --> Z["[[Observability Backup Restore and Incident Recovery]]"]
    Z --> Q["[[Test Lanes Gates and Release Proof]]"]
    X --> Z
```

Start with topology for process/environment questions, ownership for change boundaries, request lifecycle for cross-cutting HTTP behavior, and the API ledger for an exact endpoint or client-method contract. The client leaves explain how those routes become browser state. For durable internals, follow the model ledger into migration/lifecycle or the queue state machine, then follow the owning extraction, filing/auditor or search/answer body. For trust questions, follow identity into keys/storage and file lifecycle; for deployment questions, follow settings into runtime topology, observability/recovery and exact proof lanes.

The exact route ledger records 39 development routes and 38 production routes; reset is the only development-only product route. It also records every one of the 31 generated client methods. The data/jobs leaves account for all 32 models, 11 migrations and five job types while preserving material negative boundaries: SQLite does not run the full migration chain, inline jobs lack reaping/future wakeups, extraction provenance is usually document/page-shallow, auditor actions are policy-limited, questions are stateless, and citations do not prove support.

Security/operations leaves add equally important limits: sessions are opaque and vault choice implicit; only originals are envelope-encrypted while derived database knowledge remains plaintext; quota and DB/object erasure are non-atomic; production Compose has no client/TLS/edge and gives workers an invalid API healthcheck; readiness is database-connectivity-only; logging drops worker context and tracebacks; backup/restore/key rotation remain manual; CI omits runtime, production, optional S3 and private golden execution. Generated inventory, OpenAPI, Map checks and green CI remain evidence layers rather than substitutes for that qualified runtime contract.

## Traceability

- [[Contract Coverage]] semantically owns every current route, client method, model, job, migration, classified unknown and test inventory ID.
- [[Feature-to-Code Matrix]] maps those contracts back to the exact 33 feature capabilities and explicit negative classifications.
- [[Known Gaps and Non-Capabilities]] collects the qualified failure, recovery, dialect, evidence, security and operational boundaries from these leaves.

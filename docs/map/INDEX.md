# Codebase Map

Start with `cbmap orient "<task>" --budget 2000`. Read source only after the
smallest relevant pages and inventory IDs are known.

## Subsystems

- [Runtime and configuration](subsystems/runtime-configuration.md) — startup, settings, wiring, health.
- [Auth, vault, and consent](subsystems/auth-vault-consent.md) — identity, roles, isolation, AI gates.
- [Capture and documents](subsystems/capture-documents.md) — upload, samples, documents, polling.
- [Files, cryptography, and storage](subsystems/files-crypto-storage.md) — encryption and object bytes.
- [Jobs and workers](subsystems/jobs-workers.md) — dispatch, leases, retries, chaining.
- [AI extraction and provenance](subsystems/ai-extraction-provenance.md) — providers, envelopes, evidence.
- [Facts and summaries](subsystems/facts-summaries.md) — canonical facts, revisions, projections.
- [Entities, filing, and review](subsystems/entities-filing-review.md) — register, uncertainty, merge.
- [Search and grounded chat](subsystems/search-grounded-chat.md) — retrieval, ladder, citations.
- [GDPR account](subsystems/gdpr-account.md) — export and deletion.
- [Client architecture](subsystems/client-architecture.md) — React, API adapter, views, polling.
- [Data, migrations, testing, and operations](subsystems/data-migrations-testing-operations.md) — schema and proof.

## Flows

- [Authentication to vault context](flows/auth-vault-context.md)
- [Upload to extraction, filing, and polling](flows/upload-job-extraction-filing-polling.md)
- [Sample import](flows/sample-import.md)
- [Encrypted file read](flows/encrypted-file-read.md)
- [Entity filing, review, and merge](flows/entity-filing-review-merge.md)
- [Fact verification and provenance](flows/fact-verification-provenance.md)
- [Search to grounded chat](flows/search-grounded-chat.md)
- [Consent and provider fallback](flows/consent-provider-fallback.md)
- [Account export and deletion](flows/account-export-deletion.md)
- [Retry, lease, and recovery](flows/retry-lease-recovery.md)

Generated structural truth lives under `inventory/`; curated pages never copy
or overwrite it. Maintenance decisions append to [the Map log](log.md).

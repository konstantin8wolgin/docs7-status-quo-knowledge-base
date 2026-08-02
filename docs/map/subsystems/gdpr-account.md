---
id: subsystem:gdpr-account
kind: subsystem
summary: Defined owner export, authenticated account deletion, ordered database erasure, and best-effort object cleanup.
read_when: ["GDPR account export deletion", "vault data lifecycle", "hard delete storage", "new vault owned model record migration"]
sources: ["file:backend/app/models.py", "file:backend/app/schemas.py", "file:backend/alembic/versions/0010_auditor_integrity.py", "file:backend/app/domain/account.py", "file:backend/app/domain/reset.py", "file:backend/app/domain/files.py", "file:backend/app/routers/account.py"]
inventory_refs: ["route:DELETE:/api/account", "route:GET:/api/account/export"]
related: ["flow:account-export-deletion", "subsystem:files-crypto-storage"]
last_verified: 2026-08-02
status: active
---
# GDPR account export and deletion

## Responsibility
Export a documented subset of an owner's vault data and erase owned-vault rows plus the account, with cryptographic erasure followed by best-effort physical cleanup.
## Boundaries
Authenticated export or password-confirmed self-deletion intent enters; an in-memory ZIP projection or committed database/key erasure leaves. Physical object deletion is not an atomic postcondition.
## Interfaces
Account export/delete routes and ordered domain cleanup helpers.
## Dependencies
All vault-owned tables, file storage, sessions, auth context, and transaction boundaries.
## Data
Export includes selected user/vault/person/document/fact/entity/review/message/chat/audit projections and linked originals, while omitting auth, queue, extraction, fact-history, crypto, file-metadata, and non-activity audit records. Deletion enumerates owned-vault rows; business data in merely joined vaults survives with user attribution nulled where modeled.
## Invariants
Only owned vaults export; caller IDs never broaden scope; a database failure leaves the destructive transaction unapplied, and successful deletion leaves no owned vault or valid session. Wrapped-key removal provides application-level cryptographic erasure, while storage failure can leave orphan ciphertext. Migrations remain a single linear chain.
## Change points
Every new vault-owned model changes `models`, the next linear revision, an explicit export inclusion/omission decision in `schemas` and `domain.account`, deletion/storage-key order and shared-vault attribution in `domain.reset`/`domain.account`, session/key lifecycle, inventory, Map sources, and this page together.
## Proof
`backend/app/domain/account.py` → `_owned_vaults`, `export_account`, `delete_account`; `backend/app/domain/reset.py` → `_vault_storage_keys`, `_delete_vault_rows`; `backend/app/domain/files.py` → `read_file_bytes`; account/export, storage-failure, authz, lifecycle, adversarial data-isolation, SQLite/PostgreSQL migration, inventory, and Map checks.

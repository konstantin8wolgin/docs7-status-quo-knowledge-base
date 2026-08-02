---
id: flow:account-export-deletion
kind: flow
summary: Export a defined owner-data projection or erase owned vaults and the account with best-effort object cleanup.
read_when: ["account export deletion", "GDPR erase vault"]
sources: ["file:backend/app/models.py", "file:backend/app/schemas.py", "file:backend/alembic/versions/0010_auditor_integrity.py", "file:backend/app/routers/account.py", "file:backend/app/domain/account.py", "file:backend/app/domain/reset.py", "file:backend/app/domain/files.py"]
inventory_refs: ["route:GET:/api/account/export", "route:DELETE:/api/account"]
related: ["subsystem:gdpr-account", "subsystem:files-crypto-storage", "subsystem:auth-vault-consent"]
last_verified: 2026-08-02
status: active
---
# Account export and deletion

## Entry
An authenticated user who owns durable vault data requests export through the route dependency, or any authenticated password-backed user requests self-deletion. Route-policy metadata describes these gates but does not execute them.
## Sequence
Export selects the supported owned-vault projection, decrypts linked originals, and assembles one in-memory ZIP. Deletion verifies the password, removes every owned vault plus the account and sessions while scrubbing attribution in merely joined vaults, commits once, clears the cookie, then attempts physical object cleanup.
## Failures and retries
Missing ownership blocks export, and a missing key/object or decryption error aborts the archive. Database/current-subject deletion failures roll back and skip cleanup; storage deletion after commit is best-effort, so the route can succeed while orphan ciphertext remains.
## Trust boundaries
Only owned vaults are exported; only server-side metadata enumerates data; caller-supplied IDs cannot broaden scope. The export is a selected portable projection, not a database dump. Database and key-row erasure invalidates sessions and live decryption paths, but does not prove physical deletion of every object.
## Observability
Request/audit status and bounded object identifiers; exported content and secrets stay out of logs.
## Change together
For every new vault-owned model, create the next linear revision and make an explicit inclusion/omission decision in export DTOs/serialization, ordered deletion and shared-vault attribution scrubbing. Change `models`, `schemas`, `domain.account`, `domain.reset`, key/session lifecycle, SQLite/PostgreSQL gates, inventory/Map checks, and account/adversarial tests together.

## Proof
`backend/app/routers/account.py` → `_account_owner_user`, `account_export`, `account_delete`; `backend/app/domain/account.py` → `export_account`, `build_export_zip`, `delete_account`; `backend/app/domain/reset.py` → `_delete_vault_rows`; `backend/tests/test_account.py` → export omissions, owned/shared-vault deletion, and storage-failure success.

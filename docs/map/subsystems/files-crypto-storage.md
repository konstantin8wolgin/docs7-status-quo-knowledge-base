---
id: subsystem:files-crypto-storage
kind: subsystem
summary: Authenticated envelope encryption, process-selected object storage, and authorized buffered file reads.
read_when: ["encrypted file storage", "object storage crypto", "file download integrity"]
sources: ["file:backend/app/models.py", "file:backend/app/main.py", "file:backend/app/domain/files.py", "file:backend/app/crypto.py", "file:backend/app/storage.py", "file:backend/app/storage_s3.py", "file:backend/app/routers/files.py"]
inventory_refs: ["route:GET:/api/file/{document_id}", "model:FileObject", "model:VaultKey", "migration:0004"]
related: ["flow:encrypted-file-read", "subsystem:capture-documents"]
last_verified: 2026-08-02
status: active
---
# Files, cryptography, and storage

## Responsibility
Encrypt file bytes per vault, store ciphertext through the configured adapter, and return buffered plaintext only after authorization and AES-GCM authentication.
## Boundaries
Plain bytes enter AES-256-GCM with no associated data; object storage sees ciphertext, while wrapped vault/file keys and metadata stay in the database.
## Interfaces
File insertion/read helpers, one local-or-S3 adapter selected at process composition, and the buffered file route.
## Dependencies
Master key configuration, vault keys, object metadata, and request context.
## Data
`FileObject` keeps plaintext SHA-256, sizes, storage keys, `storage_provider`, and wrapped DEKs; `VaultKey` wraps vault material. Insertions do not set `storage_provider`, so even S3-backed rows retain the model default `local`.
## Invariants
Keys and plaintext never enter logs or the Map. AES-GCM tag verification authenticates ciphertext before plaintext is returned, but reads do not compare the stored SHA-256 and use no AAD binding to file/vault metadata. Reads ignore per-row `storage_provider` and use the process-selected adapter, so switching backends can strand earlier objects. Ciphertext and plaintext are read fully into memory; there is no byte-range or incremental streaming path.
## Change points
Change crypto envelope/AAD and stored-hash semantics, `FileObject` metadata/migration, adapter selection and backend-switch migration, upload/export/delete callers, download response/range policy, and crypto/storage/security tests together.
## Proof
`backend/app/main.py` → `create_app`; `backend/app/domain/files.py` → `insert_file_object`, `read_file_bytes`; `backend/app/crypto.py` → `encrypt_bytes`, `decrypt_bytes`; `backend/app/storage.py` → `object_storage_from`; `backend/app/routers/files.py` → `file`; crypto, local/S3 storage, upload, account-deletion, and cross-vault adversarial tests. No current proof covers S3 provider metadata, backend switching, SHA comparison, range reads, or streaming.

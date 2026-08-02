---
id: flow:encrypted-file-read
kind: flow
summary: Authorize a document read, buffer ciphertext, unwrap its key, authenticate/decrypt, and return buffered plaintext.
read_when: ["encrypted file read", "download decrypt storage"]
sources: ["file:backend/app/routers/files.py", "file:backend/app/routers/__init__.py", "file:backend/app/domain/files.py", "file:backend/app/crypto.py", "file:backend/app/storage.py"]
inventory_refs: ["route:GET:/api/file/{document_id}", "model:FileObject", "model:VaultKey"]
related: ["subsystem:files-crypto-storage", "subsystem:gdpr-account"]
last_verified: 2026-08-02
status: active
---
# Encrypted file read

## Entry
A vault-scoped caller requests a document file.
## Sequence
Load the vault-owned document/object, check existence through the process-selected adapter, fetch the full ciphertext, unwrap vault KEK and file DEK, authenticate/decrypt with AES-GCM, then build a full-body response with media metadata. The stored plaintext SHA-256 is not read or compared.
## Failures and retries
Missing ownership, object, or key and AES-GCM authentication/decryption failure return no plaintext. A metadata-hash mismatch alone is undetected because no read-time comparison exists.
## Trust boundaries
Storage cannot authorize reads and never receives plaintext keys. Row `storage_provider` does not select the adapter; the current process configuration does.
## Observability
Request status and object identifiers may be logged; plaintext, keys, and document content may not.
## Change together
File route/response buffering and range policy, domain read/hash checks, crypto envelope/AAD, row provider metadata plus adapter/backend migration, GDPR export/deletion, and crypto/storage/security tests.

## Proof
`backend/app/routers/files.py` → `file`; `backend/app/routers/__init__.py` → `file_response`; `backend/app/domain/files.py` → `get_vault_kek`, `read_file_bytes`; `backend/app/crypto.py` → `unwrap_key`, `decrypt_bytes`; `backend/tests/test_crypto.py` and `backend/tests/test_security_adversarial.py` → authenticated decryption, missing-key, and vault-scope behavior.

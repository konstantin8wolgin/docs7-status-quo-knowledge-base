---
id: guide-snapshot-and-evidence-manifest
title: Snapshot and Evidence Manifest
kind: guide
status: current
snapshot_commit: 5448cf335e2cb25d74d6c0e6c476b72d1e14e803
last_verified: 2026-08-02
tags:
  - status-quo/guide
parent: "[[INDEX]]"
related:
  - "[[How to Use This Knowledge Base]]"
  - "[[Truth and Status Model]]"
  - "[[Reading Paths for Humans and Agents]]"
---

> [!info] Navigation
> Parent: [[INDEX]]. Siblings: [[How to Use This Knowledge Base]] · [[Truth and Status Model]] · [[Reading Paths for Humans and Agents]].

# Snapshot and Evidence Manifest

> [!warning] Snapshot boundary
> Product truth is frozen at commit `5448cf335e2cb25d74d6c0e6c476b72d1e14e803`. Documentation-only commits after it may add or correct this corpus without changing the described runtime behavior.

## Evidence layers

| Layer | Repository location | Use |
| --- | --- | --- |
| Executable truth | `backend/`, `client/`, migrations, tests, runtime configuration, generated OpenAPI | Establish behavior and prove contracts |
| Structural inventory | `docs/map/inventory/inventory.json` | Enumerate current routes, models, jobs, migrations, and client methods |
| Curated architecture | `docs/map/INDEX.md` and its subsystem and flow pages | Explain boundaries and guide focused source reading |
| Decisions | `docs/adr/` | Explain why a durable architecture choice was made |
| Historical evidence | scoped progress notes and plans | Distinguish prior intent from current behavior only |

The current committed inventory contains 39 routes, 31 client methods, 32 models, 5 jobs, 11 migrations, 2 classified unknown probes and 65 test files. The last category is 47 backend plus 18 client files; the handbook checker and Mermaid corpus test were added after the frozen product snapshot. The inventory does not declare a generation timestamp or source commit, so this guide does not infer either. The inventory is generated structural truth; never hand-edit it.

## Citation and privacy boundary

Evidence citations use repository-relative paths plus symbols or test names. They do not use line numbers. Never read or reproduce root `.env`, credentials, raw transcripts, private documents, plaintext keys, sensitive prompt content, or private golden corpus and output.

## Structural proof

Run the finished-corpus checker in strict mode:

```bash
backend/.venv/bin/python backend/scripts/check_status_quo.py --repo-root .
```

Strict success requires current frontmatter and nonempty relationship fields, `INDEX.md` as the only root, unambiguous wikilinks, resolvable local Markdown links, parent backlinks, planned-only isolation, exact capability equality across owning feature notes and both capability ledgers, at least one technical `feature_link` for every non-absent/non-planned capability, exact first-column equality between [[Contract Coverage]] and every generated inventory section, and exact view-key/hash equality between the client registry and twelve-destination UI ledger. Every inventory ID must also occur outside a fenced code block somewhere in the corpus. It does not replace behavioral tests, Codebase Map maintenance, runtime proof, Mermaid parsing, or independent review.

The enforced contract set contains the two classified unknown probes and all 65 tests as well as routes, client methods, models, jobs, and migrations. The 33-capability equality check includes [[Capability Ledger]] and [[Feature-to-Code Matrix]]. Mermaid syntax has a separate pinned renderer lane: `cd client && npm run check:status-quo-mermaid`.

## 2026-08-02 reconciliation proof

The final proof began from documentation branch HEAD `05b232b7ebc9ef03ad0794b1bb55212e22aeefed`, committed tree `889cf62cfe0ef60b4edf0f737bbc5815df96ae13`, with product truth still frozen at the snapshot commit named above. Gates ran against the reconciled documentation worktree on top of that HEAD. This manifest does not imply that later documentation commits changed executable behavior.

### Structural and curated Map reconciliation

`./cbmap inventory build` generated 39 routes, 31 client methods, 32 models, 5 jobs, 11 migrations, and 64 tests. It was byte-identical to the inventory already committed at proof HEAD. Relative to the frozen product snapshot, the complete generated delta remains test count 63 → 64 plus `test:backend/tests/test_status_quo.py`; there is no route/model/job/migration/client-method delta.

The semantic reconciliation updated these current pages and no byte-identical page required an attestation:

- flows: `flow:account-export-deletion`, `flow:auth-vault-context`, `flow:encrypted-file-read`, `flow:fact-verification-provenance`, `flow:retry-lease-recovery`, `flow:sample-import`, `flow:search-grounded-chat`, `flow:upload-job-extraction-filing-polling`;
- subsystems: `subsystem:ai-extraction-provenance`, `subsystem:auth-vault-consent`, `subsystem:capture-documents`, `subsystem:data-migrations-testing-operations`, `subsystem:entities-filing-review`, `subsystem:facts-summaries`, `subsystem:files-crypto-storage`, `subsystem:gdpr-account`, `subsystem:jobs-workers`, `subsystem:runtime-configuration`, `subsystem:search-grounded-chat`.

| Exact command | Result |
| --- | --- |
| `./cbmap inventory build` | Exit 0; counts 39 / 31 / 32 / 5 / 11 / 64; seven generated files written by the generator only |
| `./cbmap inventory check` | Exit 0; `status: current`, no errors |
| `./cbmap impact --base 5448cf335e2cb25d74d6c0e6c476b72d1e14e803` | Before maintenance: the 19 edited page IDs were unresolved; after maintenance: the same impacts remained visible with `unresolved_page_ids: []` |
| `./cbmap maintain --base 5448cf335e2cb25d74d6c0e6c476b72d1e14e803` | Exit 0; exactly 19 updated page IDs; no attestations; generated `source-lock.json` and Map log reconciled transactionally |
| `./cbmap check --base 5448cf335e2cb25d74d6c0e6c476b72d1e14e803` | Exit 0; `status: current`, no errors |
| `./cbmap audit --max-findings 20` | Exit 0; 15 untruncated information-only asymmetric-relation advisories; no rewrite was made merely to silence them |

### Documentation, client, static, and backend gates

| Exact command | Result |
| --- | --- |
| `backend/.venv/bin/python backend/scripts/check_status_quo.py --repo-root .` | Exit 0; strict checker produced no error output |
| `backend/.venv/bin/python -m pytest backend/tests/test_status_quo.py` | Exit 0; 39 passed, 0 failed, 0 skipped in 0.45 s |
| `cd client && node --test src/*.test.mjs` | Exit 0; 73 passed, 0 failed, 0 skipped/cancelled/todo in 3968.469295 ms |
| `cd client && npm run build` | Exit 0; Vite 5.4.21 transformed 1,602 modules and built in 3.40 s; output 0.69 kB HTML, 28.53 kB CSS, 335.53 kB JavaScript |
| `ruff check backend` | Exit 127; the bare `ruff` executable is unavailable on this host's `PATH` |
| `backend/.venv/bin/ruff check backend` | Exit 0; `All checks passed!` using the repository virtualenv tool |
| `ruff format --check backend` | Exit 127; the bare `ruff` executable is unavailable on this host's `PATH` |
| `backend/.venv/bin/ruff format --check backend` | Exit 0; 132 files already formatted |
| `backend/.venv/bin/python backend/scripts/export_openapi.py --check` | Exit 0; `openapi.json is current` |
| `cd backend && .venv/bin/python -m pytest` | Exit 0; 643 passed, 34 skipped, 0 failed in 808.51 s (677 collected) on the default SQLite lane |

### Database and external-provider lanes

| Lane | Exact evidence and boundary |
| --- | --- |
| PostgreSQL | Availability probe `cd backend && .venv/bin/python -c 'import psycopg; conn = psycopg.connect("postgresql://docs7:docs7@127.0.0.1:5433/docs7", connect_timeout=5); conn.close(); print("PostgreSQL connection OK")'` exited 1 in 0.573638522 s with connection refused at `127.0.0.1:5433`. The configured PostgreSQL pytest lane was therefore unavailable and was not run; no service was started or installed. |
| S3 | The environment-gated S3 adapter test remained skipped in the full suite because no task-scoped test endpoint was available. No API-level S3 upload/download, provider-metadata, backend-switch, bucket-bootstrap, or production-permission proof was claimed. |
| Vertex | No live provider call ran and no credentials were inspected. The full suite exercised committed seed/synthetic provider behavior only; live Vertex availability, region, quota, and production calls remain external evidence. |
| Private golden backtest | The private golden corpus and its output were not read, run, or copied. That release-only evidence remains unavailable here and is not replaced by the committed synthetic fixture lane. |

### Bounded synthetic runtime and browser walkthrough

The launcher ran from a fresh tracked-only temporary copy so existing local databases, object bytes, and untracked files were outside the test. A root `.env` absence check succeeded without reading environment-file contents. The first `bash start.sh` attempt exited 127 before application startup because the shared development virtualenv has no `pip` executable. After replacing that temp-only symlink with a genuinely fresh virtualenv, `bash start.sh` exercised first-run dependency bootstrap, seeded 11 synthetic documents and 4 persons, and started Uvicorn on `127.0.0.1:8787` plus Vite on `127.0.0.1:5173`.

| Exact command or walkthrough | Result |
| --- | --- |
| `curl --fail --silent --show-error http://127.0.0.1:8787/api/health` | Exit 0; `{"ok":true,"backend":"fastapi","database":"sqlite"}` |
| `curl --fail --silent --show-error http://127.0.0.1:8787/api/ready` | Exit 0; `{"ok":true}`; this remains database-only readiness |
| In-app browser at `http://127.0.0.1:5173/` | Synthetic demo login and dashboard loaded; visible counts were 5 documents, 3 tasks, and 16 facts. The walkthrough opened `Aufnehmen` and verified two allowlisted sample choices, then opened `Dokumente` and verified five synthetic rows. It opened no original file and performed no upload, reset, deletion, or other mutation. Browser console error count was zero. |
| Bounded stop via Ctrl-C | Launcher exited 130 by deliberate interrupt after proof and ran its cleanup trap |
| `curl --silent --show-error --max-time 2 http://127.0.0.1:8787/api/health` | Exit 7 after cleanup; backend port refused the connection |
| `curl --silent --show-error --max-time 2 http://127.0.0.1:5173/` | Exit 7 after cleanup; client port refused the connection |

The isolated temporary package, including its synthetic database and object store, was moved to trash after both services stopped. It can be recovered from the desktop trash until that trash is emptied.

### Post-manifest reconciliation check

After recording the evidence above, the strict corpus checker exited 0 with no error output, `backend/.venv/bin/python -m pytest backend/tests/test_status_quo.py` passed all 39 tests in 0.50 s, `./cbmap inventory check` reported `status: current` with no errors, and `./cbmap check --base 5448cf335e2cb25d74d6c0e6c476b72d1e14e803` reported `status: current` with no errors.

## Independent AutoReview repair wave

The frozen full-branch review at documentation commit `d856f5a223ad496175c833d05c820876747b470c` found no Critical issue and three Important blockers. Source reproduction confirmed all three: the feature/rebuild layers collapsed the two membership queries in `backend/app/context.py`; the central gap register incorrectly called exported review/run/entity records omitted; and the original checker could not enforce the structural contract it claimed. Two Minor defects were also confirmed: account-deletion cookie/object-cleanup order was reversed in one lifecycle note, and three design-spec hard-break spaces made the frozen-range `git diff --check` claim false.

The single repair wave:

- records the distinct vault/role and subject membership queries, ordering, duplicate-row ambiguity, and dangling-person no-fallback behavior;
- aligns the central export omissions with the actual DTO projection and corrects deletion's commit → object-cleanup → response-cookie sequence;
- requires `parent`/nonempty `related` frontmatter and `status: current`, limits the empty parent to `INDEX.md`, resolves local links and parent backlinks, contains planned-only notes, enforces exact 33-capability and 185-inventory-ID ledger equality, requires technical reciprocity for every current capability, and compares exact UI view-key/hash mappings rather than value sets;
- adds `client/scripts/check-status-quo-mermaid.mjs` plus a client test using pinned `mermaid@11.16.0` and `jsdom@26.1.0`; all 61 Mermaid blocks parse; and
- removes the three trailing-space defects and corrects the internal proof report rather than preserving a false pass claim.

Focused repair proof before confirmation review:

| Exact command | Result |
| --- | --- |
| `backend/.venv/bin/python backend/scripts/check_status_quo.py --repo-root .` | Exit 0; no diagnostics; exact structural, capability, inventory and UI ledgers accepted |
| `backend/.venv/bin/python -m pytest backend/tests/test_status_quo.py -q` | Exit 0; 49 passed |
| `cd client && node --test src/*.test.mjs` | Exit 0; 74 passed |
| `cd client && npm run check:status-quo-mermaid` | Exit 0; 61 diagrams validated with the pinned parser |
| `cd client && npm run build` | Exit 0; Vite transformed 1,602 modules and built in 3.64 s |
| `backend/.venv/bin/ruff check backend` | Exit 0; all checks passed |
| `backend/.venv/bin/ruff format --check backend` | Exit 0; all 132 files formatted after the two edited checker files were formatted |
| `./cbmap inventory build` then `./cbmap inventory check` | Exit 0; 39 routes / 31 client methods / 32 models / 5 jobs / 11 migrations / 65 tests; inventory current |
| `./cbmap maintain --base 5448cf335e2cb25d74d6c0e6c476b72d1e14e803` | Exit 0; current, no new page updates or attestations required |
| `./cbmap check --base 5448cf335e2cb25d74d6c0e6c476b72d1e14e803` | Exit 0; current, no errors |
| `./cbmap audit --max-findings 20` | Exit 0; the same 15 information-only asymmetric-relation advisories |

The 643-pass SQLite product suite, isolated runtime walkthrough and unavailable PostgreSQL/S3/Vertex/private-golden boundaries above remain the proof for unchanged product code. The repair wave changes documentation and documentation-validation tooling only; it does not change the frozen product snapshot.

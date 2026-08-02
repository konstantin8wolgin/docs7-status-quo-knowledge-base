# Docs7 Status-Quo Knowledge Base

This repository is a standalone, public export of the evidence-backed Docs7
status-quo documentation. It describes the product as implemented at source
snapshot `5448cf335e2cb25d74d6c0e6c476b72d1e14e803`; it is not a future-product
proposal. Documentation was reconciled through source-repository commit
`7efa4bb`.

Start with **[docs/status-quo/INDEX.md](docs/status-quo/INDEX.md)**. The corpus is
structured like an Obsidian knowledge base: the root index links to feature,
technical, rebuild, and traceability atlases, and each atlas links to focused
notes so a human or agent can load only the context needed for the current
question.

## What is included

- `docs/status-quo/` — 86 current-product notes covering user-visible features,
  subfeatures, failure behavior, limitations, implementation, rebuild order,
  acceptance proof, and known non-capabilities.
- `docs/map/` — the supporting Codebase Map, flow/subsystem pages, and generated
  structural inventory used by the documentation.
- `docs/superpowers/` — the historical design and execution plan used to create
  the corpus. These files explain the documentation project; they are not the
  product's current behavior.
- `backend/scripts/check_status_quo.py` and `backend/tests/test_status_quo.py` —
  the structural validator and its test suite.
- `client/scripts/check-status-quo-mermaid.mjs` and its test — pinned Mermaid
  parsing for every diagram.
- `client/src/lib.jsx` and `client/src/view-regressions.test.mjs` — the minimal
  source evidence needed for the validator's exact UI view-key/hash comparison.
  This is not a runnable copy of the Docs7 application.

## Reading routes

| Goal | Entry point |
| --- | --- |
| Learn what the product currently does | [Feature Atlas](docs/status-quo/10-features/Feature%20Atlas.md) |
| Understand how the current system works | [Technical Atlas](docs/status-quo/20-technical/Technical%20Atlas.md) |
| Rebuild the behavior from scratch | [Rebuild Atlas](docs/status-quo/30-rebuild/Rebuild%20Atlas.md) |
| Audit every capability and contract | [Capability Ledger](docs/status-quo/40-traceability/Capability%20Ledger.md) and [Contract Coverage](docs/status-quo/40-traceability/Contract%20Coverage.md) |
| See defects, absences, and unreachable features | [Known Gaps and Non-Capabilities](docs/status-quo/40-traceability/Known%20Gaps%20and%20Non-Capabilities.md) |

## Validate the export

Python 3.11+ and Node.js 20+ are recommended.

```bash
python -m pip install -r requirements-dev.txt
python backend/scripts/check_status_quo.py --repo-root .
python -m pytest backend/tests/test_status_quo.py -q

cd client
npm ci
npm run check:status-quo-mermaid
npm test
```

The structural checker validates frontmatter, links, hierarchy, capability and
inventory parity, technical reciprocity, and the UI view registry. Mermaid
validation parses all 61 diagrams with pinned dependencies.

## Public-export boundary

The repository contains documentation, generated structural inventory, test
fixtures, and the minimal UI registry evidence named above. It excludes the
application implementation, environment files, credentials, raw transcripts,
private documents, and private golden-test data. Connection strings shown in
the evidence record use local development-only test credentials from the
documented repository gate; they are not production secrets.

Source citations intentionally use repository-relative paths and symbols. They
remain useful as a reconstruction map even though most cited product source is
not duplicated in this documentation export.

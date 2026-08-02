from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "backend/scripts/check_status_quo.py"
SNAPSHOT_COMMIT = "5448cf335e2cb25d74d6c0e6c476b72d1e14e803"

SPEC = importlib.util.spec_from_file_location("check_status_quo", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def write_inventory(repo_root: Path, **sections: list[dict[str, str]]) -> None:
    inventory = {
        "routes": [],
        "models": [],
        "jobs": [],
        "migrations": [],
        "client_methods": [],
        "unknowns": [],
        "tests": [],
        **sections,
    }
    target = repo_root / "docs/map/inventory/inventory.json"
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps(inventory), encoding="utf-8")


def write_note(
    repo_root: Path,
    relative_path: str,
    *,
    note_id: str,
    title: str,
    kind: str = "guide",
    body: str = "",
    extra_frontmatter: str = "",
    snapshot_commit: str = SNAPSHOT_COMMIT,
) -> Path:
    target = repo_root / "docs/status-quo" / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    is_index = Path(relative_path).as_posix() == "INDEX.md"
    note_basename = Path(relative_path).stem
    parent = "parent: []" if is_index else f'parent: "[[{note_basename}]]"'
    related = f'  - "[[{note_basename}]]"'
    target.write_text(
        "\n".join(
            (
                "---",
                f"id: {note_id}",
                f"title: {title}",
                f"kind: {kind}",
                "status: current",
                f"snapshot_commit: {snapshot_commit}",
                "last_verified: 2026-08-01",
                "tags:",
                "  - status-quo/test",
                parent,
                "related:",
                related,
                extra_frontmatter.rstrip("\n"),
                "---",
                "",
                body,
                "",
            )
        ),
        encoding="utf-8",
    )
    return target


def test_reports_missing_frontmatter(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    target = tmp_path / "docs/status-quo/INDEX.md"
    target.parent.mkdir(parents=True)
    target.write_text("# Status quo\n", encoding="utf-8")

    errors = CHECKER.check_corpus(tmp_path)

    assert errors == ["docs/status-quo/INDEX.md: missing frontmatter"]


@pytest.mark.parametrize(
    ("field", "original_value"),
    (
        ("id", "index"),
        ("title", "Index"),
        ("kind", "guide"),
        ("status", "current"),
        ("snapshot_commit", SNAPSHOT_COMMIT),
        ("last_verified", "2026-08-01"),
    ),
)
def test_reports_blank_required_scalar(tmp_path: Path, field: str, original_value: str) -> None:
    write_inventory(tmp_path)
    target = write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    target.write_text(
        target.read_text(encoding="utf-8").replace(f"{field}: {original_value}", f'{field}: ""'),
        encoding="utf-8",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert f"docs/status-quo/INDEX.md: frontmatter field '{field}' must not be blank" in errors


@pytest.mark.parametrize("null_value", ("null", "Null", "NULL", "~"))
def test_reports_yaml_null_required_scalar(tmp_path: Path, null_value: str) -> None:
    write_inventory(tmp_path)
    target = write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    target.write_text(
        target.read_text(encoding="utf-8").replace("id: index", f"id: {null_value}"),
        encoding="utf-8",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert "docs/status-quo/INDEX.md: frontmatter field 'id' must not be null" in errors


def test_reports_empty_tags_but_permits_empty_hub_reference_lists(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    target = write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    target.write_text(
        target.read_text(encoding="utf-8").replace("tags:\n  - status-quo/test", "tags: []"),
        encoding="utf-8",
    )
    write_note(
        tmp_path,
        "20-technical/Technical.md",
        note_id="technical",
        title="Technical",
        kind="technical",
        extra_frontmatter="""map_pages: []
inventory_refs: []
feature_links: []""",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert errors == ["docs/status-quo/INDEX.md: frontmatter field 'tags' must not be empty"]


def test_rejects_symlinked_note_without_reading_its_target(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    outside = tmp_path / "outside.md"
    outside.write_text("Read [[Private Outside Note]].\n", encoding="utf-8")
    link = tmp_path / "docs/status-quo/Leak.md"
    link.symlink_to(outside)

    errors = CHECKER.check_corpus(tmp_path)

    assert errors == ["docs/status-quo/Leak.md: symlinked note is not allowed"]


def test_rejects_symlinked_docs_ancestor_without_reading_outside(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    outside_repo = tmp_path / "outside-repo"
    write_note(outside_repo, "Private.md", note_id="private", title="Private")
    write_inventory(outside_repo)
    (repo_root / "docs").symlink_to(outside_repo / "docs", target_is_directory=True)

    errors = CHECKER.check_corpus(repo_root)

    assert errors == ["docs/status-quo: symlinked path component is not allowed: docs"]


def test_rejects_symlinked_corpus_without_reading_outside(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    write_inventory(repo_root)
    outside_repo = tmp_path / "outside-repo"
    write_note(outside_repo, "Private.md", note_id="private", title="Private")
    (repo_root / "docs/status-quo").symlink_to(
        outside_repo / "docs/status-quo", target_is_directory=True
    )

    errors = CHECKER.check_corpus(repo_root)

    assert errors == ["docs/status-quo: symlinked path component is not allowed: docs/status-quo"]


def test_rejects_symlinked_inventory_ancestor_without_reading_outside(
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "repo"
    write_note(repo_root, "INDEX.md", note_id="index", title="Index")
    outside_map = tmp_path / "outside-map"
    inventory = outside_map / "inventory/inventory.json"
    inventory.parent.mkdir(parents=True)
    inventory.write_text("not private inventory", encoding="utf-8")
    (repo_root / "docs/map").symlink_to(outside_map, target_is_directory=True)

    errors = CHECKER.check_corpus(repo_root)

    assert errors == [
        "docs/map/inventory/inventory.json: symlinked path component is not allowed: docs/map"
    ]


def test_rejects_symlinked_inventory_file_without_reading_outside(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    write_note(repo_root, "INDEX.md", note_id="index", title="Index")
    inventory = repo_root / "docs/map/inventory/inventory.json"
    inventory.parent.mkdir(parents=True)
    outside_inventory = tmp_path / "outside-inventory.json"
    outside_inventory.write_text("not private inventory", encoding="utf-8")
    inventory.symlink_to(outside_inventory)

    errors = CHECKER.check_corpus(repo_root)

    assert errors == [
        "docs/map/inventory/inventory.json: symlinked path component is not allowed: "
        "docs/map/inventory/inventory.json"
    ]


def test_reports_unreadable_note_without_raising(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    unreadable = write_note(
        tmp_path,
        "Unreadable.md",
        note_id="unreadable",
        title="Unreadable",
    ).resolve()
    original_read_text = Path.read_text

    def raise_for_unreadable(path: Path, *args, **kwargs):
        if path == unreadable:
            raise OSError("operating-system detail must not leak")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", raise_for_unreadable)

    errors = CHECKER.check_corpus(tmp_path)

    assert errors == ["docs/status-quo/Unreadable.md: unable to read note"]


def test_cli_reports_non_utf8_note_without_traceback(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    invalid = tmp_path / "docs/status-quo/Invalid UTF-8.md"
    invalid.write_bytes(b"\xff\xfe\x00")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(tmp_path)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert result.stdout.splitlines() == [
        "docs/status-quo/Invalid UTF-8.md: note is not valid UTF-8"
    ]
    assert result.stderr == ""


def test_reports_duplicate_note_id(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "One.md", note_id="same-id", title="One")
    write_note(tmp_path, "Two.md", note_id="same-id", title="Two")

    errors = CHECKER.check_corpus(tmp_path)

    assert any("duplicate id 'same-id'" in error for error in errors)


def test_reports_duplicate_human_readable_title(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "One.md", note_id="one", title="Shared title")
    write_note(tmp_path, "Two.md", note_id="two", title="Shared title")

    errors = CHECKER.check_corpus(tmp_path)

    assert any("duplicate title 'Shared title'" in error for error in errors)


def test_reports_duplicate_note_basename(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "first/Shared.md", note_id="first", title="First")
    write_note(tmp_path, "second/Shared.md", note_id="second", title="Second")

    errors = CHECKER.check_corpus(tmp_path)

    assert any("duplicate note basename 'Shared'" in error for error in errors)


def test_reports_unresolved_wikilink(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(
        tmp_path,
        "INDEX.md",
        note_id="index",
        title="Index",
        body="Read [[Missing Note]].",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert any("unresolved wikilink 'Missing Note'" in error for error in errors)


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    (
        ("delivery", "finished"),
        ("reachability", "everyone"),
        ("persistence", "database"),
        ("evidence", "probably"),
    ),
)
def test_reports_invalid_feature_status_axis(
    tmp_path: Path, field: str, invalid_value: str
) -> None:
    write_inventory(tmp_path)
    axes = {
        "delivery": "implemented",
        "reachability": "user-facing",
        "persistence": "durable",
        "evidence": "code-and-tests",
    }
    axes[field] = invalid_value
    extra = "\n".join(
        (
            "capability_ids:",
            "  - TEST-01",
            *(f"{name}: {value}" for name, value in axes.items()),
        )
    )
    write_note(
        tmp_path,
        "10-features/Feature.md",
        note_id="feature",
        title="Feature",
        kind="feature",
        extra_frontmatter=extra,
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert any(f"invalid {field} value '{invalid_value}'" in error for error in errors)


def test_reports_duplicate_capability_id_ownership(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    feature_fields = """capability_ids:
  - SHARED-01
delivery: implemented
reachability: user-facing
persistence: durable
evidence: code-and-tests"""
    write_note(
        tmp_path,
        "10-features/One.md",
        note_id="feature-one",
        title="Feature One",
        kind="feature",
        extra_frontmatter=feature_fields,
    )
    write_note(
        tmp_path,
        "10-features/Two.md",
        note_id="feature-two",
        title="Feature Two",
        kind="feature",
        extra_frontmatter=feature_fields,
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert any("duplicate capability id 'SHARED-01'" in error for error in errors)


def test_inventory_id_inside_code_fence_does_not_count_as_coverage(tmp_path: Path) -> None:
    route_id = "route:GET:/api/example"
    write_inventory(tmp_path, routes=[{"id": route_id}])
    write_note(
        tmp_path,
        "INDEX.md",
        note_id="index",
        title="Index",
        body=f"```text\n{route_id}\n```",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert f"missing inventory reference: {route_id}" in errors


def test_inventory_id_prefix_does_not_count_as_exact_coverage(tmp_path: Path) -> None:
    model_id = "model:Document"
    write_inventory(tmp_path, models=[{"id": model_id}])
    write_note(
        tmp_path,
        "INDEX.md",
        note_id="index",
        title="Index",
        body="The different ID `model:DocumentAmount` is covered.",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert f"missing inventory reference: {model_id}" in errors


@pytest.mark.parametrize("invalid_closer", ("```", "````not-a-close"))
def test_invalid_fence_closer_keeps_links_and_inventory_ids_hidden(
    tmp_path: Path, invalid_closer: str
) -> None:
    model_id = "model:Document"
    write_inventory(tmp_path, models=[{"id": model_id}])
    write_note(
        tmp_path,
        "INDEX.md",
        note_id="index",
        title="Index",
        body=(f"````markdown\n{invalid_closer}\n{model_id}\n[[Ignored Missing Link]]\n````"),
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert errors == [f"missing inventory reference: {model_id}"]


@pytest.mark.parametrize(
    "body",
    (
        "> ```text\n> model:Document\n> [[Ignored Missing Link]]\n> ```",
        "~~~text\nmodel:Document\n[[Ignored Missing Link]]\n~~~",
    ),
)
def test_markdown_fence_containers_hide_links_and_inventory_ids(tmp_path: Path, body: str) -> None:
    model_id = "model:Document"
    write_inventory(tmp_path, models=[{"id": model_id}])
    write_note(tmp_path, "INDEX.md", note_id="index", title="Index", body=body)

    errors = CHECKER.check_corpus(tmp_path)

    assert errors == [f"missing inventory reference: {model_id}"]


def test_four_space_indented_pseudo_fence_does_not_hide_following_text(
    tmp_path: Path,
) -> None:
    model_id = "model:Document"
    write_inventory(tmp_path, models=[{"id": model_id}])
    write_note(
        tmp_path,
        "INDEX.md",
        note_id="index",
        title="Index",
        body=f"    ```text\n{model_id}\n    ```",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert errors == []


def test_four_space_indented_marker_does_not_close_fence(tmp_path: Path) -> None:
    model_id = "model:Document"
    write_inventory(tmp_path, models=[{"id": model_id}])
    write_note(
        tmp_path,
        "INDEX.md",
        note_id="index",
        title="Index",
        body=(f"```text\n    ```\n{model_id}\n[[Ignored Missing Link]]\n```"),
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert errors == [f"missing inventory reference: {model_id}"]


def test_passing_minimal_corpus_resolves_paths_and_unique_basenames(tmp_path: Path) -> None:
    inventory_ids = {
        "routes": "route:GET:/api/example",
        "models": "model:app.models.Example",
        "jobs": "job:example",
        "migrations": "migration:0001_example",
        "client_methods": "client-method:example",
    }
    write_inventory(
        tmp_path,
        **{section: [{"id": item_id}] for section, item_id in inventory_ids.items()},
    )
    write_note(
        tmp_path,
        "INDEX.md",
        note_id="index",
        title="Index",
        body="""Start at [[10-features/Feature Hub]].

```markdown
[[Ignored Missing Link]]
```""",
    )
    write_note(
        tmp_path,
        "10-features/Feature Hub.md",
        note_id="feature-hub",
        title="Feature Hub",
        kind="feature-hub",
        extra_frontmatter="""capability_ids:
  - TEST-01
delivery: partial
reachability: user-facing
persistence: durable
evidence: source-only""",
        body="Continue to [[Technical Atlas]].",
    )
    write_note(
        tmp_path,
        "20-technical/Technical Atlas.md",
        note_id="technical-atlas",
        title="Technical Atlas",
        kind="technical-hub",
        extra_frontmatter="""map_pages:
  - subsystem:example
inventory_refs:
  - route:GET:/api/example
feature_links:
  - TEST-01""",
        body="\n".join((*inventory_ids.values(), "Return to [[../INDEX]].")),
    )
    write_note(
        tmp_path,
        "40-traceability/Capability Ledger.md",
        note_id="capability-ledger",
        title="Capability Ledger",
        kind="traceability",
        body="| ID | Capability |\n| --- | --- |\n| `TEST-01` | test |",
    )
    write_note(
        tmp_path,
        "40-traceability/Feature-to-Code Matrix.md",
        note_id="feature-matrix",
        title="Feature-to-Code Matrix",
        kind="traceability",
        body="| ID | Code |\n| --- | --- |\n| `TEST-01` | test |",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert errors == []


def test_reports_wrong_snapshot_commit_and_missing_technical_fields(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(
        tmp_path,
        "20-technical/Technical.md",
        note_id="technical",
        title="Technical",
        kind="technical",
        snapshot_commit="not-the-snapshot",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert any("snapshot_commit must be" in error for error in errors)
    assert any("missing required frontmatter field 'map_pages'" in error for error in errors)
    assert any("missing required frontmatter field 'inventory_refs'" in error for error in errors)
    assert any("missing required frontmatter field 'feature_links'" in error for error in errors)


def test_requires_relationship_frontmatter_and_current_corpus_status(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    target = write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    target.write_text(
        target.read_text(encoding="utf-8")
        .replace("status: current", "status: draft")
        .replace("parent: []\n", "")
        .replace('related:\n  - "[[INDEX]]"\n', ""),
        encoding="utf-8",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert "docs/status-quo/INDEX.md: missing required frontmatter field 'parent'" in errors
    assert "docs/status-quo/INDEX.md: missing required frontmatter field 'related'" in errors
    assert "docs/status-quo/INDEX.md: status must be 'current', got 'draft'" in errors


def test_reports_unresolved_local_markdown_link(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(
        tmp_path,
        "INDEX.md",
        note_id="index",
        title="Index",
        body="Read [missing](./Missing.md).",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert "docs/status-quo/INDEX.md: unresolved local Markdown link './Missing.md'" in errors


def test_parent_must_link_back_to_child(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    child = write_note(tmp_path, "Child.md", note_id="child", title="Child")
    child.write_text(
        child.read_text(encoding="utf-8").replace('parent: "[[Child]]"', 'parent: "[[INDEX]]"'),
        encoding="utf-8",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert "docs/status-quo/Child.md: parent 'INDEX' does not link back to child 'Child'" in errors


def test_only_index_may_be_a_root_and_related_must_not_be_empty(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    child = write_note(tmp_path, "Child.md", note_id="child", title="Child")
    child.write_text(
        child.read_text(encoding="utf-8")
        .replace('parent: "[[Child]]"', "parent: []")
        .replace('related:\n  - "[[Child]]"', "related: []"),
        encoding="utf-8",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert "docs/status-quo/Child.md: only INDEX.md may declare parent: []" in errors
    assert "docs/status-quo/Child.md: frontmatter field 'related' must not be empty" in errors


def test_contract_ledger_must_equal_all_inventory_sections(tmp_path: Path) -> None:
    route_id = "route:GET:/api/example"
    unknown_id = "unknown:negative-probe"
    test_id = "test:backend/tests/test_example.py"
    write_inventory(
        tmp_path,
        routes=[{"id": route_id}],
        unknowns=[{"id": unknown_id}],
        tests=[{"id": test_id}],
    )
    inventory_path = tmp_path / "docs/map/inventory/inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory["schema_version"] = 1
    inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
    write_note(
        tmp_path,
        "INDEX.md",
        note_id="index",
        title="Index",
        body=f"{route_id}\n{unknown_id}\n{test_id}",
    )
    write_note(
        tmp_path,
        "40-traceability/Contract Coverage.md",
        note_id="contracts",
        title="Contract Coverage",
        kind="traceability",
        body=f"| Contract ID | Meaning |\n| --- | --- |\n| {route_id} | route |",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert f"contract ledger missing inventory id: {unknown_id}" in errors
    assert f"contract ledger missing inventory id: {test_id}" in errors


def test_capability_ledgers_must_equal_feature_frontmatter(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    feature = write_note(
        tmp_path,
        "10-features/Feature.md",
        note_id="feature",
        title="Feature",
        kind="feature",
        extra_frontmatter="""capability_ids:
  - TEST-01
delivery: implemented
reachability: user-facing
persistence: durable
evidence: code-and-tests""",
    )
    feature.write_text(
        feature.read_text(encoding="utf-8").replace('parent: "[[Feature]]"', 'parent: "[[INDEX]]"'),
        encoding="utf-8",
    )
    write_note(
        tmp_path,
        "INDEX.md",
        note_id="index",
        title="Index",
        body="Read [[Feature]].",
    )
    write_note(
        tmp_path,
        "40-traceability/Capability Ledger.md",
        note_id="capabilities",
        title="Capability Ledger",
        kind="traceability",
        body="| ID | Capability |\n| --- | --- |\n| `TEST-01` | covered |",
    )
    write_note(
        tmp_path,
        "40-traceability/Feature-to-Code Matrix.md",
        note_id="matrix",
        title="Feature-to-Code Matrix",
        kind="traceability",
        body="| ID | Code |\n| --- | --- |\n| `OTHER-01` | wrong |",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert "feature-to-code matrix missing capability id: TEST-01" in errors
    assert "feature-to-code matrix has unknown capability id: OTHER-01" in errors


def test_empty_feature_ownership_cannot_skip_capability_ledgers(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    for relative_path, note_id, title in (
        ("40-traceability/Capability Ledger.md", "capabilities", "Capability Ledger"),
        ("40-traceability/Feature-to-Code Matrix.md", "matrix", "Feature-to-Code Matrix"),
    ):
        write_note(
            tmp_path,
            relative_path,
            note_id=note_id,
            title=title,
            kind="traceability",
            body="| ID | Meaning |\n| --- | --- |\n| `TEST-01` | orphan |",
        )

    errors = CHECKER.check_corpus(tmp_path)

    assert "capability ledger has unknown capability id: TEST-01" in errors
    assert "feature-to-code matrix has unknown capability id: TEST-01" in errors


def test_current_capability_requires_a_technical_feature_link(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    write_note(
        tmp_path,
        "10-features/Feature.md",
        note_id="feature",
        title="Feature",
        kind="feature",
        extra_frontmatter="""capability_ids:
  - TEST-01
delivery: partial
reachability: user-facing
persistence: durable
evidence: code-and-tests""",
    )
    for relative_path, note_id, title in (
        ("40-traceability/Capability Ledger.md", "capabilities", "Capability Ledger"),
        ("40-traceability/Feature-to-Code Matrix.md", "matrix", "Feature-to-Code Matrix"),
    ):
        write_note(
            tmp_path,
            relative_path,
            note_id=note_id,
            title=title,
            kind="traceability",
            body="| ID | Meaning |\n| --- | --- |\n| `TEST-01` | covered |",
        )

    errors = CHECKER.check_corpus(tmp_path)

    assert "current capability has no technical feature_link: TEST-01" in errors


def test_ui_ledger_hashes_must_equal_client_route_registry(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(tmp_path, "INDEX.md", note_id="index", title="Index")
    ui_note = write_note(
        tmp_path,
        "40-traceability/UI Surface Coverage.md",
        note_id="ui",
        title="UI Surface Coverage",
        kind="traceability",
        body="""## Twelve destinations and hashes

| Destination | View key | Hash |
| --- | --- | --- |
| Dashboard | `dashboard` | `#/forms` |
| Forms | `forms` | `#/dashboard` |

## Other surfaces
""",
    )
    assert ui_note.is_file()
    client_source = tmp_path / "client/src/lib.jsx"
    client_source.parent.mkdir(parents=True)
    client_source.write_text(
        'const VIEW_HASH_PATHS = { dashboard: "dashboard", forms: "forms" };\n',
        encoding="utf-8",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert "UI surface ledger maps view 'dashboard' to '#/forms', expected '#/dashboard'" in errors
    assert "UI surface ledger maps view 'forms' to '#/dashboard', expected '#/forms'" in errors


def test_planned_only_feature_must_be_isolated_and_warned(tmp_path: Path) -> None:
    write_inventory(tmp_path)
    write_note(
        tmp_path,
        "10-features/Feature.md",
        note_id="planned",
        title="Planned",
        kind="feature",
        extra_frontmatter="""capability_ids: []
delivery: planned-only
reachability: not-applicable
persistence: none
evidence: historical-only""",
        body="This is a future idea.",
    )

    errors = CHECKER.check_corpus(tmp_path)

    assert any(
        "planned-only feature must live under Historical Intent" in error for error in errors
    )
    assert any(
        "planned-only feature requires an explicit warning callout" in error for error in errors
    )


def test_cli_allows_only_incomplete_inventory_coverage(tmp_path: Path) -> None:
    route_id = "route:GET:/api/example"
    write_inventory(tmp_path, routes=[{"id": route_id}])
    write_note(tmp_path, "INDEX.md", note_id="index", title="Index")

    strict = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    incomplete = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(tmp_path),
            "--allow-incomplete",
        ],
        capture_output=True,
        text=True,
    )

    assert strict.returncode == 1
    assert strict.stdout.splitlines() == [f"missing inventory reference: {route_id}"]
    assert incomplete.returncode == 0
    assert incomplete.stdout == ""

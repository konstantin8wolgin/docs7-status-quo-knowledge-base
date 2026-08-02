"""Validate the status-quo knowledge-base corpus."""

import argparse
import json
import re
import sys
from pathlib import Path

SNAPSHOT_COMMIT = "5448cf335e2cb25d74d6c0e6c476b72d1e14e803"
CORPUS_PATH = Path("docs/status-quo")
INVENTORY_PATH = Path("docs/map/inventory/inventory.json")

COMMON_FIELDS = (
    "id",
    "title",
    "kind",
    "status",
    "snapshot_commit",
    "last_verified",
    "tags",
    "parent",
    "related",
)
FEATURE_FIELDS = (
    "capability_ids",
    "delivery",
    "reachability",
    "persistence",
    "evidence",
)
TECHNICAL_FIELDS = ("map_pages", "inventory_refs", "feature_links")
LIST_FIELDS = {
    "tags",
    "related",
    "capability_ids",
    "map_pages",
    "inventory_refs",
    "feature_links",
}

ALLOWED_AXIS_VALUES = {
    "delivery": {"implemented", "partial", "prototype", "planned-only", "absent"},
    "reachability": {
        "user-facing",
        "development-only",
        "backend-only",
        "dead-or-unreachable",
        "not-applicable",
    },
    "persistence": {"durable", "session-memory", "ephemeral", "none"},
    "evidence": {"runtime-code-tests", "code-and-tests", "source-only", "historical-only"},
}
INVENTORY_SECTIONS = (
    "routes",
    "models",
    "jobs",
    "migrations",
    "client_methods",
    "unknowns",
    "tests",
)
YAML_NULL_VALUES = {"null", "Null", "NULL", "~"}
WIKILINK = re.compile(r"\[\[([^\[\]\n]+)\]\]")
LOCAL_MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)")
FRONTMATTER_FIELD = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$")
LIST_ITEM = re.compile(r"^\s*-\s+(.*?)\s*$")
BLOCKQUOTE_PREFIX = re.compile(r"^ {0,3}>[ \t]?")
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INVENTORY_ID_CHARACTER = r"A-Za-z0-9_./:{}-"
CAPABILITY_ID = re.compile(r"^[A-Z][A-Z0-9]*-\d+$")
TRACEABILITY_PATH = Path("docs/status-quo/40-traceability")
CONTRACT_LEDGER_PATH = TRACEABILITY_PATH / "Contract Coverage.md"
CAPABILITY_LEDGER_PATH = TRACEABILITY_PATH / "Capability Ledger.md"
FEATURE_MATRIX_PATH = TRACEABILITY_PATH / "Feature-to-Code Matrix.md"
UI_LEDGER_PATH = TRACEABILITY_PATH / "UI Surface Coverage.md"
CLIENT_ROUTE_PATH = Path("client/src/lib.jsx")


def _display_path(repo_root: Path, path: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _first_symlink(root: Path, relative_path: Path) -> Path | None:
    candidate = root
    for part in relative_path.parts:
        candidate /= part
        if candidate.is_symlink():
            return candidate
    return None


def _symlink_diagnostic(repo_root: Path, target: Path) -> str | None:
    symlink = _first_symlink(repo_root, target)
    if symlink is None:
        return None
    return (
        f"{target.as_posix()}: symlinked path component is not allowed: "
        f"{_display_path(repo_root, symlink)}"
    )


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_frontmatter(text: str) -> tuple[dict[str, object] | None, list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, ["missing frontmatter"]

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return None, ["unterminated frontmatter"]

    fields: dict[str, object] = {}
    errors: list[str] = []
    active_list: str | None = None
    for line_number, line in enumerate(lines[1:closing_index], start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        item_match = LIST_ITEM.match(line)
        if item_match:
            if active_list is None:
                errors.append(f"frontmatter line {line_number}: list item has no field")
                continue
            value = _unquote(item_match.group(1))
            current = fields[active_list]
            if isinstance(current, list):
                current.append(value)
            continue

        field_match = FRONTMATTER_FIELD.match(line)
        if field_match is None:
            errors.append(f"frontmatter line {line_number}: unsupported syntax")
            active_list = None
            continue

        key, raw_value = field_match.groups()
        if key in fields:
            errors.append(f"frontmatter line {line_number}: duplicate field '{key}'")
            active_list = None
            continue

        raw_value = (raw_value or "").strip()
        if not raw_value or raw_value == "[]":
            fields[key] = []
            active_list = key
        elif raw_value in YAML_NULL_VALUES:
            fields[key] = None
            active_list = None
        else:
            fields[key] = _unquote(raw_value)
            active_list = None

    return fields, errors


def _blockquote_content(line: str) -> tuple[int, str]:
    depth = 0
    while True:
        match = BLOCKQUOTE_PREFIX.match(line)
        if match is None:
            return depth, line
        depth += 1
        line = line[match.end() :]


def _is_fence_close(line: str, character: str, minimum_length: int) -> bool:
    match = re.fullmatch(r" {0,3}([`~]+)[ \t]*", line)
    if match is None:
        return False
    marker = match.group(1)
    return len(marker) >= minimum_length and set(marker) == {character}


def _without_fenced_code(text: str) -> str:
    visible_lines: list[str] = []
    fence: tuple[str, int, int] | None = None
    for line in text.splitlines():
        blockquote_depth, container_content = _blockquote_content(line)
        if fence is not None:
            fence_character, minimum_length, fence_blockquote_depth = fence
            if blockquote_depth >= fence_blockquote_depth:
                if blockquote_depth == fence_blockquote_depth and _is_fence_close(
                    container_content, fence_character, minimum_length
                ):
                    fence = None
                continue
            fence = None

        fence_match = FENCE_OPEN.match(container_content)
        if fence_match:
            marker = fence_match.group(1)
            fence = (marker[0], len(marker), blockquote_depth)
            continue
        visible_lines.append(line)
    return "\n".join(visible_lines)


def _required_fields_for(note_path: Path, corpus_root: Path) -> tuple[str, ...]:
    relative_parts = note_path.relative_to(corpus_root).parts
    if relative_parts and relative_parts[0] == "10-features":
        return COMMON_FIELDS + FEATURE_FIELDS
    if relative_parts and relative_parts[0] == "20-technical":
        return COMMON_FIELDS + TECHNICAL_FIELDS
    return COMMON_FIELDS


def _resolved_wikilink_path(
    target: str,
    source_path: Path,
    corpus_root: Path,
    note_paths: set[Path],
    notes_by_basename: dict[str, list[Path]],
) -> Path | None:
    target = target.split("|", 1)[0].strip()
    target = target.split("#", 1)[0].strip()
    if not target:
        return source_path

    target_path = Path(target)
    if target_path.suffix:
        return None

    relative_candidate = (source_path.parent / f"{target}.md").resolve()
    corpus_candidate = (corpus_root / f"{target}.md").resolve()
    if relative_candidate in note_paths or corpus_candidate in note_paths:
        return relative_candidate if relative_candidate in note_paths else corpus_candidate

    basename_matches = notes_by_basename.get(target_path.name, [])
    if len(basename_matches) == 1:
        return basename_matches[0]
    return None


def _resolve_wikilink(
    target: str,
    source_path: Path,
    corpus_root: Path,
    note_paths: set[Path],
    notes_by_basename: dict[str, list[Path]],
) -> str:
    normalized_target = target.split("|", 1)[0].strip().split("#", 1)[0].strip()
    if not normalized_target:
        return "resolved"
    if (
        _resolved_wikilink_path(target, source_path, corpus_root, note_paths, notes_by_basename)
        is not None
    ):
        return "resolved"
    basename = Path(normalized_target).name
    if len(notes_by_basename.get(basename, [])) > 1:
        return "ambiguous"
    return "unresolved"


def _frontmatter_wikilinks(value: object) -> list[str]:
    values = value if isinstance(value, list) else [value]
    links: list[str] = []
    for item in values:
        if not isinstance(item, str):
            continue
        links.extend(WIKILINK.findall(item))
    return links


def _table_first_column_ids(text: str) -> list[str]:
    ids: list[str] = []
    for line in _without_fenced_code(text).splitlines():
        if not line.startswith("|"):
            continue
        first_cell = line.split("|", 2)[1].strip()
        if len(first_cell) >= 2 and first_cell.startswith("`") and first_cell.endswith("`"):
            first_cell = first_cell[1:-1]
        if first_cell and ":" in first_cell and not re.search(r"\s", first_cell):
            ids.append(first_cell)
    return ids


def _table_first_column_capabilities(text: str) -> list[str]:
    values: list[str] = []
    for line in _without_fenced_code(text).splitlines():
        if not line.startswith("|"):
            continue
        first_cell = line.split("|", 2)[1].strip().strip("`")
        if CAPABILITY_ID.fullmatch(first_cell):
            values.append(first_cell)
    return values


def _capability_deliveries(text: str) -> dict[str, str]:
    deliveries: dict[str, str] = {}
    for line in _without_fenced_code(text).splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if (
            len(cells) >= 3
            and CAPABILITY_ID.fullmatch(cells[0])
            and cells[2] in ALLOWED_AXIS_VALUES["delivery"]
        ):
            deliveries[cells[0]] = cells[2]
    return deliveries


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _client_hash_paths(text: str) -> dict[str, str]:
    match = re.search(r"const\s+VIEW_HASH_PATHS\s*=\s*\{(.*?)\};", text, re.DOTALL)
    if match is None:
        return {}
    return {
        view_name: f"#/{slug}"
        for view_name, slug in re.findall(
            r"([A-Za-z_$][A-Za-z0-9_$]*)\s*:\s*[\"']([^\"']+)[\"']",
            match.group(1),
        )
    }


def _documented_ui_hashes(text: str) -> dict[str, str]:
    section = re.search(
        r"^## Twelve destinations and hashes\s*$\n(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if section is None:
        return {}
    mappings: dict[str, str] = {}
    for line in section.group(1).splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if (
            len(cells) >= 3
            and re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", cells[1])
            and re.fullmatch(r"\#/[A-Za-z0-9_-]+", cells[2])
        ):
            mappings[cells[1]] = cells[2]
    return mappings


def _inventory_ids(repo_root: Path) -> tuple[list[str], list[str]]:
    symlink_error = _symlink_diagnostic(repo_root, INVENTORY_PATH)
    if symlink_error is not None:
        return [], [symlink_error]

    inventory_path = repo_root / INVENTORY_PATH
    resolved_inventory = inventory_path.resolve()
    try:
        resolved_inventory.relative_to(repo_root)
    except ValueError:
        return [], [f"{INVENTORY_PATH.as_posix()}: inventory resolves outside the repository"]
    if not inventory_path.is_file():
        return [], [f"{INVENTORY_PATH.as_posix()}: missing inventory"]

    try:
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [f"{INVENTORY_PATH.as_posix()}: invalid inventory: {exc}"]
    if not isinstance(inventory, dict):
        return [], [f"{INVENTORY_PATH.as_posix()}: inventory root must be an object"]

    item_ids: list[str] = []
    errors: list[str] = []
    for section in INVENTORY_SECTIONS:
        items = inventory.get(section)
        if not isinstance(items, list):
            errors.append(f"{INVENTORY_PATH.as_posix()}: section '{section}' must be a list")
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
                errors.append(f"{INVENTORY_PATH.as_posix()}: {section}[{index}] has no string id")
                continue
            item_ids.append(item["id"])
    return sorted(set(item_ids)), errors


def _inventory_has_schema_contract(repo_root: Path) -> bool:
    try:
        inventory = json.loads((repo_root / INVENTORY_PATH).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(inventory, dict) and inventory.get("schema_version") == 1


def _contains_inventory_id(text: str, item_id: str) -> bool:
    pattern = re.compile(
        rf"(?<![{INVENTORY_ID_CHARACTER}])"
        rf"{re.escape(item_id)}"
        rf"(?![{INVENTORY_ID_CHARACTER}])"
    )
    return pattern.search(text) is not None


def _check_corpus(repo_root: Path, *, allow_incomplete: bool) -> list[str]:
    repo_root = Path(repo_root).resolve()
    symlink_error = _symlink_diagnostic(repo_root, CORPUS_PATH)
    if symlink_error is not None:
        return [symlink_error]

    corpus_path = repo_root / CORPUS_PATH
    if not corpus_path.is_dir():
        return [f"{CORPUS_PATH.as_posix()}: missing corpus directory"]
    corpus_root = corpus_path.resolve()
    try:
        corpus_root.relative_to(repo_root)
    except ValueError:
        return [f"{CORPUS_PATH.as_posix()}: corpus resolves outside the repository"]

    errors: list[str] = []
    note_paths: list[Path] = []
    for candidate in sorted(corpus_root.rglob("*.md")):
        display_path = _display_path(repo_root, candidate)
        candidate_relative = candidate.relative_to(corpus_root)
        symlink = _first_symlink(corpus_root, candidate_relative)
        if symlink is not None:
            if symlink == candidate:
                errors.append(f"{display_path}: symlinked note is not allowed")
            else:
                errors.append(
                    f"{display_path}: symlinked note path is not allowed: "
                    f"{_display_path(repo_root, symlink)}"
                )
            continue
        resolved_candidate = candidate.resolve()
        try:
            resolved_candidate.relative_to(corpus_root)
        except ValueError:
            errors.append(f"{display_path}: note resolves outside the corpus")
            continue
        if resolved_candidate.is_file():
            note_paths.append(resolved_candidate)
    if not note_paths:
        if errors:
            return sorted(errors)
        return [f"{CORPUS_PATH.as_posix()}: corpus contains no Markdown notes"]

    note_texts: dict[Path, str] = {}
    note_frontmatters: dict[Path, dict[str, object]] = {}
    notes_by_basename: dict[str, list[Path]] = {}
    ids: dict[str, list[Path]] = {}
    titles: dict[str, list[Path]] = {}
    capability_owners: dict[str, list[Path]] = {}
    capability_delivery: dict[str, str] = {}
    technical_feature_links: set[str] = set()

    for note_path in note_paths:
        display_path = _display_path(repo_root, note_path)
        try:
            text = note_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{display_path}: note is not valid UTF-8")
            continue
        except OSError:
            errors.append(f"{display_path}: unable to read note")
            continue
        note_texts[note_path] = text
        notes_by_basename.setdefault(note_path.stem, []).append(note_path)

        frontmatter, parse_errors = _parse_frontmatter(text)
        errors.extend(f"{display_path}: {error}" for error in parse_errors)
        if frontmatter is None:
            continue
        note_frontmatters[note_path] = frontmatter

        for field in _required_fields_for(note_path, corpus_root):
            if field not in frontmatter:
                errors.append(f"{display_path}: missing required frontmatter field '{field}'")
                continue
            value = frontmatter[field]
            if value is None:
                errors.append(f"{display_path}: frontmatter field '{field}' must not be null")
            elif field in LIST_FIELDS and not isinstance(value, list):
                errors.append(f"{display_path}: frontmatter field '{field}' must be a list")
            elif field == "parent" and not isinstance(value, str | list):
                errors.append(
                    f"{display_path}: frontmatter field 'parent' must be a wikilink or list"
                )
            elif field == "tags" and not value:
                errors.append(f"{display_path}: frontmatter field 'tags' must not be empty")
            elif field == "related" and not value:
                errors.append(f"{display_path}: frontmatter field 'related' must not be empty")
            elif field not in LIST_FIELDS and field != "parent" and not isinstance(value, str):
                errors.append(f"{display_path}: frontmatter field '{field}' must be a scalar")
            elif (
                field not in LIST_FIELDS
                and field != "parent"
                and isinstance(value, str)
                and not value.strip()
            ):
                errors.append(f"{display_path}: frontmatter field '{field}' must not be blank")

        note_id = frontmatter.get("id")
        if isinstance(note_id, str) and note_id:
            ids.setdefault(note_id, []).append(note_path)
        title = frontmatter.get("title")
        if isinstance(title, str) and title:
            titles.setdefault(title, []).append(note_path)

        snapshot_commit = frontmatter.get("snapshot_commit")
        if (
            isinstance(snapshot_commit, str)
            and snapshot_commit.strip()
            and snapshot_commit != SNAPSHOT_COMMIT
        ):
            errors.append(
                f"{display_path}: snapshot_commit must be {SNAPSHOT_COMMIT}, "
                f"got '{snapshot_commit}'"
            )

        status = frontmatter.get("status")
        if isinstance(status, str) and status.strip() and status != "current":
            errors.append(f"{display_path}: status must be 'current', got '{status}'")

        relative_parts = note_path.relative_to(corpus_root).parts
        if relative_parts and relative_parts[0] == "10-features":
            for axis, allowed_values in ALLOWED_AXIS_VALUES.items():
                value = frontmatter.get(axis)
                if isinstance(value, str) and value.strip() and value not in allowed_values:
                    errors.append(f"{display_path}: invalid {axis} value '{value}'")
            capability_ids = frontmatter.get("capability_ids")
            if isinstance(capability_ids, list):
                for capability_id in capability_ids:
                    if isinstance(capability_id, str) and capability_id:
                        capability_owners.setdefault(capability_id, []).append(note_path)
                        delivery = frontmatter.get("delivery")
                        if isinstance(delivery, str):
                            capability_delivery[capability_id] = delivery
            if frontmatter.get("delivery") == "planned-only":
                if "Historical Intent" not in relative_parts:
                    errors.append(
                        f"{display_path}: planned-only feature must live under Historical Intent"
                    )
                visible_text = _without_fenced_code(text).lower()
                if not re.search(r"\[!(?:warning|danger)\]", visible_text):
                    errors.append(
                        f"{display_path}: planned-only feature requires an explicit warning callout"
                    )
                if not re.search(r"\bnot\b.{0,80}\b(current|rebuild contract)\b", visible_text):
                    errors.append(
                        f"{display_path}: planned-only warning must deny "
                        "current/rebuild-contract status"
                    )
        elif relative_parts and relative_parts[0] == "20-technical":
            feature_links = frontmatter.get("feature_links")
            if isinstance(feature_links, list):
                technical_feature_links.update(
                    capability_id
                    for capability_id in feature_links
                    if isinstance(capability_id, str) and capability_id
                )

    for basename, paths in sorted(notes_by_basename.items()):
        if len(paths) > 1:
            locations = ", ".join(_display_path(repo_root, path) for path in paths)
            errors.append(f"duplicate note basename '{basename}': {locations}")
    for note_id, paths in sorted(ids.items()):
        if len(paths) > 1:
            locations = ", ".join(_display_path(repo_root, path) for path in paths)
            errors.append(f"duplicate id '{note_id}': {locations}")
    for title, paths in sorted(titles.items()):
        if len(paths) > 1:
            locations = ", ".join(_display_path(repo_root, path) for path in paths)
            errors.append(f"duplicate title '{title}': {locations}")
    for capability_id, paths in sorted(capability_owners.items()):
        distinct_paths = sorted(set(paths))
        if len(distinct_paths) > 1 or len(paths) > 1:
            locations = ", ".join(_display_path(repo_root, path) for path in paths)
            errors.append(f"duplicate capability id '{capability_id}': {locations}")

    resolved_note_paths = set(note_paths)
    for source_path, text in note_texts.items():
        display_path = _display_path(repo_root, source_path)
        visible_text = _without_fenced_code(text)
        for raw_target in WIKILINK.findall(visible_text):
            resolution = _resolve_wikilink(
                raw_target,
                source_path,
                corpus_root,
                resolved_note_paths,
                notes_by_basename,
            )
            if resolution != "resolved":
                target = raw_target.split("|", 1)[0].strip()
                errors.append(f"{display_path}: {resolution} wikilink '{target}'")

        for raw_target in LOCAL_MARKDOWN_LINK.findall(visible_text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_without_anchor = target.split("#", 1)[0]
            if not target_without_anchor.lower().endswith(".md"):
                continue
            candidate = (source_path.parent / target_without_anchor).resolve()
            try:
                candidate.relative_to(repo_root)
            except ValueError:
                errors.append(f"{display_path}: local Markdown link escapes repository '{target}'")
                continue
            if not candidate.is_file():
                errors.append(f"{display_path}: unresolved local Markdown link '{target}'")

        if re.search(r"(?im)^\s*(?:[-*]\s+)?(?:TODO|TBD|FIXME)(?:\b|:)", visible_text):
            errors.append(f"{display_path}: ambiguous authoring placeholder remains")

    for child_path, frontmatter in note_frontmatters.items():
        parent_value = frontmatter.get("parent")
        parent_links = _frontmatter_wikilinks(parent_value)
        if parent_value == []:
            if child_path.name != "INDEX.md":
                errors.append(
                    f"{_display_path(repo_root, child_path)}: only INDEX.md may declare parent: []"
                )
            continue
        child_display = _display_path(repo_root, child_path)
        if len(parent_links) != 1:
            errors.append(f"{child_display}: parent must contain exactly one wikilink or be []")
            continue
        raw_parent = parent_links[0]
        parent_path = _resolved_wikilink_path(
            raw_parent,
            child_path,
            corpus_root,
            resolved_note_paths,
            notes_by_basename,
        )
        if parent_path is None:
            continue
        parent_targets = WIKILINK.findall(_without_fenced_code(note_texts[parent_path]))
        links_back = any(
            _resolved_wikilink_path(
                target,
                parent_path,
                corpus_root,
                resolved_note_paths,
                notes_by_basename,
            )
            == child_path
            for target in parent_targets
        )
        if not links_back:
            parent_name = raw_parent.split("|", 1)[0].split("#", 1)[0].strip()
            errors.append(
                f"{child_display}: parent '{parent_name}' does not link back to child "
                f"'{child_path.stem}'"
            )

    inventory_ids, inventory_errors = _inventory_ids(repo_root)
    errors.extend(inventory_errors)
    if not allow_incomplete and not inventory_errors:
        visible_corpus = "\n".join(_without_fenced_code(text) for text in note_texts.values())
        for item_id in inventory_ids:
            if not _contains_inventory_id(visible_corpus, item_id):
                errors.append(f"missing inventory reference: {item_id}")

        if inventory_ids and _inventory_has_schema_contract(repo_root):
            contract_path = (repo_root / CONTRACT_LEDGER_PATH).resolve()
            contract_text = note_texts.get(contract_path)
            if contract_text is None:
                errors.append(f"{CONTRACT_LEDGER_PATH.as_posix()}: missing exact contract ledger")
            else:
                ledger_ids = _table_first_column_ids(contract_text)
                for duplicate in _duplicates(ledger_ids):
                    errors.append(f"contract ledger duplicates inventory id: {duplicate}")
                ledger_set = set(ledger_ids)
                inventory_set = set(inventory_ids)
                for item_id in sorted(inventory_set - ledger_set):
                    errors.append(f"contract ledger missing inventory id: {item_id}")
                for item_id in sorted(ledger_set - inventory_set):
                    errors.append(f"contract ledger has unknown inventory id: {item_id}")

    capability_ledger_present = (repo_root / CAPABILITY_LEDGER_PATH).resolve() in note_texts
    feature_matrix_present = (repo_root / FEATURE_MATRIX_PATH).resolve() in note_texts
    if not allow_incomplete and (
        capability_owners or capability_ledger_present or feature_matrix_present
    ):
        capability_set = set(capability_owners)
        for path, label in (
            (CAPABILITY_LEDGER_PATH, "capability ledger"),
            (FEATURE_MATRIX_PATH, "feature-to-code matrix"),
        ):
            resolved_path = (repo_root / path).resolve()
            ledger_text = note_texts.get(resolved_path)
            if ledger_text is None:
                errors.append(f"{path.as_posix()}: missing exact {label}")
                continue
            ledger_ids = _table_first_column_capabilities(ledger_text)
            if path == CAPABILITY_LEDGER_PATH:
                capability_delivery.update(_capability_deliveries(ledger_text))
            for duplicate in _duplicates(ledger_ids):
                errors.append(f"{label} duplicates capability id: {duplicate}")
            ledger_set = set(ledger_ids)
            for capability_id in sorted(capability_set - ledger_set):
                errors.append(f"{label} missing capability id: {capability_id}")
            for capability_id in sorted(ledger_set - capability_set):
                errors.append(f"{label} has unknown capability id: {capability_id}")

        for note_path, frontmatter in note_frontmatters.items():
            if note_path.relative_to(corpus_root).parts[0] != "20-technical":
                continue
            feature_links = frontmatter.get("feature_links")
            if not isinstance(feature_links, list):
                continue
            for capability_id in feature_links:
                if isinstance(capability_id, str) and capability_id not in capability_set:
                    errors.append(
                        f"{_display_path(repo_root, note_path)}: feature_links has unknown "
                        f"capability id '{capability_id}'"
                    )

        for capability_id in sorted(capability_set - technical_feature_links):
            if capability_delivery.get(capability_id) not in {"absent", "planned-only"}:
                errors.append(f"current capability has no technical feature_link: {capability_id}")

    client_route_path = repo_root / CLIENT_ROUTE_PATH
    if not allow_incomplete and client_route_path.is_file():
        ui_ledger_path = (repo_root / UI_LEDGER_PATH).resolve()
        ui_text = note_texts.get(ui_ledger_path)
        if ui_text is None:
            errors.append(f"{UI_LEDGER_PATH.as_posix()}: missing UI surface ledger")
        else:
            client_hashes = _client_hash_paths(client_route_path.read_text(encoding="utf-8"))
            documented_hashes = _documented_ui_hashes(ui_text)
            for view_name in sorted(client_hashes.keys() - documented_hashes.keys()):
                errors.append(f"UI surface ledger missing client view: {view_name}")
            for view_name in sorted(documented_hashes.keys() - client_hashes.keys()):
                errors.append(f"UI surface ledger has unknown client view: {view_name}")
            for view_name in sorted(client_hashes.keys() & documented_hashes.keys()):
                actual_hash = documented_hashes[view_name]
                expected_hash = client_hashes[view_name]
                if actual_hash != expected_hash:
                    errors.append(
                        f"UI surface ledger maps view '{view_name}' to '{actual_hash}', "
                        f"expected '{expected_hash}'"
                    )

    return sorted(errors)


def check_corpus(repo_root: Path) -> list[str]:
    """Return deterministic validation diagnostics for a complete corpus."""

    return _check_corpus(repo_root, allow_incomplete=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help="skip inventory coverage diagnostics while the corpus is being authored",
    )
    arguments = parser.parse_args(argv)

    errors = _check_corpus(arguments.repo_root, allow_incomplete=arguments.allow_incomplete)
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

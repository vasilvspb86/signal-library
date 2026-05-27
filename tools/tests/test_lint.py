from pathlib import Path

import pytest

from validate_signals.lint import lint_one


def _write(tmp_path: Path, name: str, frontmatter: str, body: str) -> Path:
    p = tmp_path / name
    p.write_text(f"---\n{frontmatter.strip()}\n---\n\n{body.strip()}\n", encoding="utf-8")
    return p


_GOOD_FM = """
id: foo-bar
name: Foo Bar
year: 2026
domain: Workplace
human_task: "How can I do X?"
existential_essence: "Do X."
compas_segment: 1
macrotrend: Fantomatica
diffusion_stage: Emerging
status: active
captured_at: 2026-05-27
verified_at: 2026-05-27
schema_version: 1
"""

_GOOD_BODY = """
# Foo Bar

> Subtitle line.

## Anti-hype marker
This breaks the norm of doing things the old way. Several sentences of substance about why this is genuinely different.

## FROM → TO
- **From:** Old way
- **To:** New way
"""


def test_valid_signal_no_warnings(tmp_path):
    p = _write(tmp_path, "foo-bar.md", _GOOD_FM, _GOOD_BODY)
    assert lint_one(p) == []


def test_warns_when_name_equals_slug(tmp_path):
    fm = _GOOD_FM.replace("name: Foo Bar", "name: foo-bar")
    body = _GOOD_BODY.replace("# Foo Bar", "# foo-bar")
    p = _write(tmp_path, "foo-bar.md", fm, body)
    warns = lint_one(p)
    assert any("name field is the slug" in w for w in warns)


def test_does_not_warn_when_name_is_proper_case_that_maps_to_slug(tmp_path):
    """'Foo Bar' lowercased + hyphenated == 'foo-bar', but that's still a valid display name."""
    # _GOOD_FM has name: Foo Bar and the file is foo-bar.md — this used to false-positive
    p = _write(tmp_path, "foo-bar.md", _GOOD_FM, _GOOD_BODY)
    warns = lint_one(p)
    assert not any("name field" in w for w in warns)


def test_warns_on_h1_name_mismatch(tmp_path):
    body = _GOOD_BODY.replace("# Foo Bar", "# Foo Baz")
    p = _write(tmp_path, "foo-bar.md", _GOOD_FM, body)
    warns = lint_one(p)
    assert any("H1" in w and "doesn't match name" in w for w in warns)


def test_warns_on_empty_bridge_map_placeholders(tmp_path):
    body = _GOOD_BODY + "\n## Bridge Map\n- [[]]\n- [[]]\n"
    p = _write(tmp_path, "foo-bar.md", _GOOD_FM, body)
    warns = lint_one(p)
    assert any("Bridge Map" in w and "empty [[]]" in w for w in warns)
    assert any("2 empty" in w for w in warns)


def test_warns_on_empty_string_may_fields(tmp_path):
    fm = _GOOD_FM + 'category: ""\nscope: ""\n'
    p = _write(tmp_path, "foo-bar.md", fm, _GOOD_BODY)
    warns = lint_one(p)
    assert any("category" in w and "scope" in w for w in warns)


def test_warns_on_anti_hype_too_long(tmp_path):
    long_antihype = "word " * 600
    body = _GOOD_BODY.replace(
        "This breaks the norm of doing things the old way. Several sentences of substance about why this is genuinely different.",
        long_antihype,
    )
    p = _write(tmp_path, "foo-bar.md", _GOOD_FM, body)
    warns = lint_one(p)
    assert any("anti-hype" in w and "too long" in w for w in warns)


def test_warns_on_anti_hype_too_short(tmp_path):
    body = _GOOD_BODY.replace(
        "This breaks the norm of doing things the old way. Several sentences of substance about why this is genuinely different.",
        "Brief.",
    )
    p = _write(tmp_path, "foo-bar.md", _GOOD_FM, body)
    warns = lint_one(p)
    assert any("anti-hype" in w and "very short" in w for w in warns)


def test_warns_on_human_task_without_question_mark(tmp_path):
    fm = _GOOD_FM.replace('human_task: "How can I do X?"', 'human_task: "How can I do X"')
    p = _write(tmp_path, "foo-bar.md", fm, _GOOD_BODY)
    warns = lint_one(p)
    assert any("human_task" in w and "?" in w for w in warns)


def test_warns_on_template_placeholder_in_body(tmp_path):
    body = _GOOD_BODY.replace(
        "- **From:** Old way",
        "- **From:** [old behavior / value logic]",
    )
    p = _write(tmp_path, "foo-bar.md", _GOOD_FM, body)
    warns = lint_one(p)
    assert any("template placeholder text" in w for w in warns)


def test_multiple_warnings_accumulate(tmp_path):
    """A signal with multiple issues gets multiple warnings."""
    fm = _GOOD_FM.replace("name: Foo Bar", "name: foo-bar")
    fm += 'category: ""\nscope: ""\n'
    body = _GOOD_BODY.replace("# Foo Bar", "# foo-bar")
    body += "\n## Bridge Map\n- [[]]\n"
    p = _write(tmp_path, "foo-bar.md", fm, body)
    warns = lint_one(p)
    # Should fire at least: name==slug, H1 mismatch (after we change # to # foo-bar but name is still Foo Bar? actually we changed both), empty MAY fields, empty bridge map
    assert len(warns) >= 3
    assert any("name field is the slug" in w for w in warns)
    assert any("empty [[]]" in w for w in warns)

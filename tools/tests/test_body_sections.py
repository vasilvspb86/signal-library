import pytest

from validate_signals.body_sections import (
    BodySectionError,
    check_body_sections,
)
from validate_signals.frontmatter import parse_signal_file


def test_valid_signal_passes(fixtures_dir):
    fm, body = parse_signal_file(fixtures_dir / "valid_signal.md")
    check_body_sections(fm, body)


def test_missing_subtitle_fails():
    fm = {}
    body = "# Title\n\n## Anti-hype marker\nx\n\n## FROM → TO\n- From: a\n- To: b\n"
    with pytest.raises(BodySectionError, match="subtitle"):
        check_body_sections(fm, body)


def test_missing_anti_hype_fails():
    fm = {}
    body = "# Title\n\n> Subtitle.\n\n## FROM → TO\n- From: a\n- To: b\n"
    with pytest.raises(BodySectionError, match="(?i)anti-hype"):
        check_body_sections(fm, body)


def test_body_missing_from_to_with_no_frontmatter_shift_fails(fixtures_dir):
    fm, body = parse_signal_file(fixtures_dir / "body_missing_from_to.md")
    with pytest.raises(BodySectionError, match="FROM"):
        check_body_sections(fm, body)


def test_frontmatter_from_to_alone_passes(fixtures_dir):
    fm, body = parse_signal_file(fixtures_dir / "frontmatter_from_to.md")
    check_body_sections(fm, body)


def test_one_shift_field_alone_fails():
    fm = {"shift_from": "old"}  # shift_to missing
    body = "# T\n\n> S.\n\n## Anti-hype marker\nn\n"
    with pytest.raises(BodySectionError, match="FROM"):
        check_body_sections(fm, body)

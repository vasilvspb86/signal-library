from pathlib import Path

import pytest

from validate_signals.frontmatter import ParseError, parse_signal_file


def test_parses_valid_signal(fixtures_dir):
    fm, body = parse_signal_file(fixtures_dir / "valid_signal.md")
    assert fm["id"] == "vergesense-occupancy"
    assert fm["compas_segment"] == 2
    assert fm["url"] == "https://vergesense.com"
    assert "Anti-hype marker" in body


def test_raises_on_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        parse_signal_file(tmp_path / "nonexistent.md")


def test_raises_on_no_frontmatter(tmp_path):
    p = tmp_path / "no_frontmatter.md"
    p.write_text("# Just a heading\n\nNo frontmatter here.", encoding="utf-8")
    with pytest.raises(ParseError, match="no frontmatter"):
        parse_signal_file(p)


def test_raises_on_malformed_yaml(tmp_path):
    p = tmp_path / "bad_yaml.md"
    p.write_text("---\nid: x\n  bad: : indent\n---\n\nbody", encoding="utf-8")
    with pytest.raises(ParseError, match="malformed YAML"):
        parse_signal_file(p)

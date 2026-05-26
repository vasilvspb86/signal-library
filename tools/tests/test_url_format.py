import pytest

from validate_signals.frontmatter import parse_signal_file
from validate_signals.url_format import URLFormatError, check_url_format


def test_valid_url_passes(fixtures_dir):
    fm, _ = parse_signal_file(fixtures_dir / "valid_signal.md")
    check_url_format(fm)


def test_no_url_passes(fixtures_dir):
    """url is MAY — signals can omit it (pattern signals)."""
    fm, _ = parse_signal_file(fixtures_dir / "pattern_signal_no_url.md")
    check_url_format(fm)


def test_empty_url_passes(fixtures_dir):
    """Empty url string treated as absent (consistent with template defaults)."""
    fm, _ = parse_signal_file(fixtures_dir / "missing_url_signal.md")
    fm["url"] = ""
    check_url_format(fm)


def test_bad_url_fails(fixtures_dir):
    fm, _ = parse_signal_file(fixtures_dir / "bad_url_format.md")
    with pytest.raises(URLFormatError, match="url"):
        check_url_format(fm)


def test_http_scheme_passes():
    fm = {"url": "http://example.com/path"}
    check_url_format(fm)


def test_https_scheme_passes():
    fm = {"url": "https://example.com/path"}
    check_url_format(fm)


def test_ftp_scheme_fails():
    fm = {"url": "ftp://example.com/file"}
    with pytest.raises(URLFormatError, match="scheme"):
        check_url_format(fm)

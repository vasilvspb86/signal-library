"""Validate the `url` field format when present.

`url` is MAY in the schema (spec §3.2) — signals describing observed patterns
may legitimately omit it. When present, it must be a syntactically valid
http(s) URL. Liveness checking (HTTP HEAD) happens at EVAL time per
EVAL Framework §3.A, not at commit time.
"""
from urllib.parse import urlparse


class URLFormatError(ValueError):
    """Raised when the `url` field is present but malformed."""


def check_url_format(fm: dict) -> None:
    """If `url` is present and non-empty, ensure it is a valid http(s) URL."""
    url = fm.get("url")
    if not url:
        return  # url is MAY; absence is valid

    if not isinstance(url, str):
        raise URLFormatError(f"url must be a string, got {type(url).__name__}")

    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https"):
        raise URLFormatError(
            f"url scheme must be http or https, got {parsed.scheme!r}"
        )
    if not parsed.netloc:
        raise URLFormatError(f"url has no host: {url!r}")

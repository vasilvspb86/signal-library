"""Read a signal markdown file and split into frontmatter dict + body string."""
from pathlib import Path

import frontmatter
import yaml


class ParseError(ValueError):
    """Raised when a signal file cannot be parsed."""


def parse_signal_file(path: Path) -> tuple[dict, str]:
    """Parse a signal markdown file.

    Returns (frontmatter_dict, body_text).
    Raises FileNotFoundError if path does not exist.
    Raises ParseError if frontmatter is missing or YAML is malformed.
    """
    if not path.exists():
        raise FileNotFoundError(f"signal file not found: {path}")

    raw = path.read_text(encoding="utf-8")

    if not raw.lstrip().startswith("---"):
        raise ParseError(f"no frontmatter in {path}")

    try:
        post = frontmatter.loads(raw)
    except yaml.YAMLError as e:
        raise ParseError(f"malformed YAML in {path}: {e}") from e

    if not post.metadata:
        raise ParseError(f"no frontmatter in {path}")

    return post.metadata, post.content

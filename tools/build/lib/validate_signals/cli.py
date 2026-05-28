"""Pre-commit hook entry point. Validates one or more signal files.

Usage:
  python -m validate_signals.cli signals/active/foo.md [more.md ...] \
    [--taxonomy signals/_taxonomy.yml]

Exit codes:
  0 — all files valid (or no files given)
  1 — at least one file failed validation
"""
import argparse
import sys
from pathlib import Path

from .body_sections import BodySectionError, check_body_sections
from .frontmatter import ParseError, parse_signal_file
from .must_fields import MustFieldError, check_must_fields
from .taxonomy import TaxonomyError, check_taxonomy, load_taxonomy
from .url_format import URLFormatError, check_url_format


def validate_one(path: Path, taxonomy: dict) -> list[str]:
    """Validate a single signal file. Returns a list of error messages (empty on success)."""
    errors: list[str] = []
    try:
        fm, body = parse_signal_file(path)
    except (ParseError, FileNotFoundError) as e:
        return [str(e)]

    for check, exc in (
        (lambda: check_must_fields(fm), MustFieldError),
        (lambda: check_taxonomy(fm, taxonomy), TaxonomyError),
        (lambda: check_body_sections(fm, body), BodySectionError),
        (lambda: check_url_format(fm), URLFormatError),
    ):
        try:
            check()
        except exc as e:
            errors.append(str(e))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Signal Library markdown files."
    )
    parser.add_argument(
        "files", nargs="*", type=Path,
        help="Signal markdown files to validate."
    )
    parser.add_argument(
        "--taxonomy", type=Path,
        default=Path("signals/_taxonomy.yml"),
        help="Path to taxonomy YAML (default: signals/_taxonomy.yml)"
    )
    args = parser.parse_args()

    # Only validate files under signals/active/ — drafts in _inbox/ are exempt.
    files = [
        f for f in args.files
        if "active" in f.parts and "signals" in f.parts
    ]
    if not files:
        return 0

    try:
        tax = load_taxonomy(args.taxonomy)
    except FileNotFoundError:
        print(f"taxonomy not found: {args.taxonomy}", file=sys.stderr)
        return 1

    any_failed = False
    for path in files:
        errs = validate_one(path, tax)
        if errs:
            any_failed = True
            for e in errs:
                print(f"FAIL  {path}: {e}", file=sys.stderr)
        else:
            print(f"PASS  {path}")

    return 1 if any_failed else 0


if __name__ == "__main__":
    sys.exit(main())

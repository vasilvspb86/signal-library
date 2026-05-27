"""Soft quality lint for signal markdown files.

Warnings only — never blocks a push. Catches the soft issues the hard
validator (validate_signals.cli) doesn't check: stylistic, content-shape,
and "template defaults still present" mistakes.

Usage:
  python -m validate_signals.lint signals/active/*.md
"""
import argparse
import re
import sys
from pathlib import Path

from .frontmatter import ParseError, parse_signal_file

_H1_RE = re.compile(r"^# (.+?)$", re.MULTILINE)
_BODY_FROM_RE = re.compile(r"##\s*FROM\s*[→\-]+\s*TO[\s\S]*?(?:\*\*From:\*\*|From:)\s*(.+?)$", re.MULTILINE | re.IGNORECASE)
_BODY_TO_RE = re.compile(r"##\s*FROM\s*[→\-]+\s*TO[\s\S]*?(?:\*\*To:\*\*|To:)\s*(.+?)$", re.MULTILINE | re.IGNORECASE)
_ANTIHYPE_RE = re.compile(r"##\s*Anti-?hype[\s\S]*?\n([\s\S]*?)(?=\n##|\Z)", re.IGNORECASE)

# Template-default placeholder snippets to flag
_PLACEHOLDER_SNIPPETS = [
    "[old behavior / value logic]",
    "[new behavior / emerging norm]",
    "[One-line subtitle capturing the shift",
    "[What norm does this break",
]

_OPTIONAL_STR_FIELDS = (
    "url", "location", "category", "scope", "source_channel",
    "shift_from", "shift_to", "trend", "microtrend", "next",
    "existential_essence",  # required, included to catch placeholder strings
)


def _first_h1(body: str) -> str | None:
    m = _H1_RE.search(body)
    return m.group(1).strip() if m else None


def _extract_antihype(body: str) -> str:
    m = _ANTIHYPE_RE.search(body)
    return m.group(1).strip() if m else ""


def lint_one(path: Path) -> list[str]:
    """Run all soft checks on one signal. Returns list of warning messages."""
    try:
        fm, body = parse_signal_file(path)
    except (ParseError, FileNotFoundError) as e:
        return [f"parse error (run validate first): {e}"]

    warnings: list[str] = []
    slug = path.stem

    # 1. name field is literally the slug (curator pasted the filename)
    name = fm.get("name", "") or ""
    if name and name == slug:
        warnings.append(
            "name field is the slug — use a human-readable display name "
            "(e.g., 'Quantum Entanglement in Brain Myelin' instead of "
            "'quantum-entanglement-in-brain-myelin')"
        )

    # 2. H1 doesn't match name field
    h1 = _first_h1(body)
    if h1 and name and h1 != name:
        warnings.append(
            f'H1 "{h1}" doesn\'t match name field "{name}" — they should be identical'
        )

    # 3. Bridge Map has empty [[]] placeholders
    empty_bridges = body.count("[[]]")
    if empty_bridges > 0:
        warnings.append(
            f"Bridge Map has {empty_bridges} empty [[]] placeholder(s) — "
            "fill them with related signal IDs or remove the section"
        )

    # 4. MAY fields set to empty string (template default)
    empty_may = [
        f for f in _OPTIONAL_STR_FIELDS
        if isinstance(fm.get(f), str) and fm.get(f) == ""
    ]
    if empty_may:
        warnings.append(
            f"fields set to empty string (omit them or fill them): {', '.join(empty_may)}"
        )

    # 5. Anti-hype too long (>500 words = pasted abstract)
    antihype = _extract_antihype(body)
    ah_words = len(antihype.split())
    if ah_words > 500:
        warnings.append(
            f"anti-hype marker is {ah_words} words — too long; may be a pasted "
            "abstract or paper excerpt. Aim for 2-3 sentences articulating what "
            "norm the signal breaks."
        )

    # 6. Anti-hype too short (<30 chars = single fragment)
    if 0 < len(antihype) < 30:
        warnings.append(
            "anti-hype marker is very short — articulate what norm the signal breaks "
            "in 2-3 sentences, not a single phrase"
        )

    # 7. human_task doesn't end with '?'
    ht = (fm.get("human_task") or "").rstrip()
    if ht and not ht.endswith("?"):
        warnings.append("human_task doesn't end with '?' — should be a question")

    # 8. Template placeholder snippets still in body
    placeholders_found = [p for p in _PLACEHOLDER_SNIPPETS if p in body]
    if placeholders_found:
        warnings.append(
            f"body contains template placeholder text — replace before saving: "
            f"{placeholders_found[0][:50]}…"
        )

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Soft quality lint for Signal Library files (warnings only)."
    )
    parser.add_argument(
        "files", nargs="*", type=Path,
        help="Signal markdown files to lint."
    )
    args = parser.parse_args()

    # Scope to active/ files (consistent with the hard validator)
    files = [
        f for f in args.files
        if "active" in f.parts and "signals" in f.parts
    ]
    if not files:
        return 0

    total_warnings = 0
    for path in files:
        warns = lint_one(path)
        if warns:
            print(f"\n{path}")
            for w in warns:
                print(f"  WARN  {w}")
                total_warnings += 1

    if total_warnings == 0:
        print(f"lint: no warnings across {len(files)} file(s)")
    else:
        print(f"\nlint: {total_warnings} warning(s) across {len(files)} file(s) (non-blocking)")

    # Always exit 0 — lint is advisory, never blocks
    return 0


if __name__ == "__main__":
    sys.exit(main())

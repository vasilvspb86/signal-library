"""Validate the markdown body of a signal file.

Required body content:
  - One-line subtitle (a blockquote `> ...` after the H1)
  - `## Anti-hype marker` section (non-empty)
  - FROM → TO: satisfied by EITHER a `## FROM → TO` body section OR both
    `shift_from` and `shift_to` frontmatter fields filled.
"""
import re


class BodySectionError(ValueError):
    """Raised when a body section requirement is not met."""


_SUBTITLE_RE = re.compile(r"^# .+?\n+>\s*\S", re.MULTILINE | re.DOTALL)
_ANTI_HYPE_RE = re.compile(
    r"##\s*Anti-?hype[\s\S]*?\n[\s\S]*?(?=\n##|\Z)",
    re.IGNORECASE,
)
_FROM_TO_RE = re.compile(
    r"##\s*FROM\s*[→\-]+\s*TO[\s\S]*?(?:\*\*From:\*\*|From:)[\s\S]*?(?:\*\*To:\*\*|To:)",
    re.IGNORECASE,
)


def _has_subtitle(body: str) -> bool:
    return bool(_SUBTITLE_RE.search(body))


def _has_antihype(body: str) -> bool:
    match = _ANTI_HYPE_RE.search(body)
    if not match:
        return False
    # Section must have some non-trivial content (not just heading)
    section = match.group(0)
    lines_after_heading = section.split("\n", 1)[1].strip() if "\n" in section else ""
    return len(lines_after_heading) > 0


def _has_from_to(fm: dict, body: str) -> bool:
    # EITHER frontmatter pair, OR body section
    sf = (fm.get("shift_from") or "").strip()
    st = (fm.get("shift_to") or "").strip()
    if sf and st:
        return True
    return bool(_FROM_TO_RE.search(body))


def check_body_sections(fm: dict, body: str) -> None:
    """Validate required body sections + FROM→TO either-form rule.

    Raises BodySectionError if:
      - No subtitle (a `> ...` line right after the H1)
      - No `## Anti-hype marker` section with content
      - No FROM → TO in either form (body section or frontmatter pair)
    """
    errors = []
    if not _has_subtitle(body):
        errors.append("missing subtitle (a `> ...` blockquote after H1)")
    if not _has_antihype(body):
        errors.append("missing or empty `## Anti-hype marker` section")
    if not _has_from_to(fm, body):
        errors.append(
            "missing FROM → TO: provide either a `## FROM → TO` body section "
            "or both `shift_from` and `shift_to` frontmatter fields"
        )
    if errors:
        raise BodySectionError("; ".join(errors))

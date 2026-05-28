"""Verify all 12 MUST fields are present and non-blank in a signal's frontmatter."""

MUST_FIELDS: tuple[str, ...] = (
    "id",
    "name",
    "year",
    "domain",
    "human_task",
    "existential_essence",
    "compas_segment",
    "macrotrend",
    "diffusion_stage",
    "status",
    "captured_at",
    "verified_at",
)


class MustFieldError(ValueError):
    """Raised when one or more MUST fields are missing or blank."""


def check_must_fields(fm: dict) -> None:
    """Raise MustFieldError if any MUST field is missing, None, or blank string.

    Note: `url` is intentionally MAY, not MUST (spec §3.2). Signals describing
    observed patterns may have no URL.
    """
    missing = []
    for field in MUST_FIELDS:
        value = fm.get(field)
        if value is None:
            missing.append(field)
        elif isinstance(value, str) and value.strip() == "":
            missing.append(field)
    if missing:
        raise MustFieldError(
            f"MUST fields missing or blank: {', '.join(missing)}"
        )

"""Validate a signal's frontmatter against the controlled taxonomy."""
from pathlib import Path

import yaml


class TaxonomyError(ValueError):
    """Raised when frontmatter violates the controlled vocabulary."""


def load_taxonomy(path: Path) -> dict:
    """Load taxonomy YAML from disk."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_taxonomy(fm: dict, tax: dict) -> None:
    """Validate that frontmatter values are in the controlled vocab.

    Checks:
      - domain ∈ tax['domains']
      - compas_segment ∈ 1..8 (keys of tax['compas_segments'])
      - macrotrend ∈ that segment's macrotrends list
      - diffusion_stage ∈ tax['diffusion_stages']
      - schema_version == tax['schema_version']
    """
    expected_version = tax.get("schema_version")
    if fm.get("schema_version") != expected_version:
        raise TaxonomyError(
            f"schema_version mismatch: got {fm.get('schema_version')!r}, "
            f"expected {expected_version!r}"
        )

    domain = fm.get("domain")
    if domain not in tax["domains"]:
        raise TaxonomyError(
            f"domain {domain!r} not in taxonomy. Allowed: {tax['domains']}"
        )

    segment = fm.get("compas_segment")
    if segment not in tax["compas_segments"]:
        raise TaxonomyError(
            f"compas_segment {segment!r} not in 1..{max(tax['compas_segments'])}"
        )

    macrotrend = fm.get("macrotrend")
    segment_macrotrends = tax["compas_segments"][segment]["macrotrends"]
    if macrotrend not in segment_macrotrends:
        raise TaxonomyError(
            f"macrotrend {macrotrend!r} not valid for segment {segment} "
            f"(name={tax['compas_segments'][segment]['name']}). "
            f"Allowed: {segment_macrotrends}"
        )

    diffusion = fm.get("diffusion_stage")
    if diffusion not in tax["diffusion_stages"]:
        raise TaxonomyError(
            f"diffusion_stage {diffusion!r} not in taxonomy. "
            f"Allowed: {tax['diffusion_stages']}"
        )

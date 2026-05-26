import pytest

from validate_signals.frontmatter import parse_signal_file
from validate_signals.taxonomy import (
    TaxonomyError,
    check_taxonomy,
    load_taxonomy,
)


def test_loads_taxonomy(taxonomy_path):
    tax = load_taxonomy(taxonomy_path)
    assert "Workplace" in tax["domains"]
    assert tax["compas_segments"][1]["name"] == "Self-care"
    assert "Emerging" in tax["diffusion_stages"]


def test_valid_signal_passes(fixtures_dir, taxonomy_path):
    fm, _ = parse_signal_file(fixtures_dir / "valid_signal.md")
    tax = load_taxonomy(taxonomy_path)
    check_taxonomy(fm, tax)


def test_invalid_domain_fails(fixtures_dir, taxonomy_path):
    fm, _ = parse_signal_file(fixtures_dir / "invalid_domain_signal.md")
    tax = load_taxonomy(taxonomy_path)
    with pytest.raises(TaxonomyError, match="domain"):
        check_taxonomy(fm, tax)


def test_invalid_segment_fails(fixtures_dir, taxonomy_path):
    fm, _ = parse_signal_file(fixtures_dir / "invalid_segment_signal.md")
    tax = load_taxonomy(taxonomy_path)
    with pytest.raises(TaxonomyError, match="compas_segment"):
        check_taxonomy(fm, tax)


def test_macrotrend_must_match_segment(taxonomy_path):
    # Segment 1 (Self-care) has Fantomatica, but NOT Ambient Intelligence
    fm = {
        "id": "x", "name": "x", "year": 2024,
        "domain": "Workplace", "human_task": "?",
        "existential_essence": "e",
        "compas_segment": 1,
        "macrotrend": "Ambient Intelligence",  # belongs to segment 2, not 1
        "diffusion_stage": "Emerging",
        "status": "active",
        "captured_at": "2026-05-22", "verified_at": "2026-05-22",
        "schema_version": 1,
    }
    tax = load_taxonomy(taxonomy_path)
    with pytest.raises(TaxonomyError, match="macrotrend"):
        check_taxonomy(fm, tax)


def test_invalid_diffusion_stage_fails(taxonomy_path):
    fm = {
        "id": "x", "name": "x", "year": 2024,
        "domain": "Workplace", "human_task": "?",
        "existential_essence": "e",
        "compas_segment": 1, "macrotrend": "Fantomatica",
        "diffusion_stage": "Trending",  # not in vocab
        "status": "active",
        "captured_at": "2026-05-22", "verified_at": "2026-05-22",
        "schema_version": 1,
    }
    tax = load_taxonomy(taxonomy_path)
    with pytest.raises(TaxonomyError, match="diffusion_stage"):
        check_taxonomy(fm, tax)


def test_schema_version_must_match(taxonomy_path):
    fm = {
        "id": "x", "name": "x", "year": 2024,
        "domain": "Workplace", "human_task": "?",
        "existential_essence": "e",
        "compas_segment": 1, "macrotrend": "Fantomatica",
        "diffusion_stage": "Emerging",
        "status": "active",
        "captured_at": "2026-05-22", "verified_at": "2026-05-22",
        "schema_version": 99,  # wrong version
    }
    tax = load_taxonomy(taxonomy_path)
    with pytest.raises(TaxonomyError, match="schema_version"):
        check_taxonomy(fm, tax)

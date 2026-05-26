import pytest

from validate_signals.frontmatter import parse_signal_file
from validate_signals.must_fields import (
    MUST_FIELDS,
    MustFieldError,
    check_must_fields,
)


def test_must_fields_set_is_12():
    assert len(MUST_FIELDS) == 12
    assert "url" not in MUST_FIELDS               # url is MAY per spec §3.2
    assert "existential_essence" in MUST_FIELDS   # essence is MUST per spec §3.2


def test_valid_signal_passes(fixtures_dir):
    fm, _ = parse_signal_file(fixtures_dir / "valid_signal.md")
    check_must_fields(fm)  # no exception


def test_missing_essence_fails(fixtures_dir):
    fm, _ = parse_signal_file(fixtures_dir / "missing_essence_signal.md")
    with pytest.raises(MustFieldError, match="existential_essence"):
        check_must_fields(fm)


def test_missing_url_passes_because_url_is_may(fixtures_dir):
    fm, _ = parse_signal_file(fixtures_dir / "missing_url_signal.md")
    check_must_fields(fm)  # no exception


def test_missing_id_fails():
    fm = {
        "name": "x", "year": 2024, "domain": "Workplace",
        "human_task": "?", "existential_essence": "e",
        "compas_segment": 1, "macrotrend": "Fantomatica",
        "diffusion_stage": "Emerging", "status": "active",
        "captured_at": "2026-05-22", "verified_at": "2026-05-22",
        "schema_version": 1,
    }
    with pytest.raises(MustFieldError, match="id"):
        check_must_fields(fm)


def test_blank_string_counts_as_missing():
    fm = {f: "v" for f in [
        "id","name","domain","human_task","existential_essence","macrotrend",
        "diffusion_stage","status","captured_at","verified_at",
    ]}
    fm["year"] = 2024
    fm["compas_segment"] = 1
    fm["schema_version"] = 1
    fm["human_task"] = ""  # blank string
    with pytest.raises(MustFieldError, match="human_task"):
        check_must_fields(fm)

from pathlib import Path

import pytest

from signal_library.load import Signal, load_active_signals


@pytest.fixture
def populated_vault(tmp_path, fixtures_dir):
    """Build a fake vault with 3 active signals + 1 retired (should be ignored)."""
    active = tmp_path / "signals" / "active"
    retired = tmp_path / "signals" / "_retired"
    active.mkdir(parents=True)
    retired.mkdir(parents=True)
    for f in ["valid_signal.md", "missing_url_signal.md", "pattern_signal_no_url.md"]:
        (active / f).write_text(
            (fixtures_dir / f).read_text(encoding="utf-8"), encoding="utf-8"
        )
    # Retired signal — must NOT be loaded.
    (retired / "old.md").write_text(
        (fixtures_dir / "valid_signal.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return tmp_path


def test_loads_all_active_signals(populated_vault):
    signals = load_active_signals(populated_vault)
    assert len(signals) == 3
    assert all(isinstance(s, Signal) for s in signals)


def test_does_not_load_retired_signals(populated_vault):
    signals = load_active_signals(populated_vault)
    ids = {s.id for s in signals}
    assert all("old" not in i for i in ids)


def test_loads_url_when_present(populated_vault):
    signals = load_active_signals(populated_vault)
    by_id = {s.id: s for s in signals}
    assert by_id["vergesense-occupancy"].url == "https://vergesense.com"


def test_loads_signal_without_url(populated_vault):
    signals = load_active_signals(populated_vault)
    by_id = {s.id: s for s in signals}
    assert by_id["pattern-observation"].url is None


def test_signal_carries_body(populated_vault):
    signals = load_active_signals(populated_vault)
    by_id = {s.id: s for s in signals}
    assert "Anti-hype marker" in by_id["vergesense-occupancy"].body


def test_empty_vault_returns_empty_list(tmp_path):
    (tmp_path / "signals" / "active").mkdir(parents=True)
    assert load_active_signals(tmp_path) == []

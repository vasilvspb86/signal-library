from signal_library.domain_match import matches_brief_domain
from signal_library.load import Signal


def _sig(domain: str, cross: list[str] | None = None) -> Signal:
    return Signal(
        id="x", name="x", year=2024, domain=domain,
        human_task="?", existential_essence="e",
        compas_segment=1, macrotrend="Fantomatica",
        diffusion_stage="Emerging", status="active",
        captured_at="2026-05-22", verified_at="2026-05-22",
        body="", cross_industry=(cross or []),
    )


def test_exact_domain_match():
    assert matches_brief_domain("Workplace", _sig("Workplace"))


def test_domain_mismatch():
    assert not matches_brief_domain("Health", _sig("Workplace"))


def test_cross_industry_match():
    """A Workplace signal with cross_industry=[Retail] matches a Retail brief."""
    s = _sig("Workplace", cross=["Retail", "Hospitality"])
    assert matches_brief_domain("Retail", s)


def test_cross_industry_no_match():
    s = _sig("Workplace", cross=["Retail"])
    assert not matches_brief_domain("Health", s)

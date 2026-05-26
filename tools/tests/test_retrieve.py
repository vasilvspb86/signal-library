from signal_library.load import Signal
from signal_library.retrieve import Brief, RetrievalResult, retrieve_signals


def _sig(id_: str, domain: str, stage: str, cross: list | None = None) -> Signal:
    return Signal(
        id=id_, name=id_, year=2024, domain=domain,
        human_task="?", existential_essence="e",
        compas_segment=1, macrotrend="Fantomatica",
        diffusion_stage=stage, status="active",
        captured_at="2026-05-22", verified_at="2026-05-22",
        body="", cross_industry=(cross or []),
    )


def test_filters_by_domain():
    pool = [_sig("a", "Workplace", "Innovator"), _sig("b", "Health", "Innovator")]
    brief = Brief(industry="Workplace")
    out = retrieve_signals(brief, pool, k=5)
    assert {s.id for s in out.signals} == {"a"}


def test_excludes_mainstream():
    pool = [
        _sig("a", "Workplace", "Innovator"),
        _sig("b", "Workplace", "Mainstream"),
        _sig("c", "Workplace", "Early Adopter"),
    ]
    brief = Brief(industry="Workplace")
    out = retrieve_signals(brief, pool, k=5)
    assert {s.id for s in out.signals} == {"a", "c"}


def test_returns_top_k_when_more_than_k():
    pool = [_sig(f"s{i}", "Workplace", "Innovator") for i in range(10)]
    brief = Brief(industry="Workplace")
    out = retrieve_signals(brief, pool, k=3)
    assert len(out.signals) == 3


def test_flags_for_web_fallback_when_less_than_3():
    pool = [_sig("a", "Workplace", "Innovator")]
    brief = Brief(industry="Workplace")
    out = retrieve_signals(brief, pool, k=5)
    assert out.needs_web_fallback is True


def test_does_not_flag_for_web_fallback_when_3_or_more():
    pool = [_sig(f"s{i}", "Workplace", "Innovator") for i in range(5)]
    brief = Brief(industry="Workplace")
    out = retrieve_signals(brief, pool, k=5)
    assert out.needs_web_fallback is False


def test_cross_industry_signal_matches():
    pool = [_sig("a", "Workplace", "Innovator", cross=["Retail"])]
    brief = Brief(industry="Retail")
    out = retrieve_signals(brief, pool, k=5)
    assert {s.id for s in out.signals} == {"a"}

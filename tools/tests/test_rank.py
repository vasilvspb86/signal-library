from signal_library.load import Signal
from signal_library.rank import RankClient, rank_signals


class _MockLLM:
    """Mock LLM that returns IDs in a configured order."""

    def __init__(self, order: list[str]):
        self.order = order
        self.last_call: dict | None = None

    def rank(self, brief_text: str, candidates: list[Signal]) -> list[str]:
        self.last_call = {"brief": brief_text, "candidates": [c.id for c in candidates]}
        return self.order


def _sig(id_: str) -> Signal:
    return Signal(
        id=id_, name=id_, year=2024, domain="Workplace",
        human_task="?", existential_essence="e",
        compas_segment=1, macrotrend="Fantomatica",
        diffusion_stage="Innovator", status="active",
        captured_at="2026-05-22", verified_at="2026-05-22",
        body="",
    )


def test_skips_llm_when_5_or_fewer():
    """When candidate set is ≤5, no LLM call (spec §5.1 step 4)."""
    pool = [_sig(f"s{i}") for i in range(5)]
    mock = _MockLLM(order=[])
    out = rank_signals("brief text", pool, llm=mock)
    assert out == pool
    assert mock.last_call is None  # not called


def test_calls_llm_when_more_than_5():
    pool = [_sig(f"s{i}") for i in range(8)]
    mock = _MockLLM(order=["s3", "s0", "s5", "s7", "s1", "s2", "s4", "s6"])
    out = rank_signals("brief text", pool, llm=mock)
    assert [s.id for s in out] == ["s3", "s0", "s5", "s7", "s1", "s2", "s4", "s6"]
    assert mock.last_call is not None


def test_drops_unknown_ids_from_llm_response():
    """If LLM hallucinates an unknown ID, it's dropped silently."""
    pool = [_sig(f"s{i}") for i in range(6)]
    mock = _MockLLM(order=["s1", "fake-id", "s3", "s0", "s2", "s4", "s5"])
    out = rank_signals("brief text", pool, llm=mock)
    assert [s.id for s in out] == ["s1", "s3", "s0", "s2", "s4", "s5"]


def test_appends_unranked_signals_at_end():
    """If LLM omits some IDs, they get appended (preserving completeness)."""
    pool = [_sig(f"s{i}") for i in range(6)]
    mock = _MockLLM(order=["s2", "s0"])  # omits s1, s3, s4, s5
    out = rank_signals("brief text", pool, llm=mock)
    assert out[0].id == "s2"
    assert out[1].id == "s0"
    assert {s.id for s in out} == {"s0", "s1", "s2", "s3", "s4", "s5"}

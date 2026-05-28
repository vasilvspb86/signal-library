"""LLM-as-ranker for the candidate signal set.

Per spec §5.1 step 4:
- ≤5 candidates → no LLM call, return as-is.
- >5 candidates → call LLM to reorder by relevance to brief.

The LLM client is an injectable interface, so the library doesn't depend on
any specific provider. Pipeline code wires in a Claude/GPT client at runtime.
"""
from typing import Protocol

from .load import Signal


class RankClient(Protocol):
    """Anything that can rank candidate signal IDs given a brief is acceptable."""

    def rank(self, brief_text: str, candidates: list[Signal]) -> list[str]:
        """Return signal IDs in best-to-worst relevance order."""
        ...


_RANK_THRESHOLD = 5


def rank_signals(brief_text: str, candidates: list[Signal], llm: RankClient) -> list[Signal]:
    """Return candidates reordered by relevance to brief.

    If len(candidates) ≤ 5, returns candidates unchanged (no LLM call).
    Otherwise, asks the LLM for a ranking.

    Robustness:
      - Unknown IDs in LLM response are dropped.
      - Signals omitted by the LLM are appended at the end in original order.
    """
    if len(candidates) <= _RANK_THRESHOLD:
        return list(candidates)

    by_id = {s.id: s for s in candidates}
    ranked_ids = llm.rank(brief_text, candidates)

    seen: set[str] = set()
    ordered: list[Signal] = []
    for rid in ranked_ids:
        if rid in by_id and rid not in seen:
            ordered.append(by_id[rid])
            seen.add(rid)

    # Append any signal the LLM forgot
    for s in candidates:
        if s.id not in seen:
            ordered.append(s)

    return ordered

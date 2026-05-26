"""Retrieve relevant signals for a brief.

Phase 1 retrieval (per spec §5.1):
  1. Filter signals by domain (exact or cross_industry).
  2. Exclude Mainstream diffusion stage.
  3. If <3 matches, flag for web research fallback.
  4. Return top-k (caller is responsible for ranking when len > k).
"""
from dataclasses import dataclass, field

from .domain_match import matches_brief_domain
from .load import Signal


@dataclass
class Brief:
    """Minimal brief contract for retrieval. The full pipeline brief carries more."""

    industry: str
    # Add more fields as the pipeline matures (e.g., problem_statement, hypothesis)


@dataclass
class RetrievalResult:
    signals: list[Signal] = field(default_factory=list)
    needs_web_fallback: bool = False


def retrieve_signals(brief: Brief, pool: list[Signal], k: int = 5) -> RetrievalResult:
    """Filter + cap. Ranking is a separate concern (see rank.py).

    Returns up to k signals. If fewer than 3 signals match after filtering,
    `needs_web_fallback` is set to True so the caller can invoke the Web
    Researcher agent (spec §5.1 step 3).
    """
    matched = [
        s for s in pool
        if matches_brief_domain(brief.industry, s)
        and s.diffusion_stage != "Mainstream"
    ]
    needs_fallback = len(matched) < 3
    return RetrievalResult(signals=matched[:k], needs_web_fallback=needs_fallback)

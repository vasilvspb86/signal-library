"""Decide whether a signal is relevant to a brief's industry."""
from .load import Signal


def matches_brief_domain(brief_industry: str, signal: Signal) -> bool:
    """True if signal.domain == brief_industry OR brief_industry in signal.cross_industry."""
    if signal.domain == brief_industry:
        return True
    return brief_industry in signal.cross_industry

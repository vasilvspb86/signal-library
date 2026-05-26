"""Load all active signals from a vault directory."""
from dataclasses import dataclass, field
from pathlib import Path

from validate_signals.frontmatter import parse_signal_file


@dataclass
class Signal:
    """Parsed signal with the fields the pipeline needs."""

    id: str
    name: str
    year: int
    domain: str
    human_task: str
    existential_essence: str
    compas_segment: int
    macrotrend: str
    diffusion_stage: str
    status: str
    captured_at: str
    verified_at: str
    body: str
    # Optional fields
    url: str | None = None
    cross_industry: list[str] = field(default_factory=list)
    shift_from: str | None = None
    shift_to: str | None = None
    tags: list[str] = field(default_factory=list)
    # Raw frontmatter for any consumers that want the lot
    raw: dict = field(default_factory=dict)
    # Source path for debugging
    source_path: Path | None = None


def load_active_signals(vault_root: Path) -> list[Signal]:
    """Read every `.md` in `vault_root/signals/active/`. Ignores `.gitkeep`."""
    active_dir = vault_root / "signals" / "active"
    if not active_dir.exists():
        return []

    signals: list[Signal] = []
    for md in sorted(active_dir.glob("*.md")):
        fm, body = parse_signal_file(md)
        signals.append(
            Signal(
                id=fm["id"],
                name=fm["name"],
                year=fm["year"],
                domain=fm["domain"],
                human_task=fm["human_task"],
                existential_essence=fm["existential_essence"],
                compas_segment=fm["compas_segment"],
                macrotrend=fm["macrotrend"],
                diffusion_stage=fm["diffusion_stage"],
                status=fm["status"],
                captured_at=str(fm["captured_at"]),
                verified_at=str(fm["verified_at"]),
                body=body,
                url=(fm.get("url") or None) or None,
                cross_industry=fm.get("cross_industry", []) or [],
                shift_from=fm.get("shift_from") or None,
                shift_to=fm.get("shift_to") or None,
                tags=fm.get("tags", []) or [],
                raw=fm,
                source_path=md,
            )
        )
    return signals

"""Write AI-extrapolated candidate signals to the vault inbox.

Called by Quality Gate (pipeline agent 9) at report finalization (spec §6.5).
The per-report cap (top-3 ⚠ candidates) is enforced by the caller, not here.
"""
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class CandidateSignal:
    """Provenance-bearing candidate produced by pipeline web research."""

    name: str
    url: str
    why_flagged: str        # which retrieval pass / what URLs were checked
    report_id: str          # for audit traceability
    brief_excerpt: str      # context for the curator at triage time
    confidence: float       # 0..1 from the agent


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slugify(text: str) -> str:
    return _SLUG_RE.sub("-", text.lower()).strip("-") or "unnamed"


def queue_ai_candidate(vault_root: Path, cand: CandidateSignal) -> Path:
    """Write the candidate stub. Returns the written file path.

    Slug collision strategy: append `-2`, `-3`, … to the slug until unused.
    """
    inbox = vault_root / "signals" / "_inbox" / "_ai-candidates"
    inbox.mkdir(parents=True, exist_ok=True)

    base_slug = _slugify(cand.name)
    date_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    candidate_path = inbox / f"{date_prefix}-{base_slug}.md"
    counter = 2
    while candidate_path.exists():
        candidate_path = inbox / f"{date_prefix}-{base_slug}-{counter}.md"
        counter += 1

    body = _render_stub(cand)
    candidate_path.write_text(body, encoding="utf-8")
    return candidate_path


def _render_stub(cand: CandidateSignal) -> str:
    """Produce the markdown stub. Format mirrors templates/signal-draft.md."""
    return f"""---
status: draft
captured_at: {datetime.now(timezone.utc).isoformat()}
captured_via: ai-candidate
url: {cand.url}
report_id: {cand.report_id}
confidence: {cand.confidence}
schema_version: 1
---

# {cand.name}

> AI-extrapolated candidate from pipeline run {cand.report_id}.

## Why flagged
{cand.why_flagged}

## Brief context
{cand.brief_excerpt}

## Triage checklist (fill before promoting to active/)
- [ ] Verify entity exists (independent search)
- [ ] Fill all 12 MUST fields
- [ ] Anti-hype marker
- [ ] FROM → TO (body section or shift_from/shift_to frontmatter)
- [ ] Compas segment + macrotrend
- [ ] Bridge Map wikilinks (1–3)
- [ ] Worth keeping? Rename to `{{id}}.md`, move to `signals/active/`.
"""

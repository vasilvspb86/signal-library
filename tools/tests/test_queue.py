from pathlib import Path

import frontmatter

from signal_library.queue import CandidateSignal, queue_ai_candidate


def test_writes_to_ai_candidates_folder(tmp_path):
    vault = tmp_path
    (vault / "signals" / "_inbox" / "_ai-candidates").mkdir(parents=True)
    cand = CandidateSignal(
        name="HypotheticalCorp",
        url="https://example.com",
        why_flagged="Mentioned in 3 articles about ambient workplace",
        report_id="rpt-2026-05-22-001",
        brief_excerpt="Premium office REIT seeking tenant experience platform",
        confidence=0.78,
    )
    path = queue_ai_candidate(vault, cand)
    assert path.exists()
    assert path.parent.name == "_ai-candidates"


def test_stub_carries_provenance_metadata(tmp_path):
    vault = tmp_path
    (vault / "signals" / "_inbox" / "_ai-candidates").mkdir(parents=True)
    cand = CandidateSignal(
        name="X", url="https://x.com", why_flagged="why",
        report_id="rpt-001", brief_excerpt="brief", confidence=0.5,
    )
    path = queue_ai_candidate(vault, cand)
    post = frontmatter.loads(path.read_text(encoding="utf-8"))
    assert post.metadata["status"] == "draft"
    assert post.metadata["captured_via"] == "ai-candidate"
    assert post.metadata["report_id"] == "rpt-001"
    assert post.metadata["confidence"] == 0.5
    assert "why" in post.content


def test_slugifies_name_for_filename(tmp_path):
    vault = tmp_path
    (vault / "signals" / "_inbox" / "_ai-candidates").mkdir(parents=True)
    cand = CandidateSignal(
        name="Wild Co!",
        url="https://wild.co",
        why_flagged="x", report_id="rpt-X", brief_excerpt="y", confidence=0.1,
    )
    path = queue_ai_candidate(vault, cand)
    assert "wild-co" in path.name


def test_handles_duplicate_slug_by_appending_counter(tmp_path):
    vault = tmp_path
    (vault / "signals" / "_inbox" / "_ai-candidates").mkdir(parents=True)
    cand = CandidateSignal(
        name="Duplicate",
        url="https://dup.com",
        why_flagged="x", report_id="r", brief_excerpt="y", confidence=0.1,
    )
    p1 = queue_ai_candidate(vault, cand)
    p2 = queue_ai_candidate(vault, cand)
    assert p1 != p2
    assert p1.exists() and p2.exists()

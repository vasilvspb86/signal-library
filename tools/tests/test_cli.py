import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run validate-signals CLI as a subprocess."""
    return subprocess.run(
        [sys.executable, "-m", "validate_signals.cli", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_cli_passes_for_valid_signal(tmp_path, fixtures_dir, taxonomy_path):
    """CLI exits 0 when given a valid signal."""
    # Mimic the active/ scoping rule by placing the file in signals/active/.
    active_dir = tmp_path / "signals" / "active"
    active_dir.mkdir(parents=True)
    target = active_dir / "valid.md"
    shutil.copy(fixtures_dir / "valid_signal.md", target)
    result = _run_cli([str(target), "--taxonomy", str(taxonomy_path)], cwd=tmp_path)
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"


def test_cli_fails_for_missing_essence(tmp_path, fixtures_dir, taxonomy_path):
    """CLI exits non-zero and prints the field name for a MUST violation."""
    active_dir = tmp_path / "signals" / "active"
    active_dir.mkdir(parents=True)
    target = active_dir / "bad.md"
    shutil.copy(fixtures_dir / "missing_essence_signal.md", target)
    result = _run_cli([str(target), "--taxonomy", str(taxonomy_path)], cwd=tmp_path)
    assert result.returncode != 0
    assert "existential_essence" in result.stderr


def test_cli_fails_for_invalid_domain(tmp_path, fixtures_dir, taxonomy_path):
    active_dir = tmp_path / "signals" / "active"
    active_dir.mkdir(parents=True)
    target = active_dir / "bad.md"
    shutil.copy(fixtures_dir / "invalid_domain_signal.md", target)
    result = _run_cli([str(target), "--taxonomy", str(taxonomy_path)], cwd=tmp_path)
    assert result.returncode != 0
    assert "domain" in result.stderr


def test_cli_validates_multiple_files(tmp_path, fixtures_dir, taxonomy_path):
    """CLI accepts multiple file args and reports per-file outcome."""
    active_dir = tmp_path / "signals" / "active"
    active_dir.mkdir(parents=True)
    a = active_dir / "a.md"
    b = active_dir / "b.md"
    shutil.copy(fixtures_dir / "valid_signal.md", a)
    shutil.copy(fixtures_dir / "missing_essence_signal.md", b)
    result = _run_cli([str(a), str(b), "--taxonomy", str(taxonomy_path)], cwd=tmp_path)
    assert result.returncode != 0
    assert "a.md" in result.stdout  # passed file mentioned
    assert "b.md" in result.stderr  # failed file mentioned


def test_cli_no_files_exits_zero(tmp_path, taxonomy_path):
    """No-op (no files passed) is a successful exit."""
    result = _run_cli(["--taxonomy", str(taxonomy_path)], cwd=tmp_path)
    assert result.returncode == 0

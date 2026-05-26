from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return FIXTURES_DIR


@pytest.fixture
def taxonomy_path(tmp_path):
    """Write a minimal taxonomy file for tests."""
    p = tmp_path / "_taxonomy.yml"
    p.write_text(
        """
domains:
  - Workplace
  - Mobility
  - Health
compas_segments:
  1:
    name: Self-care
    macrotrends: [Fantomatica, Deep Customisation]
  2:
    name: Safety
    macrotrends: [Ambient Intelligence, New Privacy]
diffusion_stages:
  - Emerging
  - Innovator
  - Early Adopter
  - Early Majority
  - Mainstream
schema_version: 1
""",
        encoding="utf-8",
    )
    return p

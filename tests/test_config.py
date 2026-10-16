"""Offline configuration and deterministic sampling tests."""

from pathlib import Path

import pytest

from lab3package.config import load_settings
from lab3package.errors import SettingsError
from lab3package.models import HourlyRecord
from lab3package.report import ReportBuilder


def test_missing_settings(tmp_path: Path) -> None:
    """Reject a nonexistent TOML file."""
    with pytest.raises(SettingsError, match="Cannot read"):
        load_settings(tmp_path / "missing.toml")


def test_empty_settings(tmp_path: Path) -> None:
    """Reject incomplete settings."""
    path = tmp_path / "empty.toml"
    path.write_text("", encoding="utf-8")
    with pytest.raises(SettingsError, match="Missing or invalid"):
        load_settings(path)


def test_seed_reproducibility(sample_records: list[HourlyRecord]) -> None:
    """Repeated reports with the same seed produce the same sample."""
    config = Path(__file__).resolve().parents[1] / "config/lab3package.toml"
    settings = load_settings(config)
    first = ReportBuilder(sample_records, settings).build()["featured_shows"]
    second = ReportBuilder(sample_records, settings).build()["featured_shows"]
    assert first == second
    assert len(first) == settings.sample_size

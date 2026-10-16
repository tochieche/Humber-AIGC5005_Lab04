"""No-network CLI exit code and message tests."""

from pathlib import Path
from unittest.mock import patch

import pytest

from lab3package.errors import DownloadError
from lab3package.main import main
from lab3package.models import HourlyRecord


def test_missing_config_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Return exit code one and print exactly one error line."""
    result = main(["--config", str(tmp_path / "missing.toml")])
    output = capsys.readouterr()
    assert result == 1
    assert output.err.startswith("Error:")
    assert len(output.err.splitlines()) == 1
    assert "Traceback" not in output.err


def test_download_error_returns_one(capsys: pytest.CaptureFixture[str]) -> None:
    """Translate an offline source failure to code one."""
    with patch(
        "lab3package.main.WeatherDataSource.fetch",
        side_effect=DownloadError("offline"),
    ):
        result = main([])
    output = capsys.readouterr()
    assert result == 1
    assert output.err.startswith("Error: offline")


def test_success_returns_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Offline successful run writes both expected files."""
    config = Path(__file__).resolve().parents[1] / "config/lab3package.toml"
    text = config.read_text(encoding="utf-8").replace(
        'output_folder = "data/processed"', f'output_folder = "{tmp_path.as_posix()}"'
    )
    custom = tmp_path / "settings.toml"
    custom.write_text(text, encoding="utf-8")
    records = [HourlyRecord("2026-10-14T10:00", 10.0, 0.0)]
    with patch("lab3package.main.WeatherDataSource.fetch", return_value=records):
        result = main(["--config", str(custom)])
    output = capsys.readouterr()
    assert result == 0
    assert "Processed 1 records." in output.out
    assert (tmp_path / "summary.json").exists()
    assert (tmp_path / "run_info.json").exists()

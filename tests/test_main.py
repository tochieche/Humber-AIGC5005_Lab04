
"""Tests for application exit codes."""

from pathlib import Path

from lab3package.main import main


def test_missing_config_returns_one(
    tmp_path: Path,
    capsys,
) -> None:
    """Return one when the settings file does not exist."""
    missing_file = tmp_path / "missing.toml"

    exit_code = main(["--config", str(missing_file)])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.err.startswith("Error:")
    assert "Traceback" not in captured.err

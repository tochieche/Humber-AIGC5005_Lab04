
"""Tests for report output files."""

import json
from pathlib import Path

from lab3package.models import HourlyRecord
from lab3package.report import ReportBuilder


def test_report_written_to_temporary_path(
    sample_records: list[HourlyRecord],
    tmp_path: Path,
) -> None:
    """Write the report inside pytest's temporary directory."""
    output = tmp_path / "summary.json"

    builder = ReportBuilder(sample_records)
    builder.write(output)

    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["records_processed"] == 3

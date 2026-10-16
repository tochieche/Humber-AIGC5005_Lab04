"""Polymorphic weather report and reproducibility metadata."""

import json
import logging
import platform
import random
from dataclasses import asdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TypedDict, cast

from .aggregations import (
    Aggregation,
    ConditionCountAggregation,
    DailyStats,
    DailyTemperatureAggregation,
    RecentReadingsAggregation,
    RecentStats,
)
from .config import Settings
from .errors import ReportError
from .models import HourlyRecord

logger = logging.getLogger(__name__)


class Summary(TypedDict):
    """Schema for the generated JSON weather report."""

    source_url: str
    records_processed: int
    hottest_day: str
    hottest_day_max_temp_c: float | int
    daily_breakdown: DailyStats
    condition_counts: dict[str, int]
    recent_readings: RecentStats
    featured_shows: list[str]


def installed_version(name: str) -> str:
    """Return package metadata version or a missing-package marker."""
    try:
        return version(name)
    except PackageNotFoundError:
        return "not installed"


class ReportBuilder:
    """Run aggregations using their common compute interface."""

    def __init__(
        self,
        records: list[HourlyRecord],
        settings: Settings | None = None,
    ) -> None:
        """Store validated records and create the aggregation objects once."""
        self.records = records
        self.settings = settings
        self.aggregations: list[Aggregation] = [
            DailyTemperatureAggregation(),
            ConditionCountAggregation(),
            RecentReadingsAggregation(count=5),
        ]

    def build(self) -> Summary:
        """Execute aggregation objects polymorphically and build a summary."""
        logger.info("Starting report generation")
        logger.debug("Processed %s records", len(self.records))
        results = {
            type(aggregation).__name__: aggregation.compute(self.records)
            for aggregation in self.aggregations
        }
        daily = cast("DailyStats", results["DailyTemperatureAggregation"])
        conditions = cast("dict[str, int]", results["ConditionCountAggregation"])
        recent = cast("RecentStats", results["RecentReadingsAggregation"])
        if not daily:
            raise ReportError("Cannot build a weather report without valid daily data")
        hottest = max(daily, key=lambda date: daily[date]["max_temp_c"])
        shows: list[str] = []
        if self.settings is not None:
            shows = random.Random(self.settings.seed).sample(
                list(self.settings.show_names), self.settings.sample_size
            )
        return {
            "source_url": self.settings.source_url if self.settings else "",
            "records_processed": len(self.records),
            "hottest_day": hottest,
            "hottest_day_max_temp_c": daily[hottest]["max_temp_c"],
            "daily_breakdown": daily,
            "condition_counts": conditions,
            "recent_readings": recent,
            "featured_shows": shows,
        }

    def write(self, path: Path) -> Summary:
        """Write JSON weather summary, translating filesystem errors."""
        summary = self.build()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        except OSError as error:
            raise ReportError(f"Cannot write summary: {path}") from error
        return summary

    def write_run_info(self, folder: Path) -> Path:
        """Write settings, Python version and tooling versions beside the report."""
        if self.settings is None:
            raise ReportError("Settings required for run metadata")
        data = {
            "settings": {
                **asdict(self.settings),
                "output_folder": str(self.settings.output_folder),
            },
            "python_version": platform.python_version(),
            "tool_versions": {
                name: installed_version(name) for name in ("pytest", "mypy", "ruff")
            },
        }
        path = folder / "run_info.json"
        try:
            folder.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except OSError as error:
            raise ReportError(f"Cannot write run_info.json: {path}") from error
        return path

"""Polymorphic weather aggregation strategies."""

from abc import ABC, abstractmethod
from collections import Counter, defaultdict

from .models import HourlyRecord

DailyStats = dict[str, dict[str, float | int]]
RecentStats = list[dict[str, str | float]]
AggregationResult = DailyStats | dict[str, int] | RecentStats


class Aggregation(ABC):
    """Common interface for hourly weather aggregations."""

    @abstractmethod
    def compute(self, records: list[HourlyRecord]) -> AggregationResult:
        """Compute statistics from weather observations."""
        ...


class DailyTemperatureAggregation(Aggregation):
    """Group readings by day and calculate daily weather statistics."""

    def compute(self, records: list[HourlyRecord]) -> DailyStats:
        """Return minima, maxima, means, rainfall totals, and counts."""
        grouped: dict[str, list[HourlyRecord]] = defaultdict(list)
        for record in records:
            grouped[record.timestamp.split("T")[0]].append(record)
        return {
            day: {
                "min_temp_c": round(min(r.temperature for r in day_records), 1),
                "max_temp_c": round(max(r.temperature for r in day_records), 1),
                "avg_temp_c": round(
                    sum(r.temperature for r in day_records) / len(day_records), 1
                ),
                "total_precip_mm": round(sum(r.precipitation for r in day_records), 1),
                "readings": len(day_records),
            }
            for day, day_records in grouped.items()
        }


class ConditionCountAggregation(Aggregation):
    """Count observations in simple weather-condition categories."""

    def compute(self, records: list[HourlyRecord]) -> dict[str, int]:
        """Classify each hourly observation and count the categories."""
        conditions: list[str] = []
        for record in records:
            if record.precipitation > 0:
                conditions.append("Precipitation")
            elif record.temperature < 0:
                conditions.append("Freezing Dry")
            elif record.temperature < 15:
                conditions.append("Cool Dry")
            else:
                conditions.append("Warm Dry")
        return dict(Counter(conditions))


class RecentReadingsAggregation(Aggregation):
    """Return the latest observations in a JSON-ready representation."""

    def __init__(self, count: int = 5) -> None:
        """Set the maximum number of recent observations."""
        if count < 0:
            raise ValueError("Recent readings count cannot be negative")
        self.count = count

    def compute(self, records: list[HourlyRecord]) -> RecentStats:
        """Return no more than count chronological readings."""
        recent = records[-self.count :] if self.count else []
        return [
            {
                "timestamp": record.timestamp,
                "temperature_c": record.temperature,
                "precipitation_mm": record.precipitation,
            }
            for record in recent
        ]

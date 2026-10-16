"""Validated weather and show records."""

import math
from dataclasses import dataclass


class HourlyRecord:
    """An hourly observation with validated numeric measurements."""

    def __init__(
        self,
        timestamp: str | None,
        temperature: float | str | None,
        precipitation: float | str | None,
    ) -> None:
        """Validate the timestamp and normalize numeric inputs."""
        if timestamp is None or not timestamp.strip():
            raise ValueError("Timestamp cannot be None or empty.")
        if temperature is None or precipitation is None:
            raise ValueError("Temperature and precipitation cannot be None.")
        try:
            temp = float(temperature)
            precip = float(precipitation)
        except (TypeError, ValueError) as error:
            raise ValueError("Invalid temperature or precipitation value") from error
        if not math.isfinite(temp) or not math.isfinite(precip):
            raise ValueError("Invalid non-finite weather value")
        self.timestamp = timestamp
        self.temperature = temp
        self.precipitation = precip

    def __str__(self) -> str:
        """Render a readable observation."""
        return (
            f"HourlyRecord(time={self.timestamp}, temp={self.temperature}°C, "
            f"precip={self.precipitation}mm)"
        )


@dataclass(frozen=True)
class ShowRecord:
    """A show whose genre list and rating are validated on creation."""

    name: str
    genres: tuple[str, ...] | None
    rating: float | None

    def __post_init__(self) -> None:
        """Reject missing or invalid show details."""
        if not self.name.strip():
            raise ValueError("Show name is required")
        if not self.genres:
            raise ValueError("Genre list is required")
        if self.rating is None:
            raise ValueError("Rating is required")
        if not math.isfinite(self.rating) or not 0 <= self.rating <= 10:
            raise ValueError("Rating must be between 0 and 10")

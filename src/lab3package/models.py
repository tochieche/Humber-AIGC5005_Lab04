
class HourlyRecord:
    """Represent a validated hourly weather observation.

    Each record stores a timestamp, temperature in degrees
    Celsius, and precipitation in millimetres.

    The constructor validates required values and converts
    numeric inputs to floating-point numbers.
    """

    def __init__(self, timestamp, temperature, precipitation):
        """Initialize and validate an hourly weather record.

        Args:
            timestamp: Date and time of the observation.
            temperature: Temperature in degrees Celsius.
            precipitation: Precipitation in millimetres.

        Raises:
            ValueError: If any required value is missing
                or a numeric value cannot be converted.
        """
        if timestamp is None:
            raise ValueError("Timestamp cannot be None.")

        if temperature is None or precipitation is None:
            raise ValueError(
                "Temperature and precipitation cannot be None."
            )

        try:
            self.timestamp = str(timestamp)
            self.temperature = float(temperature)
            self.precipitation = float(precipitation)

        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Invalid malformed data types: {e}"
            ) from e

    def __str__(self):
        """Return a readable string describing the observation.

        Returns:
            str: Timestamp, temperature, and precipitation
                formatted for display.
        """
        return (
            f"HourlyRecord(time={self.timestamp}, "
            f"temp={self.temperature}°C, "
            f"precip={self.precipitation}mm)"
        )

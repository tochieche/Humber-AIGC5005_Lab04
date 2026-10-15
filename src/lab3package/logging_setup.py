"""Configure application-wide logging."""

import logging


def configure_logging(level: str) -> None:
    """Configure the application logging level and format."""
    numeric_level = logging.getLevelNamesMapping().get(level.upper())

    if numeric_level is None:
        raise ValueError(f"Invalid logging level: {level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        force=True,
    )

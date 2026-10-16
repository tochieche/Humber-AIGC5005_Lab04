"""Configure application-wide logging."""

import logging
import sys


def configure_logging(level: str) -> None:
    """Configure a single consistent logging format and level."""
    numeric = logging.getLevelNamesMapping().get(level.upper())
    if numeric is None:
        raise ValueError("Invalid logging level")
    logging.basicConfig(
        level=numeric,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stdout,
        force=True,
    )

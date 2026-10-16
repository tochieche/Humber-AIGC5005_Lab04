"""Command-line entry point for the lab3package weather application."""

import argparse
import logging
import sys
from pathlib import Path

from .config import DEFAULT_CONFIG, load_settings
from .errors import Lab3PackageError
from .logging_setup import configure_logging
from .report import ReportBuilder
from .sources import WeatherDataSource

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """Generate weather reports and return 0 or 1 for expected outcomes."""
    parser = argparse.ArgumentParser(description="Generate a weather summary")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args(argv)
    configure_logging("INFO")
    try:
        settings = load_settings(args.config)
        configure_logging(settings.log_level)
        logger.info("Application started")
        records = WeatherDataSource(settings.source_url, settings.timeout).fetch()
        if not records:
            raise Lab3PackageError("No valid weather records were retrieved")
        builder = ReportBuilder(records, settings)
        destination = settings.output_folder / "summary.json"
        summary = builder.write(destination)
        builder.write_run_info(settings.output_folder)
        logger.info("Report generation completed")
        print(f"Processed {summary['records_processed']} records.")
        print(f"Summary written to {destination}")
        return 0
    except Lab3PackageError as error:
        logger.error("Application failed: %s", error)
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

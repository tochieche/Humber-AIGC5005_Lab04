
"""Command-line entry point for the weather application."""

import argparse
import logging
import sys
from pathlib import Path

from .config import load_settings
from .errors import Lab3PackageError
from .logging_setup import configure_logging
from .report import ReportBuilder
from .sources import WeatherDataSource

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
     """Run the application and return a process exit code."""
    parser = argparse.ArgumentParser(
        description="Generate a weather summary report"
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/lab3package.toml"),
        help="Path to the TOML settings file",
    )

    args = parser.parse_args(argv)

    configure_logging("INFO")

    try:
        settings = load_settings(args.config)
        configure_logging(settings.log_level)

        logger.info("Application started")

        source = WeatherDataSource(
            settings.source_url,
            settings.timeout,
        )

        records = source.fetch()

        if not records:
            raise Lab3PackageError(
                "No valid weather records were retrieved"
            )

        reporter = ReportBuilder(records)

        output_path = settings.output_folder / "summary.json"
        summary = reporter.write(output_path)

        logger.info("Report generation completed")

        print(
            f"Processed {summary['records_processed']} records."
        )
        print(f"Summary written to {output_path}")

        return 0

    except Lab3PackageError as error:
        logger.error("Application failed: %s", error)
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

import sys

from lab3package import WeatherDataSource, ReportBuilder
from lab3package.config import OUTPUT_PATH, SOURCE_URL
from lab3package.sources import DataSourceError


def main():
    """Run the weather application.

    Retrieves hourly weather observations, verifies that
    valid records are available, and generates a JSON
    summary report.

    Displays the number of processed observations,
    hottest day, and report output location.

    Exits with an error message when the data source
    fails or no valid records are retrieved.
    """
    try:
        source = WeatherDataSource(SOURCE_URL)
        records = source.fetch()

    except DataSourceError as err:
        sys.exit(f"Error: Download failed from source API. {err}")

    if not records:
        sys.exit("Error: No valid records retrieved.")

    reporter = ReportBuilder(records)
    summary = reporter.write(OUTPUT_PATH)

    print(f"Read {len(records)} weather records from source API.")

    print(
        f"Hottest day was {summary['hottest_day']} with a high of "
        f"{summary['hottest_day_max_temp_c']}°C."
    )

    print(f"Summary written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

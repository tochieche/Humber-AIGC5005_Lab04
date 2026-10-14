
# Weather App Builder
This program downloads a week of hourly temperature and rain data for Toronto from an open API and summarizes it into daily stats and weather patterns. It's useful because looking through hundreds of raw weather numbers is annoying, so this automatically breaks down the highs, lows, averages, and rainfall for you.

## Data source
The data comes from the [Open-Meteo Weather API](https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=0&timezone=America/Toronto). One record represents one hour of weather data (containing a timestamp, temperature in °C, and precipitation in mm), and the API returns around 168 records for a full 7-day period.

## Setup
python -m venv .venv
source .venv/bin/activate

conda env create -f environment.yml
conda activate lab3package
pip install -r requirements.txt
pip install -e .

## Run
python main.py


## Test
python -m unittest discover -s tests -v
python -m pip check

## Example output
The retrieved output sample json is as follows:
{
  "source_url": "[https://api.open-meteo.com/v1/forecast]",
  "records_processed": 168,
  "hottest_day": "2026-09-21",
  "hottest_day_max_temp_c": 22.4,
  "daily_breakdown": {
    "2026-09-21": {
      "min_temp_c": 13.0,
      "max_temp_c": 22.4,
      "avg_temp_c": 17.8,
      "total_precip_mm": 1.2,
      "readings": 24
    }
  }
}



## Layout
src/lab3package/config.py: Centralized URL, timeout, and output path configuration.

src/lab3package/models.py: HourlyRecord class encapsulating data validation and cleaning.

src/lab3package/sources.py: WeatherDataSource class for API retrieval; only module using requests.

src/lab3package/aggregations.py: Base class and subclasses implementing polymorphism for statistics.

src/lab3package/report.py: ReportBuilder class for compiling results and writing JSON output.

src/lab3package/__init__.py: Re-exports public API names.

main.py: Thin execution entry point and clean error message handler.





## Layout
What moved
===> From Lab 02: SOURCE_URL & OUTPUT
===> To Lab 03: src/lab3package/config.py

===> From Lab 02: HourlyRecord namedtuple
===> To Lab 03: src/lab3package/models.py (HourlyRecord class)

===> From Lab 02: fetch_records()
===> To Lab 03: src/lab3package/sources.py (WeatherDataSource.fetch())


===> From Lab 02: aggregate_by_date(), classify_weather_conditions(), recent_readings()
===> To Lab 03: src/lab3package/aggregations.py (subclasses of Aggregation)

===> From Lab 02: build_summary() & write_summary()
===> To Lab 03: src/lab3package/report.py 




## Data quirks
The API doesn't return a list of neat JSON dictionaries; instead, it gives separate arrays for timestamps, temperatures, and precipitation. My code combines them into a single record.

Sometimes the API can have missing or null values or values that aren't numbers. My program checks for this and uses a try/except block to skip any corrupted readings instead of crashing or accidentally treating missing data as 0°C.


## Design choices

   ### Why I used object-oriented programming

   I organized the weather application into separate classes so that each class has one clear responsibility. This makes the program easier to understand, test, maintain, and extend.

   HourlyRecord represents and validates one hourly weather observation.

   WeatherDataSource retrieves weather information from the API.

   Aggregation provides a common interface for weather calculations.

   ReportBuilder combines the calculated results and exports them to JSON.

   This approach follows the Single Responsibility Principle because each class focuses on a specific part of the application's functionality.


   ### Why I used inheritance

   I created an abstract base class named Aggregation because the weather application performs several different calculations on the same collection of hourly records.

   The subclasses DailyTemperatureAggregation, ConditionCountAggregation, and RecentReadingsAggregation inherit from Aggregation.

   Each subclass implements the shared compute() method differently.

   Inheritance establishes a consistent interface for all aggregation operations, avoids duplicating their execution logic, and makes adding new aggregation types easier.


   ### Why I used polymorphism

   Polymorphism allows different aggregation objects to be treated through the same Aggregation interface.

   In the refactored ReportBuilder, aggregation objects are stored in a list and executed through a common loop:

   for aggregation in self.aggregations:
       results[type(aggregation).__name__] = (
           aggregation.compute(self.records)
       )

   Python automatically executes the appropriate subclass implementation of compute().

   This design reduces repetitive method calls and allows aggregation strategies to be managed consistently.


   ### Why HourlyRecord validates and cleans its own values

   I designed HourlyRecord to validate its inputs during initialization because weather data obtained from external APIs may contain missing or incorrectly formatted values.

   The constructor checks that required values are present and converts temperature and precipitation values into floating-point numbers.

   If a required value is missing or cannot be converted, the class raises a ValueError.

   Keeping validation inside HourlyRecord ensures that every successfully constructed record follows the same basic data requirements.

   It also prevents the aggregation classes from repeatedly performing the same input validation.

   Invalid observations are skipped by the data-source processing logic instead of being included in weather calculations.

   This design improves data consistency and separates data validation from statistical processing.


   ### Why I used defaultdict and Counter

   I used defaultdict in DailyTemperatureAggregation to group hourly observations by date without manually creating a list for each new date.

   I used Counter in ConditionCountAggregation to calculate the number of observations in each weather category.

   These built-in Python tools reduce unnecessary code and make the aggregation logic easier to read.


   ### Why I separated API communication from report generation

   I placed HTTP communication inside WeatherDataSource so that the rest of the application does not need to manage API requests directly.

   This separates external data retrieval from business logic and reporting.

   ReportBuilder works with validated weather records instead of HTTP responses. As a result, the reporting functionality can be tested independently using sample records without contacting the weather API.




## Known limitations

   ### Fixed geographical location
   The application currently retrieves weather data for Toronto, Ontario, using coordinates configured in the source URL.

   Users cannot select a different city or geographical location through the command line.

   A future improvement would allow users to provide custom coordinates or choose from predefined cities.


   ### Fixed weather-data period

   The API request is configured to retrieve approximately seven days of hourly observations.

   The application does not currently allow users to select arbitrary start and end dates.

   Future versions could accept a configurable date range.


   ### Dependence on an external weather API

   The application depends on the availability and responsiveness of the Open-Meteo API.

   Network outages, connection timeouts, API errors, or unexpected responses may prevent the application from generating a report.

   A future improvement would introduce retry logic with exponential backoff and optional local caching.




   ### Missing or malformed observations

   The application checks for missing or malformed weather values and skips records that cannot be converted into valid HourlyRecord objects.

   Although this prevents invalid observations from entering the calculations, skipping records may produce incomplete daily statistics.

   The application does not currently perform missing-value imputation or report detailed data-quality metrics.

   ### Fixed weather classification thresholds

   Weather categories use fixed temperature and precipitation thresholds.

   For example, dry observations below 0°C are classified as Freezing Dry, while dry observations below 15°C are classified as Cool Dry.

   These thresholds may not be appropriate for every geographical location, climate, or season.

   A future improvement would make the thresholds configurable.


   ### Limited output formats

   The application currently exports its summary as a JSON file.

   It does not provide CSV exports, an interactive dashboard, or graphical visualizations.

   Future improvements could include CSV output, Matplotlib charts, or a simple web-based dashboard.

   ### Basic handling of incomplete datasets

   The application requires valid weather observations to generate a meaningful report.

   If no valid daily observations are available, report generation cannot determine the hottest day.

   A future improvement would provide more detailed diagnostics explaining which observations were rejected and why.

   ### No persistent historical database
   The application retrieves weather observations and creates a summary report, but it does not maintain a historical database of previously downloaded information.

   Each execution processes the weather data retrieved for that run.

   A future version could store historical observations in SQLite or PostgreSQL for long-term comparison and analysis.

import ast
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from lab3package.sources import DataSourceError, WeatherDataSource


class TestSourceBoundary(unittest.TestCase):

    def test_main_does_not_import_requests(self):
        root = Path(__file__).resolve().parents[1]
        main_file = root / "main.py"
        tree = ast.parse(main_file.read_text(encoding="utf-8"))

        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)

        self.assertNotIn("requests", imports)
        self.assertFalse(
            any(name.startswith("requests.") for name in imports)
        )

    @patch("lab3package.sources.requests.get")
    def test_network_error_is_translated(self, mock_get):
        mock_get.side_effect = requests.ConnectionError(
            "Simulated network failure"
        )

        source = WeatherDataSource()

        with self.assertRaises(DataSourceError):
            source.fetch()


if __name__ == "__main__":
    unittest.main()

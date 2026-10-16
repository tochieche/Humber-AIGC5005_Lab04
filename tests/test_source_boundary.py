"""Boundary tests for HTTP isolation."""

import ast
from pathlib import Path
from unittest.mock import patch

import pytest
import requests

from lab3package.errors import DownloadError
from lab3package.sources import WeatherDataSource


def test_main_does_not_import_requests() -> None:
    """Ensure the package entry point does not import the HTTP client."""
    path = Path(__file__).resolve().parents[1] / "src/lab3package/main.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = [
        item.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for item in node.names
    ]
    assert "requests" not in names


def test_network_error_is_translated() -> None:
    """Translate a connection problem to the package error hierarchy."""
    with patch("lab3package.sources.requests.get") as get:
        get.side_effect = requests.ConnectionError("offline")
        with pytest.raises(DownloadError):
            WeatherDataSource("https://example.test").fetch()

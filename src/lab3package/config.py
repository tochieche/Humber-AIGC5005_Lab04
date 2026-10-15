
"""Load and validate application settings from TOML."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from .errors import SettingsError


@dataclass(frozen=True)
class Settings:
    """Immutable application configuration."""

    source_url: str
    timeout: float
    output_folder: Path
    seed: int
    sample_size: int
    log_level: str
    show_names: tuple[str, ...] = ()


def load_settings(path: Path) -> Settings:
    """Read a TOML file and return validated settings."""
    try:
        with path.open("rb") as file:
            content = tomllib.load(file)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise SettingsError(
            f"Cannot read settings file: {path}"
        ) from error

    try:
        app = content["app"]
        shows = content.get("shows", {})

        settings = Settings(
            source_url=str(app["source_url"]),
            timeout=float(app["timeout"]),
            output_folder=Path(app["output_folder"]),
            seed=int(app["seed"]),
            sample_size=int(app["sample_size"]),
            log_level=str(app["log_level"]).upper(),
            show_names=tuple(shows.get("names", [])),
        )
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise SettingsError(
            "Settings file contains missing or invalid fields"
        ) from error

    if not settings.source_url.startswith(("https://", "http://")):
        raise SettingsError("Invalid source URL")

    if settings.timeout <= 0:
        raise SettingsError("Timeout must be positive")

    if settings.sample_size < 0:
        raise SettingsError("Sample size cannot be negative")

    if settings.log_level not in {
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    }:
        raise SettingsError("Invalid log level")

    if settings.sample_size > len(settings.show_names):
        raise SettingsError(
            "Sample size exceeds the available show catalogue"
        )

    return settings

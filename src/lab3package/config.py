"""Validated TOML configuration."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from .errors import SettingsError

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "lab3package.toml"


@dataclass(frozen=True)
class Settings:
    """Immutable, validated application settings."""

    source_url: str
    timeout: float
    output_folder: Path
    seed: int
    sample_size: int
    log_level: str
    show_names: tuple[str, ...]


def load_settings(path: Path) -> Settings:
    """Parse and validate settings; report actionable configuration errors."""
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise SettingsError(f"Cannot read settings file: {path}") from error
    try:
        app = data["app"]
        shows = data["shows"]
        url = app["source_url"]
        timeout = app["timeout"]
        folder = app["output_folder"]
        seed = app["seed"]
        sample_size = app["sample_size"]
        level = app["log_level"]
        names = shows["names"]
        if not isinstance(url, str) or urlparse(url).scheme not in {"https", "http"}:
            raise ValueError("source_url must be an HTTP(S) URL")
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (float, int))
            or timeout <= 0
        ):
            raise ValueError("timeout must be a positive number")
        if not isinstance(folder, str) or not folder.strip():
            raise ValueError("output_folder must be a nonempty string")
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise ValueError("seed must be an integer")
        if (
            isinstance(sample_size, bool)
            or not isinstance(sample_size, int)
            or sample_size < 0
        ):
            raise ValueError("sample_size must be a nonnegative integer")
        if not isinstance(level, str) or level.upper() not in {
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }:
            raise ValueError("log_level is invalid")
        if not isinstance(names, list) or not all(
            isinstance(name, str) and bool(name.strip()) for name in names
        ):
            raise ValueError("shows.names must be a list of nonempty strings")
        if len(set(names)) != len(names) or sample_size > len(names):
            raise ValueError("show names must be unique and cover sample_size")
        output_folder = Path(folder)
        if not output_folder.is_absolute():
            output_folder = (path.resolve().parent.parent / output_folder).resolve()
        return Settings(
            url,
            float(timeout),
            output_folder,
            seed,
            sample_size,
            level.upper(),
            tuple(names),
        )
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise SettingsError(f"Missing or invalid settings: {error}") from error

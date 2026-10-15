
"""Application-specific exceptions for lab3package."""


class Lab3PackageError(Exception):
    """Base class for expected package failures."""


class DownloadError(Lab3PackageError):
    """Raised when downloading data fails."""


class ResponseFormatError(Lab3PackageError):
    """Raised when the API response has an invalid structure."""


class SettingsError(Lab3PackageError):
    """Raised when a configuration file cannot be used."""


class ReportError(Lab3PackageError):
    """Raised when the application cannot write its report."""

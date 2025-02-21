"""Base exception and warning classes."""


class SodarWarning(Warning):
    """Base warning class."""


class SodarException(BaseException):
    """Base exception class."""


class MissingFileOnImport(BaseException):
    """Raised when not all necessary files are present during import."""


class RestApiCallException(BaseException):
    """Raised on problems with REST API calls."""


class InconsistentSamplesDataException(BaseException):
    """Raised on sample inconsistencies in files."""

class BaseAppException(Exception):
    """Base exception class for all exceptions in this project."""

    def __init__(self, message: str, info: dict = None):
        """Initialize the exception with a message."""
        self.message = message
        self.info = info

    def __str__(self):
        """Return the exception message."""
        return self.message

    def __repr__(self):
        """Return the exception message."""
        return self.message

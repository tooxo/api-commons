class InvalidUrlError(RuntimeError):
    """
    Raised when a given url was invalid
    """


class IncompleteObjectError(RuntimeError):
    """
    Raised when too less data is given to complete the object
    """


class RegexMatchError(RuntimeError):
    """
    Raised, when a regex doesn't match
    """


class AsynchronousLibrariesNotFoundException(Exception):
    """
    Raised when an asynchronous exception is called while not having the
    dependencies installed
    """


class ExtractionError(RuntimeError):
    """
    Main class for errors occurring while extraction
    """


class NoResultsFound(ExtractionError):
    """
    Raised when no results were found
    """

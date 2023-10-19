import logging


def get_logger() -> logging.Logger:
    """
    Returns an instance of the default logger of this package
    """
    return logging.getLogger("migration_zero")

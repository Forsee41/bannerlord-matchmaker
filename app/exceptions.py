import logging

log = logging.getLogger(__name__)


class LoggedException(Exception):
    """
    Automatically logs an exception, using an exception message
    """

    def __init__(self, *args: object) -> None:
        log.error(args[0])
        super().__init__(*args)


class ConfigError(LoggedException):
    """An error raised when config data is invalid"""


class RoleNotFoundError(Exception):
    """An error raised when player does not have matching proficiency"""


class ProficiencyValidationError(LoggedException):
    """An error raised on trying to initialize
    PlayerClassProficiency with invalid data"""


class NotEnoughPlayersError(LoggedException):
    """
    An error raised when player picker recieved less than 12 players
    """

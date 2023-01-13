from enum import Enum


class EnvVarNames(str, Enum):
    """Aggregates all environment variable names"""

    CONFIG_FILE_PATH = "CONFIG_FILE_PATH"
    LOG_CONFIG_FILE_PATH = "LOG_CONFIG_PATH"
    MM_CONFIG_FILE_PATH = "MM_CONFIG_FILE_PATH"
    SERVICE_LOGIN = "MAIN_SERVICE_LOGIN"
    SERVICE_PASSWORD = "MAIN_SERVICE_PASSWORD"
    SERVICE_ADDRESS = "MAIN_SERVICE_ADDRESS"
    ENVIRONMENT = "ENVIRONMENT"


class Environments(str, Enum):
    DEV = "dev"
    PROD = "prod"


class PlayerRole(str, Enum):
    cav = "Cavalry"
    inf = "Infantry"
    arch = "Archer"


class PatreonRole(str, Enum):
    patreon_0 = "patreon_0"
    patreon_1 = "patreon_1"
    patreon_2 = "patreon_2"
    patreon_3 = "patreon_3"


class TeamDesignations(str, Enum):
    team1 = "team1"
    team2 = "team2"


class MapFacFieldNames(str, Enum):
    fac1 = "fac1"
    fac2 = "fac2"
    map = "map"


class LimitationType(str, Enum):
    max = "max"
    min = "min"
    fill = "fill"


class MapType(str, Enum):
    open = "open"
    close = "close"
    mix = "mix"

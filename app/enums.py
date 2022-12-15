from enum import Enum


class EnvVarNames(str, Enum):
    """Class aggregates all environment variable names"""

    CONFIG_FILE_PATH = "CONFIG_FILE_PATH"
    LOG_CONFIG_FILE_PATH = "LOG_CONFIG_PATH"
    MM_CONFIG_FILE_PATH = "MM_CONFIG_FILE_PATH"
    SERVICE_LOGIN = "MAIN_SERVICE_LOGIN"
    SERVICE_PASSWORD = "MAIN_SERVICE_PASSWORD"
    SERVICE_ADDRESS = "MAIN_SERVICE_ADDRESS"
    ENVIRONMENT = "ENVIRONMENT"


class PlayerClass(str, Enum):
    cav = "Cavalry"
    inf = "Infantry"
    arch = "Archer"


class Environments(str, Enum):
    DEV = "dev"
    PROD = "prod"

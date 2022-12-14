from enum import Enum


class EnvVarNames(str, Enum):
    """Class aggregates all environment variable names"""
    config_file_path = "CONFIG_FILE_PATH"   # optional
    log_config_file_path = "LOG_CONFIG_PATH"    # optional
    service_login = "MAIN_SERVICE_LOGIN"
    service_password = "MAIN_SERVICE_PASSWORD"
    service_address = "MAIN_SERVICE_ADDRESS"

class PlayerClass(str, Enum):
    cav = 'Cavalry'
    inf = 'Infantry'
    arch = 'Archer'


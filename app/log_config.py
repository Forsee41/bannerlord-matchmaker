import os
import logging
from logging.config import dictConfig
from pathlib import Path

import yaml

from exceptions import ConfigError
from enums import EnvVarNames


DEFAULT_LOG_CONFIG_PATH = "../logging.yaml"


def get_log_config_path() -> Path:
    """
    Gets logging config path from env vars.
    Uses default path if env var is not set
    """

    log_config_path_string = os.getenv(
        EnvVarNames.log_config_path, DEFAULT_LOG_CONFIG_PATH
    )
    try:
        log_config_path = Path(log_config_path_string)
    except Exception:
        error_msg = f"{EnvVarNames.log_config_path} env var is invalid"
        # using a root logger since module
        # level loggers can't be properly constructed
        logging.getLogger().error(error_msg)
        raise EnvironmentError(error_msg)
    return log_config_path


def get_logger_config() -> dict:
    """Parses log config file and returns a config dict"""

    log_config_path = get_log_config_path()
    try:
        with open(log_config_path, "r") as f:
            log_config_dict = yaml.safe_load(f)
    except Exception:
        error_msg = (
            f"Error loading logging config file, perhaps log config path is invalid"
        )
        logging.getLogger().error(error_msg)
        raise ConfigError(error_msg)
    return log_config_dict


def setup_loggers() -> None:
    """Sets up loggers configuration according to log config file"""
    log_config_dict = get_logger_config()
    dictConfig(log_config_dict)
    # since log config has been initialized, a module level logger is now available
    logging.getLogger(__name__).info("Loggers set up successfully")

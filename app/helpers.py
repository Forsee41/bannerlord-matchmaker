import json
import logging
import os
from pathlib import Path
from typing import Any

import yaml

from app.enums import EnvVarNames
from app.exceptions import ConfigError

log = logging.getLogger(__name__)
DEFAULT_CONFIG_FILE_PATH = "config-default.yaml"


def get_config_from_json(config_file_path: Path) -> dict[str, Any]:
    """
    Settings source that loads variables from a JSON file
    """
    try:
        with open(config_file_path) as f:
            config_dict = json.load(f)
    except Exception:
        raise ConfigError(
            "Error loading config file, perhaps config path is invalid or "
            "data is corrupted"
        )

    return config_dict


def get_config_from_yaml(config_file_path: Path) -> dict[str, Any]:
    """
    Settings source that loads variables from a YAML file
    """
    try:
        with open(config_file_path) as f:
            config_dict = yaml.safe_load(f)
    except Exception as e:
        raise ConfigError(
            "Error loading config file, perhaps config path is invalid or "
            "data is corrupted",
            e,
        )

    return config_dict


def get_app_config_file_path() -> Path:
    """
    Returns a config file path as a Path object
    Gets file path from env variable, if env variable is not set,
    uses default file path instead
    """
    env_config_file_path = os.getenv(EnvVarNames.CONFIG_FILE_PATH, None)
    if env_config_file_path is None:
        log.warning(
            f"Couldn't load {EnvVarNames.CONFIG_FILE_PATH} env var,"
            f"trying default config path"
        )
    config_file_path = env_config_file_path or DEFAULT_CONFIG_FILE_PATH
    try:
        target_path = Path(config_file_path)
    except Exception:
        error_msg = "Config file path is invalid"
        log.error(error_msg)
        raise ValueError(error_msg)

    return target_path


def get_env_mm_config_file_path() -> Path:
    """
    Returns matchmaking config file path as a Path object
    Gets file path from env variable, if env variable is not set,
    uses filepath from app config instead
    """
    env_config_file_path = os.getenv(EnvVarNames.MM_CONFIG_FILE_PATH, None)
    if env_config_file_path is None:
        log.warning(
            f"Couldn't load {EnvVarNames.CONFIG_FILE_PATH} env var,"
            f"trying config path from app config"
        )
    if env_config_file_path is None:
        raise EnvironmentError("MM config filepath env var is not set")
    try:
        target_path = Path(env_config_file_path)
    except Exception:
        error_msg = "Config file path is invalid"
        log.error(error_msg)
        raise ValueError(error_msg)

    return target_path

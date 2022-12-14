from typing import Any
import os
from pathlib import Path
import logging

from pydantic import BaseConfig, BaseSettings
import yaml

from exceptions import ConfigError
from enums import EnvVarNames


log = logging.getLogger(__name__)
DEFAULT_CONFIG_FILE_PATH = "../config-default.yaml"


class MainServiceConfig(BaseConfig):
    auth_route: str
    refresh_token_route: str
    token_refresh_time_seconds: int


def yaml_config_settings_source(_: BaseSettings) -> dict[str, Any]:
    """
    Settings source that loads variables from a YAML file
    """
    env_config_file_path = os.getenv(EnvVarNames.config_file_path, None)
    if env_config_file_path is None:
        log.warning(
            f"Couldn't load {EnvVarNames.config_file_path} env var,"
            f"trying default config path"
        )
    config_file_path = env_config_file_path or DEFAULT_CONFIG_FILE_PATH

    try:
        with open(Path(config_file_path), "r") as f:
            config_dict = yaml.safe_load(f)
    except Exception:
        error_msg = "Error loading config file, perhaps config path is invalid"
        log.error(error_msg)
        raise ConfigError(error_msg)

    return config_dict


class _ConfigAggregator(BaseConfig):
    """
    Class contains all other config references
    Is not meant do be used directly
    Used mainly for easier pydantic config file loading
    """

    main_service_config: MainServiceConfig

    @classmethod
    def customise_sources(
        cls,
        init_settings,
        env_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            yaml_config_settings_source,
            env_settings,
            file_secret_settings,
        )


main_service_config = _ConfigAggregator().main_service_config

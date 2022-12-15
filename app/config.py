from pathlib import Path
import logging

from pydantic import BaseModel, validator

from helpers import get_config_from_yaml, get_app_config_file_path


log = logging.getLogger(__name__)
DEFAULT_CONFIG_FILE_PATH = "../config-default.yaml"


class MainServiceConfig(BaseModel):
    auth_route: str
    refresh_token_route: str
    token_refresh_time_seconds: int


class EnvironmentConfig(BaseModel):
    dev_mode: bool
    use_local_mm_config: bool
    local_mm_config_path: Path

    @validator("local_mm_config_path")
    def convert_to_path_object(cls, v):
        try:
            target_path = Path(v)
        except Exception:
            error_msg = "Can not convert local mm config path into the Path object"
            log.error(error_msg)
            raise ValueError(error_msg)
        return target_path


class _ConfigAggregator(BaseModel):
    """
    Class contains all other config references
    Is not meant do be used directly
    Used mainly for easier pydantic config file loading
    """

    main_service_config: MainServiceConfig
    env_config: EnvironmentConfig

    class Config:
        config_path = get_app_config_file_path()

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                get_config_from_yaml,
                env_settings,
                file_secret_settings,
            )


def initialize_global_config() -> None:
    global main_service_config
    global env_config

    _config_aggregator = _ConfigAggregator.parse_obj(
        get_config_from_yaml(get_app_config_file_path())
    )
    main_service_config = _config_aggregator.main_service_config
    env_config = _config_aggregator.env_config


main_service_config: MainServiceConfig
env_config: EnvironmentConfig

initialize_global_config()

import logging

from pydantic import BaseModel, config

from config import env_config
from helpers import get_config_from_yaml


log = logging.getLogger(__name__)


class ValidationConfig(BaseModel):
    max_mmr: int
    min_mmr: int


class ClassesConfig(BaseModel):
    pass


class MatchmakingConfig:
    classes: ClassesConfig
    validation: ValidationConfig


class MatchmakingConfigRemote(MatchmakingConfig, BaseModel):
    pass


class MatchmakingConfigLocal(MatchmakingConfig, BaseModel):
    pass


class MatchmakingConfigHandler:
    @classmethod
    def generate_from_local_file(cls) -> MatchmakingConfigLocal:
        config_path = env_config.local_mm_config_path
        config_dict = get_config_from_yaml(config_path)
        return MatchmakingConfigLocal.parse_obj(config_dict)
        

    @classmethod
    def generate_from_dict(cls, config: dict) -> MatchmakingConfig:
        return MatchmakingConfigRemote.parse_obj(config)


    @classmethod
    def update_config(cls, new_config: dict):
        global config
        config = MatchmakingConfigRemote.parse_obj(new_config)


matchmaking_config = MatchmakingConfigHandler.generate_from_local_file()

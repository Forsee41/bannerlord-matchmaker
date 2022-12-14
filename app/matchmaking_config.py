from typing import Any

from pydantic import BaseModel, Field



class ValidationConfig(BaseModel):
    max_mmr: int
    min_mmr: int


class ClassesConfig(BaseModel):
    pass


class MatchmakingConfig(BaseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.__handler = ConfigHandler

    classes: ClassesConfig
    validation: ValidationConfig

    def update_global_config(self, new_config: dict) -> None:
        self.__handler.update_config(new_config)



class ConfigHandler:
    @classmethod
    def generate_from_dict(cls, config: dict) -> MatchmakingConfig:
        return MatchmakingConfig.parse_obj(config)

    @classmethod
    def update_config(cls, new_config: dict):
        global config
        config = MatchmakingConfig.parse_obj(new_config)


matchmaking_config = ConfigHandler.generate_from_dict({})

import logging

from pydantic import BaseModel

from config import env_config
from helpers import get_config_from_json
from enums import MapType


log = logging.getLogger(__name__)


class ClassesConfig(BaseModel):
    pass


class Map(BaseModel):
    name: str
    type: MapType
    weight: int

class Faction(str):
    pass


class Matchup(BaseModel):
    fac1: Faction
    fac2: Faction
    weight: int


class MatchupConfig(BaseModel):
    maps: list[Map]
    factions: list[str]
    matchup_weights: dict[str, list[Matchup]]
    matchup_weight_defaults: dict[MapType, list[Matchup]]


class BalanceConfig(BaseModel):
    open_map_max_cav: int
    open_map_max_arch: int
    close_map_max_cav: int
    close_map_max_arch: int


class MatchmakingConfig(BaseModel):
    classes: ClassesConfig
    matchups: MatchupConfig
    balance: BalanceConfig


class MatchmakingConfigHandler:
    @classmethod
    def generate_from_local_file(cls) -> MatchmakingConfig:
        config_path = env_config.local_mm_config_path
        config_dict = get_config_from_json(config_path)
        return MatchmakingConfig.parse_obj(config_dict)

    @classmethod
    def generate_from_dict(cls, config: dict) -> MatchmakingConfig:
        return MatchmakingConfig.parse_obj(config)

    @classmethod
    def update_config(cls, data: dict) -> None:
        global config
        new_conf = config.copy(update=data)
        # changing an existing mutable object will allow to dynamically
        # change the config in a runtime since no new objects are created
        config.classes = new_conf.classes
        config.matchups = new_conf.matchups
        config.balance = new_conf.balance


config = MatchmakingConfigHandler.generate_from_local_file()

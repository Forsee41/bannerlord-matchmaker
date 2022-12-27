import logging

from pydantic import BaseModel

from app.config import env_config
from app.helpers import get_config_from_json
from app.enums import MapType as MapTypeEnum, PlayerRole, Proficiency


log = logging.getLogger(__name__)


class ClassLimitations(BaseModel):
    max_cav: int
    max_arch: int
    max_inf: int
    min_cav: int
    min_arch: int
    min_inf: int


class Faction(str):
    pass


class Matchup(BaseModel):
    fac1: Faction
    fac2: Faction
    weight: int


class MapType(BaseModel):
    matchups: list[Matchup]
    class_limitations: ClassLimitations


class Map(BaseModel):
    name: str
    type: MapTypeEnum
    weight: int
    class_limitations: ClassLimitations | None = None
    matchups: list[Matchup] | None = None


class SwapCategory(BaseModel):
    from_role: Proficiency
    to_role: Proficiency


class Roles(BaseModel):
    swap_priority: list[SwapCategory]


class MatchmakingConfig(BaseModel):
    map_types: dict[MapTypeEnum, MapType]
    maps: list[Map]
    factions: list[Faction]
    roles: Roles


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
        config.map_types = new_conf.map_types
        config.maps = new_conf.maps
        config.factions = new_conf.factions


config = MatchmakingConfigHandler.generate_from_local_file()

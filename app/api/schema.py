from pydantic import BaseModel, Field

from ..enums import PlayerClass
from ..matchmaking_config import MatchmakingConfig as MMConfig
import matchmaking_config


config = matchmaking_config.config_instance


class Player(BaseModel):
    mmr: int = Field(gt=1)
    main: PlayerClass


    class Config:
        use_enum_values = True



class MatchmakingConfig(MMConfig):
    """Lookup to an actual config class"""
    pass


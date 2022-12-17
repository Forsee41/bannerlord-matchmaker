from pydantic import BaseModel, Field

from matchmaking_config import MatchmakingConfig as MMConfig
from enums import PlayerClass
import matchmaking_config


config = matchmaking_config.matchmaking_config


class PlayerModel(BaseModel):
    id: str
    mmr: int
    main: PlayerClass = Field(alias="mainClass")
    secondary: PlayerClass = Field(alias="secondaryClass")
    nickname: str
    discord_id: str = Field(alias="discordId")
    clan: str
    top: str = Field(alias="position")
    matches: int = Field(alias="played")
    wins: int
    winrate: float = Field(alias="wr")
    rounds: int
    assists: int
    sr: float
    mvp: int
    kills: int
    ar: float
    kr: float
    mvp_rate: float = Field(alias="mvpr")
    score: float
    igl: bool
    country: str
    kar: float
    deaths: int
    kd: float
    kda: float
    dr: float
    rank: int

    class Config:
        use_enum_values = True


class PlayerReponseModel(BaseModel):
    ...


class MatchmakingConfig(MMConfig):
    """Lookup to an actual config class"""

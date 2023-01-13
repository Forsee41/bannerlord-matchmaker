from pydantic import BaseModel

from app.enums import PatreonRole, PlayerRole
from app.matchmaking_config import MatchmakingConfig as MMConfig


class PlayerModel(BaseModel):
    id: str
    mmr: int
    cav: int
    inf: int
    arch: int
    igl: bool
    patreon: PatreonRole


class PlayerReponseModel(BaseModel):
    id: str
    role: PlayerRole
    mmr_raw: int
    mmr: int
    igl: bool


class MatchmakingConfig(MMConfig):
    """Lookup to an actual config class"""

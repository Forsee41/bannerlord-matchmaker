from pydantic import BaseModel

from app.enums import PatreonRole, PlayerRole
from app.matchmaking_config import Faction
from app.matchmaking_config import MatchmakingConfig as MMConfig


class PlayerModel(BaseModel):
    id: str
    mmr: int
    cav: int
    inf: int
    arch: int
    igl: bool
    patreon: PatreonRole = PatreonRole.patreon_0


class PlayerReponseModel(BaseModel):
    id: str
    role: PlayerRole
    role_proficiency: int
    mmr_raw: int
    mmr: int


class TeamResponseModel(BaseModel):
    players: list[PlayerReponseModel]
    igl_id: str
    avg_mmr: float


class GameResponseModel(BaseModel):
    team1: TeamResponseModel
    team2: TeamResponseModel
    avg_mmr_diff: float
    map: str
    faction1: Faction
    faction2: Faction


class MatchmakerResponeModel(BaseModel):
    undistributed_player_ids: list[str]
    games: list[GameResponseModel]


class MatchmakingConfig(MMConfig):
    """Lookup to an actual config class"""

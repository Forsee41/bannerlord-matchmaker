from enum import Enum
from matchmaker.player import Player
from enums import PlayerRole
from src.matchmaking_config import ClassLimitations


class RolePicker:
    def __init__(self, players: list[Player]) -> None:
        self.players = players


class RolePickerRule:
    def __init__(self, role: PlayerRole, boundary_per_team: int) -> None:
        self.role = role
        self.boundary = boundary_per_team * 2

    def _count_role_players(self, players: list[Player]) -> int:
        current_role_players = [
            player for player in players if player.current_class == self.role
        ]
        return len(current_role_players)


class MaxPlayersForClassRule(RolePickerRule):
    def check_players(self, players: list[Player]) -> bool:
        role_players_sum = self._count_role_players(players)
        if role_players_sum <= self.boundary:
            return True
        return False


class MinPlayersForClassRule(RolePickerRule):
    def check_players(self, players: list[Player]) -> bool:
        role_players_sum = self._count_role_players(players)
        if role_players_sum >= self.boundary:
            return True
        return False


class LimitationType(str, Enum):
    max = "max"
    min = "min"


class RolePickingRulesFactory:
    def __init__(self, limits: ClassLimitations) -> None:
        self.limits = limits

    def create_rule(
        self, limit_type: LimitationType, role: PlayerRole
    ) -> RolePickerRule:
        max_limitation_role_mapping = {
            PlayerRole.inf: self.limits.max_inf,
            PlayerRole.arch: self.limits.max_arch,
            PlayerRole.cav: self.limits.max_cav,
        }
        min_limitation_role_mapping = {
            PlayerRole.inf: self.limits.min_inf,
            PlayerRole.arch: self.limits.min_arch,
            PlayerRole.cav: self.limits.min_cav,
        }
        if limit_type == LimitationType.max:
            limit = max_limitation_role_mapping[role]
            return MaxPlayersForClassRule(role=role, boundary_per_team=limit)
        limit = min_limitation_role_mapping[role]
        return MinPlayersForClassRule(role=role, boundary_per_team=limit)

from enum import Enum
from typing import NamedTuple
from matchmaker.player import Player
from enums import PlayerRole
from src.matchmaking_config import ClassLimitations, SwapCategory


class PlayerRoleSwappingOrder(NamedTuple):
    from_role: list[Player]
    to_role: list[Player]


class RolePicker:
    def __init__(
        self, players: list[Player], swap_priority: list[SwapCategory]
    ) -> None:
        self.players = players
        self.swap_priority = swap_priority

    def get_mains(self, role: PlayerRole) -> list[Player]:
        return list([player for player in self.players if player.main == role])

    def get_flexes(self, role: PlayerRole) -> list[Player]:
        return list([player for player in self.players if role in player.flexes])

    def get_secondaries(self, role: PlayerRole) -> list[Player]:
        return list([player for player in self.players if player.second == role])

    def get_offclassers(self, role: PlayerRole) -> list[Player]:
        return list([player for player in self.players if player.offclass == role])

    def _find_best_role_replacements(
        self, from_role: PlayerRole, to_role: PlayerRole, amount: int
    ) -> list[Player]:
        players_to_swap: list[Player] = []
        considered_players = list(
            [player for player in self.players if player.current_role == from_role]
        )
        for swap_category in self.swap_priority:
            swap_category_matching_players = list(
                [
                    player
                    for player 
                    in considered_players
                    if player.get_role_proficiency(from_role) == swap_category.from_role
                    and player.get_role_proficiency(to_role) == swap_category.to_role
                ]
            )
            swap_category_matching_players.sort(reverse=True)
            for player in swap_category_matching_players:
                players_to_swap.append(player)
                if len(players_to_swap) == amount:
                    return players_to_swap
        return players_to_swap


class RolePickerRule:
    def __init__(self, role: PlayerRole, boundary_per_team: int) -> None:
        self.role = role
        self.boundary = boundary_per_team * 2

    def _count_role_players(self, players: list[Player]) -> int:
        current_role_players = [
            player for player in players if player.current_role == self.role
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

from __future__ import annotations

from abc import ABC, abstractmethod

from app.enums import PlayerRole
from app.matchmaker.player_pool import PlayerPool
from app.matchmaking_config import ClassLimitations, Map, MatchmakingConfig


class RoleLimitationRule(ABC):
    """
    Represents restraining rule for Role Picker. Has either upper or lower
    class limit as a boundary.
    Implements methods to check passed players for the rule compliance and to
    recieve an amount of possible/required swaps from/into the role.
    """

    def __init__(self, role: PlayerRole, boundary_per_team: int) -> None:
        self.role = role
        self.boundary = boundary_per_team * 2

    def _count_role_players(self, players: PlayerPool) -> int:
        return players.get_role_players_amount(self.role)

    @abstractmethod
    def get_swaps_from_role_amount(self, players: PlayerPool) -> int:
        ...

    @abstractmethod
    def get_swaps_into_role_amount(self, players: PlayerPool) -> int:
        ...


class RolePickingRules:
    """
    Contains swapping rules. Has min and max rule categories.
    """

    def __init__(self) -> None:
        self.min = {}
        self.max = {}

    min: dict[PlayerRole, MinPlayersForClassRule]
    max: dict[PlayerRole, MaxPlayersForClassRule]


class MaxPlayersForClassRule(RoleLimitationRule):
    def check_players(self, players: PlayerPool) -> bool:
        role_players_sum = self._count_role_players(players)
        if role_players_sum <= self.boundary:
            return True
        return False

    def get_swaps_from_role_amount(self, players: PlayerPool) -> int:
        role_players_sum = self._count_role_players(players)
        swaps_amount = role_players_sum - self.boundary
        return swaps_amount if swaps_amount > 0 else 0

    def get_swaps_into_role_amount(self, players: PlayerPool) -> int:
        role_players_sum = self._count_role_players(players)
        swaps_amount = self.boundary - role_players_sum
        return swaps_amount if swaps_amount > 0 else 0


class MinPlayersForClassRule(RoleLimitationRule):
    def check_players(self, players: PlayerPool) -> bool:
        role_players_sum = self._count_role_players(players)
        if role_players_sum >= self.boundary:
            return True
        return False

    def get_swaps_from_role_amount(self, players: PlayerPool) -> int:
        role_players_sum = self._count_role_players(players)
        swaps_amount = self.boundary - role_players_sum
        return swaps_amount if swaps_amount > 0 else 0

    def get_swaps_into_role_amount(self, players: PlayerPool) -> int:
        role_players_sum = self._count_role_players(players)
        swaps_amount = role_players_sum - self.boundary
        return swaps_amount if swaps_amount > 0 else 0


class RolePickingRulesFactory:
    """
    Creates role picker rules using the limits config dict.
    """

    def __init__(self, limits: ClassLimitations) -> None:
        self.limits = limits

    def _create_min_rule(self, role: PlayerRole) -> MinPlayersForClassRule:
        min_limitation_role_mapping = {
            PlayerRole.inf: self.limits.min_inf,
            PlayerRole.arch: self.limits.min_arch,
            PlayerRole.cav: self.limits.min_cav,
        }
        limit = min_limitation_role_mapping[role]
        return MinPlayersForClassRule(role=role, boundary_per_team=limit)

    def _create_max_rule(self, role: PlayerRole) -> MaxPlayersForClassRule:
        max_limitation_role_mapping = {
            PlayerRole.inf: self.limits.max_inf,
            PlayerRole.arch: self.limits.max_arch,
            PlayerRole.cav: self.limits.max_cav,
        }
        limit = max_limitation_role_mapping[role]
        return MaxPlayersForClassRule(role=role, boundary_per_team=limit)

    def populate_rules(self, rules_preset: RolePickingRules) -> RolePickingRules:
        """
        Takes a RolePickingRules empty preset
        and populates it using the factory's limits
        """
        for role in PlayerRole:
            rules_preset.min[role] = self._create_min_rule(role=role)
            rules_preset.max[role] = self._create_max_rule(role=role)
        return rules_preset

    def create_rules(self) -> RolePickingRules:
        """
        Returns populated RoleSwappingRules object.
        Uses the factory's limits as rules boundaries.
        """
        rules = RolePickingRules()
        self.populate_rules(rules)
        return rules


class RoleLimitsConfigRetriever:
    def __init__(self, config: MatchmakingConfig) -> None:
        self.config = config

    def get_map_role_limits(self, map: Map) -> ClassLimitations:
        if map.class_limitations is None:
            return self.config.map_types[map.type].class_limitations
        return map.class_limitations

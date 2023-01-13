from __future__ import annotations

import itertools
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import total_ordering

from app.enums import PlayerRole
from app.matchmaker.player import Player
from app.matchmaker.player_pool import PlayerPool
from app.matchmaking_config import ClassLimitations

log = logging.getLogger(__name__)


@total_ordering
@dataclass(order=False)
class RoleSwap:
    """
    A class representing player's role swap. Contains a player object,
    config and a target role.
    Implements total ordering comparision to easily sort a list
    of swaps and compare one another.

    Config (swap priority) has to be manually passed into the constructor.
    Use RoleSwapFactory to avoid it.

    All swaps comparision logic is incapsulated here.
    It does not respect class limits since it doesn't know of them.
    """

    player: Player
    to_role: PlayerRole
    avg_mmr: float

    def __post_init__(self) -> None:
        if self.player.current_role == self.to_role:
            raise ValueError(
                "Role swap target role should not be the"
                " same as the player's current role"
            )
        self.from_role = self.player.current_role

    @property
    def is_promotion(self) -> bool:
        return self.swap_score > 0

    @property
    def current_role(self) -> PlayerRole:
        return self.player.current_role

    @property
    def swap_score(self) -> float:
        target_role_prof = self.player.get_role_proficiency(self.to_role)
        from_role_prof = self.player.get_role_proficiency(self.from_role)
        return target_role_prof - from_role_prof

    @property
    def is_swapped(self) -> bool:
        return self.player.current_role == self.to_role

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, RoleSwap):
            return NotImplemented
        return all(
            (
                self.player.get_role_proficiency(self.player.current_role)
                == __o.player.get_role_proficiency(self.player.current_role),
                self.player.get_role_proficiency(self.to_role)
                == __o.player.get_role_proficiency(self.to_role),
                self.player.mmr == __o.player.mmr,
            )
        )

    def __gt__(self, __o: object) -> bool:
        if not isinstance(__o, RoleSwap):
            return NotImplemented
        return self.swap_score > __o.swap_score

    def apply(self) -> None:
        self.player.current_role = self.to_role

    def revert(self) -> None:
        self.player.current_role = self.from_role


class RolePickerRule:
    pass


class RoleLimitationRule(ABC, RolePickerRule):
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
        current_role_players = [
            player for player in players if player.current_role == self.role
        ]
        return len(current_role_players)

    @abstractmethod
    def get_swaps_from_role_amount(self, players: PlayerPool) -> int:
        ...

    @abstractmethod
    def get_swaps_into_role_amount(self, players: PlayerPool) -> int:
        ...


class RoleSwappingRules:
    """
    A dict of swapping rules. Rule is accessed via a key of a limit_type - role tuple.
    Has a convenience add_rule method.
    """

    def __init__(self) -> None:
        self.min = {}
        self.max = {}
        self.fill = {}

    min: dict[PlayerRole, MinPlayersForClassRule]
    max: dict[PlayerRole, MaxPlayersForClassRule]
    fill: dict[PlayerRole, FillClassRule]


@dataclass
class RoleSwapFactory:
    """
    Easens role swaps constructing. Automatically passes the stored config into
    the swaps. Requires the config in it's constructor
    """

    avg_mmr: float = 0

    def set_avg_mmr(self, avg_mmr: float) -> None:
        self.avg_mmr = avg_mmr

    def __call__(self, player: Player, target_role: PlayerRole) -> RoleSwap:
        return RoleSwap(
            player=player,
            to_role=target_role,
            avg_mmr=self.avg_mmr,
        )


class RolePicker:
    """
    Incapsulates the logic of choosing player's roles.
    set_player_roles is a main interface method that returns a list of players
    with choosen roles.

    Requires a list of 12 players, a set of rules and a role swap factory.
    """

    def __init__(
        self,
        players: PlayerPool,
        swap_factory: RoleSwapFactory,
        rules: RoleSwappingRules,
    ) -> None:
        self.players = players
        self.swap_factory = swap_factory
        self.swap_factory.set_avg_mmr(self.players.avg_mmr)
        self.rules = rules
        self.target_cav_amount = self.rules.max[PlayerRole.cav].boundary
        self.target_arch_amount = self.rules.max[PlayerRole.arch].boundary
        self.target_inf_amount = 12 - self.target_cav_amount - self.target_arch_amount

    def set_player_roles(self) -> PlayerPool:
        """
        Sets the players roles and returns a player list with
        applied changes
        """
        self._set_target_role_players_amounts()
        self.manage_player_roles()
        return self.players

    def manage_player_roles(self) -> PlayerPool:
        """
        Sets the player roles based on current
        target players amounts for each role

        Swaps players until target amount of players for
        each role is satisfied.
        """
        swaps = self._create_all_swaps()
        swapped_players: list[Player] = []

        for swap in swaps:
            if swap.player in swapped_players:
                continue
            start_unsatisfied_slots = self._get_target_unsatisfied_slots_amount()
            swap.apply()
            result_unsatisfied_slots = self._get_target_unsatisfied_slots_amount()
            if result_unsatisfied_slots > start_unsatisfied_slots:
                swap.revert()
            else:
                swapped_players.append(swap.player)

        return self.players

    def _create_all_swaps(self) -> list[RoleSwap]:
        """Creates all possible swaps of players, 24 in total"""
        swaps = []
        for player in self.players:
            target_roles = self._swapping_targets_map[player.current_role]
            swaps.append(self.swap_factory(player, target_roles[0]))
            swaps.append(self.swap_factory(player, target_roles[1]))
        swaps.sort(reverse=True)
        return swaps

    def _get_rule_unsatisfied_slots_amount(self) -> int:
        """Finds a sum of slots, required to get changed by rules"""
        result = 0
        for role in PlayerRole:
            role_max_limit_diff = (
                self.players.get_role_players_amount(role)
                - self.rules.max[role].boundary
            )
            result += role_max_limit_diff if role_max_limit_diff > 0 else 0

            role_min_limit_diff = self.rules.min[
                role
            ].boundary - self.players.get_role_players_amount(role)
            result += role_min_limit_diff if role_min_limit_diff > 0 else 0
        return result

    def _get_target_unsatisfied_slots_amount(self) -> int:
        """FInds a sum of slots, required to get changed by current targets"""
        result = 0
        result += abs(
            self.players.get_role_players_amount(PlayerRole.cav)
            - self.target_cav_amount
        )
        result += abs(
            self.players.get_role_players_amount(PlayerRole.inf)
            - self.target_inf_amount
        )
        result += abs(
            self.players.get_role_players_amount(PlayerRole.arch)
            - self.target_arch_amount
        )
        log.debug(f"Unsatisfied slots: {result}")

        return result

    def _calculate_current_score(self) -> float:
        """
        Calculates a 'score' for current target slots, respecting cav and arch
        fills. Used to find the best possible target players amounts for each role,
        since checking for rules compliance is not respecting cav and arch fills
        """
        score = self._get_rule_unsatisfied_slots_amount()
        if not self.rules.fill[PlayerRole.cav] and not self.rules.fill[PlayerRole.arch]:
            return score
        max_cav_rule = self.rules.max[PlayerRole.cav]
        min_cav_rule = self.rules.min[PlayerRole.cav]
        if (
            self.players.check_odd_role_players_amount(PlayerRole.cav)
            and max_cav_rule.check_players(self.players)
            and min_cav_rule.check_players(self.players)
        ):
            current_cav = self.players.get_role_players_amount(PlayerRole.cav)
            ideal_cav_amount = (
                current_cav + 1 if self.rules.fill[PlayerRole.cav] else current_cav - 1
            )
            if self.target_cav_amount != ideal_cav_amount:
                return score + 0.5
        max_arch_rule = self.rules.max[PlayerRole.arch]
        min_arch_rule = self.rules.min[PlayerRole.arch]
        if (
            self.players.check_odd_role_players_amount(PlayerRole.arch)
            and max_arch_rule.check_players(self.players)
            and min_arch_rule.check_players(self.players)
        ):
            current_arch = self.players.get_role_players_amount(PlayerRole.arch)
            ideal_arch_amount = (
                current_arch + 1
                if self.rules.fill[PlayerRole.cav]
                else current_arch - 1
            )
            if self.target_arch_amount != ideal_arch_amount:
                return score + 0.5
        return score

    def _set_target_role_players_amounts(self):
        """
        Finds the best permutation of target slots for each role, using the current
        players' roles, cav/arch fills and rules' boundaries
        """
        possible_roles_distributions = [
            (12, 0, 0),
            (10, 2, 0),
            (8, 4, 0),
            (8, 2, 2),
            (6, 4, 2),
            (6, 6, 0),
        ]
        best_permutation = (
            self.target_cav_amount,
            self.target_inf_amount,
            self.target_arch_amount,
        )
        best_score = self._calculate_current_score()
        for role_distribution in possible_roles_distributions:
            for permutation in itertools.permutations(role_distribution):
                self.target_cav_amount = permutation[0]
                self.target_inf_amount = permutation[1]
                self.target_arch_amount = permutation[2]
                score = self._calculate_current_score()
                if score < best_score:
                    best_permutation = permutation
                    best_score = score
        self.target_cav_amount = best_permutation[0]
        self.target_inf_amount = best_permutation[1]
        self.target_arch_amount = best_permutation[2]
        log.debug(
            f"Target cav: {self.target_cav_amount}"
            f"Target inf: {self.target_inf_amount}"
            f"Target arch: {self.target_arch_amount}"
        )

    _swapping_targets_map = {
        PlayerRole.cav: [PlayerRole.inf, PlayerRole.arch],
        PlayerRole.inf: [PlayerRole.cav, PlayerRole.arch],
        PlayerRole.arch: [PlayerRole.inf, PlayerRole.cav],
    }


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


@dataclass
class FillClassRule(RolePickerRule):
    value: bool
    role: PlayerRole

    def __bool__(self):
        return self.value


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

    def _create_fill_rule(self, role: PlayerRole) -> FillClassRule:
        fill_rules_mapping = {
            PlayerRole.inf: False,
            PlayerRole.arch: self.limits.fill_arch,
            PlayerRole.cav: self.limits.fill_cav,
        }
        value = fill_rules_mapping[role]
        return FillClassRule(role=role, value=value)

    def _create_max_rule(self, role: PlayerRole) -> MaxPlayersForClassRule:
        max_limitation_role_mapping = {
            PlayerRole.inf: self.limits.max_inf,
            PlayerRole.arch: self.limits.max_arch,
            PlayerRole.cav: self.limits.max_cav,
        }
        limit = max_limitation_role_mapping[role]
        return MaxPlayersForClassRule(role=role, boundary_per_team=limit)

    def populate_rules(self, rules_preset: RoleSwappingRules) -> RoleSwappingRules:
        """
        Takes a RoleSwappingRules empty preset
        and populates it using the factory's limits
        """
        for role in PlayerRole:
            rules_preset.min[role] = self._create_min_rule(role=role)
            rules_preset.max[role] = self._create_max_rule(role=role)
            rules_preset.fill[role] = self._create_fill_rule(role=role)
        return rules_preset

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import NamedTuple

from app.enums import PlayerRole
from app.matchmaker.player import Player
from app.matchmaking_config import ClassLimitations, SwapCategory


class PlayerRoleSwappingOrder(NamedTuple):
    from_role: list[Player]
    to_role: list[Player]


class LimitationType(str, Enum):
    max = "max"
    min = "min"


@total_ordering
@dataclass(order=False)
class RoleSwap:
    player: Player
    to_role: PlayerRole
    swap_priority: list[SwapCategory]

    @property
    def current_role(self) -> PlayerRole:
        return self.player.current_role

    def __eq__(self, __o: RoleSwap) -> bool:
        return all(
            (
                self.player.get_role_proficiency(self.player.current_role)
                == __o.player.get_role_proficiency(self.player.current_role),
                self.player.get_role_proficiency(self.to_role)
                == __o.player.get_role_proficiency(self.to_role),
                self.player.mmr == __o.player.mmr,
            )
        )

    def __gt__(self, __o: RoleSwap) -> bool:
        for swap_category in self.swap_priority:
            other_matching_category: bool = (
                __o.player.current_role == swap_category.from_role
                and __o.to_role == swap_category.to_role
            )
            self_matching_cagegory: bool = (
                self.player.current_role == swap_category.from_role
                and self.to_role == swap_category.to_role
            )
            if self_matching_cagegory and not other_matching_category:
                return True
            if other_matching_category and not self_matching_cagegory:
                return False
            if self_matching_cagegory and other_matching_category:
                if swap_category.desc_mmr_sort:
                    return self.player.mmr > __o.player.mmr
                else:
                    return self.player.mmr < __o.player.mmr

        # there will always be at least 1 match in swap categories,
        # but LSP is not happy about conditional returns,
        # added bool return that will never be reached
        return False

    def apply(self) -> None:
        self.player.current_role = self.to_role


class RolePickerRule(ABC):
    def __init__(self, role: PlayerRole, boundary_per_team: int) -> None:
        self.role = role
        self.boundary = boundary_per_team * 2

    def _count_role_players(self, players: list[Player]) -> int:
        current_role_players = [
            player for player in players if player.current_role == self.role
        ]
        return len(current_role_players)

    @abstractmethod
    def get_swaps_from_role_amount(self, players: list[Player]) -> int:
        ...

    @abstractmethod
    def get_swaps_into_role_amount(self, players: list[Player]) -> int:
        ...


class RoleSwappingRules(dict):
    def add_rule(
        self, limit_type: LimitationType, role: PlayerRole, rule: RolePickerRule
    ) -> None:
        self[(limit_type, role)] = rule


@dataclass
class RoleSwapFactory:
    swap_priority: list[SwapCategory]

    def __call__(self, player: Player, target_role: PlayerRole) -> RoleSwap:
        return RoleSwap(
            player=player, to_role=target_role, swap_priority=self.swap_priority
        )


@dataclass
class RolePicker:

    players: list[Player]
    swap_factory: RoleSwapFactory
    rules: RoleSwappingRules
    fill_cav: bool
    fill_arch: bool

    _swapping_targets_map = {
        PlayerRole.cav: [PlayerRole.inf, PlayerRole.arch],
        PlayerRole.inf: [PlayerRole.cav, PlayerRole.arch],
        PlayerRole.arch: [PlayerRole.inf, PlayerRole.cav],
    }

    def set_player_roles(self) -> list[Player]:
        self._manage_cav()
        self._manage_arch()
        self._manage_inf()
        self._fix_odd_cav_arch()
        return self.players

    def _manage_inf(self) -> None:
        max_limit_rule = self.rules[LimitationType.max, PlayerRole.cav]
        min_limit_rule = self.rules[LimitationType.min, PlayerRole.cav]
        if min_limit_rule.check_players() and max_limit_rule.check_player():
            return
        if not min_limit_rule.check_players():
            swapping_players_amount = min_limit_rule.get_swaps_into_role_amount()
            swaps = self._find_best_swaps_to_role(
                PlayerRole.inf, swapping_players_amount
            )
            for swap in swaps:
                swap.apply()

        if max_limit_rule.check_players():
            return
        swapping_players_amount = max_limit_rule.get_swaps_from_role_amount()

        # since _find_best_target_role only respects the current amount of
        # players on a possible target roles, have to find best swaps 1 by 1
        for swap in range(swapping_players_amount):
            self._find_best_swaps_from_role(PlayerRole.inf, 1)[0].apply()

    def _manage_cav_fills(self):
        max_limit_rule = self.rules[LimitationType.max, PlayerRole.cav]
        min_limit_rule = self.rules[LimitationType.min, PlayerRole.cav]

        if max_limit_rule.check_players(self.players) and min_limit_rule.check_players(
            self.players
        ):
            if not len(self._find_role_players(PlayerRole.cav)) % 2 == 1:
                return
            if self.fill_cav:
                self._find_best_swaps_to_role(
                    to_role=PlayerRole.cav, swapping_players_amount=1
                )[0].apply()
            else:
                self._find_best_swaps_from_role(
                    role=PlayerRole.cav, swapping_players_amount=1
                )[0].apply()
            return

    def _fix_odd_cav_arch(self) -> None:
        cav_needs_fix = False
        arch_needs_fix = False
        if len(self._find_role_players(PlayerRole.cav)) % 2 == 1:
            cav_needs_fix = True
        if len(self._find_role_players(PlayerRole.arch)) % 2 == 1:
            arch_needs_fix = True
        arch_inf_swap = self._find_best_role_to_role_swaps(
            PlayerRole.arch, PlayerRole.inf, 1
        )[0]
        arch_cav_swap = self._find_best_role_to_role_swaps(
            PlayerRole.arch, PlayerRole.cav, 1
        )[0]
        cav_arch_swap = self._find_best_role_to_role_swaps(
            PlayerRole.cav, PlayerRole.arch, 1
        )[0]
        cav_inf_swap = self._find_best_role_to_role_swaps(
            PlayerRole.cav, PlayerRole.inf, 1
        )[0]
        if cav_needs_fix and arch_needs_fix:
            possible_swaps = [cav_arch_swap, arch_cav_swap, cav_inf_swap, arch_inf_swap]
            possible_swaps.sort(reverse=True)
            best_swap = possible_swaps[0]
            if best_swap.to_role == PlayerRole.inf:
                arch_inf_swap.apply()
                cav_inf_swap.apply()
            else:
                best_swap.apply()
            return
        if cav_needs_fix:
            cav_inf_swap.apply()
        if arch_needs_fix:
            arch_inf_swap.apply()

    def _manage_arch_fills(self) -> None:
        max_limit_rule = self.rules[LimitationType.max, PlayerRole.arch]
        min_limit_rule = self.rules[LimitationType.min, PlayerRole.arch]

        if max_limit_rule.check_players(self.players) and min_limit_rule.check_players(
            self.players
        ):
            if not len(self._find_role_players(PlayerRole.arch)) % 2 == 1:
                return
            if self.fill_arch:
                self._find_best_role_to_role_swaps(
                    from_role=PlayerRole.inf,
                    to_role=PlayerRole.arch,
                    swapping_players_amount=1,
                )[0].apply()
            else:
                self._find_best_role_to_role_swaps(
                    from_role=PlayerRole.arch,
                    to_role=PlayerRole.inf,
                    swapping_players_amount=1,
                )[0].apply()

    def _manage_cav(self) -> None:
        max_limit_rule = self.rules[LimitationType.max, PlayerRole.cav]
        min_limit_rule = self.rules[LimitationType.min, PlayerRole.cav]

        if not max_limit_rule.check_players(self.players):
            required_swaps_from_role = max_limit_rule.get_swaps_from_role_amount(
                self.players
            )
            best_swaps = self._find_best_swaps_from_role(
                PlayerRole.cav, required_swaps_from_role
            )
            for swap in best_swaps:
                swap.apply()

        if not min_limit_rule.check_players(self.players):
            required_swaps_to_role = min_limit_rule.get_swaps_into_role_amount(
                self.players
            )
            best_swaps = self._find_best_swaps_to_role(
                PlayerRole.cav, required_swaps_to_role
            )
            for swap in best_swaps:
                swap.apply()

        self._manage_cav_fills()

    def _manage_arch(self) -> None:
        max_limit_rule = self.rules[LimitationType.max, PlayerRole.arch]
        min_limit_rule = self.rules[LimitationType.min, PlayerRole.arch]

        if not max_limit_rule.check_players(self.players):
            required_swaps_from_role = max_limit_rule.get_swaps_from_role_amount(
                self.players
            )
            best_swaps = self._find_best_role_to_role_swaps(
                PlayerRole.arch, PlayerRole.inf, required_swaps_from_role
            )
            for swap in best_swaps:
                swap.apply()

        if not min_limit_rule.check_players(self.players):
            required_swaps_to_role = min_limit_rule.get_swaps_into_role_amount(
                self.players
            )
            best_swaps = self._find_best_role_to_role_swaps(
                PlayerRole.inf, PlayerRole.arch, required_swaps_to_role
            )
            for swap in best_swaps:
                swap.apply()

        self._manage_arch_fills()

    def _find_role_players(self, role: PlayerRole) -> list[Player]:
        return [player for player in self.players if player.current_role == role]

    def _find_best_swaps_from_role(
        self, role: PlayerRole, swapping_players_amount: int
    ) -> list[RoleSwap]:
        role_players = [
            player for player in self.players if player.current_role == role
        ]
        best_swaps_per_player = [
            self.swap_factory(player, self._find_best_target_role(player))
            for player in role_players
        ]
        best_swaps_per_player.sort(reverse=True)
        return best_swaps_per_player[:swapping_players_amount]

    def _find_best_role_to_role_swaps(
        self, from_role: PlayerRole, to_role: PlayerRole, swapping_players_amount: int
    ) -> list[RoleSwap]:
        from_role_players = [
            player for player in self.players if player.current_role == from_role
        ]
        swaps = [self.swap_factory(player, to_role) for player in from_role_players]
        swaps.sort(reverse=True)
        return swaps[:swapping_players_amount]

    def _find_best_target_role(self, player: Player) -> PlayerRole:
        target_roles = self._swapping_targets_map[player.current_role]
        if (
            self.rules[LimitationType.max, target_roles[0]].get_swaps_into_role_amount
            == 0
        ):
            return target_roles[1]
        if (
            self.rules[LimitationType.max, target_roles[1]].get_swaps_into_role_amount
            == 0
        ):
            return target_roles[0]
        role_swaps = [
            self.swap_factory(player, target_roles[0]),
            self.swap_factory(player, target_roles[1]),
        ]
        role_swaps.sort(reverse=True)
        return role_swaps[0].to_role

    def _find_best_swaps_to_role(
        self,
        to_role: PlayerRole,
        swapping_players_amount: int,
    ) -> list[RoleSwap]:
        result_players: list[RoleSwap] = []
        donor_roles = self._swapping_targets_map[to_role]
        swap_candidates = [
            player for player in self.players if player.current_role != to_role
        ]

        player_swap_list = [
            self.swap_factory(player, to_role) for player in swap_candidates
        ]

        player_swap_list.sort(reverse=True)
        first_donor_category_max_swaps = self.rules[
            LimitationType.min, donor_roles[0]
        ].find_allowed_swaps_amount(self.players)
        second_donor_category_max_swaps = self.rules[
            LimitationType.min, donor_roles[1]
        ].find_allowed_swaps_amount(self.players)

        for player_swap in player_swap_list:
            if (
                player_swap.current_role == donor_roles[0]
                and first_donor_category_max_swaps > 0
            ):
                result_players.append(player_swap)
                first_donor_category_max_swaps -= 1
            elif second_donor_category_max_swaps > 0:
                result_players.append(player_swap)
                second_donor_category_max_swaps -= 1
            if len(result_players) == swapping_players_amount:
                return result_players

        # if role limits are valid, this should never get reached, however LSP is not
        # happy about conditional returns
        return result_players


class MaxPlayersForClassRule(RolePickerRule):
    def check_players(self, players: list[Player]) -> bool:
        role_players_sum = self._count_role_players(players)
        if role_players_sum <= self.boundary:
            return True
        return False

    def get_swaps_from_role_amount(self, players: list[Player]) -> int:
        role_players_sum = self._count_role_players(players)
        swaps_amount = role_players_sum - self.boundary
        return swaps_amount if swaps_amount > 0 else 0

    def get_swaps_into_role_amount(self, players: list[Player]) -> int:
        """Returns an amount of allowed swaps INTO the role"""
        role_players_sum = self._count_role_players(players)
        swaps_amount = self.boundary - role_players_sum
        return swaps_amount if swaps_amount > 0 else 0


class MinPlayersForClassRule(RolePickerRule):
    def check_players(self, players: list[Player]) -> bool:
        role_players_sum = self._count_role_players(players)
        if role_players_sum >= self.boundary:
            return True
        return False

    def get_swaps_from_role_amount(self, players: list[Player]) -> int:
        role_players_sum = self._count_role_players(players)
        swaps_amount = self.boundary - role_players_sum
        return swaps_amount if swaps_amount > 0 else 0

    def get_swaps_into_role_amount(self, players: list[Player]) -> int:
        role_players_sum = self._count_role_players(players)
        swaps_amount = role_players_sum - self.boundary
        return swaps_amount if swaps_amount > 0 else 0


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

    def populate_rules(self, rules_preset: RoleSwappingRules) -> RoleSwappingRules:
        rules = [
            (LimitationType.max, PlayerRole.inf),
            (LimitationType.min, PlayerRole.inf),
            (LimitationType.max, PlayerRole.arch),
            (LimitationType.min, PlayerRole.arch),
            (LimitationType.max, PlayerRole.cav),
            (LimitationType.min, PlayerRole.cav),
        ]
        for limit_type, role in rules:
            rules_preset.add_rule(limit_type, role, self.create_rule(limit_type, role))
        return rules_preset

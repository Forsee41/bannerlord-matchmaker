from __future__ import annotations

import logging

from app.enums import PlayerRole
from app.matchmaker.game.role_picker_rules import RolePickingRules
from app.matchmaker.game.role_swap import RoleSwap, RoleSwapFactory
from app.matchmaker.player_pool import PlayerPool

log = logging.getLogger(__name__)


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
        rules: RolePickingRules,
    ) -> None:
        self.players = players
        self.swap_factory = swap_factory
        self.swap_factory.set_avg_mmr(self.players.avg_mmr)
        self.rules = rules

    def set_player_roles(self) -> PlayerPool:
        """
        Sets the player roles.
        Applies the best possible swaps until the rules are satisfied.
        """

        while self._get_required_swaps_amount() != 0:
            swaps = self._create_all_swaps()
            for swap in swaps:
                start_required_swaps = self._get_required_swaps_amount()
                swap.apply()
                result_required_swaps = self._get_required_swaps_amount()
                if result_required_swaps >= start_required_swaps:
                    swap.revert()
                else:
                    break
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

    def _get_required_swaps_amount(self) -> int:
        """Finds a sum of slots, required to get changed by the rules"""
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

    _swapping_targets_map = {
        PlayerRole.cav: [PlayerRole.inf, PlayerRole.arch],
        PlayerRole.inf: [PlayerRole.cav, PlayerRole.arch],
        PlayerRole.arch: [PlayerRole.inf, PlayerRole.cav],
    }

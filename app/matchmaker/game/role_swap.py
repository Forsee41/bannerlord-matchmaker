from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering

from app.enums import PlayerRole
from app.matchmaker.player import Player


@total_ordering
@dataclass(order=False)
class RoleSwap:
    """
    A class representing player's role swap. Contains a player object,
    a target role and context mmr info, avg_mmr, current mmr deviation and
    and avg mmr deviation.
    Implements total ordering comparision to easily sort a list
    of swaps and compare one another.

    Mmr context has to be manually passed into the constructor.
    Use RoleSwapFactory to automate it.

    All swaps comparision logic is incapsulated here.
    It does not respect class limits since it doesn't know of them.
    """

    player: Player
    to_role: PlayerRole
    avg_mmr: float = 0
    avg_deviation: float = 0
    mmr_deviation: float = 0

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


@dataclass
class RoleSwapFactory:
    """
    Easens role swaps constructing. Automatically passes the stored mmr info into
    the swaps. Requires mmr info in it's constructor
    """

    avg_mmr: float = 0
    mmr_deviation: float = 0
    avg_mmr_deviation: float = 0

    def set_avg_mmr(self, avg_mmr: float) -> None:
        self.avg_mmr = avg_mmr

    def set_mmr_deviation(self, deviation: float) -> None:
        self.mmr_deviation = deviation

    def set_avg_mmr_deviation(self, avg_deviation: float) -> None:
        self.avg_mmr_deviation = avg_deviation

    def __call__(self, player: Player, target_role: PlayerRole) -> RoleSwap:
        return RoleSwap(
            player=player,
            to_role=target_role,
            avg_mmr=self.avg_mmr,
            avg_deviation=self.avg_mmr_deviation,
            mmr_deviation=self.mmr_deviation,
        )

import pytest

from app.matchmaker.player import Player
from app.enums import PlayerRole
from app.matchmaker.game.role_picker import RoleSwap
from app.matchmaking_config import SwapCategory


class TestRoleSwap:
    def test_role_swap_validator_wrong_input(
        self, default_players: list[Player], default_swap_priority: list[SwapCategory]
    ) -> None:
        first_player = default_players[0]
        first_player.current_role = PlayerRole.cav
        with pytest.raises(ValueError):
            RoleSwap(first_player, PlayerRole.cav, default_swap_priority, 10)

    @pytest.mark.parametrize(
        "current,target",
        [
            (PlayerRole.cav, PlayerRole.arch),
            (PlayerRole.cav, PlayerRole.inf),
            (PlayerRole.inf, PlayerRole.cav),
        ],
    )
    def test_role_swap_validator_correct_input(
        self,
        default_players: list[Player],
        default_swap_priority: list[SwapCategory],
        current: PlayerRole,
        target: PlayerRole,
    ) -> None:
        first_player = default_players[0]
        first_player.current_role = current
        swap = RoleSwap(first_player, target, default_swap_priority, 10)
        assert swap

    def test_role_swap_equal_swaps(
        self, default_players: list[Player], default_swap_priority: list[SwapCategory]
    ):
        first_player = default_players[0]
        second_player = default_players[1]
        first_player.mmr_raw = 1000
        second_player.mmr_raw = 1000
        first_player.current_role = PlayerRole.cav
        second_player.current_role = PlayerRole.cav
        second_player._class_proficiency = first_player._class_proficiency
        first_swap = RoleSwap(first_player, PlayerRole.arch, default_swap_priority, 10)
        second_swap = RoleSwap(second_player, PlayerRole.arch, default_swap_priority, 10)
        assert first_swap == second_swap


if __name__ == "__main__":
    pytest.main()

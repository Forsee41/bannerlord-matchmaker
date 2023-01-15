import pytest

from app.enums import PlayerRole
from app.matchmaker.game.role_swap import RoleSwap
from app.matchmaker.player import Player
from app.matchmaker.player_pool import PlayerPool


class TestRoleSwap:
    def test_role_swap_validator_wrong_input(
        self, default_players: list[Player]
    ) -> None:
        first_player = default_players[0]
        first_player.current_role = PlayerRole.cav
        with pytest.raises(ValueError):
            RoleSwap(first_player, PlayerRole.cav, 10)

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
        default_players: PlayerPool,
        current: PlayerRole,
        target: PlayerRole,
    ) -> None:
        first_player = default_players[0]
        first_player.current_role = current
        swap = RoleSwap(first_player, target, 10)
        assert swap

    def test_role_swap_equal_swaps(self, default_players: PlayerPool):
        first_player = default_players[0]
        second_player = default_players[1]
        first_player.mmr_raw = 1000
        second_player.mmr_raw = 1000
        first_player.current_role = PlayerRole.cav
        second_player.current_role = PlayerRole.cav
        second_player._role_proficiency = first_player._role_proficiency
        first_swap = RoleSwap(first_player, PlayerRole.arch, 10)
        second_swap = RoleSwap(second_player, PlayerRole.arch, 10)
        assert first_swap == second_swap

    def test_role_swap_basic_comparision(self, default_players: PlayerPool):
        first_player = next(
            player for player in default_players if player.id == "Quadri"
        )
        second_player = next(
            player for player in default_players if player.id == "Relynar"
        )
        first_swap = RoleSwap(first_player, PlayerRole.cav, 0)
        second_swap = RoleSwap(second_player, PlayerRole.inf, 0)
        swap_comparision = second_swap > first_swap
        assert swap_comparision

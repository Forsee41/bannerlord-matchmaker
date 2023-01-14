from typing import Callable

import pytest

from app.enums import PlayerRole
from app.matchmaker.game.role_picker import RolePicker, RoleSwap
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


class TestRolePicker:
    def test_default_players_no_errors(self, default_role_picker: RolePicker):
        default_role_picker.set_player_roles()
        assert default_role_picker

    def test_picker_changes_roles(self, default_role_picker: RolePicker):
        players = default_role_picker.set_player_roles()
        offclass_counter = 0
        for player in players:
            if player.is_offclass:
                offclass_counter += 1
        assert offclass_counter > 0

    def test_even_role_slots(self, default_role_picker: RolePicker):
        players = default_role_picker.set_player_roles()
        role_slots = {role: 0 for role in PlayerRole}
        for player in players:
            role_slots[player.current_role] += 1
        for slots_amount in role_slots.values():
            assert slots_amount % 2 == 0

    def test_all_cav(self, get_role_picker: Callable[[str], RolePicker]) -> None:
        picker = get_role_picker("all_cav")
        result_playerpool = picker.set_player_roles()
        assert result_playerpool.get_role_players_amount(PlayerRole.cav) == 4


if __name__ == "__main__":
    pytest.main()

from typing import Callable

import pytest

from app.enums import PlayerRole
from app.matchmaker.game.role_picker import RolePicker


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

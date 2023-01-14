from typing import Callable

import pytest

from app.enums import PlayerRole
from app.matchmaker.game.role_picker import RolePicker
from app.matchmaker.player import Player
from app.matchmaker.player_pool import PlayerPool


def test_default_players(default_players: PlayerPool) -> None:
    assert all([isinstance(player, Player) for player in default_players])
    assert len(default_players) == 12
    assert default_players[0] != default_players[1]
    assert isinstance(default_players[0].current_role, PlayerRole)


def test_default_role_picker(default_role_picker: RolePicker):
    assert isinstance(default_role_picker, RolePicker)


def test_role_picker_loads_different_data(get_role_picker: Callable[[str], RolePicker]):
    role_picker_all_cav = get_role_picker("all_cav")
    players = role_picker_all_cav.players
    assert all((player.current_role == PlayerRole.cav for player in players))


if __name__ == "__main__":
    pytest.main()

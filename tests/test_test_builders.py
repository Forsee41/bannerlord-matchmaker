import pytest

from app.enums import PlayerRole
from app.matchmaker.game.role_picker import RolePicker
from app.matchmaker.player import Player


def test_default_players(default_players: list[Player]) -> None:
    assert all([isinstance(player, Player) for player in default_players])
    assert len(default_players) == 12
    assert default_players[0] != default_players[1]
    assert isinstance(default_players[0].current_role, PlayerRole)


def test_default_role_picker(default_role_picker: RolePicker):
    assert isinstance(default_role_picker, RolePicker)


if __name__ == "__main__":
    pytest.main()

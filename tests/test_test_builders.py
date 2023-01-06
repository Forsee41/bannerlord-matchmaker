import pytest

from app.matchmaker.player import Player

from app.enums import PlayerRole


def test_default_players(default_players: list[Player]) -> None:
    assert all([isinstance(player, Player) for player in default_players])
    assert len(default_players) == 12
    assert default_players[0] != default_players[1]
    assert isinstance(default_players[0].current_role, PlayerRole)


if __name__ == "__main__":
    pytest.main()

import json
from pathlib import Path
from typing import Any, Callable

import pytest
from app.matchmaking_config import MatchmakingConfig, MatchmakingConfigHandler, SwapCategory

from app.enums import Proficiency
from app.matchmaker.player import Player, RoleProficiency


@pytest.fixture()
def default_player_testdata() -> list[dict]:
    json_data_path = Path("tests/test_data/default_players.json")
    with open(json_data_path, "r") as file:
        player_data = json.load(file)
    return player_data


@pytest.fixture()
def proficiency_constructor() -> Callable[[dict[str, str]], RoleProficiency]:
    def constructor(proficiency_data: dict[str, str]):
        player_cav_prof = Proficiency(proficiency_data["Cavalry"])
        player_inf_prof = Proficiency(proficiency_data["Infantry"])
        player_arch_prof = Proficiency(proficiency_data["Archer"])
        player_proficiency = RoleProficiency(
            cav=player_cav_prof, arch=player_arch_prof, inf=player_inf_prof
        )
        return player_proficiency

    return constructor


@pytest.fixture()
def player_constructor(
    proficiency_constructor: Callable[[dict[str, str]], RoleProficiency]
) -> Callable[[dict[str, Any]], Player]:
    def constructor(player_data: dict[str, Any]) -> Player:
        player_proficiency = proficiency_constructor(player_data["proficiency"])
        player = Player(
            id=player_data["id"],
            igl=player_data["igl"],
            class_proficiency=player_proficiency,
            mmr=player_data["mmr"],
        )
        return player

    return constructor


@pytest.fixture()
def default_players(
    default_player_testdata: list[dict],
    player_constructor: Callable[[dict[str, Any]], Player],
) -> list[Player]:
    result_player_list: list[Player] = []
    for player_data in default_player_testdata:
        result_player_list.append(player_constructor(player_data))
    return result_player_list


@pytest.fixture()
def default_config() -> MatchmakingConfig:
    return MatchmakingConfigHandler.generate_from_local_file()


@pytest.fixture()
def default_swap_priority(default_config: MatchmakingConfig) -> list[SwapCategory]:
    return default_config.roles.swap_priority


if __name__ == "__main__":
    pytest.main()

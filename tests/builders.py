from typing import Any, Callable

import pytest

from app.enums import MapType
from app.matchmaker.game.role_picker import RolePicker
from app.matchmaker.game.role_picker_rules import (
    RolePickingRules,
    RolePickingRulesFactory,
)
from app.matchmaker.game.role_swap import RoleSwapFactory
from app.matchmaker.player import Player, RoleProficiency
from app.matchmaker.player_pool import PlayerPool
from app.matchmaking_config import (
    MatchmakingConfig,
    MatchmakingConfigHandler,
    SwapCategory,
)


@pytest.fixture()
def default_config() -> MatchmakingConfig:
    return MatchmakingConfigHandler.generate_from_local_file()


@pytest.fixture()
def default_swap_priority(default_config: MatchmakingConfig) -> list[SwapCategory]:
    return default_config.roles.swap_priority


@pytest.fixture()
def get_players(
    player_constructor: Callable[[dict[str, Any]], PlayerPool],
    players_testdata_loader: Callable[[str], list[dict]],
) -> Callable[[str], PlayerPool]:
    def create_players(playerpool_name: str) -> PlayerPool:
        player_pool: PlayerPool = PlayerPool([])
        players_data = players_testdata_loader(playerpool_name + ".json")
        for player_data in players_data:
            player_pool.append(player_constructor(player_data))
        return player_pool

    return create_players


PlayerConstructorInput = Callable[
    [
        int,
        int,
        int,
        int,
        bool,
    ],
    Player,
]


@pytest.fixture()
def default_role_swapping_rules(default_config: MatchmakingConfig) -> RolePickingRules:
    limits = default_config.map_types[MapType.open].class_limitations
    rules = RolePickingRules()
    rules_factory = RolePickingRulesFactory(limits)
    rules_factory.populate_rules(rules)
    return rules


@pytest.fixture()
def default_players(get_players: Callable[[str], PlayerPool]) -> PlayerPool:
    return get_players("default")


@pytest.fixture()
def default_role_picker(get_role_picker: Callable[[str], RolePicker]):
    return get_role_picker("default")


@pytest.fixture()
def get_role_picker(
    get_players: Callable[[str], PlayerPool],
    default_role_swapping_rules: RolePickingRules,
) -> Callable[[str], RolePicker]:
    def get_role_picker(player_pool: str) -> RolePicker:
        players = get_players(player_pool)
        avg_mmr = players.avg_mmr
        swap_factory = RoleSwapFactory(avg_mmr)
        picker = RolePicker(
            players=players,
            swap_factory=swap_factory,
            rules=default_role_swapping_rules,
        )
        return picker

    return get_role_picker


@pytest.fixture
def player(proficiency_constructor: Callable) -> PlayerConstructorInput:
    id_counter = 0

    def player_constructor(
        cav_prof: int = 0,
        arch_prof: int = 5,
        inf_prof: int = 10,
        mmr: int = 3000,
        igl: bool = False,
    ):
        nonlocal id_counter
        proficiency_data = {
            "Cavalry": cav_prof,
            "Infantry": inf_prof,
            "Archer": arch_prof,
        }
        proficiency = proficiency_constructor(proficiency_data)
        player = Player(
            id=str(id_counter), igl=igl, mmr=mmr, role_proficiency=proficiency
        )
        return player

    return player_constructor


@pytest.fixture()
def player_constructor(
    proficiency_constructor: Callable[[dict[str, str]], RoleProficiency]
) -> Callable[[dict[str, Any]], Player]:
    def constructor(player_data: dict[str, Any]) -> Player:
        player_proficiency = proficiency_constructor(player_data["proficiency"])
        player = Player(
            id=player_data["id"],
            igl=player_data["igl"],
            role_proficiency=player_proficiency,
            mmr=player_data["mmr"],
        )
        return player

    return constructor


@pytest.fixture()
def proficiency_constructor() -> Callable[[dict[str, str]], RoleProficiency]:
    def constructor(proficiency_data: dict[str, str]):
        player_cav_prof = int(proficiency_data["Cavalry"])
        player_inf_prof = int(proficiency_data["Infantry"])
        player_arch_prof = int(proficiency_data["Archer"])
        player_proficiency = RoleProficiency(
            cav=player_cav_prof, arch=player_arch_prof, inf=player_inf_prof
        )
        return player_proficiency

    return constructor


if __name__ == "__main__":
    pytest.main()

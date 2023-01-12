from typing import Any, Callable

import pytest

from app.enums import MapType, Proficiency
from app.matchmaker.game.role_picker import (
    RolePicker,
    RolePickingRulesFactory,
    RoleSwapFactory,
    RoleSwappingRules,
)
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
def default_players(
    default_player_testdata: list[dict],
    player_constructor: Callable[[dict[str, Any]], Player],
) -> PlayerPool:
    player_pool: PlayerPool = PlayerPool([])
    for player_data in default_player_testdata:
        player_pool.append(player_constructor(player_data))
    return player_pool


PlayerConstructorInput = Callable[
    [
        Proficiency,
        Proficiency,
        Proficiency,
        int,
        bool,
    ],
    Player,
]


@pytest.fixture()
def default_role_swapping_rules(default_config: MatchmakingConfig) -> RoleSwappingRules:
    limits = default_config.map_types[MapType.open].class_limitations
    rules = RoleSwappingRules()
    rules_factory = RolePickingRulesFactory(limits)
    rules_factory.populate_rules(rules)
    return rules


@pytest.fixture()
def default_role_picker(
    default_players: PlayerPool,
    default_config: MatchmakingConfig,
    default_role_swapping_rules: RoleSwappingRules,
):
    avg_mmr = default_players.avg_mmr
    swap_priority = default_config.roles.swap_priority
    swap_factory = RoleSwapFactory(swap_priority, avg_mmr)
    picker = RolePicker(
        players=default_players,
        swap_factory=swap_factory,
        rules=default_role_swapping_rules,
    )
    return picker


@pytest.fixture
def player(proficiency_constructor: Callable) -> PlayerConstructorInput:
    id_counter = 0

    def player_constructor(
        cav_prof: Proficiency = Proficiency.offclass,
        arch_prof: Proficiency = Proficiency.second,
        inf_prof: Proficiency = Proficiency.main,
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
            id=str(id_counter), igl=igl, mmr=mmr, class_proficiency=proficiency
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
            class_proficiency=player_proficiency,
            mmr=player_data["mmr"],
        )
        return player

    return constructor


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


if __name__ == "__main__":
    pytest.main()

from dataclasses import dataclass
from functools import cached_property
from matchmaker.matchups.faction import Faction

from matchmaker.matchups.map import Map
from matchmaking_config import config
from enums import MapType


@dataclass
class Matchup:
    map: Map
    factions: tuple[Faction]
    weight: int

    @cached_property
    def max_cav_per_team(self) -> int:
        is_open = self.map.type == MapType.open
        if is_open:
            return config.balance.open_map_max_cav
        else:
            return config.balance.close_map_max_cav

    @cached_property
    def max_arch_per_team(self) -> int:
        is_open = self.map.type == MapType.open
        if is_open:
            return config.balance.open_map_max_arch
        else:
            return config.balance.close_map_max_arch

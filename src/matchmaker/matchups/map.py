from dataclasses import dataclass

from matchmaker.matchups.faction import Faction
from enums import MapType


@dataclass
class Map:
    name: str
    type: MapType
    matchup_weights: dict[tuple[Faction], int]

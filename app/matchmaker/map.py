from dataclasses import dataclass

from enums import MapType


@dataclass
class Map:
    name: str
    type: MapType

from typing import Any, Protocol
from enums import MapFacFieldNames

from matchmaker.map import Map
from matchmaker.faction import Faction
from matchmaker.player import Player


class PlayerAdapterProtocol(Protocol):
    def get_matchmaker_player(self) -> Player:
        ...

    def export_results(self) -> Any:
        ...


class MatchmakingController:
    def from_player_adapters(
        self, players: list[PlayerAdapterProtocol]
    ) -> dict[str, list]:
        """
        Accepts a list of PlayerAdapter objects, containing player data
        Returns an adapter export data, check the adapter's export_result
        method for an export model specs
        """
        player_list = [player.get_matchmaker_player() for player in players]
        assert player_list
        return {}

    def _choose_map_fac(self) -> dict[MapFacFieldNames, Map | Faction]:
        ...

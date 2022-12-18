from typing import Any, Protocol
from app.api.schema import PlayerModel

from matchmaker.player import Player


class PlayerConverterProtocol(Protocol):
    @staticmethod
    def get_matchmaker_player(player: PlayerModel) -> Player:
        ...

    @staticmethod
    def export_to_response_model(export_data: dict) -> Any:
        ...


class MatchmakingController:
    def from_player_models(
        self, players: list[PlayerModel], converter: PlayerConverterProtocol
    ) -> dict[str, list]:
        """
        Accepts a list of PlayerAdapter objects, containing player data
        Returns an adapter export data, check the adapter's export_result
        method for an export model specs
        """
        player_list = [converter.get_matchmaker_player(player) for player in players]
        assert player_list
        return {}

from typing import Any, Protocol

from app.matchmaker.player import Player


class PlayerConverterProtocol(Protocol):
    @staticmethod
    def get_matchmaker_player(player: Any) -> Player:
        ...

    @staticmethod
    def export_to_response_model(export_data: dict) -> Any:
        ...


class MatchmakingController:
    def from_player_models(
        self, players: list[Any], converter: PlayerConverterProtocol
    ) -> dict[str, list]:
        """
        Accepts a list of players and a convrerter to transform them into mm
        player objects
        Returns a converter export data, check the converter's export_to_response_model
        method for an export model specs
        """
        player_list = [converter.get_matchmaker_player(player) for player in players]
        assert player_list
        return {}

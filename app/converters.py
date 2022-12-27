from app.api.schema import PlayerModel, PlayerReponseModel
from app.matchmaker.player import Player


class PlayerConverter:
    """
    Adapts matchmaking data types to an api models
    """

    @staticmethod
    def get_matchmaker_player(player_model: PlayerModel) -> Player:
        ...

    @staticmethod
    def export_to_response_model(player: Player) -> PlayerReponseModel:
        ...

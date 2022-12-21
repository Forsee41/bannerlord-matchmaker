from api.schema import PlayerModel, PlayerReponseModel
from matchmaker.player import Player
from matchmaking_config import config


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

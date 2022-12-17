from api.schema import PlayerModel, PlayerReponseModel
from matchmaker.player import Player
import matchmaking_config


config = matchmaking_config.matchmaking_config


class PlayerAdapter:
    """
    Adapts matchmaking data types to an api models
    """

    @staticmethod
    def get_matchmaker_player(player_model: PlayerModel) -> Player:
        ...

    @staticmethod
    def get_response_model_inst(player: Player) -> PlayerReponseModel:
        ...

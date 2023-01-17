from app.api.schema import PlayerModel, PlayerReponseModel
from app.matchmaker.player import Player, RoleProficiency


class PlayerConverter:
    """
    Adapts matchmaking data types to an api models
    """

    @staticmethod
    def get_matchmaker_player(player_model: PlayerModel) -> Player:
        proficiency = RoleProficiency(
            cav=player_model.cav, arch=player_model.arch, inf=player_model.inf
        )
        player = Player(
            id=player_model.id,
            igl=player_model.igl,
            mmr=player_model.igl,
            role_proficiency=proficiency,
        )
        return player

    @staticmethod
    def export_to_response_model(player: Player) -> PlayerReponseModel:
        return PlayerReponseModel(
            id=player.id,
            role=player.current_role,
            mmr_raw=player.mmr_raw,
            mmr=player.mmr,
            role_proficiency=player.get_role_proficiency(player.current_role),
        )

from app.api.schema import (
    GameResponseModel,
    MatchmakerResponeModel,
    PlayerModel,
    PlayerReponseModel,
    TeamResponseModel,
)
from app.matchmaker.game.team import Team
from app.matchmaker.player import Player, RoleProficiency
from app.matchmaking_config import Faction, Map


class PlayerConverter:
    """
    Adapts matchmaking data types to an api models
    """

    def get_matchmaker_player(self, player_model: PlayerModel) -> Player:
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

    def export_to_response_model(self, player: Player) -> PlayerReponseModel:
        return PlayerReponseModel(
            id=player.id,
            role=player.current_role,
            mmr_raw=player.mmr_raw,
            mmr=player.mmr,
            role_proficiency=player.get_role_proficiency(player.current_role),
        )


class MatchmakerConverter:
    """
    Contains methods to convert matchmaker data to an api models and vice versa
    """

    def __init__(self, player_converter: PlayerConverter) -> None:
        self.player_converter = player_converter

    def create_matchmaker_playerlist(
        self,
        players: list[PlayerModel],
    ) -> list[Player]:
        return [
            self.player_converter.get_matchmaker_player(player) for player in players
        ]

    def create_team_result(self, team: Team) -> TeamResponseModel:
        players = [
            self.player_converter.export_to_response_model(player) for player in team
        ]
        igl_id = team.get_igl().id
        result = TeamResponseModel(players=players, igl_id=igl_id, avg_mmr=team.avg_mmr)
        return result

    def create_game_result(
        self, map: Map, fac1: Faction, fac2: Faction, team1: Team, team2: Team
    ) -> GameResponseModel:
        avg_mmr_diff = abs(team1.avg_mmr - team2.avg_mmr)
        team1_response = self.create_team_result(team1)
        team2_response = self.create_team_result(team2)
        result = GameResponseModel(
            team1=team1_response,
            team2=team2_response,
            avg_mmr_diff=avg_mmr_diff,
            map=map.name,
            faction1=fac1,
            faction2=fac2,
        )
        return result

    def get_player_ids(self, players: list[Player]) -> list[str]:
        return [player.id for player in players]

    def create_matchmaker_response(
        self, games: list[GameResponseModel], undistributed_player_ids: list[str]
    ) -> MatchmakerResponeModel:
        return MatchmakerResponeModel(
            games=games, undistributed_player_ids=undistributed_player_ids
        )

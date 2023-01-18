from copy import deepcopy
from typing import Any, Protocol

from app.matchmaker.game.balancer_rules import (
    ArchEqualityRule,
    CavEqualityRule,
    IglBalanceRule,
    InfEqualityRule,
)
from app.matchmaker.game.player_balancer import PlayerBalancer
from app.matchmaker.game.role_picker import RolePicker
from app.matchmaker.game.role_picker_rules import (
    RoleLimitsConfigRetriever,
    RolePickingRulesFactory,
)
from app.matchmaker.game.role_swap import RoleSwapFactory
from app.matchmaker.game.team import Team
from app.matchmaker.matchups.matchup_picker import (
    MatchupConfigRetriever,
    MatchupRandomPicker,
)
from app.matchmaker.player import Player
from app.matchmaker.player_picker import PlayerPicker
from app.matchmaker.player_pool import PlayerPool
from app.matchmaking_config import ClassLimitations, Faction, Map, MatchmakingConfig


class MatchmakerConverterProtocol(Protocol):
    def get_player_ids(self, players: list[Player]) -> list[str]:
        ...

    def create_game_result(
        self, map: Map, fac1: Faction, fac2: Faction, team1: Team, team2: Team
    ) -> Any:
        ...

    def create_matchmaker_response(
        self, games: list[Any], undistributed_player_ids: list[str]
    ):
        ...

    def create_matchmaker_playerlist(self, players: list[Any]) -> list[Player]:
        ...


class MatchmakingController:
    def __init__(
        self, converter: MatchmakerConverterProtocol, config: MatchmakingConfig
    ) -> None:
        self.converter = converter
        self.config = deepcopy(config)

    def create_games(self, players: list[Any]) -> Any:
        """
        Accepts a list of players and a convrerter to transform them into mm
        player objects
        Returns a converter export data, check the converter's export_to_response_model
        method for an export model specs
        """
        limits_config_retriever = RoleLimitsConfigRetriever(self.config)
        mm_players = self.converter.create_matchmaker_playerlist(players)
        result_games: list[Any] = []
        player_pools, excluded_players = self._create_player_pools(mm_players)
        for player_pool in player_pools:
            map, fac1, fac2 = self._choose_matchup()
            role_limits = limits_config_retriever.get_map_role_limits(map)
            players_with_chosen_roles = self._choose_roles(player_pool, role_limits)
            team1, team2 = self._create_teams(players_with_chosen_roles)
            game = self.converter.create_game_result(map, fac1, fac2, team1, team2)
            result_games.append(game)
        excluded_player_ids = [player.id for player in excluded_players]
        result = self.converter.create_matchmaker_response(
            result_games, excluded_player_ids
        )
        return result

    def _create_teams(self, players: PlayerPool) -> tuple[Team, Team]:
        balancer_rules = [
            CavEqualityRule(),
            InfEqualityRule(),
            ArchEqualityRule(),
            IglBalanceRule(),
        ]
        balancer = PlayerBalancer(players, balancer_rules)
        team1, team2 = balancer.create_teams()
        return team1, team2

    def _choose_roles(
        self, players: PlayerPool, limits: ClassLimitations
    ) -> PlayerPool:
        rules_factory = RolePickingRulesFactory(limits)
        rules = rules_factory.create_rules()
        swap_factory = RoleSwapFactory()
        role_picker = RolePicker(players, swap_factory, rules)
        result_playerpool = role_picker.set_player_roles()
        return result_playerpool

    def _create_player_pools(
        self, players: list[Player]
    ) -> tuple[list[PlayerPool], list[Player]]:
        player_picker = PlayerPicker(players)
        player_pools = player_picker.split_into_games()
        excluded_players = player_picker.excluded_players
        return player_pools, excluded_players

    def _choose_matchup(self) -> tuple[Map, Faction, Faction]:
        matchup_picker = MatchupRandomPicker()
        matchup_config_retriever = MatchupConfigRetriever(self.config)
        map = matchup_picker.choose_map(self.config.maps)
        matchups = matchup_config_retriever.get_matchups_for_map(map)
        matchup = matchup_picker.choose_matchup(matchups)
        return map, matchup.fac1, matchup.fac2

    def process_game(self, players: PlayerPool, config: MatchmakingConfig) -> Any:
        ...

import itertools
import logging
from collections.abc import Iterable
from copy import copy

from app.exceptions import TeamsCreatingError
from app.matchmaker.game.balancer_rules import BalanceRule
from app.matchmaker.game.team import Team
from app.matchmaker.player import Player
from app.matchmaker.player_pool import PlayerPool

log = logging.getLogger(__name__)


class PlayerBalancer:
    def __init__(self, players: PlayerPool, rules: list[BalanceRule]) -> None:
        self.players = players
        self.rules = rules

    def create_teams(self) -> tuple[Team, Team]:
        best_teams: tuple[Team, Team] | None = None
        while best_teams is None:
            try:
                best_teams = self._create_teams_with_current_rules()
            except TeamsCreatingError:
                rule = self.rules.pop()
                log.info(
                    "Can't create teams using the current ruleset"
                    f"removing {rule} and trying again"
                )
        return best_teams

    def _create_teams_with_current_rules(self) -> tuple[Team, Team]:
        best_teams: tuple[Team, Team] | None = None
        best_mmr_diff: float | None = None
        for players in itertools.combinations(self.players, 6):
            team1, team2 = self._get_teams_by_players(players)
            if not all((rule.check_teams(team1, team2) for rule in self.rules)):
                continue
            current_mmr_diff = abs(team1.avg_mmr - team2.avg_mmr)
            if best_mmr_diff is None or current_mmr_diff < best_mmr_diff:
                best_mmr_diff = current_mmr_diff
                best_teams = team1, team2
        if best_teams is None:
            raise TeamsCreatingError
        return best_teams

    def _get_teams_by_players(self, players: Iterable[Player]) -> tuple[Team, Team]:
        team1_playerlist = list(players)
        team2_playerlist = copy(self.players)
        for player in team1_playerlist:
            team2_playerlist.remove(player)
        team1 = Team(team1_playerlist)
        team2 = Team(team2_playerlist)
        return team1, team2

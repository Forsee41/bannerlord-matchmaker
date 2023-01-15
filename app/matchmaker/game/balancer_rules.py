from abc import ABC, abstractmethod

from app.exceptions import NotEnoughIglsError
from app.matchmaker.game.team import Team
from app.matchmaker.player import Player


class BalanceRule(ABC):
    @abstractmethod
    def check_teams(self, team1: Team, team2: Team) -> bool:
        ...


class CavEqualityRule(BalanceRule):
    def check_teams(self, team1: Team, team2: Team) -> bool:
        return team1.total_cav == team2.total_cav


class InfEqualityRule(BalanceRule):
    def check_teams(self, team1: Team, team2: Team) -> bool:
        return team1.total_inf == team2.total_inf


class ArchEqualityRule(BalanceRule):
    def check_teams(self, team1: Team, team2: Team) -> bool:
        return team1.total_arch == team2.total_arch


class IglBalanceRule(BalanceRule):
    def check_teams(self, team1: Team, team2: Team) -> bool:
        try:
            igl1, igl2 = self._find_best_igls(team1, team2)
        except NotEnoughIglsError:
            return True
        return (igl1 in team1 and igl2 in team2) or (igl1 in team2 and igl2 in team1)

    def _find_best_igls(self, team1: Team, team2: Team) -> tuple[Player, Player]:
        all_players = team1 + team2
        igls = [igl for igl in all_players if igl.igl]
        if len(igls) < 2:
            raise NotEnoughIglsError
        igls.sort(reverse=True)
        return igls[0], igls[1]

from abc import ABC, abstractmethod

from app.matchmaker.game.team import Team


class TeamCreatingRule(ABC):
    def __init__(self, team1: Team, team2: Team) -> None:
        self.team1 = team1
        self.team2 = team2
        super().__init__()

    @abstractmethod
    def check_teams(self) -> bool:
        ...


class CavEqualityRule(TeamCreatingRule):
    def check_teams(self) -> bool:
        return self.team1.total_cav == self.team2.total_cav


class InfEqualityRule(TeamCreatingRule):
    def check_teams(self) -> bool:
        return self.team1.total_inf == self.team2.total_inf


class ArchEqualityRule(TeamCreatingRule):
    def check_teams(self) -> bool:
        return self.team1.total_arch == self.team2.total_arch


class IglBalanceRule(TeamCreatingRule):
    def check_teams(self) -> bool:
        return self.team1.has_igl == self.team2.has_igl

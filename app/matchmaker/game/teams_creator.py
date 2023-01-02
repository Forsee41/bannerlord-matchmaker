from typing import Protocol


class TeamCreatingRule(Protocol):
    def check_teams(self) -> bool:
        """Checks passed teams for rule compliance"""
        ...

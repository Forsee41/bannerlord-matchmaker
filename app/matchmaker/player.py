import logging
from functools import total_ordering
from typing import Any

from app.enums import PlayerRole
from app.exceptions import ProficiencyValidationError, RoleNotFoundError

log = logging.getLogger(__name__)


class RoleProficiency(dict):
    def __init__(self, cav: int, arch: int, inf: int):
        super().__init__()
        self[PlayerRole.cav] = cav
        self[PlayerRole.arch] = arch
        self[PlayerRole.inf] = inf
        self._validate_input()

    def _validate_input(self) -> None:
        if not any([self[key] == 10 for key in self]):
            raise ProficiencyValidationError(
                "Player must have a class with proficiency 10"
            )
        if any([self[key] < 0 or self[key] > 10 for key in self]):
            raise ProficiencyValidationError(
                "Proficiency must be in a diapason of 0 >= prof >= 10"
            )
        if sum([self[key] == 10 for key in self]) > 1:
            raise ProficiencyValidationError(
                "There must be only one role with proficiency of 10"
            )


@total_ordering
class Player:
    def __init__(
        self,
        id: str,
        igl: bool,
        mmr: int,
        role_proficiency: RoleProficiency,
    ) -> None:
        self.nickname = id
        self.id = id
        self.igl = igl
        self.mmr_raw = mmr
        self._role_proficiency = role_proficiency
        self.current_role = self.main

    def get_role_proficiency(self, role: PlayerRole):
        return self._role_proficiency[role]

    @property
    def is_offclass(self) -> bool:
        return self.main != self.current_role

    @property
    def current_proficiency(self) -> int:
        return self.get_role_proficiency(self.current_role)

    @property
    def mmr_reduced(self) -> int:
        return self.mmr_raw - 10

    @property
    def mmr(self) -> int:
        return self.mmr_raw if self.current_role == self.main else self.mmr_reduced

    @property
    def main(self) -> PlayerRole:
        return self._find_role_by_proficiency(10)

    def export_dict(self) -> dict:
        result: dict[str, Any] = {}
        result["nickname"] = self.nickname
        result["current_class"] = self.current_role
        result["igl"] = self.igl
        result["mmr_raw"] = self.mmr_raw
        result["mmr_reduced"] = self.mmr_reduced
        result["is_offclass"] = self.is_offclass
        return result

    def __post_init__(self) -> None:
        self.current_role = self.main

    def __eq__(self, other) -> bool:
        return self.mmr == other.mmr

    def __lt__(self, other) -> bool:
        return self.mmr < other.mmr

    def _find_role_by_proficiency(self, proficiency: int) -> PlayerRole:
        all_matching_roles = self._find_roles_by_proficiency(proficiency)
        try:
            return all_matching_roles[0]
        except IndexError:
            raise RoleNotFoundError

    def _find_roles_by_proficiency(self, proficiency: int) -> list[PlayerRole]:
        result = []
        for game_class in self._role_proficiency:
            if self._role_proficiency[game_class] == proficiency:
                result.append(game_class)
        return result

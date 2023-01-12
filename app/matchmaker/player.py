import logging
from functools import total_ordering
from typing import Any

from app.enums import PlayerRole, Proficiency
from app.exceptions import ProficiencyValidationError, RoleNotFoundError

log = logging.getLogger(__name__)


class RoleProficiency(dict):
    def __init__(self, cav: Proficiency, arch: Proficiency, inf: Proficiency):
        super().__init__()
        self[PlayerRole.cav] = cav
        self[PlayerRole.arch] = arch
        self[PlayerRole.inf] = inf
        self._validate_input()

    def _validate_input(self) -> None:
        prof_count = {prof: 0 for prof in Proficiency}

        for game_class in self:
            if self[game_class] in prof_count:
                prof_count[self[game_class]] += 1

        if prof_count[Proficiency.main] != 1:
            raise ProficiencyValidationError("Player must have one main class")

        if prof_count[Proficiency.flex] + prof_count[Proficiency.second] == 0:
            raise ProficiencyValidationError(
                "Player must have a second class or at least one flex class"
            )

        if prof_count[Proficiency.flex] > 0 and prof_count[Proficiency.second] > 0:
            raise ProficiencyValidationError(
                "Player must not have a second and a flex class simultaneously"
            )

        if prof_count[Proficiency.second] > 1:
            raise ProficiencyValidationError("Player must have max 1 second class")


@total_ordering
class Player:
    def __init__(
        self,
        id: str,
        igl: bool,
        mmr: int,
        class_proficiency: RoleProficiency,
    ) -> None:
        self.nickname = id
        self.id = id
        self.igl = igl
        self.mmr_raw = mmr
        self._class_proficiency = class_proficiency
        self.current_role = self.main

    def get_role_proficiency(self, role: PlayerRole):
        return self._class_proficiency[role]

    @property
    def is_offclass(self) -> bool:
        return self.main != self.current_role

    @property
    def current_proficiency(self) -> Proficiency:
        return self.get_role_proficiency(self.current_role)

    @property
    def mmr_reduced(self) -> int:
        ...

    @property
    def mmr(self) -> int:
        return self.mmr_raw if self.current_role == self.main else self.mmr_reduced

    @property
    def main(self) -> PlayerRole:
        return self._find_role_by_proficiency(Proficiency.main)

    @property
    def second(self) -> PlayerRole | None:
        try:
            return self._find_role_by_proficiency(Proficiency.second)
        except RoleNotFoundError:
            return None

    @property
    def offclass(self) -> PlayerRole | None:
        try:
            return self._find_role_by_proficiency(Proficiency.offclass)
        except RoleNotFoundError:
            return None

    @property
    def alt_class(self) -> PlayerRole:
        try:
            return self._find_role_by_proficiency(Proficiency.second)
        except RoleNotFoundError:
            pass
        return self._find_role_by_proficiency(Proficiency.flex)

    @property
    def flexes(self) -> list[PlayerRole]:
        return self._find_roles_by_proficiency(Proficiency.flex)

    @property
    def prof_roles(self) -> list[PlayerRole]:
        result = self.flexes
        result.append(self.main)
        return result

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

    def _find_role_by_proficiency(self, proficiency: Proficiency) -> PlayerRole:
        all_matching_roles = self._find_roles_by_proficiency(proficiency)
        try:
            return all_matching_roles[0]
        except IndexError:
            raise RoleNotFoundError

    def _find_roles_by_proficiency(self, proficiency: Proficiency) -> list[PlayerRole]:
        result = []
        for game_class in self._class_proficiency:
            if self._class_proficiency[game_class] == proficiency:
                result.append(game_class)
        return result

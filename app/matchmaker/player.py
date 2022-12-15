import logging
from dataclasses import dataclass, field

from exceptions import RoleNotFoundError, ProficiencyValidationError
from enums import PlayerClass, Proficiency


log = logging.getLogger(__name__)


@dataclass
class ClassProficiency:
    cav: Proficiency
    arch: Proficiency
    inf: Proficiency

    def __post_init__(self) -> None:
        role_count = {Proficiency.main: 0, Proficiency.second: 0, Proficiency.flex: 0}

        for game_class in (self.cav, self.arch, self.inf):
            if game_class in role_count:
                role_count[game_class] += 1

        if role_count[Proficiency.main] != 1:
            raise ProficiencyValidationError("Player must have one main class")

        if role_count[Proficiency.flex] + role_count[Proficiency.second] == 0:
            raise ProficiencyValidationError(
                "Player must have a second class or at least one flex class"
            )


@dataclass
class Player:
    _class_proficiency: ClassProficiency
    current_class: PlayerClass = field(compare=False, init=False)
    secondary: PlayerClass = field(compare=False)
    igl: bool = field(compare=False)
    mmr: int = field(compare=True)

    def __post_init__(self) -> None:
        self.current_class = self.main

    @property
    def main(self) -> PlayerClass:
        return self._find_role_by_proficiency(Proficiency.main)

    @property
    def second(self) -> PlayerClass|None:
        try:
            return self._find_role_by_proficiency(Proficiency.second)
        except ProficiencyValidationError:
            return None

    @property
    def alt_class(self) -> PlayerClass:
        try:
            return self._find_role_by_proficiency(Proficiency.second)
        except RoleNotFoundError:
            pass
        return self._find_role_by_proficiency(Proficiency.flex)

    @property
    def flexes(self) -> list[PlayerClass]:
        return self._find_flex_roles()

    def _find_role_by_proficiency(self, proficiency: Proficiency) -> PlayerClass:
        if self._class_proficiency.inf == proficiency:
            return PlayerClass.inf
        if self._class_proficiency.arch == proficiency:
            return PlayerClass.arch
        if self._class_proficiency.cav == proficiency:
            return PlayerClass.cav
        raise RoleNotFoundError

    def _find_flex_roles(self) -> list[PlayerClass]:
        result = []
        if self._class_proficiency.inf == Proficiency.flex:
            result.append(PlayerClass.inf)
        if self._class_proficiency.arch == Proficiency.flex:
            result.append(PlayerClass.arch)
        if self._class_proficiency.cav == Proficiency.flex:
            result.append(PlayerClass.cav)
        return result

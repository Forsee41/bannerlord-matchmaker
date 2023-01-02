import pytest

from app.matchmaker import player
from app.enums import Proficiency
from app.exceptions import ProficiencyValidationError


class TestProficiencyClass:
    @pytest.mark.parametrize(
        "cav,inf,arch",
        [
            (Proficiency.main, Proficiency.second, Proficiency.offclass),
            (Proficiency.flex, Proficiency.main, Proficiency.offclass),
            (Proficiency.flex, Proficiency.flex, Proficiency.main),
        ],
    )
    def test_class_proficiency_valid_input(self, cav, inf, arch):
        proficiency = player.RoleProficiency(cav=cav, arch=arch, inf=inf)
        assert proficiency

    def test_class_proficiency_flex_and_second(self):
        with pytest.raises(ProficiencyValidationError):
            proficiency = player.RoleProficiency(
                cav=Proficiency.main, inf=Proficiency.flex, arch=Proficiency.second
            )
            assert proficiency

    def test_class_proficiency_double_second(self):
        with pytest.raises(ProficiencyValidationError):
            proficiency = player.RoleProficiency(
                cav=Proficiency.main, inf=Proficiency.second, arch=Proficiency.second
            )
            assert proficiency

    def test_class_proficiency_double_main(self):
        with pytest.raises(ProficiencyValidationError):
            proficiency = player.RoleProficiency(
                cav=Proficiency.main, inf=Proficiency.main, arch=Proficiency.second
            )
            assert proficiency

    def test_class_proficiency_no_main(self):
        with pytest.raises(ProficiencyValidationError):
            proficiency = player.RoleProficiency(
                cav=Proficiency.flex, inf=Proficiency.offclass, arch=Proficiency.second
            )
            assert proficiency

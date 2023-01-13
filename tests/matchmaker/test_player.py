import pytest

from app.exceptions import ProficiencyValidationError
from app.matchmaker import player


class TestProficiencyClass:
    @pytest.mark.parametrize(
        "cav,inf,arch",
        [
            (10, 5, 0),
            (9, 10, 0),
            (9, 9, 10),
        ],
    )
    def test_class_proficiency_valid_input(self, cav, inf, arch):
        proficiency = player.RoleProficiency(cav=cav, arch=arch, inf=inf)
        assert proficiency

    def test_class_proficiency_double_main(self):
        with pytest.raises(ProficiencyValidationError):
            proficiency = player.RoleProficiency(cav=10, inf=10, arch=5)
            assert proficiency

    def test_class_proficiency_no_main(self):
        with pytest.raises(ProficiencyValidationError):
            proficiency = player.RoleProficiency(cav=9, inf=0, arch=5)
            assert proficiency

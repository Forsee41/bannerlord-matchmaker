from matchmaker import player
from enums import Proficiency


class TestProficiencyClass:
    def test_class_proficiency_valid_input(self):
        proficiency = player.ClassProficiency(
            cav=Proficiency.main, arch=Proficiency.second, inf=Proficiency.offclass
        )
        assert proficiency

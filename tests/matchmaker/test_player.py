from matchmaker import player
from enums import Proficiency


def test_class_proficiency_class():
    proficiency = player.ClassProficiency(
        cav=Proficiency.main, arch=Proficiency.second, inf=Proficiency.offclass
    )
    assert proficiency

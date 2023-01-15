from typing import Callable

import pytest

from app.matchmaker.game.player_balancer import PlayerBalancer
from app.matchmaker.game.team import Team
from app.matchmaker.game.team_creating_rules import BalanceRule


@pytest.mark.xfail
class TestTeamsCreator:
    def test_output_validity(self, default_player_balancer: PlayerBalancer) -> None:
        teams = default_player_balancer.create_teams()
        assert isinstance(teams[0], Team)
        assert isinstance(teams[1], Team)

    def test_balancer_minimizes_mmr_diff(
        self, get_player_balancer: Callable[[str], PlayerBalancer]
    ) -> None:
        balancer = get_player_balancer("all_inf")
        team1, team2 = balancer.create_teams()
        assert team1.avg_mmr == team2.avg_mmr

    @pytest.mark.parametrize("playerpool", (("all_inf"), ("default"), ("all_cav")))
    def test_balancer_respects_rules(
        self,
        get_player_balancer: Callable[[str], PlayerBalancer],
        default_balancer_rules: list[BalanceRule],
        playerpool: str,
    ) -> None:
        balancer = get_player_balancer(playerpool)
        team1, team2 = balancer.create_teams()
        for rule in default_balancer_rules:
            assert rule.check_teams(team1, team2)

from app.enums import PlayerRole
from app.matchmaker.player import Player


class Team(list):
    def __init__(self, players: list[Player]) -> None:
        super().__init__()
        team_length = len(players)
        if team_length != 6:
            raise ValueError(
                f"There should be 6 players passed to the team "
                f"constructor, got {team_length} instead"
            )
        self += players

    @property
    def avg_mmr(self) -> float:
        total_mmr = sum([player.mmr_raw for player in self])
        avg_mmr = total_mmr / 6
        return avg_mmr

    @property
    def total_cav(self) -> int:
        return self._count_players_by_role(PlayerRole.cav)

    @property
    def total_inf(self) -> int:
        return self._count_players_by_role(PlayerRole.inf)

    @property
    def total_arch(self) -> int:
        return self._count_players_by_role(PlayerRole.arch)

    @property
    def has_igl(self) -> bool:
        return any([player.igl for player in self])

    def _count_players_by_role(self, target_role: PlayerRole) -> int:
        return len(list(filter((lambda p: p.current_role == target_role), self)))

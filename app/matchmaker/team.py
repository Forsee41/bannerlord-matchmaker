from matchmaker.player import Player
from enums import PlayerClass


class Team:
    def __init__(self, players: list[Player]) -> None:
        team_length = len(players)
        if team_length != 6:
            raise ValueError(f"Team length must be 6, got {team_length} instead")
        self.players = players

    @property
    def avg_mmr(self) -> float:
        total_mmr = 0
        for player in self.players:
            total_mmr += player.mmr
        return total_mmr

    @staticmethod
    def count_players_by_class(
        target_class: PlayerClass, player_list: list[Player]
    ) -> int:
        return len(
            list(filter((lambda p: p.current_class == target_class), player_list))
        )

    @property
    def total_cav(self) -> int:
        return self.count_players_by_class(PlayerClass.cav, self.players)

    @property
    def total_inf(self) -> int:
        return self.count_players_by_class(PlayerClass.inf, self.players)

    @property
    def total_arch(self) -> int:
        return self.count_players_by_class(PlayerClass.arch, self.players)

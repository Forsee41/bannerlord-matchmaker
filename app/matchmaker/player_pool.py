from app.enums import PlayerRole
from app.matchmaker.player import Player


class PlayerPool(list):
    def __init__(self, players: list[Player]):
        super().__init__()
        self += players

    def get_role_players_amount(self, role: PlayerRole) -> int:
        return len([player for player in self if player.current_role == role])

    def check_odd_role_players_amount(self, role: PlayerRole) -> bool:
        return True if self.get_role_players_amount(role) % 2 == 1 else False

    @property
    def avg_mmr(self):
        total_mmr = sum([player.mmr for player in self])
        avg_mmr = total_mmr / 12
        return avg_mmr

    @property
    def mmr_deviation(self):
        dev_squares_sum = 0
        for player in self:
            dev_squares_sum += (self.avg_mmr - player.mmr) ** 2
        return (dev_squares_sum / len(self)) ** 0.5

import random
from copy import copy
from dataclasses import dataclass, field

from app.exceptions import NotEnoughPlayersError
from app.matchmaker.player import Player
from app.matchmaker.player_pool import PlayerPool


@dataclass
class PlayerPicker:
    player_list: list[Player]
    excluded_players: list[Player] = field(init=False)
    enrolled_players: list[Player] = field(init=False)

    def __post_init__(self):
        if len(self.player_list) < 12:
            raise NotEnoughPlayersError

    @property
    def game_slots_amount(self) -> int:
        return self.games_amount * 4

    @property
    def games_amount(self) -> int:
        return len(self.player_list) // 12

    @property
    def excluded_players_amount(self) -> int:
        return len(self.player_list) - self.game_slots_amount

    def enroll_players(self) -> list[Player]:
        """
        Picks players for a game
        Sets excluded_players and enrolled_players instance variables and returns
        enrolled players list
        """
        input_players = copy(self.player_list)
        excluded_players = []
        for _ in range(self.excluded_players_amount):
            excluded_player = random.choice(input_players)
            excluded_players.append(excluded_player)
            input_players.remove(excluded_player)

        self.excluded_players = excluded_players
        self.enrolled_players = input_players
        return input_players

    def split_into_games(self) -> list[PlayerPool]:
        result = []
        enrolled_players = self.enrolled_players
        enrolled_players.sort(key=(lambda player: player.mmr_raw))
        for game in range(self.games_amount):
            player_group = enrolled_players[game * 12 : (game + 1) * 12]
            player_pool = PlayerPool(player_group)
            result.append(player_pool)
        return result

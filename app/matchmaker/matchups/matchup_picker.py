import random

from app.matchmaking_config import Map, MatchmakingConfig, Matchup


class MatchupRandomPicker:
    """
    Containing methods to randomly choose maps and matchups using their weights
    """

    @staticmethod
    def choose_map(maplist: list[Map]) -> Map:
        """Randomly chooses a map using a list of maps, respecting their weights"""
        weights = [map.weight for map in maplist]
        chosen_map = random.choices(population=maplist, weights=weights, k=1)[0]
        return chosen_map

    @staticmethod
    def choose_matchup(matchup_list: list[Matchup]) -> Matchup:
        """
        Randomly chooses a matchup using a list of matchups, respecting their weights
        """
        weights = [matchup.weight for matchup in matchup_list]
        matchup = random.choices(population=matchup_list, weights=weights, k=1)[0]
        return matchup


class MatchupConfigRetriever:
    """Retrieves matchups from a config"""

    def __init__(self, matchup_config: MatchmakingConfig) -> None:
        self.mm_config = matchup_config

    def get_matchups_for_map(self, map: Map) -> list[Matchup]:
        """
        Exctracting a list of matchups for a chosen map from a mm config
        """
        if map.matchups is not None:
            matchup_list = map.matchups
        else:
            matchup_list = self.mm_config.map_types[map.type].matchups

        return matchup_list

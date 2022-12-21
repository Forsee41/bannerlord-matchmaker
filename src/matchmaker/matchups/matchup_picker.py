import random

from matchmaking_config import Matchup, config, Map


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

    @staticmethod
    def get_raw_map_matchups(map: Map) -> list[Matchup]:
        """
        Exctacting a list of matchups for a chosen map from a current mm config
        """
        if map.name in config.matchups.matchup_weights:
            matchup_list = config.matchups.matchup_weights[map.name]
        else:
            matchup_list = config.matchups.matchup_weight_defaults[map.type]
        return matchup_list

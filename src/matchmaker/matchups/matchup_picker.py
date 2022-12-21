import random

from matchmaking_config import Matchup, config, Map


class MatchupPicker:
    @staticmethod
    def choose_map() -> Map:
        maplist = config.matchups.maps
        weights = [map.weight for map in maplist]
        chosen_map = random.choices(population=maplist, weights=weights, k=1)[0]
        return chosen_map

    @classmethod
    def choose_matchup(cls, map: Map) -> Matchup:
        if map.name in config.matchups.matchup_weights:
            matchup_list = config.matchups.matchup_weights[map.name]
        else:
            matchup_list = config.matchups.matchup_weight_defaults[map.type]
        weights = [matchup.weight for matchup in matchup_list]
        matchup = random.choices(population=matchup_list, weights=weights, k=1)[0]
        return matchup

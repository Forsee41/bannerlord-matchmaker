import random

from matchmaking_config import Matchup, config, Map


class MatchupPicker:
    @staticmethod
    def choose_map(maplist: list[Map]) -> Map:
        weights = [map.weight for map in maplist]
        chosen_map = random.choices(population=maplist, weights=weights, k=1)[0]
        return chosen_map

    @staticmethod
    def choose_matchup(matchup_list: list[Matchup]) -> Matchup:
        weights = [matchup.weight for matchup in matchup_list]
        matchup = random.choices(population=matchup_list, weights=weights, k=1)[0]
        return matchup

    @staticmethod
    def get_raw_map_matchups(map: Map) -> list[Matchup]:
        if map.name in config.matchups.matchup_weights:
            matchup_list = config.matchups.matchup_weights[map.name]
        else:
            matchup_list = config.matchups.matchup_weight_defaults[map.type]
        return matchup_list
        

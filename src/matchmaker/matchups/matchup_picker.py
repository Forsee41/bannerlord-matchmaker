import random
from matchmaker.matchups.faction import Faction

from matchmaking_config import MatchupModel, config, MapModel


class MatchupPicker:
    @staticmethod
    def choose_map() -> MapModel:
        maplist = config.matchups.maps
        chosen_map = random.choice(maplist)
        return chosen_map

    @classmethod
    def choose_factions(cls, map: MapModel) -> tuple[Faction, Faction]:
        matchup = cls._choose_matchup(map)
        return Faction(matchup.fac1), Faction(matchup.fac2)

    @staticmethod
    def _construct_matchup_weight_lists(matchups: list[MatchupModel]):
        weights = [matchup.weight for matchup in matchups]
        return matchups, weights

    @classmethod
    def _choose_matchup(cls, map: MapModel) -> MatchupModel:
        if map.name in config.matchups.matchup_weights:
            matchup_list = config.matchups.matchup_weights[map.name]
        else:
            matchup_list = config.matchups.matchup_weight_defaults[map.type]
        matchups, weights = cls._construct_matchup_weight_lists(matchup_list)
        matchup = random.choices(population=matchups, weights=weights, k=1)[0]
        return matchup

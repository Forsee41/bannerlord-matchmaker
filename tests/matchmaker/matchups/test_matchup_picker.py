import pytest

from app.enums import MapType
from app.matchmaker.matchups.matchup_picker import MatchupConfigRetriever, MatchupRandomPicker
from app.matchmaking_config import Map, Matchup, config


class TestMatchupRandomPicker:
    def test_choose_map_default_maps(self):
        matchup_picker = MatchupRandomPicker()
        maplist = config.maps
        chosen_map = matchup_picker.choose_map(maplist)
        assert isinstance(chosen_map, Map)
        assert chosen_map in config.maps
        assert chosen_map.weight > 0

    def test_choose_map_with_zero_weight_maps(self):
        matchup_picker = MatchupRandomPicker()
        maplist = config.maps[:3]
        maplist[2].weight = 0
        maplist[1].weight = 0
        maplist[0].weight = 1
        chosen_map = matchup_picker.choose_map(maplist)
        assert chosen_map == maplist[0]

    def test_choose_map_all_maps_zero_weight(self):
        matchup_picker = MatchupRandomPicker()
        maplist = config.maps[:3]
        for map in maplist:
            map.weight = 0
        with pytest.raises(ValueError):
            chosen_map = matchup_picker.choose_map(maplist)
            assert not chosen_map

    def test_choose_matchup_valid_matchups(self):
        matchup_picker = MatchupRandomPicker()
        matchups = config.map_types[MapType.open].matchups
        chosen_matchup = matchup_picker.choose_matchup(matchups)
        assert isinstance(chosen_matchup, Matchup)
        assert chosen_matchup in matchups
        assert chosen_matchup.weight > 0

    def test_choose_matchup_with_zero_weight_matchups(self):
        matchup_picker = MatchupRandomPicker()
        matchups = config.map_types[MapType.open].matchups
        for matchup in matchups:
            matchup.weight = 0
        matchups[0].weight = 1
        chosen_matchup = matchup_picker.choose_matchup(matchups)
        assert chosen_matchup in matchups
        assert chosen_matchup.weight > 0
        assert chosen_matchup == matchups[0]

    def test_choose_matchup_all_matchups_zero_weight(self):
        matchup_picker = MatchupRandomPicker()
        matchups = config.map_types[MapType.open].matchups
        for matchup in matchups:
            matchup.weight = 0
        with pytest.raises(ValueError):
            chosen_matchup = matchup_picker.choose_matchup(matchups)
            assert not chosen_matchup

class TestMatchupConfigRetriever:
    def test_map_with_specified_matchups(self):
        map = config.maps[0]
        matchups = config.map_types[MapType.open].matchups
        map.matchups = matchups
        config_retriever = MatchupConfigRetriever(matchup_config=config)
        result_matchups = config_retriever.get_matchups_for_map(map=map)
        assert result_matchups == matchups

    def test_map_with_unspecified_matchups(self):
        map = config.maps[0]
        map.matchups = None
        map.type = MapType.open
        expected_matchups = config.map_types[MapType.open].matchups
        config_retriever = MatchupConfigRetriever(matchup_config=config)
        result_matchups = config_retriever.get_matchups_for_map(map=map)
        assert result_matchups == expected_matchups


if __name__ == "__main__":
   pytest.main() 

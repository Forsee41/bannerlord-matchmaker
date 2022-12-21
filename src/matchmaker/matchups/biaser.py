from matchmaking_config import Map, MatchupModel


class MatchupBiaser:
    """Contains methods to bias passed matchups based on players' prevailing classes"""

    @staticmethod
    def bias_map_pool(maplist: list[Map]) -> list[Map]:
        """
        Takes a map list, adds a bias to their weights
        and returns a tuple of lists of maps and their weights
        """
        return maplist

    @staticmethod
    def bias_matchups(matchups: list[MatchupModel]) -> list[MatchupModel]:
        """
        Takes a list of matchups, changes their weights according
        to bias and returns them
        """
        return matchups


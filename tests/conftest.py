import json
import os
from pathlib import Path

import pytest

pytest_plugins = [
    "tests.builders",
]


@pytest.fixture(scope="session")
def testdata_path() -> str:
    testdata_path = os.getenv("TESTDATA_PATH", None)
    if not testdata_path:
        testdata_path = "tests/test_data/"
    return testdata_path


@pytest.fixture(scope="session")
def default_player_testdata(testdata_path: str) -> list[dict]:
    json_data_path = Path(testdata_path + "default_players.json")
    with open(json_data_path, "r") as file:
        player_data = json.load(file)
    return player_data


if __name__ == "__main__":
    pytest.main()

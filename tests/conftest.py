import json
import os
from pathlib import Path
from typing import Callable

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
def players_testdata_loader(testdata_path: str) -> Callable[[str], list[dict]]:
    def load_players_testdata(testdata_name: str) -> list[dict]:
        json_data_path = Path(testdata_path + testdata_name)
        with open(json_data_path, "r") as file:
            player_data = json.load(file)
        return player_data

    return load_players_testdata


if __name__ == "__main__":
    pytest.main()

import pytest
from pydantic import BaseModel

from app.enums import MapType
from app.matchmaking_config import config


class TestLocalConfigLoading:
    def test_default_config_loading(self):
        assert config, "MM config is not properly loaded"
        assert isinstance(config, BaseModel), "MM config has improper type"
        assert config.map_types[MapType.open].class_limitations.max_arch == 2


if __name__ == "__main__":
    pytest.main()

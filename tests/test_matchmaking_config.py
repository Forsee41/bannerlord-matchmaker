from pydantic import BaseModel
from app.matchmaking_config import config
from app.enums import MapType


class TestLocalConfigLoading:
    def test_default_config_loading(self):
        assert config, "MM config is not properly loaded"
        assert isinstance(config, BaseModel), "MM config has improper type"
        assert config.map_types[MapType.open].class_limitations.max_arch == 2
        

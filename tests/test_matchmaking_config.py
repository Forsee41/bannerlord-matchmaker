from pydantic import BaseModel
import matchmaking_config
from enums import MapType


class TestLocalConfigLoading:
    def test_default_config_loading(self):
        config = matchmaking_config.config
        assert config, "MM config is not properly loaded"
        assert isinstance(config, BaseModel), "MM config has improper type"
        assert config.map_types[MapType.open].class_limitations.max_arch == 2
        

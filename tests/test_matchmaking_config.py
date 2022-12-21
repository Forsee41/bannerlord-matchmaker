from pydantic import BaseModel
import matchmaking_config


class TestLocalConfigLoading:
    def test_default_config_loading(self):
        config = matchmaking_config.config
        assert config, "MM config is not properly loaded"
        assert isinstance(config, BaseModel), "MM config has improper type"
        assert config.balance.open_map_max_arch == 2
        

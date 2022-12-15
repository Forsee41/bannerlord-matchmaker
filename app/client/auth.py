import logging
import os
from dataclasses import dataclass

import httpx

from config import main_service_config
from enums import EnvVarNames


log = logging.getLogger(__name__)


@dataclass
class MainServiceCreds:
    address: str
    login: str
    password: str


AcessToken = str
RefreshToken = str


class MainServiceAuthentifier:
    access_token: AcessToken
    refresh_token: RefreshToken
    auth_route = main_service_config.auth_route
    refresh_token_route = main_service_config.refresh_token_route

    def get_env_service_creds(self) -> MainServiceCreds:

        env_vars = {
            EnvVarNames.SERVICE_ADDRESS: "",
            EnvVarNames.SERVICE_LOGIN: "",
            EnvVarNames.SERVICE_PASSWORD: "",
        }
        for env_var_name in env_vars:
            value = os.getenv(env_var_name)
            if value is None:
                error_msg = f"Couldn't load {env_var_name} env var"
                log.error(error_msg)
                raise EnvironmentError(error_msg)
            env_vars[env_var_name] = value

        return MainServiceCreds(
            address=env_vars[EnvVarNames.SERVICE_ADDRESS],
            login=env_vars[EnvVarNames.SERVICE_LOGIN],
            password=env_vars[EnvVarNames.SERVICE_PASSWORD],
        )

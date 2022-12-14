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
        main_service_login = os.getenv(EnvVarNames.service_login, None)
        main_service_password = os.getenv(EnvVarNames.service_password, None)
        main_service_address = os.getenv(EnvVarNames.service_address, None)

        if main_service_login is None:
            error_msg = f"Couldn't load {EnvVarNames.service_login} env var"
            log.error(error_msg)
            raise EnvironmentError(error_msg)

        if main_service_address is None:
            error_msg = f"Couldn't load {EnvVarNames.service_address} env var"
            log.error(error_msg)
            raise EnvironmentError(error_msg)

        if main_service_password is None:
            error_msg = f"Couldn't load {EnvVarNames.service_password} env var"
            log.error(error_msg)
            raise EnvironmentError(error_msg)

        return MainServiceCreds(
            address=main_service_address,
            login=main_service_login,
            password=main_service_password,
        )

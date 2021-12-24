import requests
import logging
from json import loads
from requests import auth
from requests.api import head
from requests.auth import HTTPBasicAuth

log = logging.getLogger(__name__)


class FMCBaseClient(object):
    """
    This class is inherited by all FMC API classes and is always instantiated and is where the auth token for the FMC
    is obtained and other functions that are needed by multiple inherited classes
    """

    def __init__(
        self,
        fmc_ip: str,
        username: str,
        password: str,
        verify: bool = True,
        fmc_port: str = None,
        timeout: int = 30,
    ):
        self.fdm_port = str(fmc_port) if fmc_port else None
        self.base_url = f"https://{fmc_ip}:{self.fmc_port}" if fmc_port else f"https://{fmc_ip}"
        self.verify = verify  # allow API self-signed certs * DANGER *
        self.common_prefix = f"{self.base_url}/api/fmc_platform/v1"
        self.verify = verify
        self.timeout = timeout
        self.username = username
        self.password = password
        self.headers = None
        self.token = None

    def get_auth_token(self):
        self.token = self.parse_auth_headers(self.post("/auth/generatetoken"))

    def get(self, endpoint: str, post_data: dict = None, headers: dict = None) -> dict:
        if headers is None:  # Allows us to override obj headers
            headers = self.headers
        r = requests.get(
            self.common_prefix + endpoint,
            headers={"Content-Type": "application/json", "X-auth-access-token": self.token["X-auth-access-token"]},
            verify=self.verify,
        )
        if r.status_code == 200:
            return r.json()
        else:
            log.error(f"API call failed with status code:{r.status_code}")

    def post(self, endpoint: str, post_data: dict = None, headers: dict = None) -> dict:
        if headers is None:  # Allows us to override headers
            headers = self.headers
        try:
            response = requests.post(
                self.common_prefix + endpoint,
                headers={"Content-Type": "application/json"},
                json=post_data,
                auth=HTTPBasicAuth(self.username, self.password),
                verify=self.verify,
                timeout=self.timeout,
            )
            if response.content:
                payload = loads(response.content.decode("utf-8"))
            elif response.status_code == 204:
                return response.headers
            else:
                payload = dict()
            return payload
        except FileNotFoundError as e:
            log.error(e)
            return {"status_code": 500}

    def parse_auth_headers(self, headers: dict):
        return {
            "USER_UUID": headers.get("USER_UUID"),
            "X-auth-access-token": headers.get("X-auth-access-token"),
            "X-auth-refresh-token": headers.get("X-auth-refresh-token"),
            "DOMAIN_ID": headers.get("DOMAIN_ID"),
            "DOMAIN_UUID": headers.get("DOMAIN_UUID"),
            "global": headers.get("global"),
            "DOMAINS": headers.get("DOMAINS"),
        }

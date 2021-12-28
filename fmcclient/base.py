import logging
import requests
from json import loads
from requests.auth import HTTPBasicAuth
from functools import wraps
from urllib.error import HTTPError

log = logging.getLogger(__name__)


class FMCHTTPWrapper(object):
    """This decorator class wraps all API methods of ths client and solves a number of issues.
    All http requests are handled by this decorator to catch 401, 404, and other errors.
    """

    # TODO work out the logic to obtain a new token but watch for race condition
    def __call__(self, fn):
        @wraps(fn)
        def new_func(*args, **kwargs):
            try:
                res = fn(*args, **kwargs)
                if res.status_code == 204:
                    # HTTP 204 No Content has no body to return. Only return the headers.
                    return res.headers
                elif res.status_code == 200:
                    try:
                        # Test to see if there is a valid json response.
                        _res = res.json()
                    except ValueError:
                        # Not a json response (could be local file read or non json data)
                        return res
                    if "error" in _res and _res["error"]["status"] in (401, 400):
                        raise HTTPError(res.url, _res["error"]["status"], _res["error"]["message"])
                return res.json()  # This should be a json response
            except HTTPError as err:
                if err.code == 401 or err.code == 400:
                    log.error(f"FMCHTTPWrapper called by {fn.__name__} - Our token appears to be invalid: {err}")
                    raise
                elif err.code == 404:
                    log.error(
                        f"FMCHTTPWrapper called by {fn.__name__} - We have called an endpoint path that is invalid: {err}"
                    )
                    raise
                else:
                    log.error(f"FMCHTTPWrapper called by {fn.__name__} - HTTP Error returned: {err}")
                    raise

        return new_func


class FMCBaseClient(object):
    """
    This class is inherited by all FMC API classes and is always instantiated and is where the auth token for the FMC
    is obtained and other functions that are needed by multiple inherited classes
    """

    PLATFORM_PREFIX = f"/api/fmc_platform/v1"
    CONFIG_PREFIX = f"/api/fmc_config/v1"

    def __init__(
        self,
        fmc_ip: str,
        username: str,
        password: str,
        verify: bool = True,
        fmc_port: str = None,
        timeout: int = 30,
    ):
        self.fmc_port = str(fmc_port) if fmc_port else None
        self.base_url = f"https://{fmc_ip}:{self.fmc_port}" if fmc_port else f"https://{fmc_ip}"
        self.verify = verify  # allow API self-signed certs * DANGER *
        self.timeout = timeout
        self.username = username
        self.password = password
        self.token = None

    def set_headers(self, headers=None):
        if headers is None:
            if self.token is not None:
                return {
                    "Content-Type": "application/json",
                    "X-auth-access-token": self.token.get("X-auth-access-token"),
                }
            else:
                return {"Content-Type": "application/json"}
        else:
            return headers

    def get_auth_token(self):
        self.token = self.parse_auth_headers(self.post(f"{self.PLATFORM_PREFIX}/auth/generatetoken", auth=True))

    @FMCHTTPWrapper()
    def get(self, endpoint: str, **kwargs) -> dict:
        """
        Perform an http get using the requests library
        :param endpoint: API endpoint to call. Like /api/fmc_platform/v1/domain/{domain_uuid}/devices/devicerecords
        :param headers: HTTP headers, including the auth token
        :param auth: Boolean True for passing basic auth with http req, otherwise omit or False
        :return: dict
        :rtype: dict
        """
        # data: dict = None, headers: dict = None, params: dict = None
        # kwargs:
        headers = kwargs.get("headers")
        auth = HTTPBasicAuth(self.username, self.password) if kwargs.get("auth") else None
        params = kwargs.get("params")
        my_headers = self.set_headers(headers=headers)
        r = requests.get(self.base_url + endpoint, headers=my_headers, verify=self.verify, params=params, auth=auth)
        return r

    @FMCHTTPWrapper()
    def post(self, endpoint: str, **kwargs) -> dict:
        """
        Perform an http post using the requests library
        :param endpoint: API endpoint to call. Like /api/fmc_platform/v1/domain/{domain_uuid}/devices/devicerecords
        :param data: dict of the data we wish to put or post
        :param headers: http headers, including the auth token
        :param auth: Boolean True for passing basic auth with http req, otherwise omit or False
        :return: dict
        :rtype: dict
        """
        # kwargs:
        data = kwargs.get("data")
        headers = kwargs.get("headers")
        auth = HTTPBasicAuth(self.username, self.password) if kwargs.get("auth") else None

        log.debug(f"Calling endpoint: {self.base_url + endpoint}")
        my_headers = self.set_headers(headers=headers)
        log.debug(f"Post payload: {data}")
        r = requests.post(
            self.base_url + endpoint,
            headers=my_headers,
            json=data,
            auth=auth,
            verify=self.verify,
            timeout=self.timeout,
        )
        log.debug(f"HTTP Request Status Code: {r.status_code}")
        return r

    @FMCHTTPWrapper()
    def put(self, endpoint: str, **kwargs) -> dict:
        """
        Perform an http put using the requests library
        :param endpoint: API endpoint to call. Like /api/fmc_platform/v1/domain/{domain_uuid}/devices/devicerecords
        :param data: dict of the data we wish to modify/put
        :param headers: HTTP headers, including the auth token
        :param auth: Boolean True for passing basic auth with http req, otherwise omit or False
        :return: dict
        :rtype: dict
        """
        # kwargs:
        data = kwargs.get("data")
        headers = kwargs.get("headers")
        auth = HTTPBasicAuth(self.username, self.password) if kwargs.get("auth") else None

        log.debug(f"Calling endpoint: {self.base_url + endpoint}")
        my_headers = self.set_headers(headers=headers)
        log.debug(f"Put payload: {data}")
        r = requests.put(
            self.base_url + endpoint,
            headers=my_headers,
            json=data,
            verify=self.verify,
            timeout=self.timeout,
        )
        log.debug(f"HTTP Request Status Code: {r.status_code}")
        return r

    @FMCHTTPWrapper()
    def delete(self, endpoint: str, **kwargs) -> dict:
        """
        Perform an http delete using the requests library
        :param endpoint: API endpoint to call. Like /api/fmc_platform/v1/domain/{domain_uuid}/devices/devicerecords
        :param headers: http headers, including the auth token
        """
        headers = kwargs.get("headers")
        my_headers = self.set_headers(headers=headers)
        r = requests.delete(self.base_url + endpoint, headers=my_headers, verify=self.verify, timeout=self.timeout)
        return r

    def parse_auth_headers(self, headers: dict):
        return {
            "USER_UUID": headers.get("USER_UUID"),
            "X-auth-access-token": headers.get("X-auth-access-token"),
            "X-auth-refresh-token": headers.get("X-auth-refresh-token"),
            "DOMAIN_ID": headers.get("DOMAIN_ID"),
            "DOMAIN_UUID": headers.get("DOMAIN_UUID"),
            "global": headers.get("global"),
            "DOMAINS": loads(headers.get("DOMAINS")),
        }
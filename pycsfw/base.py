import logging
import requests
from json import loads
from functools import wraps
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from .exceptions import DuplicateObject, DuplicateStaticRoute, RateLimitExceeded, ObjectDeletionRestricted

log = logging.getLogger(__name__)


# class DuplicateObject(Exception):
#     """Raise this exception when the API returns a 400 a duplicate object was attempted to be created"""
#
#     def __init__(self, msg):
#         self.msg = msg
#
#
# class DuplicateStaticRoute(Exception):
#     """Raise this exception when the API returns a 400 with a duplicate static route message"""
#
#     def __init__(self, msg):
#         self.msg = msg
#
#
# class RateLimitExceeded(Exception):
#     """Raise this exception when the API returns a 429 indicating we have been rate limited."""
#
#     def __init__(self, msg):
#         self.msg = msg
#
#
# class ObjectDeletionRestricted(Exception):
#     """When deleting a network object group, if the group still has members, the delete operaton will fail."""
#
#     def __init__(self, msg):
#         self.msg = msg


class HTTPWrapper(object):
    """This decorator class wraps all API calls from this client.
    All http requests are handled by this decorator to catch 401, 404, 422, and other errors.
    """

    # TODO work out the logic to obtain a new token but watch for race condition
    def __call__(self, fn):
        @wraps(fn)
        def new_func(*args, **kwargs):
            try:
                res = fn(*args, **kwargs)
                log.debug(f"Returned http status code:{res.status_code}")
                if res.status_code == 204:
                    # HTTP 204 No Content has no body to return. Only return the headers.
                    return res.headers
                elif 200 <= res.status_code <= 299:
                    try:
                        # Test to see if there is a valid json response.
                        _res = res.json()
                    except ValueError:
                        # Not a json response (could be local file read or non json data)
                        return res
                else:
                    res.raise_for_status()
                return res.json()  # This should be a json response
            except HTTPError as err:
                if res.status_code == 400:
                    """
                    Catch duplicate object errors and raise DuplicateObject exception.
                    Let the consumer decide how to handle these
                    """
                    log.error(f"FMCHTTPWrapper called by method {fn.__name__} - {err.response.text}")
                    err_msg = loads(err.response.text)
                    for msg in err_msg["error"]["messages"]:
                        if "Duplicate" in msg.get("description") or "already exists" in msg.get("description"):
                            raise DuplicateObject(msg.get("description"))
                        elif "same interface and gateway in another route" in msg.get("description"):
                            raise DuplicateStaticRoute(msg.get("description"))
                        elif "Object deletion restricted" in msg.get("description"):
                            raise ObjectDeletionRestricted(msg.get("description"))
                    raise
                elif res.status_code == 401:
                    """Catch authentication errors"""
                    log.error(
                        f"FMCHTTPWrapper called by {fn.__name__} - 401 Forbidden: Invalid token?: {err.response.text}"
                    )
                    raise
                elif res.status_code == 403:
                    """Catch forbidden errors"""
                    log.error(f"FMCHTTPWrapper called by {fn.__name__} - 403 Forbidden: {err.response.text}")
                    raise
                elif res.status_code == 404:
                    log.error(f"FMCHTTPWrapper called by {fn.__name__} - 404 Not Found: {err.response.text}")
                    raise
                elif res.status_code == 405:
                    log.error(f"FMCHTTPWrapper called by {fn.__name__} - 405 Method Not Allowed: {err.response.text}")
                    log.error(err.response.text)
                    raise
                elif res.status_code == 422:
                    log.error(
                        f"FMCHTTPWrapper called by {fn.__name__} - 422 Unprocessable Entity (Invalid Input):"
                        "{err.response.text}"
                    )
                    log.error(err.response.text)
                    raise
                elif res.status_code == 429:
                    log.error(
                        "We have been rate-limited by the Firewall Manager. (Default is 120 messages per minute from"
                        "an individual IP address. We are pausing requests for 30 seconds..."
                    )
                    raise RateLimitExceeded("API rate limit exceeded.")

                else:
                    log.error(f"FMCHTTPWrapper called by {fn.__name__} - HTTP Error returned: {err.response.text}")
                    raise

        return new_func


class BaseClient(object):
    """
    This class is inherited by all FMC API classes and is always instantiated and is where the auth token for the CSFMC
    is obtained and other functions that are needed by multiple inherited classes
    """

    PLATFORM_PREFIX = f"/api/fmc_platform/v1"
    CONFIG_PREFIX = f"/api/fmc_config/v1"

    def __init__(
        self,
        ip: str,
        username: str,
        password: str,
        verify: str = None,
        port: str = None,
        timeout: int = 30,
    ) -> None:
        """
        :param ip: The IP of the Cisco Secure Firewall Management Center
        :param username: The username for the CSFMC
        :param password: The password for the CSFMC
        :param verify: path to the CA certificate for the CA you want to use for certificate validation
        :param port: The port that the CSFMC API is listening on (Default = 443)
        :param timeout: TCP timeout when attempting to reach the CSFMC API
        """
        self.port = str(port) if port else None
        self.base_url = f"https://{ip}:{self.port}" if port else f"https://{ip}"
        self.verify = verify
        self.timeout = timeout
        self.username = username
        self.password = password
        self.token = None
        self.domain_uuid = None
        self.get_auth_token()

    def set_headers(self, headers: dict = None) -> dict:
        """
        Used to override the headers that will be sent with every API call to the CSFMC
        :param headers: dict of headers to send with each API call. Note that if a user supplies this variable,
                        they will also need "Content-Type" and "X-auth-access-token" headers in this dict
        """
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

    @HTTPWrapper()
    def get(self, endpoint: str, **kwargs: dict) -> dict:
        """
        Perform an http get using the requests library
        :param endpoint: API endpoint to call. Like /api/fmc_platform/v1/domain/{domain_uuid}/devices/devicerecords
        :param headers: HTTP headers, including the auth token
        :param auth: Boolean True for passing basic auth with http req, otherwise omit or False
        :param params: The http parameters (http query) to append to the URL
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

    @HTTPWrapper()
    def post(self, endpoint: str, **kwargs: dict) -> dict:
        """
        Perform an http post using the requests library
        :param endpoint: API endpoint to call. Like /api/fmc_platform/v1/domain/{domain_uuid}/devices/devicerecords
        :param data: dict of the data we wish to put or post
        :param headers: http headers, including the auth token
        :param auth: Boolean True for passing basic auth with http req, otherwise omit or False
        :param params: The http parameters (http query) to append to the URL
        :return: dict
        :rtype: dict
        """
        # kwargs:
        data = kwargs.get("data")
        headers = kwargs.get("headers")
        params = kwargs.get("params")
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
            params=params,
        )
        return r

    @HTTPWrapper()
    def put(self, endpoint: str, **kwargs: dict) -> dict:
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
        return r

    @HTTPWrapper()
    def delete(self, endpoint: str, **kwargs: dict) -> dict:
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

    def _serialize_objects(self, obj_list: list) -> list:
        serializable_objs = []
        for i, net_obj in enumerate(obj_list):
            obj_list[i].metadata = None
            serializable_objs.append(obj_list[i].dict(exclude_unset=True))
        return serializable_objs

    def get_domain_uuid(self, domain_name: str) -> str:
        """
        Given a Cisco Secure Firewall Manager Domain, set and then return the domain's UUID
        :param domain_name: The domain name of the Firewall Manager's domain. e.g. "Global/Customer A"
        :return: The str containing the UUID of the domain on which we wish to perfomm API calls
        :rtype: str
        """
        domain_uuid = [domain for domain in self.token["DOMAINS"] if domain["name"] == domain_name]
        if domain_uuid:
            self.domain_uuid = domain_uuid[0].get("uuid")

import logging

log = logging.getLogger(__name__)


class DuplicateObject(Exception):
    """Raise this exception when the API returns a 400 a duplicate object was attempted to be created"""

    def __init__(self, msg="DuplicateObject Error"):
        self.msg = msg


class DuplicateStaticRoute(Exception):
    """Raise this exception when the API returns a 400 with a duplicate static route message"""

    def __init__(self, msg):
        self.msg = msg


class RateLimitExceeded(Exception):
    """Raise this exception when the API returns a 429 indicating we have been rate limited."""

    def __init__(self, msg="RateLimitExceeded Error"):
        self.msg = msg


class ObjectDeletionRestricted(Exception):
    """When deleting a network object group, if the group still has members, the delete operaton will fail."""

    def __init__(self, msg="ObjectDeletionRestricted Error"):
        self.msg = msg

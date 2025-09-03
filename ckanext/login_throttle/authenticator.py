import logging

from ckan.lib.authenticator import default_authenticate
import ckan.plugins.toolkit as tk
from ckan.model import User, AnonymousUser

from .login_throttle import LoginThrottle
import ckanext.login_throttle.config as throttle_config

log = logging.getLogger(__name__)


def get_request_ip_address(request):
    """Retrieves the IP address from the request if possible"""
    remote_addr = request.headers.get("X-Forwarded-For") or request.environ.get(
        "REMOTE_ADDR"
    )
    if remote_addr is None:
        log.critical("X-Forwarded-For header/REMOTE_ADDR missing from request.")

    return remote_addr


def get_login_throttle_key(request, user_name):
    login_throttle_key = get_request_ip_address(request)
    if throttle_config.login_throttle_brute_force_key() == "user_name":
        login_throttle_key = user_name

    return login_throttle_key


def get_user_throttle(user_name):
    if throttle_config.login_throttle_brute_force_key() != "user_name":
        return {}
    return LoginThrottle(User.by_name(user_name), user_name).get()


def get_address_throttle(address):
    if throttle_config.login_throttle_brute_force_key() == "user_name":
        return {}
    return LoginThrottle(None, address).get()


def reset_user_throttle(user_name):
    if throttle_config.login_throttle_brute_force_key() != "user_name":
        return
    LoginThrottle(User.by_name(user_name), user_name).reset()


def reset_address_throttle(address):
    if throttle_config.login_throttle_brute_force_key() == "user_name":
        return
    LoginThrottle(None, address).reset()


def authenticate(identity):
    """A username/password authenticator that throttles login request
    by user name, ie only a limited number of attempts can be made
    to log into a specific account within a period of time."""
    # Run through the CKAN auth sequence first, so we can hit the DB
    # in every case and make timing attacks a little more difficult.
    ckan_auth_result = default_authenticate(identity)

    try:
        user_name = identity["login"]
    except KeyError:
        return None

    login_throttle_key = get_login_throttle_key(tk.request, user_name)

    if login_throttle_key is None:
        return None

    throttle = LoginThrottle(User.by_name(user_name), login_throttle_key)
    # Check if there is a lock on the requested user, and abort if
    # we have a lock.

    if throttle.is_locked():
        return AnonymousUser()

    if ckan_auth_result is None:
        # Increment the throttle counter if the login failed.
        throttle.increment()
        return None

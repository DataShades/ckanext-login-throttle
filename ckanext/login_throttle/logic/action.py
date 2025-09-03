from ckanext.login_throttle.authenticator import (
    get_user_throttle,
    get_address_throttle,
    reset_user_throttle,
    reset_address_throttle,
    get_login_throttle_key,
)
import ckan.plugins.toolkit as tk


def login_throttle_user_reset(context, data_dict):
    """
    Reset throttling information for a user, allowing logins

    address: user name
    """
    tk.check_access("login_throttle_user_reset", context, data_dict)
    user = tk.get_or_bust(data_dict, "user")
    return reset_user_throttle(user)


def login_throttle_address_reset(context, data_dict):
    """
    Reset throttling information for an address, allowing logins

    address: IP address
    """
    tk.check_access("login_throttle_address_reset", context, data_dict)
    address = tk.get_or_bust(data_dict, "address")
    return reset_address_throttle(address)


def login_throttle_user_show(context, data_dict):
    """
    Retrieve the throttling information for a user

    user: user name
    """
    tk.check_access("login_throttle_user_show", context, data_dict)
    user = tk.get_or_bust(data_dict, "user")
    return get_user_throttle(user)


def login_throttle_address_show(context, data_dict):
    """
    Retrieve the throttling information for an IP address

    address: IP address
    """

    tk.check_access("login_throttle_address_show", context, data_dict)
    address = tk.get_or_bust(data_dict, "address")
    return get_address_throttle(address)


@tk.chained_action
def user_update(up_func, context, data_dict):
    """
    ckanext-login-throttle: reset throttling information for updated users
    to allow new login attempts after password reset
    """
    rval = up_func(context, data_dict)

    tk.get_action("login_throttle_user_reset")(
        dict(context, ignore_auth=True), {"user": rval["name"]}
    )

    login_throttle_key = get_login_throttle_key(tk.request, rval["name"])
    # Need to make sure we clear the Address
    if login_throttle_key and login_throttle_key != rval["name"]:
        tk.get_action("login_throttle_address_reset")(
            dict(context, ignore_auth=True), {"address": login_throttle_key}
        )

    return rval

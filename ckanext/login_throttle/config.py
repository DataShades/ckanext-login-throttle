import ckan.plugins.toolkit as tk

LOGIN_THROTTLE_KEY = "ckanext.login_throttle.brute_force_key"
LOGIN_THROTTLE_FOOTER_PATH = "ckanext.login_throttle.brute_force_footer_path"
LOGIN_THROTTLE_LOCK_TIMEOUT = "ckanext.login_throttle.lock_timeout"
LOGIN_THROTTLE_MAX_COUNT = "ckanext.login_throttle.login_max_count"
LOGIN_THROTTLE_BLOCK_LOCK_NOTIFICATION = (
    "ckanext.login_throttle.disable_lock_notification"
)


def login_throttle_brute_force_key():
    return tk.config.get(LOGIN_THROTTLE_KEY)


def login_throttle_footer_path():
    return tk.config.get(LOGIN_THROTTLE_FOOTER_PATH)


def login_throttle_lock_timeout():
    return tk.config.get(LOGIN_THROTTLE_LOCK_TIMEOUT)


def login_throttle_max_count():
    return tk.config.get(LOGIN_THROTTLE_MAX_COUNT)


def login_throttle_block_lock_notification():
    return tk.config.get(LOGIN_THROTTLE_BLOCK_LOCK_NOTIFICATION)

import pytest

from ckan.lib.helpers import url_for
from ckan.tests import factories, helpers
from ckan.model import User

from ckanext.login_throttle.login_throttle import LoginThrottle


@pytest.mark.usefixtures("clean_db", "with_plugins")
class TestLoginThrottleAuthenticator:
    @pytest.mark.ckan_config("ckanext.login_throttle.disable_lock_notification", True)
    def test_login_throttle_authenticator(self, app, normal_user):
        username = normal_user["name"]
        address = "127.0.0.1"

        # Make sure no old records
        LoginThrottle(User.by_name(username), address).delete()

        app.post(
            url_for("user.login"),
            data={"login": username, "password": "TestPassword123"},
            environ_overrides={"REMOTE_ADDR": address},
        )

        result = helpers.call_action(
            "login_throttle_address_show", {"ignore_auth": True}, address=address
        )

        assert result.get("count") == 1

        app.post(
            url_for("user.login"),
            data={"login": username, "password": "TestPassword1"},
            environ_overrides={"REMOTE_ADDR": address},
        )

        result = helpers.call_action(
            "login_throttle_address_show", {"ignore_auth": True}, address=address
        )

        assert result.get("count") == 1

        app.post(
            url_for("user.login"),
            data={"login": username, "password": "TestPassword123"},
            environ_overrides={"REMOTE_ADDR": address},
        )

        result = helpers.call_action(
            "login_throttle_address_show", {"ignore_auth": True}, address=address
        )

        # User should be locked
        resp = app.post(
            url_for("user.login"),
            data={"login": username, "password": "TestPassword1"},
            environ_overrides={"REMOTE_ADDR": address},
        )

        assert helpers.body_contains(resp, '<li><a href="/user/login">Log in</a></li>')

        locked = LoginThrottle(User.by_name(username), address).is_locked()

        assert True == locked

        locked = LoginThrottle(User.by_name(username), address).reset()

        resp = app.post(
            url_for("user.login"),
            data={"login": username, "password": "TestPassword1"},
            environ_overrides={"REMOTE_ADDR": address},
        )

        assert False == helpers.body_contains(
            resp, '<li><a href="/user/login">Log in</a></li>'
        )
        assert helpers.body_contains(resp, '<span class="text">Profile settings</span>')

        # clear Redis keys
        LoginThrottle(User.by_name(username), address).delete()

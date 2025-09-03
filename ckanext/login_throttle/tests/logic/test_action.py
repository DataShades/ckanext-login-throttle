import pytest

from ckan.lib.helpers import url_for
from ckan.tests import factories, helpers
from ckan.model import User

from ckanext.login_throttle.login_throttle import LoginThrottle


@pytest.mark.usefixtures("clean_db", "with_plugins")
class TestLoginThrottleActions:
    @pytest.mark.ckan_config("ckanext.login_throttle.brute_force_key", "user_name")
    def test_reset_throttle_user(self, app, normal_user):
        username = normal_user["name"]

        # Make sure no old records
        LoginThrottle(User.by_name(username), username).delete()

        app.post(
            url_for("user.login"),
            data={"login": username, "password": "TestPassword123"},
        )

        result = helpers.call_action(
            "login_throttle_user_show", {"ignore_auth": True}, user=username
        )

        assert result.get("count") == 1

        helpers.call_action(
            "login_throttle_user_reset", {"ignore_auth": True}, user=username
        )

        result = helpers.call_action(
            "login_throttle_user_show", {"ignore_auth": True}, user=username
        )

        assert result.get("count") == 0

        # clear Redis keys
        LoginThrottle(User.by_name(username), username).delete()

    @pytest.mark.ckan_config("ckanext.login_throttle.brute_force_key", "user_name")
    def test_show_throttle_user(self, app, normal_user):
        username = normal_user["name"]

        # Make sure no old records
        LoginThrottle(User.by_name(username), username).delete()

        result = helpers.call_action(
            "login_throttle_user_show", {"ignore_auth": True}, user=username
        )

        assert result == {}

        app.post(
            url_for("user.login"),
            data={"login": username, "password": "TestPassword123"},
        )

        result = helpers.call_action(
            "login_throttle_user_show", {"ignore_auth": True}, user=username
        )

        assert result.get("count") == 1

        # clear Redis keys
        LoginThrottle(User.by_name(username), username).delete()
        # assert False

    def test_reset_throttle_address(self, app, normal_user):
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

        helpers.call_action(
            "login_throttle_address_reset", {"ignore_auth": True}, address=address
        )

        result = helpers.call_action(
            "login_throttle_address_show", {"ignore_auth": True}, address=address
        )

        assert result.get("count") == 0

        # clear Redis keys
        LoginThrottle(User.by_name(username), address).delete()

    def test_show_throttle_address(self, app, normal_user):
        username = normal_user["name"]
        address = "127.0.0.1"

        # Make sure no old records
        LoginThrottle(User.by_name(username), address).delete()

        result = helpers.call_action(
            "login_throttle_address_show", {"ignore_auth": True}, address=address
        )

        assert result == {}

        app.post(
            url_for("user.login"),
            data={"login": username, "password": "TestPassword123"},
            environ_overrides={"REMOTE_ADDR": address},
        )

        result = helpers.call_action(
            "login_throttle_address_show", {"ignore_auth": True}, address=address
        )

        assert result.get("count") == 1

        # clear Redis keys
        LoginThrottle(User.by_name(username), address).delete()

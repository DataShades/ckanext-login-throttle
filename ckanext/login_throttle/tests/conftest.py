import pytest

from ckan.tests import factories


@pytest.fixture
def normal_user():
    return factories.User(password="TestPassword1", name="test_throttle_user")

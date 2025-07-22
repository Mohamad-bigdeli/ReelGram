import pytest
from rest_framework.test import APIClient
from apps.users.tests.fixtures import *

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
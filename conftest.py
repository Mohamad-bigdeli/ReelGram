import pytest
from rest_framework.test import APIClient
from apps.users.tests.fixtures import *

@pytest.fixture(scope="class")
def api_client() -> APIClient:
    return APIClient()
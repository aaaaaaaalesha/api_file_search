import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def unexpected_search_id():
    return 'c303282d-f2e6-46ca-a04a-35d3d873712d'

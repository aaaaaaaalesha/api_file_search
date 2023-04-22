import os

import pytest

from rest_framework.test import APIClient
from django.conf import settings


@pytest.fixture(scope='session')
def django_set_search_dir():
    settings.SEARCH_DIR = os.path.join(
        settings.BASE_DIR.parent,
        'tests',
        'test_searchdir',
    )


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def unexpected_search_id():
    return 'c303282d-f2e6-46ca-a04a-35d3d873712d'

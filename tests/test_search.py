from http import HTTPStatus

from django.db.utils import IntegrityError
import pytest

from search.models import Search

@pytest.mark.django_db(transaction=True)
class TestSearchAPI:
    pass
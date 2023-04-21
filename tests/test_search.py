import os.path
import uuid

import pytest

from http import HTTPStatus
from rest_framework.test import APIClient

from search.models import Search


@pytest.mark.django_db
class TestSearchAPI:
    URL_SEARCH = '/search'
    URL_SEARCHES = '/searches/'

    def test_search_not_found(self, client: APIClient):
        response = client.post(self.URL_SEARCH, data={})
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Endpoint `{self.URL_SEARCH}` not found, check *urls.py*.'
        )

    def test_searches_not_finished(self, client: APIClient, unexpected_search_id: str):
        response = client.get(self.URL_SEARCHES + unexpected_search_id)
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Endpoint `{self.URL_SEARCHES}` not found, check *urls.py*.'
        )

        assert response.status_code == HTTPStatus.OK
        assert response.data and 'finished' in response.data

        assert not response.data['finished'], (
            'Response must be { "finished" = false } in case of uncompleted search.'
        )

    def test_search(
            self,
            client,
            search_params_0,
            search_params_1,
            search_params_2,
            search_python_files,
            search_result_0,
            search_result_1,
            search_result_2,
            search_python_files_result,
    ):
        for search_params, search_results in zip(
                (search_params_0, search_params_1, search_params_2, search_python_files),
                (search_result_0, search_result_1, search_result_2, search_python_files_result),
        ):
            # POST.
            response = client.post(self.URL_SEARCH, data=search_params)
            assert response.status_code == HTTPStatus.CREATED, (
                f'POST request to {self.URL_SEARCH} have status code {response.status_code}.'
            )

            assert response.data and 'search_id' in response.data, (
                'Response body have no key search_id.'
            )

            search_id = response.data['search_id']

            assert Search.objects.filter(
                search_id=uuid.UUID(search_id)
            ).exists(), (
                f'search_id={search_id} not found in database after POST method'
            )

            # GET.
            url_searches = self.URL_SEARCHES + search_id
            response = client.get(url_searches)
            assert response.status_code == HTTPStatus.OK, (
                f'GET request to {url_searches} have status code {response.status_code}.'
            )
            assert response.data['finished'] == search_results['finished'], (
                'It seems like search not finished yet.'
            )

            assert len(response.data['paths']) == len(search_results['paths']), (
                f'Fail size of response paths list.'
            )

            assert set(
                os.path.basename(p) for p in response.data['paths']
            ) == set(
                os.path.basename(p) for p in search_results['paths']
            )

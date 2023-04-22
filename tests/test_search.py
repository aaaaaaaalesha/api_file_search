import json
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

    def __base_search_case(self, client, search_params, search_results):
        # POST to /search
        response = client.post(
            self.URL_SEARCH,
            data=search_params,
            format='json',
        )
        # Check that we receive the correct status code.
        assert response.status_code == HTTPStatus.CREATED, (
            f'POST request to {self.URL_SEARCH} have status code {response.status_code}.'
        )
        # Check that search_id exists in response.
        assert response.data and 'search_id' in response.data, (
            'Response body have no key search_id.'
        )

        search_id = response.data['search_id']
        # Check that search_id now exists in database.
        assert Search.objects.filter(
            search_id=uuid.UUID(search_id)
        ).exists(), (
            f'search_id={search_id} not found in database after POST method'
        )

        # GET to /searches/<search_id>
        url_searches = self.URL_SEARCHES + search_id
        response = client.get(url_searches)

        # Check status code.
        assert response.status_code == HTTPStatus.OK, (
            f'GET request to {url_searches} have status code {response.status_code}.'
        )
        # Check "finished" field is correct.
        assert response.data['finished'] == search_results['finished'], (
            'It seems like search not finished yet.'
        )
        # Check that counts of files are equal.
        assert len(response.data['paths']) == len(search_results['paths']), (
            f'Fail size of response paths list.'
        )
        # Check that found files are correct.
        assert set(
            os.path.basename(p) for p in response.data['paths']
        ) == set(
            os.path.basename(p) for p in search_results['paths']
        )

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

    def test_invalid_request(self, client: APIClient, invalid_params):
        response = client.post(self.URL_SEARCH, data=invalid_params, format='json')
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_search_all(
            self,
            client: APIClient,
            search_all,
            search_result_all,
    ):
        # To search all files, we need to no pass any parameters to request body.
        self.__base_search_case(client, search_all, search_result_all)

    def test_search_python_files(
            self,
            client: APIClient,
            python_files_mask,
            python_files_result,
    ):
        self.__base_search_case(client, python_files_mask, python_files_result)

    def test_complex_search(
            self,
            client,
            search_params_1,
            search_params_2,
            search_result_1,
            search_result_2,
    ):
        for search_params, search_result in zip(
                (search_params_1, search_params_2),
                (search_result_1, search_result_2),
        ):
            self.__base_search_case(client, search_params, search_result)

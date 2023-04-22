import json

import pytest


@pytest.fixture
def invalid_params():
    return {
        "text": 1,
        "file_mask": False,
        "size": 10,
        "creation_time": 10e-10,
    }


@pytest.fixture
def search_all():
    return {}


@pytest.fixture
def python_files_mask():
    return {
        "file_mask": "*.py",
    }


@pytest.fixture
def search_params_1():
    return {
        "text": "aaaaaaaalesha",
        "file_mask": "*.*",
        "size": {
            "value": 200,
            "operator": "gt",
        },
    }


@pytest.fixture
def search_params_2():
    return {
        "text": "std::",
        "file_mask": "[!u]*.hpp",
        "size": {
            "value": 1213,
            "operator": "gt",
        },
        "creation_time": {
            "value": "2022-09-13T11:00:00Z",
            "operator": "ge",
        }
    }

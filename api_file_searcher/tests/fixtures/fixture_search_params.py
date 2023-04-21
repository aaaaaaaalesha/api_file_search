import pytest


@pytest.fixture
def search_params_0():
    return {}


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


@pytest.fixture
def search_python_files():
    return {
        "file_mask": "*.py",
    }

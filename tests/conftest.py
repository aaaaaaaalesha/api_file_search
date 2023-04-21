import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = 'api_file_searcher'

if (
        PROJECT_DIR_NAME not in root_dir_content
        or not os.path.isdir(os.path.join(BASE_DIR, PROJECT_DIR_NAME))
):
    assert False, (
        f'In directory `{BASE_DIR}` not found directory '
        f'`{PROJECT_DIR_NAME}`. Make sure that tou have correct project structure.'
    )

MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
project_dir_content = os.listdir(MANAGE_PATH)
FILENAME = 'manage.py'

if FILENAME not in project_dir_content:
    assert False, (
        f'In directory `{MANAGE_PATH}` not found file `{FILENAME}`. '
        f'Make sure that tou have correct project structure.'
    )

pytest_plugins = [
    'tests.fixtures.fixture_data',
    'tests.fixtures.fixture_search_params',
    'tests.fixtures.fixture_search_results',
]

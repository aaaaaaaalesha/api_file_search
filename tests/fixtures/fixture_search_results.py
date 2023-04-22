import os
import pytest


@pytest.fixture
def search_result_all():
    return {
        'finished': True,
        'paths': [
            'Procfile',
            os.path.join('testcompressed.zip', 'dir', 'test_splay_tree.py'),
            os.path.join('testcompressed.zip', 'dir', 'test_unordered_map.cpp'),
            os.path.join('testcompressed.zip', 'dir', 'test_unrolled_linked_list.cpp'),
            os.path.join('testcompressed.zip', 'favicon-16x16.png'),
            os.path.join('testcompressed.zip', '20.03.01.000_9.tif.aux.xml'),
            os.path.join('testcompressed.zip', 'colorfile.clr'),
            os.path.join('testcompressed.zip', 'hello.txt'),
            'testcompressed.zip',
            os.path.join('splay_tree', 'splay_tree.py'),
            os.path.join('unordered_map', 'array.hpp'),
            os.path.join('unordered_map', 'iterator.hpp'),
            os.path.join('unordered_map', 'unordered_map.hpp'),
            os.path.join('unrolled_linked_list', 'array.hpp'),
            os.path.join('unrolled_linked_list', 'iterator.hpp'),
            os.path.join('unrolled_linked_list', 'unrolled_linked_list.hpp'),
        ],
    }


@pytest.fixture
def python_files_result():
    return {
        'finished': True,
        'paths': [
            os.path.join('testcompressed.zip', 'dir', 'test_splay_tree.py'),
            os.path.join('splay_tree', 'splay_tree.py'),
        ],
    }


@pytest.fixture
def search_result_1():
    return {
        'finished': True,
        'paths': [
            os.path.join('testcompressed.zip', 'dir', 'test_unordered_map.cpp'),
            os.path.join('testcompressed.zip', 'dir', 'test_unrolled_linked_list.cpp'),
            os.path.join('splay_tree', 'splay_tree.py'),
            os.path.join('unordered_map', 'array.hpp'),
            os.path.join('unordered_map', 'iterator.hpp'),
            os.path.join('unordered_map', 'unordered_map.hpp'),
            os.path.join('unrolled_linked_list', 'array.hpp'),
            os.path.join('unrolled_linked_list', 'iterator.hpp'),
            os.path.join('unrolled_linked_list', 'unrolled_linked_list.hpp'),
        ],
    }


@pytest.fixture
def search_result_2():
    return {
        'finished': True,
        'paths': [
            os.path.join('unordered_map', 'iterator.hpp'),
            os.path.join('unrolled_linked_list', 'array.hpp'),
            os.path.join('unrolled_linked_list', 'iterator.hpp'),
        ],
    }

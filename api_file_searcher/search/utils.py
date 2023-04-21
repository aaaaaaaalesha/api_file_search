import os
import zipfile
import datetime as dt

from fnmatch import fnmatch
from typing import Any, TypeAlias

from django.conf import settings

SearchParams: TypeAlias = dict[str, dict[str, Any] | str] | None

# Available SearchParams keys.
TEXT_KEY = 'text'
FILE_MASK_KEY = 'file_mask'
SIZE_KEY = 'size'
CREATION_TIME_KEY = 'creation_time'
VALUE_KEY = 'value'
OPERATOR_KEY = 'operator'


def search(
        search_params: SearchParams,
        search_dir=settings.SEARCH_DIR,
) -> list[str]:
    """
    Implements searching files in passed directory.
    Searches can be performed:
        - by the occurrence of a substring of text in the content of the file;
        - by file_mask in glob format;
        - by file size;
        - by file creation time.
    :param search_params: 
        - "text" substring whose occurrence is checked in target file contents;
        - "file_mask": string file mask with glob format;
        - "size": dict with two params: file size in bytes
        and operator (one of 'eq', 'gt', 'lt', 'ge', 'le');
        - "creation_time" dict with two params: creation time string in
        format RFC 3339 and operator (one of 'eq', 'gt', 'lt', 'ge', 'le');
    :param search_dir: entrypoint directory of searching files.

    :return: list of paths matching the search parameters.
    """
    paths = []
    for dirpath, _, filenames in os.walk(search_dir):
        for filename in filenames:
            __collect_matching_files(
                # Construct path to file.
                os.path.join(dirpath, filename),
                search_params,
                search_dir,
                collect_to=paths,
            )

    return paths


def __zip_handler(
        filepath: str,
        search_params: SearchParams,
        search_dir: str,
        collect_to: list[str],
) -> None:
    """
    Search files inside zip file (excluding nested zips).
    :param filepath: path to zip file.
    :param search_dir: path to target search directory root.
    :param collect_to: list where suitable files will be collected.
    :return: None.
    """
    with zipfile.ZipFile(filepath, 'r') as zip_file:
        for file_info in zip_file.infolist():
            if file_info.filename.endswith('.zip'):
                continue

            # Check size of file.
            if SIZE_KEY in search_params:
                value = search_params[SIZE_KEY][VALUE_KEY]
                operator = search_params[SIZE_KEY][OPERATOR_KEY]
                if not settings.OPERATOR[operator](file_info.file_size, value):
                    continue

            # Check file creation time.
            if CREATION_TIME_KEY in search_params:
                value = search_params[CREATION_TIME_KEY][VALUE_KEY]
                operator = search_params[CREATION_TIME_KEY][OPERATOR_KEY]
                if not settings.OPERATOR[operator](
                        dt.datetime(*file_info.date_time),
                        dt.datetime.fromisoformat(value),
                ):
                    continue

            # Check file_mask.
            if FILE_MASK_KEY in search_params and not fnmatch(
                    os.path.basename(file_info.filename),
                    search_params[FILE_MASK_KEY],
            ):
                return

            # And finally check file content.
            if TEXT_KEY in search_params:
                with zip_file.open(file_info, mode='r') as file:
                    if TEXT_KEY not in file.read().decode(errors='ignore'):
                        return

            collect_to.append(os.path.join(
                filepath[len(search_dir) + 1:],
                file_info.filename,
            ))


def __collect_matching_files(
        filepath: str,
        search_params: SearchParams,
        search_dir: str,
        collect_to: list[str],
) -> None:
    """
    Collects paths to files that satisfy the passed parameters.
    If the file is a zip archive, searches for files within the archives (excluding nested zip archives).
    :param filepath: path to zip file.
    :param search_dir: path to target search directory root.
    :param collect_to: list where suitable files will be collected.
    :return: None.
    """
    if filepath.endswith('.zip'):
        __zip_handler(filepath, search_params, search_dir, collect_to)
        return

    # Firstly check metadata. Its easier and less complex.
    # Check size of file.
    if SIZE_KEY in search_params:
        value = search_params[SIZE_KEY][VALUE_KEY]
        operator = search_params[SIZE_KEY][OPERATOR_KEY]
        if not settings.OPERATOR[operator](os.path.getsize(filepath), value):
            return

    # Check file creation time.
    if CREATION_TIME_KEY in search_params:
        value = search_params[CREATION_TIME_KEY][VALUE_KEY]
        operator = search_params[CREATION_TIME_KEY][OPERATOR_KEY]
        if not settings.OPERATOR[operator](
                os.path.getctime(filepath),
                dt.datetime.fromisoformat(value).timestamp(),
        ):
            return

    # Check file_mask.
    if FILE_MASK_KEY in search_params and not fnmatch(
            os.path.basename(filepath), search_params[FILE_MASK_KEY]
    ):
        return

    # And finally check file content.
    if TEXT_KEY in search_params:
        with open(filepath, mode='r', encoding='UTF-8') as file:
            if search_params[TEXT_KEY] not in file.read():
                return

    collect_to.append(filepath[len(search_dir) + 1:])

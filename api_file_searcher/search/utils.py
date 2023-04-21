import os
import zipfile
import datetime as dt

from fnmatch import fnmatch

from django.conf import settings


def search(
        text: str | None,
        filemask: str | None,
        size: dict[str, int | str] | None,
        creation_time: dict[str, str] | None,
        search_dir=settings.SEARCH_DIR,
) -> list[str]:
    """
    Implements searching files in passed directory.
    Searches can be performed:
        - by the occurrence of a substring of text in the content of the file;
        - by file_mask in glob format;
        - by file size;
        - by file creation time.
    :param text: substring whose occurrence is checked in target file contents.
    :param filemask: string file mask with glob format.
    :param size: tuple with two params: file size in bytes
    and operator (one of 'eq', 'gt', 'lt', 'ge', 'le').
    :param creation_time: tuple with two params: creation time string in
    format RFC 3339 and operator.
    (one of 'eq', 'gt', 'lt', 'ge', 'le')
    :param search_dir: entrypoint directory of searching files.

    :return: list of paths matching the search parameters.
    """
    paths = []
    for dirpath, subdirs, filenames in os.walk(search_dir):
        for filename in filenames:
            __collect_matching_files(
                os.path.join(dirpath, filename),
                text,
                filemask,
                size,
                creation_time,
                search_dir,
                collect_to=paths,
            )

    return paths


def __zip_handler(
        filepath: str,
        text: str | None,
        filemask: str | None,
        size: dict[str, int | str] | None,
        creation_time: dict[str, str] | None,
        search_dir: str,
        collect_to: list[str],
) -> None:
    """
    Search files inside zip file (excluding nested zips).
    :param filepath:
    :param text:
    :param filemask:
    :param size:
    :param creation_time:
    :param search_dir:
    :param collect_to:
    :return:
    """
    with zipfile.ZipFile(filepath, 'r') as zip_file:
        for file_info in zip_file.infolist():
            if file_info.filename.endswith('.zip'):
                continue

            # Check size of file.
            if size is not None:
                value, operator = size['value'], size['operator']
                if not settings.OPERATOR[operator](file_info.file_size, value):
                    continue

            # Check file creation time.
            if creation_time is not None:
                value, operator = creation_time['value'], creation_time['operator']
                if not settings.OPERATOR[operator](
                        file_info.date_time,  # TODO: fix mistake
                        dt.datetime.fromisoformat(value).timestamp()
                ):
                    continue

            # Check filemask.
            if filemask is not None and not fnmatch(os.path.basename(file_info.filename), filemask):
                return

            # And finally check file content.
            if text is not None:
                with zip_file.open(file_info, mode='r') as file:
                    if text not in file.read().decode(errors='ignore'):
                        return

            collect_to.append(os.path.join(filepath[len(search_dir) + 1:], file_info.filename))


def __collect_matching_files(
        filepath: str,
        text: str | None,
        filemask: str | None,
        size: dict[str, int | str] | None,
        creation_time: dict[str, str] | None,
        search_dir: str,
        collect_to: list[str],
) -> None:
    """
    Collects paths to files that satisfy the passed parameters.
    If the file is a zip archive, searches for files within the archives (excluding nested zip archives).
    :param filepath:
    :param text:
    :param filemask:
    :param size:
    :param creation_time:
    :param search_dir:
    :param collect_to:
    :return:
    """
    if filepath.endswith('.zip'):
        __zip_handler(
            filepath,
            text,
            filemask,
            size,
            creation_time,
            search_dir,
            collect_to,
        )
        return

    # Firstly check metadata. Its easier and less complex.
    # Check size of file.
    if size is not None:
        value, operator = size['value'], size['operator']
        if not settings.OPERATOR[operator](os.path.getsize(filepath), value):
            return

    # Check file creation time.
    if creation_time is not None:
        value, operator = creation_time['value'], creation_time['operator']
        if not settings.OPERATOR[operator](
                os.path.getctime(filepath),
                dt.datetime.fromisoformat(value).timestamp(),
        ):
            return

    # Check filemask.
    if filemask is not None and not fnmatch(os.path.basename(filepath), filemask):
        return

    # And finally check file content.
    if text is not None:
        with open(filepath, mode='r', encoding='UTF-8') as file:
            if text not in file.read():
                return

    collect_to.append(filepath[len(search_dir) + 1:])

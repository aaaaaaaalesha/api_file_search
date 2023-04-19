import os
import glob
import fnmatch

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Search, SearchResult
from .serializers import SearchSerializer, SearchResultSerializer

from typing import Optional, List, Tuple

# TODO: maybe move it to another place
SEARCH_DIR = os.getenv('SEARCH_DIR', default='.')


class SearchView(APIView):
    @staticmethod
    def __search(
            text: Optional[str],
            filemask: Optional[str],
            size: Optional[Tuple[int, str]],
            creation_time: Optional[Tuple[int, str]],
            search_dir=SEARCH_DIR,
    ) -> List[str]:
        """
        Implements searching files in passed directory.
        Searches can be performed:
            - by the occurrence of a substring of text in the content of the file;
            - by file_mask in glob format;
            - by file size;
            - by file creation time.
        :param text: substring whose occurrence is checked in target file contents
        :param filemask: string file mask with glob format
        :param size: tuple with two params: file size in bytes and operator (one of 'eq', 'gt', 'lt', 'ge', 'le')
        :param creation_time: tuple with two params: creation time string in format RFC 3339 and operator
        (one of 'eq', 'gt', 'lt', 'ge', 'le').

        :return: list of paths matching the search parameters.
        """
        result = []
        for dirpath, dirnames, filenames in os.walk(search_dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                # substr matching
                with open(file_path, mode='r', encoding='utf-8') as file:
                    if text in file.read():
                        pass
                # file mask matching
                if fnmatch.fnmatch(file_path, filemask):
                    pass

                # size matching

                # file creation time matching


    def post(self, request) -> Response:
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            search = serializer.save()
            # запустите поиск файлов в фоновом режиме
            return Response(
                {'search_id': str(search.search_id)},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class SearchResultView(APIView):
    def get(self, request, search_id):
        search = get_object_or_404(Search, search_id=search_id)
        if search.is_finished:
            serializer = SearchResultSerializer(search.results, many=True)
            return Response({'results': serializer.data})

        return Response({'status': 'search is not finished yet'})

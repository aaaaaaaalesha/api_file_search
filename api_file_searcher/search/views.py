import uuid

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import Search
from .serializers import SearchSerializer
from .utils import search


@action(detail=False, methods=['post'])
class SearchView(APIView):
    def post(self, request: Request) -> Response:
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            found_paths = search(
                serializer.data.get('text'),
                serializer.data.get('filemask'),
                serializer.data.get('size'),
                serializer.data.get('creation time'),
            )
            uuid.uuid4()

            # return Response(
            #     {'search_id': str()},
            #     status=status.HTTP_201_CREATED,
            # )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@action(detail=False, methods=['get'])
class SearchResultView(APIView):
    def get(self, request: Request, search_id: str):
        search = get_object_or_404(Search, search_id=search_id)
        if search.is_finished:
            serializer = SearchResultSerializer(search.results, many=True)
            return Response({'results': serializer.data})

        return Response({'status': 'search is not finished yet'})

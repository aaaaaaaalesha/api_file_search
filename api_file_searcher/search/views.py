import json
import uuid

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist

from .models import Search
from .serializers import SearchSerializer
from .utils import search


@action(detail=False, methods=['post'])
class SearchView(APIView):
    def post(self, request: Request) -> Response:
        serializer = SearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        found_paths = search(
            serializer.data.get('text'),
            serializer.data.get('filemask'),
            serializer.data.get('size'),
            serializer.data.get('creation time'),
        )

        search_id = uuid.uuid1()
        Search.objects.create(
            search_id=search_id,
            paths=json.dumps(found_paths),
        )

        return Response(
            {'search_id': str(search_id)},
            status=status.HTTP_201_CREATED,
        )


@action(detail=False, methods=['get'])
class SearchResultView(APIView):
    def get(self, request: Request, search_id: str) -> Response:
        try:
            search_result = Search.objects.get(search_id=search_id)
        except ObjectDoesNotExist:
            return Response({'finished': False}, status=status.HTTP_200_OK)

        return Response(
            {
                'finished': True,
                'paths': json.loads(search_result.paths),
            },
            status=status.HTTP_200_OK,
        )

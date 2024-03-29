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
    @staticmethod
    def post(request: Request) -> Response:
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        found_paths = search(serializer.data)
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
    @staticmethod
    def get(request: Request, search_id: str) -> Response:
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

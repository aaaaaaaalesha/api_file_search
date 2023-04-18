from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Search, SearchResult
from .serializers import SearchSerializer, SearchResultSerializer


class SearchView(APIView):
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

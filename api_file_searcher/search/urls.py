from django.urls import path
from .views import SearchView, SearchResultView

app_name = 'search'

urlpatterns = [
    path(
        'search/',
        SearchView.as_view(),
        name='search',
    ),
    path(
        'searches/<str:search_id>/',
        SearchResultView.as_view(),
        name='search_results',
    )
]

from django.urls import path
from .views import SearchResultsListView

app_name = 'search'

urlpatterns = [
    path('search/', SearchResultsListView.as_view(), name='searchResult'), 
]
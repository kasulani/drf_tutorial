from django.urls import path
from .views import ListSongsView, ListSingleSongView


urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('songs/<int:pk>/', ListSingleSongView.as_view(), name="songs-detail")
]

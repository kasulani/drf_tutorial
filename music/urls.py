from django.urls import path
from .views import ListCreateSongsView, SongsDetailView


urlpatterns = [
    path('songs/', ListCreateSongsView.as_view(), name="songs-list-create"),
    path('songs/<int:pk>/', SongsDetailView.as_view(), name="songs-detail")
]

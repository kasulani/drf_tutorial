from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Songs
from .serializers import SongsSerializer


class ListSongsView(ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer


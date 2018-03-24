from rest_framework.response import Response
from rest_framework import generics
from .models import Songs
from .serializers import SongsSerializer


class ListSongsView(generics.ListAPIView):
    """
    GET songs/
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer


class ListSingleSongView(generics.RetrieveAPIView):
    """
    GET songs/:id/
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.get(pk=kwargs["pk"])
        return Response(SongsSerializer(queryset).data)

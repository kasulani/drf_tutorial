from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .models import Songs
from .serializers import SongsSerializer


class ListCreateSongsView(generics.ListCreateAPIView):
    """
    GET songs/
    POST songs/
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

    def post(self, request, *args, **kwargs):
        title = request.data.get("title", "")
        artist = request.data.get("artist", "")
        if not title and not artist:
            return Response(
                data={
                    "message": "Both title and artist are required to add a song"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        a_song = Songs.objects.create(title=title, artist=artist)
        return Response(
            data=SongsSerializer(a_song).data,
            status=status.HTTP_201_CREATED
        )


class SongsDetailView(generics.RetrieveAPIView):
    """
    GET songs/:id/
    PUT songs/:id/
    DELETE songs/:id/
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.get(pk=kwargs["pk"])
            return Response(SongsSerializer(queryset).data)
        except Songs.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

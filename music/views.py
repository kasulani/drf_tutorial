from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .decorators import validate_request_data
from .models import Songs
from .serializers import SongsSerializer


class ListCreateSongsView(generics.ListCreateAPIView):
    """
    GET songs/
    POST songs/
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

    @validate_request_data
    def post(self, request, *args, **kwargs):
        a_song = Songs.objects.create(
            title=request.data["title"],
            artist=request.data["artist"]
        )
        return Response(
            data=SongsSerializer(a_song).data,
            status=status.HTTP_201_CREATED
        )


class SongsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET songs/:id/
    PUT songs/:id/
    DELETE songs/:id/
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(SongsSerializer(a_song).data)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            serializer = SongsSerializer()
            updated_song = serializer.update(a_song, request.data)
            return Response(SongsSerializer(updated_song).data)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            a_song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Songs.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

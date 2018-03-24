import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer

# tests for models


class SongsModelTest(APITestCase):
    def setUp(self):
        self.a_song = Songs.objects.create(
            title="Ugandan anthem",
            artist="George William Kakoma"
        )

    def test_song(self):
        """"
        This test ensures that the song created in the setup
        exists
        """
        self.assertEqual(self.a_song.title, "Ugandan anthem")
        self.assertEqual(self.a_song.artist, "George William Kakoma")
        self.assertEqual(str(self.a_song), "Ugandan anthem - George William Kakoma")

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(title="", artist=""):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def setUp(self):
        # add test data
        self.create_song("like glue", "sean paul")
        self.create_song("simple song", "konshens")
        self.create_song("love is wicked", "brick and lace")
        self.create_song("jam rock", "damien marley")
        # post data
        self.data = {
            "title": "test song",
            "artist": "test artist"
        }


class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-list-create", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetASingleSongsTest(BaseViewTest):

    def test_get_a_song(self):
        """
        This test ensures that a single song of a given id is
        returned
        """
        # hit the API endpoint
        response = self.client.get(
            reverse(
                "songs-detail",
                kwargs={
                    "version": "v1",
                    "pk": 1
                }
            )
        )
        # fetch the data from db
        expected = Songs.objects.get(pk=1)
        serialized = SongsSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AddSongsTest(BaseViewTest):

    def test_create_a_song(self):
        """
        This test ensures that a single song can be added
        """
        # hit the API endpoint
        response = self.client.post(
            reverse(
                "songs-list-create",
                kwargs={
                    "version": "v1"
                }
            ),
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.data, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

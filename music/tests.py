import json
from django.urls import reverse
from django.contrib.auth.models import User

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
        """
        Create a song in the db
        :param title:
        :param artist:
        :return:
        """
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def make_a_request(self, kind="post", **kwargs):
        """
        Make a post request to create a song
        :param kind: HTTP VERB
        :return:
        """
        if kind == "post":
            return self.client.post(
                reverse(
                    "songs-list-create",
                    kwargs={
                        "version": kwargs["version"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        elif kind == "put":
            return self.client.put(
                reverse(
                    "songs-detail",
                    kwargs={
                        "version": kwargs["version"],
                        "pk": kwargs["id"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        else:
            return None

    def fetch_a_song(self, pk=0):
        return self.client.get(
            reverse(
                "songs-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def delete_a_song(self, pk=0):
        return self.client.delete(
            reverse(
                "songs-detail",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )

    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse("create-token"),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

    def register_a_user(self, username="", password="", email=""):
        return self.client.post(
            reverse(
                "auth-register",
                kwargs={
                    "version": "v1"
                }
            ),
            data=json.dumps(
                {
                    "username": username,
                    "password": password,
                    "email": email
                }
            ),
            content_type='application/json'
        )

    def setUp(self):
        # create a admin user
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        # add test data
        self.create_song("like glue", "sean paul")
        self.create_song("simple song", "konshens")
        self.create_song("love is wicked", "brick and lace")
        self.create_song("jam rock", "damien marley")
        self.valid_data = {
            "title": "test song",
            "artist": "test artist"
        }
        self.invalid_data = {
            "title": "",
            "artist": ""
        }
        self.valid_song_id = 1
        self.invalid_song_id = 100


class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        self.login_client('test_user', 'testing')
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
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.fetch_a_song(self.valid_song_id)
        # fetch the data from db
        expected = Songs.objects.get(pk=self.valid_song_id)
        serialized = SongsSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a song that does not exist
        response = self.fetch_a_song(self.invalid_song_id)
        self.assertEqual(
            response.data["message"],
            "Song with id: 100 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddSongsTest(BaseViewTest):

    def test_create_a_song(self):
        """
        This test ensures that a single song can be added
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.make_a_request(
            kind="post",
            version="v1",
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "Both title and artist are required to add a song"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSongsTest(BaseViewTest):

    def test_update_a_song(self):
        """
        This test ensures that a single song can be updated. In this
        test we update the second song in the db with valid data and
        the third song with invalid data and make assertions
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            kind="put",
            version="v1",
            id=2,
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with invalid data
        response = self.make_a_request(
            kind="put",
            version="v1",
            id=3,
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "Both title and artist are required to add a song"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSongsTest(BaseViewTest):

    def test_delete_a_song(self):
        """
        This test ensures that when a song of given id can be deleted
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.delete_a_song(1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # test with invalid data
        response = self.delete_a_song(100)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_a_user("test_user", "testing")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthRegisterUserTest(BaseViewTest):
    """
    Tests for auth/register/ endpoint
    """
    def test_register_a_user(self):
        response = self.register_a_user("new_user", "new_pass", "new_user@mail.com")
        # assert status code is 201 CREATED
        self.assertEqual(response.data["username"], "new_user")
        self.assertEqual(response.data["email"], "new_user@mail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.register_a_user()
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
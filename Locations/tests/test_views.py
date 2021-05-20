import json
from django.test import TestCase, Client
from Locations.models import Location
from django.urls import reverse
from users.models import CustomUser
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from Locations.models import Category


class TestView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="test1@gmail.com", password='1234')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.token.key)

    def test_creator_locations_GET(self):
        response = self.client.get(reverse('creator_locations'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.creator_location.count(), 0)
        self.assertEqual(response.content, b'[]')
        Category.objects.create(title='s', slug='s')
        data = {
            "name": "string",
            "is_private": True,
            "latitude": 0,
            "longitude": 0.2,
            "kinds": [
                1
            ],
            "city": "string",
            "state": "string",
            "description": "string",
            "address": "string"
        }
        self.client.generic(method="POST", path='/api/location/create/', data=json.dumps(data),
                                   content_type='application/json')
        response = self.client.get(reverse('creator_locations'), content_type='application/json')
        self.assertEqual(self.user.creator_location.count(), 1)
        self.assertNotEqual(response.content, b'[]')

        # print(response.content)





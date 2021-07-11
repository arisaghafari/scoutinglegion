import json
from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TestView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="test1@gmail.com", password='1234')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.token.key)

    def test_creator_hichhikes_GET(self):
        response = self.client.get(reverse('creator_hichhikes'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.creator_hichhike.count(), 0)
        self.assertEqual(response.content, b'[]')
        data = {
            "creator_type": "d",
            "creator_gender": 'm',
            "creator_age": 25,
            "source": "shiraz",
            "source_state": "fars",
            "destination": "tehran",
            "destination_state": "tehran",
            "fellow_traveler_num": 2,
            "description": "string",
            "cities": ["abadeh", "esfahan"]
        }
        re = self.client.generic(method="POST", path=reverse('create_hichhike'), data=json.dumps(data),
                                   content_type='application/json')
        response = self.client.get(reverse('creator_hichhikes'), content_type='application/json')
        # print(re)
        self.assertEqual(self.user.creator_hichhike.count(), 1)
        self.assertNotEqual(response.content, b'[]')

        # print(response.content)




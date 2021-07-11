import json
from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from hichhike.models import *


class TestView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="test1@gmail.com", password='1234')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.token.key)
        self.data = {
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

    def test_creator_hichhikes_GET(self):
        response = self.client.get(reverse('creator_hichhikes'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.creator_hichhike.count(), 0)
        self.assertEqual(response.content, b'[]')

        re = self.client.generic(method="POST", path=reverse('create_hichhike'), data=json.dumps(self.data),
                                   content_type='application/json')
        response = self.client.get(reverse('creator_hichhikes'), content_type='application/json')
        # print(re)
        self.assertEqual(self.user.creator_hichhike.count(), 1)
        self.assertNotEqual(response.content, b'[]')

    def test_create_hischike(self):
        re = self.client.generic(method="POST", path=reverse('create_hichhike'), data=json.dumps(self.data),
                                   content_type='application/json')
        self.assertEqual(Hichhike.objects.count(), 1)

    def test_passenger_joinrequest(self):
        user = CustomUser.objects.create_user(email="driver@gmail.com", username="driver", password='1234')
        Hichhike.objects.create(creator=user ,creator_type="d", source="", source_state="", destination_state="",
                            destination="", fellow_traveler_num=2, trip_time="2021-07-11T12:26:38.762340Z",creator_age
                                =23)
        data = {
            "id": Hichhike.objects.first().id
        }
        res = self.client.generic(method="POST", path=reverse('passenger_joinrequest'), data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(JoinRequest.objects.count(), 1)

    def test_driver_joinrequest(self):
        u = CustomUser.objects.create_user(email="passenegr123@gmail.com", username="passenegr123", password='1234')
        Hichhike.objects.create(creator=self.user, creator_type="d", source="", source_state="", destination_state="",
                            destination="", fellow_traveler_num=2, trip_time="2021-07-11T12:26:38.762340Z",creator_age
                                =23)
        JoinRequest.objects.create(hichhike_id=Hichhike.objects.first().id, passenger=u)
        accept_data = {
            "id": JoinRequest.objects.first().id,
            "accept": 1
        }
        self.client.generic(method="POST", path=reverse('driver_joinrequest'), data=json.dumps(accept_data),
                                 content_type='application/json')
        self.assertEqual(Participants.objects.count(), 1)






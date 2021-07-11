import json
from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from hichhike.models import *
import datetime


class TestView2(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(email="driver@gmail.com", username="driver", password='1234')
        self.token1 = Token.objects.create(user=self.user1)
        self.driver = APIClient()
        self.driver.credentials(HTTP_AUTHORIZATION='token ' + self.token1.key)
        self.user2 = CustomUser.objects.create_user(email="passenger@gmail.com", username="passenger", password='1234')
        self.token2 = Token.objects.create(user=self.user2)
        self.passenger = APIClient()
        self.passenger.credentials(HTTP_AUTHORIZATION='token ' + self.token2.key)
        hours_added = datetime.timedelta(hours=10)
        future_date_and_time = datetime.datetime.now() + hours_added
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
            "cities": ["abadeh", "esfahan"],
            "trip_time": "{}".format(future_date_and_time)
        }
        self.driver.generic(method="POST", path=reverse('create_hichhike'), data=json.dumps(self.data),
                            content_type='application/json')

    def test_senario1(self):
        data = {
            "creator_type": "p",
            "creator_gender": 'm',
            "creator_age": 25,
            "source": "shiraz",
            "source_state": "fars",
            "destination": "tehran",
            "destination_state": "tehran",
        }
        self.passenger.generic(method="POST", path=reverse('create_hichhike'), data=json.dumps(data),
                            content_type='application/json')
        response = self.passenger.get(reverse('suggest_hichhike'), content_type='application/json')
        self.assertNotEqual(response.content, b'[]')



    def test_senario2(self):
        data = {
            "creator_type": "p",
            "creator_gender": 'm',
            "creator_age": 25,
            "source": "shiraz",
            "source_state": "fars",
            "destination": "abadeh",
            "destination_state": "fars",
        }
        self.passenger.generic(method="POST", path=reverse('create_hichhike'), data=json.dumps(data),
                            content_type='application/json')
        response = self.passenger.get(reverse('suggest_hichhike'), content_type='application/json')
        self.assertNotEqual(response.content, b'[]')

    def test_senario3(self):
        data = {
            "creator_type": "p",
            "creator_gender": 'm',
            "creator_age": 25,
            "source": "esfahan",
            "source_state": "esfahan",
            "destination": "tehran",
            "destination_state": "tehran",
        }
        self.passenger.generic(method="POST", path=reverse('create_hichhike'), data=json.dumps(data),
                            content_type='application/json')
        response = self.passenger.get(reverse('suggest_hichhike'), content_type='application/json')
        self.assertNotEqual(response.content, b'[]')
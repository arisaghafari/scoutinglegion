import json
from django.test import TestCase, Client
from Locations.models import *
from django.urls import reverse
from users.models import CustomUser
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from Locations.serializers import *


class TestView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="test1@gmail.com", password='1234')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.token.key)
        self.category1 = Category.objects.create(title='s')
        self.category2 = Category.objects.create(title='a')
        self.loc_data = {
            "name": "string",
            "is_private": True,
            "latitude": 0,
            "longitude": 0.2,
            "kinds": [
                3, 4
            ],
            "city": "string",
            "state": "string",
            "description": "string",
            "address": "string"
        }


    def test_creator_locations_GET(self):
        response = self.client.get(reverse('creator_locations'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.creator_location.count(), 0)
        self.assertEqual(response.content, b'[]')

        self.client.generic(method="POST", path='/api/location/create/', data=json.dumps(self.loc_data),
                                   content_type='application/json')
        response = self.client.get(reverse('creator_locations'), content_type='application/json')
        self.assertEqual(self.user.creator_location.count(), 1)
        self.assertNotEqual(response.content, b'[]')

    def test_valued_rate_POST(self):
        loc1 = Location.objects.create(name='loc', latitude=0.0, longitude=0.0, city='tehran', state='tehran',
                                            image='', description=' ', address='tehrn', creator=self.user,
                                            is_private=True)
        loc1.kinds.add(self.category1)
        self.assertEqual(Location.objects.count(), 1)
        data = {
            "location": 2,
            "rating": 5,
        }
        response = self.client.generic(method="POST", path='/api/location/rate/', content_type='application/json', data=json.dumps(data))
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.get(location=2).rating, 5)
        self.assertEqual(response.status_code, 200)
        data = {
            "location": 2,
            "rating": 4,
        }
        response = self.client.generic(method="POST", path='/api/location/rate/', content_type='application/json',
                                       data=json.dumps(data))
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.get(location=2).rating, 4)
        self.assertEqual(response.status_code, 200)

    def test_get_categories_GET(self):
        response = self.client.get(reverse('get_category'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.all().count(), 2)
        categories = [
            {
                "id": 5,
                "title": "s"
            },
            {
                "id": 6,
                "title": "a"
            }
        ]
        self.assertEqual(CategorySerializer(Category.objects.all(), many=True).data, categories)






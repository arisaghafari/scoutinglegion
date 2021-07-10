import json
from django.test import TestCase
from django.urls import reverse
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
        self.loc = Location.objects.create(name='loc', latitude=1.0, longitude=0.0, city='tehran', state='tehran',
                                       image='', description=' ', address='tehrn', creator=self.user,
                                       is_private=True)
        self.loc.kinds.add(self.category1)

    def test_creator_locations_GET(self):
        response = self.client.get(reverse('creator_locations'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(self.user.creator_location.count(), 0)
        # self.assertEqual(response.content, b'[]')
        #
        # self.client.generic(method="POST", path='/api/location/create/', data=json.dumps(self.loc_data),
        #                            content_type='application/json')
        # response = self.client.get(reverse('creator_locations'), content_type='application/json')
        self.assertEqual(self.user.creator_location.count(), 1)
        self.assertNotEqual(response.content, b'[]')

    def test_valued_rate_POST(self):
        self.assertEqual(Location.objects.count(), 1)
        print(LocationSerializers(Location.objects.all(), many=True).data)
        data = {
            "location": 4,
            "rating": 5,
        }
        response = self.client.generic(method="POST", path='/api/location/rate/', content_type='application/json',
                                       data=json.dumps(data))
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.get(location=4).rating, 5)
        self.assertEqual(response.status_code, 200)
        data = {
            "location": 4,
            "rating": 4,
        }
        response = self.client.generic(method="POST", path='/api/location/rate/', content_type='application/json',
                                       data=json.dumps(data))
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.get(location=4).rating, 4)
        self.assertEqual(response.status_code, 200)

    def test_get_categories_GET(self):
        response = self.client.get(reverse('get_category'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # print(response.status_code)
        self.assertEqual(Category.objects.all().count(), 2)
        categories = [
            {
                "id": 7,
                "title": "s"
            },
            {
                "id": 8,
                "title": "a"
            }
        ]
        self.assertEqual(CategorySerializer(Category.objects.all(), many=True).data, categories)

    def test_comment_list_GET(self):
        self.assertEqual(Comment.objects.filter(location=1).count(), 0)
        data = {
            "location": 1,
            "body": "test body"
        }
        response = self.client.generic(method="POST", path='/api/location/comments/create', content_type='application/json',
                                       data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.filter(location=1).count(), 1)
        data2 = {
            "location": 1,
            "body": "test body2"
        }
        response = self.client.generic(method="POST", path='/api/location/comments/create', content_type='application/json',
                                       data=json.dumps(data2))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.filter(location=1).count(), 2)
        self.assertEqual(Comment.objects.filter(creator=self.user).count(), 2)





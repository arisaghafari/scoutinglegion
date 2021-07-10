import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from Locations.serializers import *

class TestView2(TestCase):
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
        self.loc = Location.objects.create(name='loc', latitude=2.0, longitude=0.0, city='tehran', state='tehran',
                                       image='', description=' ', address='tehrn', creator=self.user,
                                       is_private=True)
        self.loc.kinds.add(self.category1)

    def test_comment_list_GET(self):
        # print(LocationSerializers(Location.objects.all(), many=True).data)
        response = self.client.get(reverse('comments'), {'location': '5'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[]')
        data2 = {
            "location": 5,
            "body": "test body2"
        }
        response = self.client.generic(method="POST", path='/api/location/comments/create',
                                       content_type='application/json',
                                       data=json.dumps(data2))
        self.assertNotEqual(response.content, b'[]')
        self.assertEqual(Comment.objects.filter(location=5).count(), 1)

    def test_search_GET(self):
        response = self.client.get(reverse('search'), {'search': 'loc'})
        self.assertEqual(response.status_code, 200)

    # def test_location_detail_GET(self):
    #     pass
    #
    # def test_all_location(self):
    #     pass







from django.test import TestCase
from Locations.models import *
from users.models import CustomUser

class TestModels(TestCase):
    def setUp(self):
        # self.user = CustomUser.objects.create_user('arisaghafari68@gmail.com', '1234')
        self.category1 = Category.objects.create(title='sport')
        self.category2 = Category.objects.create(title='sport in gym')

    # def test_lat_lon_unique(self, kinds):
    #     kinds = kinds.set(self.category1)
    #     Location.objects.create(
    #         name='loc1', latitude=0.0, longitude=0.0, city='tehran', state='tehran', image='',
    #         description='test loc1', address='tehran mantagheye 6 ..', creator=self.user,
    #         is_private=True, kinds=kinds
    #     )

    def test_category_slug(self):
        self.assertEqual(self.category1.slug, 'sport')
        self.assertEqual(self.category2.slug, 'sport-in-gym')
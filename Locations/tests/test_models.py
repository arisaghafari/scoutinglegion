from django.test import TestCase
from Locations.models import *

class TestModels(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title='sport')
        self.category2 = Category.objects.create(title='sport in gym')

    def test_category_slug(self):
        self.assertEqual(self.category1.slug, 'sport')
        self.assertEqual(self.category2.slug, 'sport-in-gym')
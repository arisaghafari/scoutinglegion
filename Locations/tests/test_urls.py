from django.test import SimpleTestCase
from django.urls import resolve, reverse
import Locations
from Locations.views import CreateLocationViewSet, LocationManageView


class TestUrls(SimpleTestCase):
    def test_create_location(self):
        url = reverse('create_location')
        self.assertEqual(resolve(url).func.view_class, CreateLocationViewSet)

    def test_view_location(self):
        url = reverse('creator_locations')
        self.assertEqual(resolve(url).func.view_class, LocationManageView)

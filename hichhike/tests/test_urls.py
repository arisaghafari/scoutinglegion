from django.test import SimpleTestCase
from django.urls import resolve, reverse
import Locations
from hichhike.views import CreateHichhike, HichhikeManageView


class TestUrls(SimpleTestCase):
    def test_create_hichhike(self):
        url = reverse('create_hichhike')
        self.assertEqual(resolve(url).func.view_class, CreateHichhike)

    def test_view_hichhike(self):
        url = reverse('creator_hichhikes')
        self.assertEqual(resolve(url).func.view_class, HichhikeManageView)

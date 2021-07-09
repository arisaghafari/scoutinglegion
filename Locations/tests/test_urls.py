from django.test import SimpleTestCase
from django.urls import resolve, reverse
import Locations
from Locations.views import *


class TestUrls(SimpleTestCase):
    def test_create_location(self):
        url = reverse('create_location')
        self.assertEqual(resolve(url).func.view_class, CreateLocationViewSet)

    def test_view_location(self):
        url = reverse('creator_locations')
        self.assertEqual(resolve(url).func.view_class, LocationManageView)

    def test_valued_rate(self):
        url = reverse('rate')
        self.assertEqual(resolve(url).func, Valued_Rate)

    def test_get_category(self):
        url = reverse('get_category')
        self.assertEqual(resolve(url).func, get_all_categories)

    def test_comments_list(self):
        url = reverse('comments')
        self.assertEqual(resolve(url).func.view_class, CommentList)

    def test_comment_detail(self):
        url = reverse('comments_detail', args=[1,])
        self.assertEqual(resolve(url).func.view_class, CommentDetail)

    def test_location_detail(self):
        url = reverse('location_detail', args=[1,])
        self.assertEqual(resolve(url).func.view_class, GetLocationDetails)

    def test_all_locations(self):
        url = reverse('all_locations')
        self.assertEqual(resolve(url).func.view_class, AllLocations)

    def test_search(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func.view_class, SearchByName)
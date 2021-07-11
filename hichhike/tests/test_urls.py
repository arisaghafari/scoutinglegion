from django.test import SimpleTestCase
from django.urls import resolve, reverse
import Locations
from hichhike.views import *


class TestUrls(SimpleTestCase):
    def test_create_hichhike(self):
        url = reverse('create_hichhike')
        self.assertEqual(resolve(url).func.view_class, CreateHichhike)

    def test_view_hichhike(self):
        url = reverse('creator_hichhikes')
        self.assertEqual(resolve(url).func.view_class, HichhikeManageView)

    def test_hichhike_detail(self):
        url = reverse('hichhike_detail')
        self.assertEqual(resolve(url).func.view_class, GetHichhikeDetails)

    def test_passenger_joinrequest(self):
        url = reverse('passenger_joinrequest')
        self.assertEqual(resolve(url).func.view_class, PassengerJoinRequestsViewSet)

    def test_driver_joinrequest(self):
        url = reverse('driver_joinrequest')
        self.assertEqual(resolve(url).func.view_class, DriverJoinRequestsViewSet)

    def test_my_passengers(self):
        url = reverse('my_passengers')
        self.assertEqual(resolve(url).func.view_class, ParticipantsDriverViewSet)

    def test_my_travels(self):
        url = reverse('my_travels')
        self.assertEqual(resolve(url).func.view_class, ParticipantsPassengerViewSet)

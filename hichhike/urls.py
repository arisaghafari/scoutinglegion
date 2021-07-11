from django.urls import path, include
from .views import *

urlpatterns = [
    path('list/', HichhikeManageView.as_view(), name="creator_hichhikes"),
    path('create/', CreateHichhike.as_view(), name="create_hichhike"),
    path('detail/<int:id>', GetHichhikeDetails.as_view(), name="hichhike_detail"),
    path('suggest_hichhike/', SuggestHichhike.as_view(), name="suggest_hichhike"),
    path('passenger_joinrequest/', PassengerJoinRequestsViewSet.as_view(), name="passenger_joinrequest"),
    path('driver_joinrequest/', DriverJoinRequestsViewSet.as_view(), name="driver_joinrequest"),
    path('my_passengers/', ParticipantsDriverViewSet.as_view(), name="my_passengers"),
    path('my_travels/', ParticipantsPassengerViewSet.as_view(), name="my_travels")
]
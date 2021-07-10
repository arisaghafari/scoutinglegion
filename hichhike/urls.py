from django.urls import path, include
from .views import *

urlpatterns = [
    path('list/', HichhikeManageView.as_view(), name="creator_hichhikes"),
    path('create/', CreateHichhike.as_view(), name="create_hichhike"),
    path('detail/<int:id>', GetHichhikeDetails.as_view()),
    path('suggest_hichhike/', SuggestHichhike.as_view()),
    path('passenger_joinrequest/', PassengerJoinRequestsViewSet.as_view()),
    path('driver_joinrequest/', DriverJoinRequestsViewSet.as_view()),
    path('Participants/', ParticipantsViewSet.as_view())
]
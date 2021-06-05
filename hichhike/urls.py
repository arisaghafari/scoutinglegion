from django.urls import path, include
from .views import *

urlpatterns = [
    path('list/', HichhikeList.as_view(), name="creator_hichhikes"),
    path('create/', CreateHichhike.as_view(), name="create_hichhike"),
    path('detail/<int:id>', GetHichhikeDetails.as_view()),
    path('suggest_hichhike/', SuggestHichhike.as_view())
]
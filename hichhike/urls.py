from django.urls import path, include
from .views import *

urlpatterns = [
    path('list/', HichhikeList.as_view()),
    path('create/', CreateHichhike.as_view()),
    path('detail/<int:id>', GetHichhikeDetails.as_view()),
]
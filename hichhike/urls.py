from django.urls import path, include
from .views import *

urlpatterns = [
    path('list/', HichhikeList.as_view()),
]
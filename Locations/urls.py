
from django.urls import include, path
import Locations.views as views

urlpatterns = [
    path('create/', views.CreateLocationViewSet.as_view()),
    path('find-nearby/', views.NearbyLocationsViewSet.as_view()),
]

from django.urls import include, path
from .views import *

urlpatterns = [
    path('create/', CreateLocationViewSet.as_view()),
    path('creator_locations/', ViewLocationViewSet.as_view()),
    path('location_detail/<slug:id>', GetLocationDetails.as_view()),
    path('get_locations/', AllLocations.as_view()),
    path('search_by_name/<slug:name>', search_location_by_name),
]
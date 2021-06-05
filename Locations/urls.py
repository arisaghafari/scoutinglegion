
from django.urls import include, path, re_path
from .views import *

urlpatterns = [
    path('create/', CreateLocationViewSet.as_view(), name='create_location'),
    path('creator_locations/', LocationManageView.as_view(), name='creator_locations'),
    path('location_detail/<slug:id>', GetLocationDetails.as_view()),
    path('get_locations/', AllLocations.as_view()),
    # path('search_by_name/<slug:name>', SearchByName.as_view()),
    re_path(r'search_by_name/(?P<name>[-\w|\W]+)/', SearchByName.as_view()),
    # ?P<name>[\w|\W]+
]
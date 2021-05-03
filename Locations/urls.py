
from django.urls import include, path
import Locations.views as views

urlpatterns = [
    path('create/', views.CreateLocationViewSet.as_view()),
    path('find-nearby/', views.NearbyLocationsViewSet.as_view()),
    path('details/', views.GetLocationDetailsViewSet.as_view()),
    path('creator_locations/', views.ViewLocationViewSet.as_view()),
    path('get_locations/', views.get_all_locations),
    path('location_detail/<slug:id>', views.location_detail),
    path('search_by_name/<slug:name>', views.search_location_by_name),
    path('category/<slug:slug>', views.categoryLocation),
]
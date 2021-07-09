
from django.conf.urls import url
from django.urls import include, path, re_path
from .views import *

# app_name = 'Locations'
urlpatterns = [
    path('create/', CreateLocationViewSet.as_view(), name='create_location'),
    path('creator_locations/', LocationManageView.as_view(), name='creator_locations'),
    path('location_detail/<slug:id>', GetLocationDetails.as_view(), name='location_detail'),
    path('get_locations/', AllLocations.as_view(), name='all_locations'),
    path('search_by_name/', SearchByName.as_view(), name='search'),
    path('getCategory/', get_all_categories, name='get_category'),
    path('comments/', CommentList.as_view(), name='comments'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comments_detail'),
    path('rate/', Valued_Rate, name='rate'),
]
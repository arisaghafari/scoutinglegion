from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import LocationSerializers
from .models import Location
from shapely import geometry
# Create your views here.


class CreateLocationViewSet(generics.CreateAPIView):
    queryset = Location.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = LocationSerializers


class NearbyLocationsViewSet(generics.ListAPIView):
    serializer_class = LocationSerializers
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        lat = float(self.request.query_params['lat'])
        long = float(self.request.query_params['long'])
        center_loc = [lat, long]
        state = None
        if 'state' in self.request.query_params:
            state = self.request.query_params['state']
        locations = get_nearby_locations(center_loc, state)
        serializer = self.get_serializer(locations, many=True)
        loc_data = serializer.data
        return Response(loc_data)


def get_nearby_locations(center_loc, state):
    locations = []
    all_loc = []
    if state is not None:
        all_loc = Location.objects.filter(state=state)
    else:
        all_loc = Location.objects.all()
    for loc in all_loc:
        curr_loc = [loc.latitude, loc.longitude]
        if is_inside(center_loc, curr_loc) is True:
            locations.append(loc)
    return locations


def is_inside(center_loc, loc, radius=0.05):
    point_1 = geometry.Point(center_loc[0], center_loc[1])
    point_2 = geometry.Point(loc[0], loc[1])
    circle_buffer = point_1.buffer(radius)
    return circle_buffer.contains(point_2)

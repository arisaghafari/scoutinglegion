from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import Location, Category
from shapely import geometry
from urllib.request import urlopen
import json


class GetLocationDetailsViewSet(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LocationSerializers

    def get(self, request, *args, **kwargs):
        lat = float(self.request.query_params['lat'])
        long = float(self.request.query_params['long'])
        if Location.objects.filter(latitude=lat, longitude=long).exists():
            loc = Location.objects.get(latitude=lat, longitude=long)
            queryset = [loc, ]
            serializer = self.get_serializer(queryset, many=True)
            loc_data = serializer.data
            return Response(loc_data)
        else:
            return Response("couldn't find the location")


class CreateLocationViewSet(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializers

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)


class ViewLocationViewSet(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializers

    def get(self, request, *args, **kwargs):
        queryset = Location.objects.filter(creator=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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

@api_view()
def get_all_locations(request):
    radius = request.query_params['radius']
    lon = request.query_params['lon']
    lat = request.query_params['lat']
    if request.query_params['kinds'] == '':
        kinds = ''
    else:
        kinds = '&kinds=' + request.query_params['kinds']
    if request.query_params['rate'] == 'all':
        rate = ''
    else:
        rate = '&rate=' + request.query_params['rate']
    url = 'http://api.opentripmap.com/0.1/en/places/radius?radius=' + radius + '&lon=' + lon + '&lat=' + lat + kinds + rate + '&apikey=5ae2e3f221c38a28845f05b60743dfd0a4eaed6030e537cb1f99a226&format=json&src_attr=wikidata'
    with urlopen(url) as u:
        data = u.read()

    open_trip_map_data = json.loads(data.decode('utf-8'))

    center_loc = [float(lat), float(lon)]
    state = None
    if 'state' in request.query_params:
        state = request.query_params['state']
    locations = get_nearby_locations(center_loc, state)
    own_data = LocationSerializers(locations, many=True)
    return Response(own_data.data + open_trip_map_data, status.HTTP_200_OK)

def location_detail_opentripmap(id):
    url = 'http://api.opentripmap.com/0.1/en/places/xid/' + id + '?apikey=5ae2e3f221c38a28845f05b60743dfd0a4eaed6030e537cb1f99a226'
    with urlopen(url) as u:
        data = u.read()
    l = json.loads(data.decode('utf-8'))
    return l

@api_view()
def location_detail(request, id):
    try:
        if type(id) == int:
            location = Location.objects.get(id = id)
            l = LocationSerializers(location)
            return Response(l.data, status.HTTP_200_OK)
        else:
            l = location_detail_opentripmap(id)
            return Response(l, status.HTTP_200_OK)
    except Location.DoesNotExist:
        try:
            l = location_detail_opentripmap(id)
            return Response(l, status.HTTP_200_OK)
        except:
            return Response({"this location does not exist!!"}, status.HTTP_404_NOT_FOUND)

    return Response({"oops"})

def search_location_by_name_own_database(name):
    pass

@api_view()
def search_location_by_name(request, name):
    loc = search_location_by_name_own_database(name)
    if loc == None:
        url = 'http://api.opentripmap.com/0.1/en/places/geoname?name='+name+'&country=IR&apikey=5ae2e3f221c38a28845f05b60743dfd0a4eaed6030e537cb1f99a226'
        with urlopen(url) as u:
            data = u.read()

        pdata = json.loads(data.decode('utf-8'))
        return Response(pdata, status.HTTP_200_OK)
    else:
        return Response({"be zoodi !!!!"}, status.HTTP_200_OK)
"""""
@api_view()
def categoryLocation(request, slug):
    radius = request.query_params['radius']
    lon = request.query_params['lon']
    lat = request.query_params['lat']
    if request.query_params['kinds'] == '':
        kinds = ''
    else:
        kinds = '&kinds=' + request.query_params['kinds']
    if request.query_params['rate'] == 'all':
        rate = ''
    else:
        rate = '&rate=' + request.query_params['rate']
    url = 'http://api.opentripmap.com/0.1/en/places/radius?radius=' + radius + '&lon=' + lon + '&lat=' + lat + kinds + rate + '&apikey=5ae2e3f221c38a28845f05b60743dfd0a4eaed6030e537cb1f99a226&format=json&src_attr=wikidata'
    with urlopen(url) as u:
        data = u.read()

    open_trip_map_data = json.loads(data.decode('utf-8'))

    center_loc = [float(lat), float(lon)]
    state = None
    if 'state' in request.query_params:
        state = request.query_params['state']
    locations = get_nearby_locations(center_loc, state)
    own_data = LocationSerializers(locations, many=True)
    category = get_object_or_404(Category, slug=slug)
    locationList = []
    for d in own_data.data:
        p = category.location.get(id = d["id"])
        sr_p = LocationSerializers(p)
        locationList.append(sr_p.data)
    for d in open_trip_map_data:
        if category.title in d["kinds"]:
            locationList.append(d)
    return Response(locationList, status.HTTP_200_OK)
"""""
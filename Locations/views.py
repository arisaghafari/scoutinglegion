from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import Location, Category
from shapely import geometry
from urllib.request import urlopen
from lxml import html
import requests
from django.core.paginator import Paginator
import json
from rest_framework import generics
from geopy.geocoders import Nominatim


class CreateLocationViewSet(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializers

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)


class ViewLocationViewSet(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = GetLocationSerializers

    def get(self, request, *args, **kwargs):
        queryset = Location.objects.filter(creator=self.request.user).order_by('-id')
        serializer = self.get_serializer(queryset, many=True)
        if 'page' in list(self.request.query_params):
            paginator = Paginator(serializer.data, 10)
            if int(self.request.query_params['page']) <= paginator.num_pages:
                data = paginator.page(self.request.query_params['page']).object_list
                return Response(data={
                    'has_next': int(self.request.query_params['page']) < paginator.num_pages,
                    'data': data
                }
                )
        # serializer = self.get_serializer(queryset, many=True)
        print(get_city_state(lat=35.7243253,lon=51.4083653))
        return Response(serializer.data)


class AllLocations(generics.ListAPIView):
    serializer_class = GetLocationSerializers
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        if self.OwnData(request) == []:
            complete_data = self.OpenTripMapData(request)
        else:
            complete_data = self.OwnData(request) + self.OpenTripMapData(request)
        return Response(complete_data, status.HTTP_200_OK)
        #return Response(self.OwnData(request), status.HTTP_200_OK)

    def is_inside(self, center_loc, loc, radius=0.05):
        point_1 = geometry.Point(center_loc[0], center_loc[1])
        point_2 = geometry.Point(loc[0], loc[1])
        circle_buffer = point_1.buffer(radius)
        return circle_buffer.contains(point_2)

    def get_nearby_locations(self, center_loc, state):
        locations = []
        all_loc = []
        if state is not None:
            all_loc = Location.objects.filter(state=state, is_private=False)
        else:
            all_loc = Location.objects.filter(is_private=False)
        for loc in all_loc:
            curr_loc = [loc.latitude, loc.longitude]
            if self.is_inside(center_loc, curr_loc) is True:
                locations.append(loc)
        return locations

    def OpenTripMapData(self, request):
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
        return open_trip_map_data

    def OwnData(self, request):
        lon = request.query_params['lon']
        lat = request.query_params['lat']
        center_loc = [float(lat), float(lon)]
        state = None
        if 'state' in request.query_params:
            state = request.query_params['state']
        locations = self.get_nearby_locations(center_loc, state)
        own_data = self.get_serializer(locations, many=True)

        locationList = []
        if request.query_params['kinds'] == '':
            for o in own_data.data:
                o['xid'] = 'own-' + str(o['id'])
            return own_data.data
        else:
            categories = request.query_params['kinds'].split(',')
            for category in categories:
                try:
                    c = Category.objects.get(title=category)
                    for d in own_data.data:
                        if c.location.filter(id=d["id"]).exists():
                            p = c.location.get(id=d["id"])
                            sr_p = self.get_serializer(p)
                            sr_p.data['xid'] = 'own-' + str(sr_p.data['id'])
                            locationList.append(sr_p.data)
                except Category.DoesNotExist:
                    pass

            return locationList

class GetLocationDetails(generics.ListAPIView):
    serializer_class = GetLocationSerializers
    permission_classes = (permissions.AllowAny,)
    def get(self, request, **kwargs):
        id = kwargs['id']
        if 'own-' in kwargs['id']:
            id = kwargs['id'][4:]
            if Location.objects.filter(id=int(id)).exists():
                location = Location.objects.get(id=int(id))
                l = self.get_serializer(location)
                return Response(l.data, status.HTTP_200_OK)
        else:
            l = self.location_detail_opentripmap(request, kwargs['id'])
            return Response(l, status.HTTP_200_OK)

    def location_detail_opentripmap(self,request, id):

        url = 'http://api.opentripmap.com/0.1/en/places/xid/' + id + '?apikey=5ae2e3f221c38a28845f05b60743dfd0a4eaed6030e537cb1f99a226'
        with urlopen(url) as u:
            data = u.read()
        l = json.loads(data.decode('utf-8'))
        if "image" in l:
            image_url = l["image"]
            l["image"] = self.get_image(image_url)

        return l

    def get_image(self, url):
        html_page = requests.get(url)
        document = html.fromstring(html_page.text)
        try:
            img_url = document.xpath('//div[@class="fullImageLink"]//img/@src')
            return img_url
        except:
            return None

# @api_view()
# def get_all_categories(request):
#     category = Category.objects.all()
#     category_sr = CategorySerializer(category, many=True)
#     return Response(category_sr.data)

##########################################################
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


def get_city_state(lat, lon):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(str(lat) + "," + str(lon))
    address = location.raw['address']
    return location
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *
from rest_framework import generics
from itertools import chain


class HichhikeList(generics.ListAPIView):
    queryset = Hichhike.objects.all()
    serializer_class = HichhikeSerializer

    def get(self, request, *args, **kwargs):
        queryset = Hichhike.objects.filter(creator=self.request.user).order_by('-created')
        sr_trip = self.get_serializer(queryset, many=True)
        if 'page' in list(self.request.query_params):
            paginator = Paginator(sr_trip.data, 10)
            if int(self.request.query_params['page']) <= paginator.num_pages:
                data = paginator.page(self.request.query_params['page']).object_list
                return Response(data={
                    'has_next': int(self.request.query_params['page']) < paginator.num_pages,
                    'data': data
                }
                )
        return Response(sr_trip.data)


class CreateHichhike(generics.CreateAPIView):
    queryset = Hichhike.objects.all()
    serializer_class = HichhikeSerializer

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)


class GetHichhikeDetails(generics.ListAPIView):
    serializer_class = HichhikeSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, **kwargs):
        if Hichhike.objects.filter(id=kwargs['id']).exists():
            trip = Hichhike.objects.get(id=kwargs['id'])
            sr_trip = self.get_serializer(trip)
            return Response(sr_trip.data, status.HTTP_200_OK)
        else:
            return Response({"this trip does'nt exist!!!"}, status.HTTP_200_OK)


class SuggestHichhike(generics.ListAPIView):
    serializer_class = HichhikeSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        passenger_trip = Hichhike.objects.filter(creator=self.request.user, creator_type='p')
        queryset = self.suggester(passenger_trip)
        sr_trip = self.get_serializer(queryset, many=True)
        if 'page' in list(self.request.query_params):
            paginator = Paginator(sr_trip.data, 10)
            if int(self.request.query_params['page']) <= paginator.num_pages:
                data = paginator.page(self.request.query_params['page']).object_list
                return Response(data={
                    'has_next': int(self.request.query_params['page']) < paginator.num_pages,
                    'data': data
                }
                )
        return Response(sr_trip.data)

    def suggester(self, trips):
        sources = [t.source for t in trips]
        destinations = [t.destination for t in trips]
        gender = [t.creator_type for t in trips][0]

        return self.get_trips(sources, destinations)
        # return (query1 | query2).distinct()

    def get_trips(self, sources, destinations):
        first = Hichhike.objects.filter(creator_type='d', source__in=sources, destination__in=destinations)
        print(first)
        second = Hichhike.objects.filter(creator_type='d', source__in=sources, cities__overlap=destinations)
        print(second)
        third = Hichhike.objects.filter(creator_type='d', cities__overlap=sources, destination__in=destinations)
        print(third)
        return first | second | third




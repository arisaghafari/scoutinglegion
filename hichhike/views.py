import datetime

from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *
from rest_framework import generics
from Locations.views import BaseManageView
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


class HichhikeUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = HichhikeSerializer

    def get_object(self):
        if Hichhike.objects.filter(id=self.request.data['id']).count() != 0 \
                and Hichhike.objects.filter(id=self.request.data['id']).first().creator == self.request.user:

            return Hichhike.objects.get(pk=self.request.data['id'])
        else:
            return Response('can not find this location', status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, *args, **kwargs):
        if Hichhike.objects.filter(id=request.query_params['hichhike_id']).count() != 0:
            instance = Hichhike.objects.get(id=request.query_params['hichhike_id'])
            if instance.creator == self.request.user:
                self.perform_destroy(instance)
                return Response('hichhike deleted', status=status.HTTP_200_OK)
            else:
                return Response("you don't have permission")
        else:
            return Response('can not find this hichhike', status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if type(instance) != Response:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response('can not find this hichhike for you', status=status.HTTP_404_NOT_FOUND)


class HichhikeManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'DELETE': HichhikeUpdateDelete.as_view,
        'GET': HichhikeList.as_view,
        'PUT': HichhikeUpdateDelete.as_view
    }



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
        gender = [t.creator_gender for t in trips]

        return self.get_trips(sources, destinations, gender)
        # return (query1 | query2).distinct()

    def get_trips(self, sources, destinations, gender):
        hours_added = datetime.timedelta(hours=1)
        future_date_and_time = datetime.datetime.now() + hours_added
        first = Hichhike.objects.filter(creator_type='d').\
            filter(source__in=sources, destination__in=destinations,
                   trip_time__gte=future_date_and_time).order_by('-created')
        print(first)
        second = Hichhike.objects.filter(creator_type='d').\
            filter(source__in=sources, cities__overlap=destinations,
                   trip_time__gte=future_date_and_time).order_by('-created')
        print(second)
        third = Hichhike.objects.filter(creator_type='d').\
            filter(cities__overlap=sources, destination__in=destinations,
                   trip_time__gte=future_date_and_time).order_by('-created')
        print(third)
        return first | second | third


class DriverJoinRequestsViewSet(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = JoinRequestsSerializer

    def get_queryset(self):
        return JoinRequest.objects.filter(hichhike__creator=self.request.user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        join_request = JoinRequest.objects.get(pk=self.request.data['id'])
        if int(self.request.data['accept']) == 1:
            passenger = join_request.passenger
            Participants.objects.create(hichhike=join_request.hichhike, passenger=join_request.passenger)
            join_request.hichhike.fellow_traveler_num -= 1
            join_request.hichhike.save()
        join_request.delete()
        data = self.get_serializer(JoinRequest.objects.filter(hichhike__creator=self.request.user), many=True).data
        return Response(data)


class PassengerJoinRequestsViewSet(generics.ListAPIView, generics.CreateAPIView):
    serializer_class = JoinRequestsSerializer

    def get_queryset(self):
        return JoinRequest.objects.filter(passenger=self.request.user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        hch = Hichhike.objects.get(id=self.request.data['id'])
        if hch.fellow_traveler_num > 0:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(passenger=self.request.user, hichhike_id=self.request.data['id'])
            return Response(serializer.data)
        else:
            return Response('Capacity is complete', status=status.HTTP_404_NOT_FOUND)


class ParticipantsDriverViewSet(generics.ListAPIView):
    serializer_class = ParticipantsDriverSerializer

    def get_queryset(self):
        return Participants.objects.filter(hichhike__creator=self.request.user).order_by('-created_at')


class ParticipantsPassengerViewSet(generics.ListAPIView):
    serializer_class = ParticipantsPassengerSerializer

    def get_queryset(self):
        return Participants.objects.filter(passenger=self.request.user).order_by('-created_at')





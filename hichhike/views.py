from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *
from rest_framework import generics

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


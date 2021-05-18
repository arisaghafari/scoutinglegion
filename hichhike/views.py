from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

class HichhikeList(APIView):
    def get(self, request):
        trip = Hichhike.objects.all()
        sr_trip = HichhikeSerializer(trip, many=True)
        return Response(sr_trip.data)

    def post(self, request):
        sr_trip = HichhikeSerializer(data=request.data)
        if sr_trip.is_valid():
            sr_trip.save(creator=self.request.user)
            return Response(sr_trip.data, status=status.HTTP_201_CREATED)
        return Response(sr_trip.errors, status=status.HTTP_400_BAD_REQUEST)
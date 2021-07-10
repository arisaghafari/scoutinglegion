from rest_framework import serializers
from .models import *

class HichhikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    creator_id = serializers.IntegerField(source='creator.pk', required=False)
    creator_firstname = serializers.CharField(source='creator.firstname', required=False)
    creator_lastname = serializers.CharField(source='creator.lastname', required=False)
    creator_profile_picture = serializers.ImageField(source='creator.profile_picture', required=False)
    creator_username = serializers.CharField(source='creator.username', required=False)

    class Meta:
        model = Hichhike
        fields = ['id', 'creator_id', 'creator_firstname', 'creator_lastname', 'creator_profile_picture',
                  'creator_username', 'creator_type', 'creator_gender', 'creator_age', 'source', 'destination',
                  'fellow_traveler_num', 'description', 'cities', 'created', 'trip_time', 'source_state',
                  'destination_state']
        optional_fields = ['cities', 'trip_time', 'cities', 'fellow_traveler_num', ]


class JoinRequestsSerializer(serializers.ModelSerializer):
    hichhike_id = serializers.IntegerField(source='hichhike.pk', required=False)
    hichhike_capacity = serializers.IntegerField(source='hichhike.fellow_traveler_num', required=False)
    hichhike_source = serializers.CharField(source='hichhike.source', required=False)
    hichhike_destination = serializers.CharField(source='hichhike.destination', required=False)
    hichhike_description = serializers.CharField(source='hichhike.description', required=False)
    hichhike_trip_time = serializers.DateTimeField(source='hichhike.trip_time', required=False)
    passenger_id = serializers.IntegerField(source='passenger.pk', required=False)
    passenger_firstname = serializers.CharField(source='passenger.firstname', required=False)
    passenger_lastname = serializers.CharField(source='passenger.lastname', required=False)
    passenger_username = serializers.CharField(source='passenger.username', required=False)
    passenger_profile_picture = serializers.ImageField(source='passenger.profile_picture', required=False)

    class Meta:
        model = JoinRequest
        fields = ('id', 'hichhike_id', 'hichhike_capacity', 'passenger_id', 'passenger_firstname', 'passenger_lastname',
                  'hichhike_source', 'hichhike_destination',
                  'hichhike_description', 'hichhike_trip_time'
                  , 'passenger_username', 'passenger_profile_picture')


class ParticipantsDriverSerializer(serializers.ModelSerializer):
    hichhike_id = serializers.IntegerField(source='hichhike.pk', required=False)
    hichhike_source = serializers.CharField(source='hichhike.source', required=False)
    hichhike_destination = serializers.CharField(source='hichhike.destination', required=False)
    hichhike_description = serializers.CharField(source='hichhike.description', required=False)
    hichhike_trip_time = serializers.DateTimeField(source='hichhike.trip_time', required=False)
    passenger_id = serializers.IntegerField(source='passenger.pk', required=False)
    passenger_firstname = serializers.CharField(source='passenger.firstname', required=False)
    passenger_lastname = serializers.CharField(source='passenger.lastname', required=False)
    passenger_username = serializers.CharField(source='passenger.username', required=False)
    passenger_profile_picture = serializers.ImageField(source='passenger.profile_picture', required=False)
    class Meta:
        model = JoinRequest
        fields = ('id', 'hichhike_id', 'passenger_id', 'passenger_firstname', 'passenger_lastname',
                  'hichhike_source', 'hichhike_destination',
                  'hichhike_description', 'hichhike_trip_time'
                  , 'passenger_username', 'passenger_profile_picture')


class ParticipantsPassengerSerializer(serializers.ModelSerializer):
    hichhike_id = serializers.IntegerField(source='hichhike.pk', required=False)
    hichhike_source = serializers.CharField(source='hichhike.source', required=False)
    hichhike_destination = serializers.CharField(source='hichhike.destination', required=False)
    hichhike_description = serializers.CharField(source='hichhike.description', required=False)
    hichhike_trip_time = serializers.DateTimeField(source='hichhike.trip_time', required=False)
    hichhike_capacity = serializers.IntegerField(source='hichhike.fellow_traveler_num', required=False)
    hichhike_creator = serializers.IntegerField(source='hichhike.creator.pk', required=False)
    hichhike_creator_username = serializers.CharField(source='hichhike.creator.username', required=False)
    hichhike_creator_firstname = serializers.CharField(source='hichhike.creator.firstname', required=False)
    hichhike_creator_lastname = serializers.CharField(source='hichhike.creator.lastname', required=False)
    hichhike_creator_profile_picture = serializers.ImageField\
        (source='hichhike.creator.profile_picture', required=False)

    class Meta:
        model = JoinRequest
        fields = ('id', 'hichhike_id', 'hichhike_creator','hichhike_source', 'hichhike_destination',
                  'hichhike_description', 'hichhike_trip_time',
                  'hichhike_capacity', 'hichhike_creator_username', 'hichhike_creator_firstname'
                  , 'hichhike_creator_lastname', 'hichhike_creator_profile_picture')

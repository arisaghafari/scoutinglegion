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
                  'fellow_traveler_num', 'description', 'cities_list', 'jcreated', 'jtrip_time']

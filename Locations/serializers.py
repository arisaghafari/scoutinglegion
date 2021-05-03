from rest_framework import serializers
from users.serializers import UserDetailSerializers
from rest_framework.validators import UniqueValidator

from .models import *


class LocationSerializers(serializers.ModelSerializer):
    creator_id = serializers.IntegerField(source='creator.pk', required=False)
    creator_firstname = serializers.CharField(source='creator.firstname', required=False)
    creator_lastname = serializers.CharField(source='creator.lastname', required=False)
    creator_profile_picture = serializers.ImageField(source='creator.profile_picture', required=False)
    creator_username = serializers.CharField(source='creator.username', required=False)

    class Meta:
        model = Location
        fields = ['id', 'loc_name', 'creator_id', 'creator_firstname', 'creator_lastname', 'creator_username',
                  'creator_profile_picture',
                  'latitude', 'longitude', 'category', 'city', 'state', 'loc_picture', 'description', 'address']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

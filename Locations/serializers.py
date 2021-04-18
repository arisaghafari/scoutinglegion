from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Location


class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'loc_name', 'latitude', 'longitude', 'category', 'type', 'city', 'state', 'loc_picture',
                  'description']

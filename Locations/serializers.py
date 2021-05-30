from django.db.models import fields
from rest_framework import serializers
from users.serializers import UserDetailSerializers
from rest_framework.validators import UniqueValidator

from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        #fields = '__all__'
        fields = ['id', 'title']


class GetLocationSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    creator_id = serializers.IntegerField(source='creator.pk', required=False)
    creator_firstname = serializers.CharField(source='creator.firstname', required=False)
    creator_lastname = serializers.CharField(source='creator.lastname', required=False)
    creator_profile_picture = serializers.ImageField(source='creator.profile_picture', required=False)
    creator_username = serializers.CharField(source='creator.username', required=False)
    kinds = serializers.StringRelatedField(many=True)

    class Meta:
        model = Location

        fields = ['id', 'name', 'creator_id', 'creator_firstname', 'creator_lastname', 'creator_username',
                  'creator_profile_picture', 'is_private',
                  'latitude', 'longitude', 'kinds', 'city', 'state', 'image', 'description', 'address']

    def to_representation(self, instance):
        data = super(GetLocationSerializers, self).to_representation(instance)
        request = self.context.get('request', None)
        if request.method == 'GET':
            data['xid'] = 'own_'+ str(data['id'])
            data['image'] = [data['image']]
            data['point'] = {'lon': data['longitude'], 'lat': data['latitude']}
            data['kinds'] = ",".join(data['kinds'])
        return data



class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'creator', 'is_private',
                  'latitude', 'longitude', 'kinds', 'city', 'state', 'image', 'description', 'address']

class CommentSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    creator_profile_picture = serializers.ImageField(source='creator.profile_picture', required=False)
    creator_username = serializers.ReadOnlyField(source='creator.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'creator_profile_picture', 'creator_username', 'location', 'body', 'created_on', 'active']



from django.db.models import fields, Count, Q, Avg
from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        #fields = '__all__'
        fields = ['id', 'title']


class GetLocationSerializers(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField('get_ratings_detail')
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
                  'latitude', 'longitude', 'kinds', 'city', 'state', 'image', 'description', 'address', 'ratings']

    def to_representation(self, instance):
        data = super(GetLocationSerializers, self).to_representation(instance)
        request = self.context.get('request', None)
        if request.method == 'GET':
            data['xid'] = 'own_'+ str(data['id'])
            data['image'] = [data['image']]
            data['point'] = {'lon': data['longitude'], 'lat': data['latitude']}
            data['kinds'] = ",".join(data['kinds'])
        return data

    def get_ratings_detail(self, obj):
        ratings = Rating.objects.filter(location=obj).aggregate(Avg('rating'))
        return ratings

class RateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['location', 'rating']

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


import base64
import uuid

import six
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CustomUser


class UserDetailSerializers(serializers.ModelSerializer):
    firstname = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    lastname = serializers.CharField(required=False, allow_null=True,  allow_blank=True)
    email = serializers.EmailField(required=False, validators=[
        UniqueValidator(queryset=CustomUser.objects.all())
    ])
    username = serializers.CharField(required=False, validators=[
        UniqueValidator(queryset=CustomUser.objects.all())
    ])
    city = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'city', 'firstname', 'lastname', 'profile_picture']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'city', 'firstname', 'lastname', 'profile_picture']


class UserRegistrationSerializer(RegisterSerializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    city = serializers.CharField(max_length=100, required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    firstname = serializers.CharField(max_length=100, required=False)
    lastname = serializers.CharField(max_length=100, required=False)
    profile_picture = serializers.ImageField(required=False)

    def validate_password1(self, password):
        return password

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("the two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        super(UserRegistrationSerializer, self).get_cleaned_data()
        return {
            'password': self.validated_data.get('password1', ''),
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'city': self.validated_data.get('city', ''),
            'firstname': self.validated_data.get('firstname', ''),
            'lastname': self.validated_data.get('lastname', ''),
            'profile_picture': self.validated_data.get('profile_picture', ''),

        }
    def save(self, request):
        cleaned_data = self.get_cleaned_data()
        user = CustomUser.objects.create_user(**cleaned_data)
        return user


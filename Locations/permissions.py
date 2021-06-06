from rest_framework import permissions
from .models import Location
from users.models import CustomUser


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsLocationCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        custom_user = CustomUser.objects.get(pk=request.user.id)
        return obj.creator == custom_user





from rest_framework import generics, permissions
from .serializers import UserDetailSerializers
from .models import CustomUser
from rest_framework.response import Response
from django.http import QueryDict


class UserDetailViewSet(generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = UserDetailSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        custom_user = CustomUser.objects.get(pk=self.request.user.id)
        queryset = [custom_user, ]
        serializer = self.get_serializer(queryset, many=True)
        user_data = serializer.data[0]
        return Response(user_data)

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.id)



from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from .settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('users.urls')),
    path('api/location/', include('Locations.urls')),
    path('api/hichhike/', include('hichhike.urls')),
    path('schema/', get_schema_view(title="Scouting Legion")),
    path('swagger-docs/', get_swagger_view(title="Scouting Legion")),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

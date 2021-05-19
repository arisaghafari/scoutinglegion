from allauth.account.views import confirm_email
from django.conf.urls import url
from django.urls import include, path
import users.views as views

urlpatterns = [
    url(r'^', include('rest_auth.urls')),
    url(r'^register/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    path('profile/', views.UserDetailViewSet.as_view()),
]

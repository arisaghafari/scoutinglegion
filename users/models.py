from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=100, null=False, unique=True)
    firstname = models.CharField(_('first name'), max_length=100, null=True, blank=True)
    lastname = models.CharField(_('last name'), max_length=100, null=True, blank=True)
    city = models.CharField(_('city of residence'), max_length=100, null=False)
    profile_picture = models.ImageField(_('profile picture'), null=True, blank=True, upload_to='Uploaded/userprofile')
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

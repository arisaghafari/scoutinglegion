from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser


# Create your models here.
class Location(models.Model):
    loc_name = models.CharField(_('name'), max_length=200, null=False)
    latitude = models.FloatField(_('location latitude'), null=False, blank=False)
    longitude = models.FloatField(_('location longitude'), null=False, blank=False)
    category = models.CharField(_('category'), max_length=100, null=True, blank=True)
    type = models.CharField(_('type'), max_length=100, null=True, blank=True)
    city = models.CharField(_('city of location'), max_length=100, null=False)
    state = models.CharField(_('state of location'), max_length=100, null=False)
    loc_picture = models.ImageField(_('location picture'), null=True, blank=True, upload_to='Uploaded/location_picture')
    description = models.TextField(_('location description'), null=True, blank=True)
    creator = models.ForeignKey(CustomUser, related_name="creator_location", on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = ('latitude', 'longitude',)

    def __str__(self):
        return self.loc_name
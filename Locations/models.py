from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField(_('name'), max_length=200, null=False, blank=True)
    latitude = models.FloatField(_('location latitude'), null=False, blank=False)
    longitude = models.FloatField(_('location longitude'), null=False, blank=False)
    city = models.CharField(_('city of location'), max_length=100, null=False)
    state = models.CharField(_('state of location'), max_length=100, null=False)
    image = models.ImageField(_('location picture'), null=True, blank=True, upload_to='Uploaded/location_picture')
    description = models.TextField(_('location description'), null=True, blank=True)
    address = models.CharField(_('location address'), max_length=200, null=False)
    creator = models.ForeignKey(CustomUser, related_name="creator_location", on_delete=models.CASCADE, default=None)
    is_private = models.BooleanField(_('is private location'), default=False)
    kinds = models.ManyToManyField(Category, related_name="location")

    class Meta:
        unique_together = ('latitude', 'longitude',)

    def __str__(self):
        return self.name

class Comment(models.Model):
    creator = models.ForeignKey(CustomUser, related_name="creator_comment", on_delete=models.CASCADE, default=None)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.creator.username)

class Rating(models.Model):
    # class Meta:
    #     unique_together = ['user_rate', 'location']

    user_rate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='Urate')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='Lrate')
    rating = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return 'Rating(Item ='+ str(self.location)+', Stars ='+ str(self.rating)+')'
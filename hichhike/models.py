from django.db import models
from users.models import CustomUser
from django.contrib.postgres.fields import ArrayField
from extensions.utils import jalali_converter

class Hichhike(models.Model):
    TYPE_CHOICES = (
        ('d', 'راننده'),
        ('p', 'مسافر'),
    )
    GENDER_CHOICES = (
        ('m', 'اقا'),
        ('f', 'خانوم'),
    )
    creator = models.ForeignKey(CustomUser, related_name="creator_hichhike", on_delete=models.CASCADE, default=None)
    creator_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    creator_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    creator_age = models.IntegerField()
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    fellow_traveler_num = models.IntegerField()
    description = models.TextField(blank=True)
    cities = ArrayField(models.CharField(max_length=200), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    trip_time = models.DateTimeField(blank=True)

    def __str__(self):
        return str(self.creator) + "_" + self.destination

    def jcreated(self):
        return jalali_converter(self.created)

    def jtrip_time(self):
        return jalali_converter(self.trip_time)

    def cities_list(self):
        list = ""
        for c in self.cities:
            if list == "":
                list = str(c)
            else:
                list += ' ,' + str(c)
        return list
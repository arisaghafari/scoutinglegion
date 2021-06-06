from django.contrib import admin
from .models import *

# class HichhikeAdmin(admin.ModelAdmin):
#     list_display = ("creator", "source", "destination", "jcreated", "jtrip_time")
#     search_fields = ("source", "destination")
#
#
# admin.site.register(Hichhike, HichhikeAdmin)
admin.site.register(Hichhike)
admin.site.register(Participants)
admin.site.register(JoinRequest)
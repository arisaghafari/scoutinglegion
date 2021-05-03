from django.contrib import admin

# Register your models here.
from .models import *

class LocationAdmin(admin.ModelAdmin):
    list_display = ("loc_name", "kinds_to_str", "creator", "latitude", "longitude")
    search_fields = ("title", "description")

    def kinds_to_str(self, obj):
        return " ,".join([Category.title for Category in obj.kinds.all()])

admin.site.register(Location, LocationAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug" : ("title",)}

admin.site.register(Category, CategoryAdmin)

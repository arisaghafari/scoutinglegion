from django.contrib import admin
from .models import *

class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "kinds_to_str", "creator", "latitude", "longitude")
    search_fields = ("title", "description")

    def kinds_to_str(self, obj):
        return " ,".join([Category.title for Category in obj.kinds.all()])

admin.site.register(Location, LocationAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug" : ("title",)}

admin.site.register(Category, CategoryAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('creator', 'body', 'location', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('body',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

class RateAdmin(admin.ModelAdmin):
    list_display = ("user_rate", "location")
    search_fields = ("user_rate", "location")

admin.site.register(Rating, RateAdmin)
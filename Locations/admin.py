from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Location)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug" : ("title",)}

admin.site.register(Category, CategoryAdmin)

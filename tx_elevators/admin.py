from django.contrib import admin

from . import models


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name_1', 'city', 'latitude', 'longitude')
    search_fields = ('name_1', 'name_2')
admin.site.register(models.Building, BuildingAdmin)

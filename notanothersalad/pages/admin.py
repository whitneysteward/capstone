from django.contrib import admin
from .models import Restaurant, Image


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu')


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Image)
# Register your models here.

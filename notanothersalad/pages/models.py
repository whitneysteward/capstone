from django.db import models
from django.contrib.gis.db import models as gismodels


class Image(models.Model):
    image = models.ImageField()
    description = models.TextField()
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    menu = models.CharField(max_length=1000)
    images = models.ManyToManyField(Image)
    description = models.TextField()

    def __str__(self):
        return self.name


class Location(models.Model):
    lat = models.CharField(max_length=255)
    lon = models.CharField(max_length=255)
    pnt = gismodels.PointField(srid=4326)
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant.name

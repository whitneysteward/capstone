from django.db import models


class Image(models.Model):
    image = models.ImageField()
    description = models.TextField()
# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length= 250)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=250, blank=True)
    images = models.ManyToManyField(Image)

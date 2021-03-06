from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Restaurant, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'description', 'name')


class RestaurantSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ('pk', 'name', 'address', 'phone', 'menu','images','description')
        depth = 1


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

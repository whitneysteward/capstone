from django.shortcuts import render, HttpResponse
from .models import Restaurant
from django.core import serializers
from .serializers import RestaurantSerializer, UserSerializer, GroupSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
# Create your views here.
def home (request):
    return render (request,'home.html')


def results(request):
    res = Restaurant.objects.exclude(images__isnull=True)
    print(res)
    data = serializers.serialize("json", Restaurant.objects.exclude(images__isnull=True))
    return HttpResponse(data, content_type='application/json')

def restaurant(request,pk):
    rest = Restaurant.objects.get(pk=pk)
    img = rest.images.all()[0]
    return render (request, 'rest_modal.html', {"rest": rest, 'img': img})

class RestaurantResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Restaurant.objects.exclude(images__isnull=True)
    serializer_class = RestaurantSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

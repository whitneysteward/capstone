from django.shortcuts import render, HttpResponse
from .models import Restaurant, Image
from django.core import serializers
from .serializers import RestaurantSerializer, UserSerializer, GroupSerializer
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.gis.measure import Distance, D
from .models import Location, Restaurant
from django.contrib.gis.geos import Point
import requests
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import urllib
import requests



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def home (request):
    return render (request,'search.html')


def results(request):
    data = serializers.serialize("json", Restaurant.objects.exclude(images__isnull=True))
    return HttpResponse(data, content_type='application/json')

def restaurant(request,pk):
    rest = Restaurant.objects.get(pk=pk)
    img = rest.images.all()[0]
    return render (request, 'rest_modal.html', {"rest": rest, 'img': img})

# Location hack to make sure this works correctly
class LocationHk:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


def locationresults(request):
    if request.method == "GET":
        address = request.GET["address"]
        address_decoded = urllib.parse.unquote(urllib.parse.unquote(address))
        radius = request.GET["radius"]
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+ address +'&key=AIzaSyDWyg85ZiDtKq_kWXp5LzjVoTpZb6ljhvw')
        adr = r.json()
        lat  = adr['results'][0]['geometry']['location']['lat']
        lng = adr['results'][0]['geometry']['location']['lng']
        location = LocationHk(lat, lng)
        myloc = Point(location.latitude, location.longitude)
        qs = Location.objects.filter(pnt__distance_lte=(myloc, D(mi=radius)))
        restpks = []
        for pk in qs:
            restpks.append(pk.pk)
        qs_rest = Restaurant.objects.filter(pk__in=restpks).exclude(images__isnull=True)
        serializer = RestaurantSerializer(qs_rest, many=True)

        return JSONResponse(serializer.data)
    return HttpResponse("Nothing to see!")

@csrf_exempt
def addrest(request):
    if request.method == "POST":
        name = request.POST["Restaurant"]
        address = request.POST["Address"]
        phone = request.POST["Phone"]
        picture = request.FILES["picture"]
        description = request.POST["description"]
        exists = Restaurant.objects.filter(name=name)
        if len(exists)> 0:
            return HttpResponse("Restaurant already exists!")
        else:


            obj = Restaurant()
            img = Image()
            obj.name = name
            obj.address = address
            obj.phone = phone
            obj.menu = ""

            obj.description = description
            obj.save()
            img.image = picture
            img.name = 'newImg'
            img.description = ''
            img.save()
            obj.images.add(img)
            obj.save()

            geolocator = Nominatim()
            location = geolocator.geocode(str(address), timeout=60)

            loc = Location()
            loc.lat = location.latitude
            loc.lon = location.longitude
            point = GEOSGeometry('POINT('+ str(location.latitude) + ' ' + str(location.longitude)+')', srid=4326)
            loc.pnt = point
            loc.restaurant = obj
            loc.save()
            return HttpResponse("Success!")
    return HttpResponse("Nothing to see!")


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

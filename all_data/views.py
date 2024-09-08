from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from app_user.models import Restaurant
from . serializers import RestaurantSerializer


@api_view(['GET'])
def restaurant_data(request):
      restaurants = Restaurant.objects.all()
      serializer = RestaurantSerializer(restaurants, many=True)
      return Response(serializer.data, status=HTTP_200_OK)

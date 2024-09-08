from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from app_user.models import Restaurant
from . serializers import RestaurantSerializer


# @api_view(['GET'])
# def restaurant_data(request):
#       restaurants = Restaurant.objects.all()
      
#       # setup pagination
#       paginator = PageNumberPagination()
#       paginator.page_size = 20
#       result_page = paginator.paginate_queryset(restaurants, request)
      
#       # serialize the paginate data
#       serializer = RestaurantSerializer(result_page, many=True)
      
#       # return the paginated data
#       return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def search_all(request):
      query = request.query_params.get('query', None)
      
      if query:
            restaurants = Restaurant.objects.filter(
                  Q(name__icontains = query) |        # Search restaurant
                  Q(location__icontains = query) |          # search location
                  Q(categories__name__icontains = query) |        # search categories
                  Q(categories__menus__name__icontains = query) |       # search menus
                  Q(categories__menus__items__name__icontains = query)        # search items
            ).distinct()
      else:
            restaurants = Restaurant.objects.all()
            
            
      paginator = PageNumberPagination()
      paginator.page_size = 15
      result_page = paginator.paginate_queryset(restaurants, request)
      
      serializer = RestaurantSerializer(result_page, many = True)
      return paginator.get_paginated_response(serializer.data)
            
            
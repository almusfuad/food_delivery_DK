from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from app_user.models import Restaurant, Employee
from app_user.permissions import IsOwner
from . serializers import RestaurantSerializer, OwnerRestaurantSerializer, EmployeeSerializer



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
            
      # Setup pagination      
      paginator = PageNumberPagination()
      paginator.page_size = 15
      result_page = paginator.paginate_queryset(restaurants, request)
      
      # Setup data serializer
      serializer = RestaurantSerializer(result_page, many = True)
      return paginator.get_paginated_response(serializer.data)
            

@api_view(['GET'])
@permission_classes([IsOwner])
def owner_restaurants(request):
      user = request.user
      
      # Fetch all the restaurants owned by logged in user
      restaurants = Restaurant.objects.filter(owner = user.profile)
      
      if not restaurants:
            return Response({'error': f'No restaurants found for the owner {user.username}'}, status=HTTP_404_NOT_FOUND)
      
      # Serialize the data
      serializer = OwnerRestaurantSerializer(restaurants, many = True)
      
      return Response({'restaurants': serializer.data}, status=HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_employees(request):
      user = request.user
      
      # checking for manager
      try:
            employee = Employee.objects.get(user = user)
      except Employee.DoesNotExist:
            return Response({'error': 'No employee record found for this user.'}, status=HTTP_404_NOT_FOUND)
      
      if not employee.isManager:
            return Response({'error': 'You are not authorized to view employees.'}, status=HTTP_401_UNAUTHORIZED)
      
      # fetch all employees
      restaurant = employee.restaurant
      employees = Employee.objects.filter(restaurant = restaurant)
      
      serializer = EmployeeSerializer(employees, many = True)
      return Response({'employees': serializer.data}, status=HTTP_200_OK)
      
      
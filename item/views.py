from functools import wraps
from django.db.models import Q
from rest_framework.status import *
from rest_framework.response import Response
from . permissions import CanAdd, CanManage
from rest_framework.decorators import api_view, permission_classes
from . models import Category
from . serializers import CategorySerializer, MenuSerializer, ItemSerializer, ModifierSerializer
from app_user.models import Restaurant, Employee





@api_view(['POST', 'GET'])
@permission_classes([CanAdd])
def add_category(request):
      user = request.user
      if request.method == "POST":
            # Extract data from the request
            category_name = request.data.get('name')
            description = request.data.get('description')
            restaurant_id = request.data.get('restaurant')
            
            # Check if required fields are present
            if not category_name or not restaurant_id:
                  return Response({'error': 'Name and restaurant are required.'}, status=HTTP_400_BAD_REQUEST)

            # Try to retrieve the Restaurant instance
            try:
                  restaurant = Restaurant.objects.get(id=restaurant_id)
            except Restaurant.DoesNotExist:
                  return Response({'error': 'Restaurant does not exist.'}, status=HTTP_404_NOT_FOUND)

            # Check if the user has the right permissions
            if user.profile.role == 'owner' or Employee(user = user, restaurant=restaurant, isManager=True).exists():
                  # Create the Category
                  category = Category.objects.create(
                        restaurant=restaurant,
                        name=category_name,
                        description=description,
                  )
                  
                  # Serialize the created Category
                  category_serializer = CategorySerializer(category)
                  return Response({'message': 'Category created successfully.', 'data': category_serializer.data}, status=HTTP_201_CREATED)
            else:
                  return Response({'error': 'You are not the owner or manager of this restaurant.'}, status=HTTP_403_FORBIDDEN)
            
      elif request.method == 'GET':
            categories = Category.objects.filter(
                  Q(restaurant__owner = user.profile) |
                  Q(restaurant__employees__user = user)
            ).distinct()
            
            category_serializer = CategorySerializer(categories, many=True)
            return Response({'categories': category_serializer.data}, status=HTTP_200_OK)
            




@api_view(['POST'])
@permission_classes([CanAdd])
def add_menu(request):
      if request.method == 'POST':
            serializer = MenuSerializer(data = request.data, context = {'request': request})
            
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
      
@api_view(["POST"])
@permission_classes([CanAdd])
def add_item(request):
      if request.method == 'POST':
            serializer = ItemSerializer(data = request.data, context = {'request': request})
            
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
      
@api_view(["POST"])
@permission_classes([CanAdd])
def add_modifier(request):
      if request.method == 'POST':
            serializer = ModifierSerializer(data = request.data, context = {"request": request})
            
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors)
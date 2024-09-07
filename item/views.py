from functools import wraps
from rest_framework.status import *
from rest_framework.response import Response
from . permissions import CanAdd, CanManage
from rest_framework.decorators import api_view, permission_classes
from . models import Category
from . serializers import CategorySerializer, MenuSerializer, ItemSerializer, ModifierSerializer
from app_user.models import Restaurant





@api_view(['POST'])
@permission_classes([CanAdd])
def add_category(request):
      user = request.user
      
      # handle get_request
      if request.method == 'GET':
            restaurants = Restaurant.objects.filter(owner__user = user)
            
            if not Restaurant.exists():
                  return Response({'error': "You don't own a restaurant."}, status=HTTP_404_NOT_FOUND)
            
            categories = Category.objects.filter(restaurant__in = restaurants)
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
      
      if request.method == "POST":
            restaurant_id = request.data.get('restaurant')
            
            try:
                  restaurant = Restaurant.objects.get(id = restaurant_id, owner__user = user)
            except Restaurant.DoesNotExist:
                  return Response({'error': 'Create categories for your own restaurant.'}, status = HTTP_400_BAD_REQUEST)
            
            data = request.data.copy()
            data['restaurant'] = restaurant.id
            serializer = CategorySerializer(data = request.data, context = {'request': request})
            
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
      

@api_view(['PUT', 'DELETE'])
@permission_classes([CanManage])
def manage_category(request, pk=None):
      if pk is not None:
            try:
                  category = Category.objects.get(pk=pk)
            except Category.DoesNotExist:
                  return Response({"error": "Category not found."}, status=HTTP_404_NOT_FOUND)
            
            if request.method == "PUT":
                  serializer = CategorySerializer(category, data=request.data, context = {'request': request})
                  if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                  return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            
            elif request.method == "DELETE":
                  category.delete()



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
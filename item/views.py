from functools import wraps
from rest_framework.status import *
from rest_framework.response import Response
from . permissions import CanAdd, CanManage
from rest_framework.decorators import api_view, permission_classes
from . models import Category
from . serializers import CategorySerializer, MenuSerializer, ItemSerializer, ModifierSerializer





@api_view(['POST'])
@permission_classes([CanAdd])
def add_category(request):
      # POST: create a new Category
      if request.method == 'POST':
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
                  return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors)
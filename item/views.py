from functools import wraps
from django.db.models import Q
from rest_framework.status import *
from rest_framework.response import Response
from . permissions import CanAccess, CanManage
from rest_framework.decorators import api_view, permission_classes
from . models import Category, Menu, Item, Modifier
from . serializers import CategorySerializer, MenuSerializer, ItemSerializer, ModifierSerializer, ItemModifierSerializer
from app_user.models import Restaurant, Employee
from app_user.serializers import RestaurantSerializer





@api_view(['POST', 'GET'])
@permission_classes([CanAccess, CanManage])
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
            




@api_view(['POST', 'GET'])
@permission_classes([CanAccess, CanManage])
def add_menu(request):
      user = request.user
      if request.method == 'POST':
            # extract data from the request
            category_id = request.data.get('category')
            name = request.data.get('name')
            description = request.data.get('description')
            
            if not category_id or not name:
                  return Response({'error': 'Category and name are required.'}, status=HTTP_400_BAD_REQUEST)
            
            # retrieve category instance
            try:
                  category = Menu.objects.get(id = category_id)
                  restaurant_id = category.restaurant.id
            except Menu.DoesNotExist:
                  return Response({'error': 'No menu Find'}, status=HTTP_404_NOT_FOUND)
            
            # Check for permission
            if user.profile.role == 'owner': 
                  if restaurant_id not in user.profile.restaurants.values_list('id', flat=True):
                        return Response({'error': 'You do not have permissions for this Restaurant.'}, status=HTTP_403_FORBIDDEN)
            elif user.employee.isManager:
                  if user.employee.restaurant.id != restaurant_id:
                        return Response({'error': 'You do not have permissions for this Restaurant.'}, status=HTTP_403_FORBIDDEN) 
            
            menu_data = {
                  'category': category_id,
                  'name': name,
                  'description': description,
            }
            serializer = MenuSerializer(data = menu_data)
            if serializer.is_valid():
                  serializer.save()
                  return Response({'message': 'Menu created successfully.'}, status=HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
      
      # Get the menus
      elif request.method == 'GET':
            menus = Menu.objects.filter(
                  Q(category__restaurant__owner = user.profile) |
                  Q(category__restaurant__employees__user = user)
            ).distinct()
            
            menu_serializer = MenuSerializer(menus, many=True)
            return Response({'menus': menu_serializer.data}, status=HTTP_200_OK)
      
@api_view(["POST","GET"])
@permission_classes([CanAccess, CanManage])
def add_item(request):
      user = request.user
      if request.method == 'POST':
            item_name = request.data.get('name')
            description = request.data.get('description')
            menu_id = request.data.get('menu')
            price = request.data.get('price')
            
            if not menu_id or not item_name or not price:
                  return Response({'error': "Missing required fill."}, status=HTTP_406_NOT_ACCEPTABLE)      
            
            try:
                  menu = Menu.objects.get(id = menu_id)
                  restaurant_id = menu.category.restaurant.id
            except Menu.DoesNotExist:
                  return Response({'error': 'No menu Find'}, status=HTTP_404_NOT_FOUND)
            
            if user.profile.role == 'owner': 
                  if restaurant_id not in user.profile.restaurants.values_list('id', flat=True):
                        return Response({'error': 'You do not have permissions for this Restaurant.'}, status=HTTP_403_FORBIDDEN)
            elif user.employee.isManager:
                  if user.employee.restaurant.id != restaurant_id:
                        return Response({'error': 'You do not have permissions for this Restaurant.'}, status=HTTP_403_FORBIDDEN)      
            
            item_data = {
                  'menu': menu_id,
                  'name': item_name,
                  'description': description,
                  'price': price,
            }
            serializer = ItemSerializer(data = item_data)
            if serializer.is_valid():
                  serializer.save()
                  return Response({'message': "Item create successfully.", 'item_data': serializer.data}, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
      
      elif request.method == "GET":
            items = Item.objects.filter(
                  Q(menu__category__restaurant__owner = user.profile) |
                  Q(menu__category__restaurant__employees__user = user)
            ).distinct()
            
            item_serializer = ItemSerializer(items, many=True)
            return Response({'items': item_serializer.data}, status=HTTP_200_OK)



@api_view(["POST", "GET"])
@permission_classes([CanAccess, CanManage])
def add_modifier(request):
      user = request.user
      if request.method == 'POST':
            modifier_name = request.data.get('name')
            restaurant_id = request.data.get('restaurant')
            description = request.data.get('description')
            price = request.data.get('price')
            
            if not modifier_name or not restaurant_id or not price:
                  return Response({'error': "Required data are missing"}, status=HTTP_403_FORBIDDEN)
            
            if user.profile.role == 'owner': 
                  if restaurant_id not in user.profile.restaurants.values_list('id', flat=True):
                        return Response({'error': 'You do not have permissions for this Restaurant.'}, status=HTTP_403_FORBIDDEN)
            elif user.employee.isManager:
                  if user.employee.restaurant.id != restaurant_id:
                        return Response({'error': 'You do not have permissions for this Restaurant.'}, status=HTTP_403_FORBIDDEN)
            
            modifier_data = {
                  'name': modifier_name,
                  'restaurant': restaurant_id,
                  'description': description,
                  'price': price
            }
            serializer = ModifierSerializer(data = modifier_data)
            if serializer.is_valid():
                  serializer.save()
                  return Response({"message": "Modifier create successfully.", "modifier": serializer.data}, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_403_FORBIDDEN)
      
      elif request.method == "GET":
            modifiers = Modifier.objects.filter(
                  Q(restaurant__owner = user.profile) |
                  Q(restaurant__employees__user = user)
            ).distinct()
            
            modifier_serializer = ModifierSerializer(modifiers, many = True)
            return Response({'modifiers': modifier_serializer.data}, status=HTTP_200_OK)




@api_view(['POST'])
@permission_classes([CanAccess])
def add_item_modifier(request):
      if request.method == 'POST':
            item_id = request.data.get('item')
            modifier_id = request.data.get('modifier')
            
            if not item_id or not modifier_id:
                  return Response({'error': 'Items and Modifiers both are required.'}, status=HTTP_406_NOT_ACCEPTABLE)
            
            item_modifier = {
                  'item': item_id,
                  'modifier': modifier_id,
            }
            serializer = ItemModifierSerializer(data = item_modifier)
            if serializer.is_valid():
                  serializer.save()
                  return Response({'message': 'ItemModifier created successfully', 'data': serializer.data}, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# # Get all data for customer
# @api_view(['GET'])
# def all(request):
#       try:
#             restaurants = Restaurant.objects.prefetch_related(
#                   'categories__menus__items',
#                   'modifiers'
#             ).all()
            
#             restaurant_serializer = RestaurantSerializer(restaurants, many=True)
#             return Response({'restaurants': restaurant_serializer.data}, status=HTTP_200_OK)
#       except Restaurant.DoesNotExist:
#             return Response({"error": "No data available now. Try again letter."}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            
from rest_framework import serializers
from item.models import Category, Menu, Item, Modifier
from app_user.models import Restaurant, Employee
from django.contrib.auth.models import User


# Serializers for getting restaurant data
class ItemSerializer(serializers.ModelSerializer):
      class Meta:
            model = Item
            fields = ['id', 'name', 'description', 'price']

class ModifierSerializer(serializers.ModelSerializer):
      class Meta:
            model = Modifier
            fields = ['id', 'name', 'description', 'price']

class MenuSerializer(serializers.ModelSerializer):
      items = ItemSerializer(many = True, read_only=True)
      
      class Meta:
            model = Menu
            fields = ['id', 'name', 'items']
            
class CategorySerializer(serializers.ModelSerializer):
      menus = MenuSerializer(many=True, read_only=True)
      
      class Meta:
            model = Category
            fields = ['id', 'name', 'menus']
            
class RestaurantSerializer(serializers.ModelSerializer):
      categories = CategorySerializer(many=True, read_only=True)
      modifiers = ModifierSerializer(many=True, read_only=True)
      
      class Meta:
            model = Restaurant
            fields = ['id', 'name', 'categories', 'modifiers']
            


# Serializers for getting Owner data
class UserSerializer(serializers.ModelSerializer):
      class Meta:
            model = User
            fields = ['first_name', 'last_name', 'username', 'email']


# Also use this serializer for manager to view the restaurant employees
class EmployeeSerializer(serializers.ModelSerializer):
      user = UserSerializer(read_only = True)
      
      class Meta:
            model = Employee
            fields = ['user', 'isManager']
            
class OwnerRestaurantSerializer(serializers.ModelSerializer):
      employees = EmployeeSerializer(many = True, read_only = True)
      
      class Meta:
            model = Restaurant
            fields = ['id', 'name', 'location', 'employees']
            
      
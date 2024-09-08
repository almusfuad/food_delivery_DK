from rest_framework import serializers
from item.models import Category, Menu, Item, Modifier, ItemModifier
from app_user.models import Restaurant


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
      
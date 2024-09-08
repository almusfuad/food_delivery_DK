from rest_framework import serializers
from . models import Menu, Category, Item, Modifier, ItemModifier
from app_user.models import Restaurant


class CategorySerializer(serializers.ModelSerializer):
      restaurant_name = serializers.CharField(source='restaurant.name', read_only = True)
      
      class Meta:
            model = Category
            fields = ['id', 'restaurant', 'restaurant_name', 'name', 'description']
            read_only_fields = ['restaurant_name']

      
      def create(self, validated_data):
            return super().create(validated_data)
      
      def update(self, instance, validated_data):
            validated_data.pop('restaurant', None)          # Prevent changing the restaurant of the category
            return super().update(instance, validated_data)
      
      
class MenuSerializer(serializers.ModelSerializer):
      category_name = serializers.CharField(source = "category.name", read_only = True) # Display category name
      
      class Meta:
            model = Menu
            fields = ['id', 'category', 'category_name', 'name', 'description']
            read_only_fields = ['category_name']            
            
      def create(self, validated_data):
            return super().create(validated_data)
      
      
class ItemSerializer(serializers.ModelSerializer):
      menu_name = serializers.CharField(source = 'menu.name', read_only = True)
      
      class Meta:
            model = Item
            fields = ['id', 'menu', 'menu_name', 'name', 'description', 'price']
            read_only_fields = ['menu_name']
            
      def create(self, validated_data):
            return super().create(validated_data)
      

class ModifierSerializer(serializers.ModelSerializer):
      restaurant_name = serializers.CharField(read_only = True, source = 'restaurant.name')
      
      class Meta:
            model = Modifier
            fields = ['id', 'restaurant', 'restaurant_name', 'name', 'description', 'price']
            read_only_fields = ['restaurant_name']
            
      def create(self, validated_data):
            return super().create(validated_data)

      
      
class ItemModifierSerializer(serializers.ModelSerializer):
      item_name = serializers.CharField(source = 'item.name', read_only = True)
      modifier_name = serializers.CharField(source = 'modifier.name', read_only = True)
      
      class Meta:
            model=ItemModifier
            fields = ['id', 'item', 'item_name', 'modifier', 'modifier_name']
            read_only_fields = ['item_name', 'modifier_name']
            
      def create(self, validated_data):
            return super().create(validated_data)
      
      
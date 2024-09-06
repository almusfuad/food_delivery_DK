from rest_framework import serializers
from . models import Menu, Category, Item, Modifier, ItemModifier


class CategorySerializer(serializers.ModelSerializer): 
      class Meta:
            model = Category
            fields = ['id', 'user', 'name', 'description']
            read_only_fields = ['user']
            
      
      def create(self, validated_data):
            validated_data['user'] = self.context['request'].user       # Get auto logged user
            return super().create(validated_data)
      
      def update(self, instance, validated_data):
            validated_data.pop('user', None)          # Prevent changing the owner of the menu
            return super().update(instance, validated_data)
      
      
class MenuSerializer(serializers.ModelSerializer):
      category_name = serializers.CharField(source = "category.name", read_only = True) # Display category name
      
      class Meta:
            model = Menu
            fields = ['id', 'category', 'category_name', 'name', 'description']
            read_only_fields = ['category_name']
            
            
      def create(self, validated_data):
            return super().create(validated_data)
      
      def update(self, instance, validated_data):
            return super().update(instance, validated_data)
      
      
class ItemSerializer(serializers.ModelSerializer):
      menu_name = serializers.CharField(source = 'menu.name', read_only = True)
      
      class Meta:
            model = Item
            fields = ['id', 'menu', 'menu_name', 'name', 'description', 'price']
            read_only_fields = ['menu_name']
            
      def create(self, validated_data):
            return super().create(validated_data)
      
      
      def update(self, instance, validated_data):
            return super().update(instance, validated_data)
      

class ModifierSerializer(serializers.ModelSerializer):
      
      class Meta:
            model = Modifier
            fields = ['id', 'name', 'description', 'price']
            
      def create(self, validated_data):
            return super().create(validated_data)
      
      def update(self, instance, validated_data):
            return super().update(instance, validated_data)
      
      
class ItemModifierSerializer(serializers.ModelSerializer):
      item_name = serializers.CharField(source = 'item.name', read_only = True)
      modifier_name = serializers.CharField(source = 'modifier.name', read_only = True)
      
      class Meta:
            model=ItemModifier
            fields = ['id', 'item', 'item_name', 'modifier', 'modifier_name']
            read_only_fields = ['item_name', 'modifier_name']
            
      def create(self, validated_data):
            return super().create(validated_data)
      
      
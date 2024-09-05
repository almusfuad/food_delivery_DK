from rest_framework import serializers
from . models import Menu, Category, Item, Modifier


class MenuSerializer(serializers.ModelSerializer): 
      class Meta:
            model = Menu
            fields = ['id', 'user', 'name', 'description']
            read_only_fields = ['user']
            
      
      def create(self, validated_data):
            validated_data['user'] = self.context['request'].user       # Get auto logged user
            return super().create(validated_data)
      
      def update(self, instance, validated_data):
            validated_data.pop('user', None)          # Prevent changing the owner of the menu
            return super().update(instance, validated_data)
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import UserProfiles


class UserRegisterSerializer(serializers.ModelSerializer):
      password = serializers.CharField(write_only=True)
      password_confirm = serializers.CharField(write_only=True)
      role = serializers.ChoiceField(choices = UserProfiles.ROLE_CHOICES)
      
      class Meta:
            model = User
            fields = [
                  'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'role'
            ]
            
      def validate(self, data):
            if data['password'] != data['password_confirm']:
                  raise serializers.ValidationError({"password": "Password doesn't match."})
            return data
      
      
      def create(self, validated_data):
            validated_data.pop("password_confirm")
            password = validated_data.pop('password')
            role = validated_data.pop('role')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            
            # Create user role
            UserProfiles.objects.create(user=user, role=role)
            
            # generate token while registration
            token, created = Token.objects.get_or_create(user = user)
            
            return user, token
            
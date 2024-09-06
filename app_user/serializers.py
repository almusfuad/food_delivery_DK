from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import UserProfile, Employee, Restaurant


class UserRegisterSerializer(serializers.ModelSerializer):
      password = serializers.CharField(write_only=True)
      password_confirm = serializers.CharField(write_only=True)
      role = serializers.ChoiceField(choices = UserProfile.ROLE_CHOICES)
      
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
            UserProfile.objects.create(user=user, role=role)
            
            # generate token while registration
            token, created = Token.objects.get_or_create(user = user)
            
            return user, token


class UserLoginSerializer(serializers.Serializer):
      username = serializers.CharField()
      password = serializers.CharField()
      
      def validate(self, data):
            user = authenticate(
                  username = data['username'],
                  password = data['password']
            )
            
            if user is None:
                  raise serializers.ValidationError("Invalid username or password.")
            return {"user": user}
      
      
      
class EmployeeManageSerializer(serializers.ModelSerializer):
      username = serializers.CharField(source = "user.username", required = False)
      email = serializers.CharField(source = "user.email", required = False)
      first_name = serializers.CharField(source = "user.first_name", required = False)
      last_name = serializers.CharField(source = "user.last_name", required = False)
      password = serializers.CharField(write_only = True, required = False)
      
      
      class Meta:
            model = Employee
            fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'owner']
            
      def create(self, validated_data):
            user_data = validated_data.pop('user')
            password = user_data.pop('password', None)
            user = User.objects.create(**user_data)
            
            if password:
                  user.set_password(password)
            user.save()
            
            employee = Employee.objects.create(user = user, **validated_data)
            return employee
      
      def update(self, instance, validated_data):
            user_data = validated_data.pop('user', None)
            if user_data:
                  for attr, value in user_data.items():
                        setattr(instance.user, attr, value)
                  instance.user.save()
            return super().update(instance, validated_data)
      
      def to_representation(self, instance):
            data = super().to_representation(instance)
            return data


class RestaurantSerializer(serializers.ModelSerializer):
      owner_name = serializers.CharField(source = 'user.username', read_only = True)
      
      class Meta:
            model = Restaurant
            fields = ['id', 'owner', 'owner_name', 'name', 'location']
            read_only_fields = ['owner_name']
            
      def create(self, validated_data):
            return super().create(validated_data)
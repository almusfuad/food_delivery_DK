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
      username = serializers.CharField(source="user.username", required=False)
      email = serializers.CharField(source="user.email", required=False)
      first_name = serializers.CharField(source="user.first_name", required=False)
      last_name = serializers.CharField(source="user.last_name", required=False)

      class Meta:
            model = Employee
            fields = ['id', 'username', 'email', 'first_name', 'last_name', 'isManager', 'restaurant']
      
      def create(self, validated_data):
            print(f"Validated data in serializer: {validated_data}")
            user_data = validated_data.pop('user', {})
            
            print(f"user data for creation: {user_data}")

            user = User.objects.create(**user_data)
            
            user.save()
            
            restaurant = validated_data.pop('restaurant', None)
            employee = Employee.objects.create(user=user, restaurant=restaurant, **validated_data)
            return employee
      

      
      def to_representation(self, instance):
            data = super().to_representation(instance)
            return data


class RestaurantSerializer(serializers.ModelSerializer):
      owner_name = serializers.CharField(source = 'owner.user.username', read_only = True)
      
      class Meta:
            model = Restaurant
            fields = ['id', 'owner', 'owner_name', 'name', 'location']
            read_only_fields = ['owner_name']
            
      def create(self, validated_data):
            return super().create(validated_data)
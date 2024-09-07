import random
import string
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout as auth_logout, login as auth_login
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer, UserLoginSerializer, EmployeeManageSerializer, RestaurantSerializer
from . permissions import IsOwner
from . models import Employee, Restaurant


# for employee creation a auto generate password will assign
def generate_password(length = 8):
      return ''.join(random.choice(string.ascii_letters + string.digits, k=length))


@api_view(['POST'])
def registration(request):
      try:
            reg_serializer = UserRegisterSerializer(data = request.data)
            if reg_serializer.is_valid():
                  user, token = reg_serializer.save()
                  # auth_login(request, user)         # login after a successful registration
                  return Response(
                        {
                              "message": "User registered successfully.",
                              "username": user.username,
                              'token': token.key,
                        },
                        status=HTTP_201_CREATED)
            return Response({'error': reg_serializer.errors}, status=HTTP_400_BAD_REQUEST)
      
      except Exception as e:
            print(f"Error during registration: {e}")
            return Response({'error': "An unexpected error occurred. Please try again later."}, status=HTTP_500_INTERNAL_SERVER_ERROR)
      
@api_view(['POST'])
def user_login(request):
      try:
            login_serializer = UserLoginSerializer(data = request.data)
            if login_serializer.is_valid():
                  user = login_serializer.validated_data['user']
                  auth_login(request, user)
                  
                  token, created = Token.objects.get_or_create(user = user)
                  
                  # Response data
                  user_data = {
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.profile.role,
                        "token": token.key,
                  }
                  
                  return Response({"user_data": user_data}, status=HTTP_200_OK)
            return Response({"Error": login_serializer.errors}, status=HTTP_400_BAD_REQUEST)
      
      except Exception as e:
            print(f"Error during login: {e}")
            return Response({"error": "An unexpected error occurred. Please try again latter."}, status=HTTP_502_BAD_GATEWAY)
      

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_logout(request):
      try:
            user = request.user
            
            # Delete the token and logout the user
            Token.objects.filter(user = user).delete()
            auth_logout(request)
            
            return Response({"message": "Logged out successfully."}, status=HTTP_200_OK)
      except Exception as e:
            print(f"Logout error: {e}")
            return Response({"During logged out an error has occurred. Try again later."}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsOwner])
def owner_manage_employee(request, pk=None):
      
      # Check the owner for permissions
      owner_profile = request.user.profile
      if owner_profile.role != 'owner':
            return Response({"error": "Only owner can create or delete employee."}, status=HTTP_400_BAD_REQUEST)
      
      try:
            restaurant = Restaurant.objects.get(owner = owner_profile)
      except Exception as e:
            return Response({'error': 'Owner does not have a restaurant.'}, status=HTTP_404_NOT_FOUND)
      
      # create an employee
      if request.method == 'POST':
            generated_password = generate_password()
            
            is_manager = request.data.get('isManager', False)
            
            # create user for employee
            request.data['user'] = {
                  'username': request.data.get('username'),
                  'email': request.data.get('email'),
                  'first_name': request.data.get('first_name'),
                  'last_name': request.data.get('last_name'),
                  'password': generated_password,
            }
            request.data['restaurant'] = restaurant.id
            request.data['isManager'] = is_manager
            
            try:
                  serializer = EmployeeManageSerializer(data = request.data)
                  if serializer.is_valid():
                        employee = serializer.save()
                        return Response({
                              'message': 'Employee created successfully.',
                              'username': employee.user.username,
                              'password': generated_password,
                              'isManager': employee.isManager
                        }, status=HTTP_201_CREATED)
                  return Response({'error': serializer.errors}, status=HTTP_406_NOT_ACCEPTABLE)
            except Exception as e:
                  print(f"Employee creation error: {e}")
                  return Response({'error': "Employee creation failed"}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated, IsOwner])
def manage_restaurant(request):
      owner_profile = request.user.profile
      
      # create new restaurant
      if request.method == 'POST':
            request.data['owner'] = owner_profile.id
            
            serializer = RestaurantSerializer(data = request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
      
      # Handle get request
      elif request.method == "GET":
            if owner_profile.role != 'owner':
                  return Response({'error': "Only owners can view their restaurant"}, status=HTTP_403_FORBIDDEN)
            
            restaurants = Restaurant.objects.filter(owner = owner_profile)
            serializer = RestaurantSerializer(restaurants, many = True)
            return Response(serializer.data, status=HTTP_200_OK)
            
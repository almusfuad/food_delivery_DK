import secrets
import string
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import logout as auth_logout, login as auth_login
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer, UserLoginSerializer, EmployeeRegistrationSerializer


# for employee creation a auto generate password will assign
def generate_password(length = 10):
      # Generate secure password as Django accepts
      characters = string.ascii_letters + string.digits + string.punctuation
      password = ''.join(secrets.choice(characters) for i in range(length))
      return password


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
      
      
@api_view(["POST"])
def add_employee(request):
      try:
            # check the user
            if request.user.profile.role != 'owner':
                  return Response(
                        {"error": "Only a restaurant owners can add employees."},
                        status=HTTP_403_FORBIDDEN
                  )
                  
            # Generate and assign password to the serializer
            generated_password = generate_password()
            request.data['password'] = generated_password
            employee_serializer = EmployeeRegistrationSerializer(data = request.data)
            
            if employee_serializer.is_valid():
                  employee = employee_serializer.save()
                  return Response(
                        {
                              "message":"Employee created successfully.",
                              "username": employee.username,
                              "role": employee.profile.role,
                              "password": generated_password,
                        },
                        status=HTTP_201_CREATED
                  )                  
            return Response({"error": employee_serializer.errors}, status=HTTP_400_BAD_REQUEST)
      except Exception as e:
            print(f"Add employee error: {e}")
            return Response({"error": "An error occurred. Try again later."}, status=HTTP_502_BAD_GATEWAY)
      
      
@api_view(["GET"])
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
            
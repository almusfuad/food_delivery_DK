from rest_framework import status, response, permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login as auth_login
from .serializers import UserRegisterSerializer

# Create your views here.
@api_view(['POST'])
def registration(request):
      try:
            reg_serializer = UserRegisterSerializer(data = request.data)
            if reg_serializer.is_valid():
                  user, token = reg_serializer.save()
                  # auth_login(request, user)
                  return response.Response(
                        {
                              "message": "User registered successfully.",
                              "username": user.username,
                              'token': token.key,
                        },
                        status=status.HTTP_201_CREATED)
            return response.Response({'error': reg_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
      
      except Exception as e:
            print(f"Error during registration: {e}")
            return response.Response({'error': "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
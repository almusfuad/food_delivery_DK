from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from . models import Menu
from . serializers import MenuSerializer


@api_view(['POST', 'PUT', 'DELETE'])
def manage_menu(request, pk=None):
      # creating menu
      if request.method == "POST":
            menu_serializer = MenuSerializer(data = request.data, context = {'request': request})
            if menu_serializer.is_valid():
                  menu_serializer.save()
                  return Response(menu_serializer.data, status=HTTP_201_CREATED)
            return Response(menu_serializer.errors, status=HTTP_400_BAD_REQUEST)
      
      elif request.method == 'PUT' and pk is not None:
            try:
                  menu = Menu.object.get(pk = pk)
            except Menu.DoesNotExist:
                  return Response({"detail": "Menu not found."}, status=HTTP_404_NOT_FOUND)
      
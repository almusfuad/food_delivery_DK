from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import *
from .serializers import OrderSerializer
from .permissions import CanOrder


@api_view(['POST'])
@permission_classes([CanOrder])
def create_order(request):
      serializer = OrderSerializer(data=request.data)
      
      if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response({'message': 'Your order is successfully placed.', 'order_data': serializer.data}, status=HTTP_201_CREATED)
      return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
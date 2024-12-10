from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers import *
from asgiref.sync import sync_to_async


class CreateOrder(APIView):
    async def post(self, request, *args, **kwargs):
        order_serializer = OrderSerializer(data=request.data)
        if await sync_to_async(order_serializer.is_valid)():
            # create Order by serializer
            await order_serializer.acreate(order_serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


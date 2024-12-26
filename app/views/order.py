from app.views import *
from app.utils import *


class CreateOrder(APIView):
    async def post(self, request, *args, **kwargs):
        order_serializer = OrderSerializer(data=request.data)
        if await sync_to_async(order_serializer.is_valid)():
            # create Order by serializer
            await order_serializer.acreate(order_serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetShippingDate(APIView):
    async def post(self, request: AsyncRequest):
        # get client
        client_id = request.data.get('client', None)
        client: Client = await Client.objects.aget(id=client_id)

        shipping_date: datetime = await get_next_nearest_day_by_weekdays(client.days_of_the_week)
        response = {
            'date': shipping_date.strftime('%d.%m.%Y')
        }
        return Response(response, status=status.HTTP_200_OK)

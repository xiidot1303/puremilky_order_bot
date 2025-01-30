from app.views import *
from app.utils import *
from app.services.recommended_order_service import *


class RecommendedOrdersByClient(APIView):
    @sync_to_async
    def post(self, request, *args, **kwargs):
        client_id = request.data.get('client', None)
        # client: Client = await Client.objects.aget(id=client_id)
        recommended_orders = filter_recommended_orders_by_client(client_id)
        serializer = RecommendedOrderSerializer(
            recommended_orders, many=True, context={'client_id': client_id})
        return Response(serializer.data, status=status.HTTP_200_OK)

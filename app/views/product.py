from app.views import *
from adrf.views import APIView
from app.services.product_service import *


class ProductListByCategoryView(APIView):
    async def post(self, request: AsyncRequest):
        # Get the title from the POST request data
        category_id = request.data.get('category', None)

        # Filter products by category
        products = await filter_products_by_category(category_id)

        # Serialize the filtered products data
        serializer = ProductSerializer(products, many=True)
        return Response(await serializer.adata, status=status.HTTP_200_OK)

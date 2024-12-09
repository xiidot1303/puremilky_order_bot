from app.views import *
from adrf.views import APIView
from app.services.product_service import *
from app.services.client_service import *


class CategoryListView(APIView):
    async def post(self, request: AsyncRequest):
        # get all categories
        categories = await sync_to_async(Category.objects.all)()

        # Serialize the filtered products data
        serializer = CategorySerializer(categories, many=True)
        return Response(await serializer.adata, status=status.HTTP_200_OK)


class ProductListByCategoryView(APIView):
    async def post(self, request: AsyncRequest):
        # Get the title from the POST request data
        category_id = request.data.get('category', None)
        client_id = request.data.get('client', None)

        client: Client = await Client.objects.aget(id=client_id)

        # Filter products by category
        products = await filter_products_by_category_and_by_client(category_id, client.price_type_uuid)

        # Serialize the filtered products data
        serializer = ProductSerializer(products, many=True)
        return Response(await serializer.adata, status=status.HTTP_200_OK)


class ProductListByTitleView(APIView):
    async def post(self, request: AsyncRequest):
        # Get the title from the POST request data
        title = request.data.get('title', None)
        client_id = request.data.get('client', None)

        client: Client = await Client.objects.aget(id=client_id)

        # Filter products by title
        products = await filter_products_by_title(title, client.price_type_uuid)

        # Serialize the filtered products data
        serializer = ProductSerializer(products, many=True)
        return Response(await serializer.adata, status=status.HTTP_200_OK)

from app.views import *
from adrf.views import APIView
from app.services.product_service import *


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

        # Filter products by category
        products = await filter_products_by_category(category_id)

        # Serialize the filtered products data
        serializer = ProductSerializer(products, many=True)
        return Response(await serializer.adata, status=status.HTTP_200_OK)


class ProductListByTitleView(APIView):
    async def post(self, request: AsyncRequest):
        # Get the title from the POST request data
        title = request.data.get('title', None)

        # Filter products by title
        products = await filter_products_by_title(title)

        # Serialize the filtered products data
        serializer = ProductSerializer(products, many=True)
        return Response(await serializer.adata, status=status.HTTP_200_OK)

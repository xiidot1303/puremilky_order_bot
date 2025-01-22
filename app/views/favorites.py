from app.views import *
from app.utils import *
from app.services.favorites_service import *


class CreateFavorites(APIView):
    async def post(self, request, *args, **kwargs):
        favorites_serializer = FavoritesSerializerByData(data=request.data)
        if await sync_to_async(favorites_serializer.is_valid)():
            # create Favorites by serializer
            await favorites_serializer.acreate(favorites_serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(favorites_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteFavorites(APIView):
    async def post(self, request: AsyncRequest, *args, **kwargs):
        favorites_id = request.data.get('favorites_id', None)
        favorites = await Favorites.objects.filter().afirst()
        await favorites.adelete()
        return Response(status=status.HTTP_200_OK)


class FavoritesListByClient(APIView):
    def post(self, request: AsyncRequest):
        client_id = request.data.get('client', None)
        favorites = filter_favorites_of_client(client_id)
        serializer = FavoritesSerializer(
            favorites, many=True, context={'client_id': client_id})
        return Response(serializer.data, status=status.HTTP_200_OK)

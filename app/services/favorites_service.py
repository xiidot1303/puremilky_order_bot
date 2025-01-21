from app.services import *
from app.models import Favorites


def filter_favorites_of_client(client_id):
    query = Favorites.objects.filter(
        client__id=client_id).prefetch_related('favoritesitem_set')
    return query

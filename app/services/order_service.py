from app.models import Order, OrderItem
from django.db.models import QuerySet, F
from asgiref.sync import sync_to_async


filter_unpublished_orders_dict = {
    'published': False
}


@sync_to_async
def get_order_items_details_of_order(order: Order):
    query = OrderItem.objects.filter(order=order).annotate(
        quantity=F('count'),
        product_uuid=F('product__uuid'),  # Rename 'count' to 'quantity'
    ).values(
        'product_uuid',
        'price',
        'quantity'
    )
    return list(query)


def filter_orders_of_client(client_id):
    query = Order.objects.filter(client__id=client_id).prefetch_related('orderitem_set')
    return query

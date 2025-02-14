from app.models import Order, OrderItem, MinOrderAmount, Product, Client, Bonus
from django.db.models import QuerySet, F, IntegerField, ExpressionWrapper
from asgiref.sync import sync_to_async


filter_unpublished_orders_dict = {
    'published': False
}


@sync_to_async
def get_order_items_details_of_order(order: Order):
    details = []
    for order_item in OrderItem.objects.filter(order=order):
        order_item: OrderItem
        product: Product = order_item.product
        client: Client = order_item.order.client
        bonus: Bonus = Bonus.objects.filter(product=product, client=client, type_bonus="item_free_12_1").exists()
        order_detail = {
            'product_uuid': order_item.product.uuid,
            'price': order_item.price,
            'quantity': order_item.count,
            'quantity_bonus': order_item.count // 12 if bonus else 0
        }
        details.append(order_detail)
    return details


def filter_orders_of_client(client_id):
    query = Order.objects.filter(
        client__id=client_id).prefetch_related('orderitem_set')
    return query


async def get_min_order_amount_by_region(region: str):
    obj = await MinOrderAmount.objects.filter(region=region).afirst()
    return obj.amount if obj else 0

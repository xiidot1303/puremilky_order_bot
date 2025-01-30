from app.services import *
from app.models import RecommendedOrder, Client, Product


async def update_recommended_orders_using_data(data: list, region='samarkand'):
    # delete old objects
    await RecommendedOrder.objects.filter(region=region).adelete()

    new_recommended_orders = []

    for item in data:
        client: Client = await Client.objects.filter(uuid=item['client_uuid']).afirst()
        product: Product = await Product.objects.filter(uuid=item['product_uuid']).afirst()
        quantity = item['quantity_order']
        if client and product and quantity != 0:
            price_type = RecommendedOrder(
                client=client,
                product=product,
                quantity=quantity,
                region=region
            )
            new_recommended_orders.append(price_type)

    # Create new price types if any
    if new_recommended_orders:
        for r in range(0, len(new_recommended_orders), 500):
            await RecommendedOrder.objects.abulk_create(new_recommended_orders[r:r+500])


def filter_recommended_orders_by_client(client_id):
    return RecommendedOrder.objects.filter(client__id=client_id)

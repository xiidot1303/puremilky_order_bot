from app.services.order_service import *
from app.services.one_c_service import *
from app.utils import get_next_nearest_day_by_weekdays


async def publish_orders_to_one_c():
    async for order in Order.objects.filter(**filter_unpublished_orders_dict):
        try:
            order: Order
            client = await order.get_client
            order_details = await get_order_items_details_of_order(order)
            shipping_date: datetime = await get_next_nearest_day_by_weekdays(client.days_of_the_week)
            response = await create_order_api(
                shipping_date, client.uuid, order_details, client.region
            )
            order.published = True
            await order.asave()
        except:
            None

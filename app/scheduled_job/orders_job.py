from app.services.order_service import *
from app.services.one_c_service import *
from app.services.client_service import *
from app.utils import get_next_nearest_day_by_weekdays
from bot.control.updater import application, NewsletterUpdate
from bot.models import Bot_user
from bot.bot import Strings


async def publish_orders_to_one_c():
    async for order in Order.objects.filter(**filter_unpublished_orders_dict):
        try:
            order: Order
            client = await order.get_client
            bot_user = await order.get_bot_user
            order_details = await get_order_items_details_of_order(order)
            shipping_date: datetime = await get_next_nearest_day_by_weekdays(client.days_of_the_week)
            response = await create_order_api(
                shipping_date, client.uuid, order_details, bot_user.phone if bot_user else "", client.region
            )
            order.published = True
            await order.asave()
        except:
            None


async def send_reminder_about_order():
RUSSIAN_WEEKDAYS = ["Понедельник", "Вторник", "Среда",
                    "Четверг", "Пятница", "Суббота", "Воскресенье"]
tomorrow: datetime = datetime_now() + timedelta(days=1)
weekday = RUSSIAN_WEEKDAYS[tomorrow.weekday()]
async for client in Client.objects.filter(days_of_the_week__contains=weekday):
    # get bot user by client
    bot_user: Bot_user = await Bot_user.objects.filter(client__id=client.id).afirst()
    if bot_user:
        text = Strings(user_id=bot_user.user_id).reminder_about_order
        markup = None
        await application.update_queue.put(
            NewsletterUpdate(bot_user.user_id, text, reply_markup=markup)
        )

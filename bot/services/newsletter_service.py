from bot.bot import *
import asyncio

async def send_alert_about_activation_notify(context: CustomContext):
    user_id = context.job.user_id
    text = Strings(user_id=user_id).successfully_activated
    await send_newsletter(bot, user_id, text)

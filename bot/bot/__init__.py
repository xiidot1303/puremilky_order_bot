from bot import *
from telegram import Update, MenuButtonWebApp
from telegram.ext import ContextTypes, CallbackContext, ExtBot, Application
from dataclasses import dataclass
from asgiref.sync import sync_to_async
from bot.utils import *
from bot.utils.bot_functions import *
from bot.utils.keyboards import *
from bot.services import *
from bot.resources.conversationList import *
from app.services import filter_objects_sync
from config import WEBAPP_URL


async def is_message_back(update: Update):
    if update.message.text == Strings(update.effective_user.id).back:
        return True
    else:
        return False


async def main_menu(update: Update, context: CustomContext):
    bot = context.bot

    await bot.send_message(
        update.effective_user.id,
        context.words.main_menu,
        reply_markup=ReplyKeyboardRemove(True)
    )
    bot_user: Bot_user = await get_object_by_update(update)
    client_id = (await bot_user.get_client).id
    webapp = WebAppInfo(url=f"{WEBAPP_URL}?client={client_id}")
    menu_button = MenuButtonWebApp(
        text=context.words.order,
        web_app=webapp
    )
    await context.bot.set_chat_menu_button(
        context._user_id, menu_button=menu_button
    )

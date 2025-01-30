from bot.bot import *
from app.services.client_service import *


async def _to_the_selecting_lang(update: Update, context: CustomContext):
    text = Strings.hello
    markup = await select_lang_keyboard()
    await update_message_reply_text(update, text, reply_markup=markup)
    return SELECT_LANG


async def _to_the_getting_client_id(update: Update, context: CustomContext):
    text = context.words.type_your_client_id
    markup = await reply_keyboard_remove()
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_CLIENT_ID


async def _to_the_getting_contact(update: Update, context: CustomContext):
    text = context.words.send_number
    markup = ReplyKeyboardMarkup([[
        KeyboardButton(text=context.words.leave_number, request_contact=True)
    ]], resize_keyboard=True, one_time_keyboard=True)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_CONTACT


async def get_lang(update: Update, context: CustomContext):
    response = update.effective_message.text
    if response == Strings.uz_ru[0]:
        lang = 0
    else:
        lang = 1
    context.user_data['lang'] = lang

    return await _to_the_getting_contact(update, context)


async def get_contact(update: Update, context: CustomContext):
    phone_number = update.effective_message.contact.phone_number
    lang = context.user_data['lang']
    obj, created = await Bot_user.objects.aget_or_create(
        user_id=update.effective_user.id,
        defaults={
            'lang': lang,
            'phone': phone_number,
            'name': update.effective_user.first_name
        }
    )
    if not created:
        obj.lang = lang
        obj.phone = phone_number
        obj.name = update.effective_user.first_name
        await obj.asave()

    if 'client_id' in context.user_data:
        if client := await get_client_by_uuid(context.user_data['client_id']):
            obj.client = client
            await obj.asave()
            await main_menu(update, context)
            return ConversationHandler.END

    return await _to_the_getting_client_id(update, context)


async def get_client_id(update: Update, context: CustomContext):
    client_id = update.effective_message.text
    client: Client = await get_client_by_uuid(client_id)
    if client:
        # set client to bot user
        bot_user: Bot_user = await get_object_by_update(update)
        bot_user.client = client
        await bot_user.asave()
        # return to main menu
        await main_menu(update, context)
        return ConversationHandler.END
    else:
        text = context.words.client_id_is_incorrect
        await update_message_reply_text(update, text)
        return

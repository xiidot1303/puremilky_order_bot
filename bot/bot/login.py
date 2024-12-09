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


async def get_lang(update: Update, context: CustomContext):
    response = update.effective_message.text
    if response == Strings.uz_ru[0]:
        lang = 0
    else:
        lang = 1

    obj, created = await Bot_user.objects.aget_or_create(
        user_id=update.effective_user.id,
        defaults={
            'lang': lang
        }
    )
    if not created:
        obj.lang = lang
        await obj.asave()

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


async def start(update: Update, context: CustomContext):
    return await _to_the_selecting_lang(update, context)

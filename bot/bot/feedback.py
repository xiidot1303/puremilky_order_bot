from bot.bot import *
from app.services.feedback_service import *


async def get_feedback(update: Update, context: CustomContext):
    feedback_text = update.effective_message.text
    bot_user: Bot_user = await get_object_by_update(update)
    await create_feedback(feedback_text, bot_user=bot_user)
    await update.message.reply_text(
        text=context.words.feedback_received
    )
    await main_menu(update, context)
    return ConversationHandler.END


async def start(update: Update, context: CustomContext):
    await main_menu(update, context)
    return ConversationHandler.END

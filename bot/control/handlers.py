from bot import *
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler,
    TypeHandler,
    ConversationHandler
)

from bot.resources.conversationList import *

from bot.bot import (
    main, login
)

exceptions_for_filter_text = (~filters.COMMAND) & (
    ~filters.Text(Strings.main_menu))

login_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', main.start)
    ],
    states={
        SELECT_LANG: [MessageHandler(
            filters.Text(Strings.uz_ru),
            login.get_lang
        )],

        GET_CLIENT_ID: [
            MessageHandler(
                filters.TEXT & exceptions_for_filter_text,
                login.get_client_id
            )
        ]
    },
    fallbacks=[
        CommandHandler('start', login.start)
    ],
    persistent=True,
    name='login'
)

handlers = [
    login_handler,
    TypeHandler(type=NewsletterUpdate, callback=main.newsletter_update)
]

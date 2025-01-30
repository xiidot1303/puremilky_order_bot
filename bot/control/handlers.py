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
        GET_CONTACT: [
            MessageHandler(filters.CONTACT, login.get_contact),
            MessageHandler(filters.TEXT & exceptions_for_filter_text,
                           login._to_the_getting_contact)
        ],
        GET_CLIENT_ID: [
            MessageHandler(
                filters.TEXT & exceptions_for_filter_text,
                login.get_client_id
            )
        ]
    },
    fallbacks=[
        CommandHandler('start', main.start)
    ],
    persistent=True,
    name='login'
)

handlers = [
    login_handler,
    CommandHandler('logout', main.logout),
    TypeHandler(type=NewsletterUpdate, callback=main.newsletter_update)
]

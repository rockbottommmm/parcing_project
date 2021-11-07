from dialog import dialog_start, dialog_category, dialog_tags, dialog_filters, dialog_fallback, dialog_numbers
from handlers import greet_user, talk_to_me
import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

"""Это основной файл для запуска бота. Здесь описаны все его настройки"""

# Ниже происходит логирование ситуаций, возникших в ходе работы бота

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

"""Это функция main. Она запускает бота. Следовательно, чтобы запустить бота,
нужно использовать именно файл bot.py"""


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
# Ниже идет описание диалога - последовательность сообщений, высылаемых пользователю
    dialog = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Выбрать категорию)$'), dialog_start)],
        states={
            "category": [MessageHandler(Filters.text, dialog_category)],
            "tag": [MessageHandler(Filters.text, dialog_tags)],
            "filters": [MessageHandler(Filters.text, dialog_filters)],
            "posts_number": [MessageHandler(Filters.text, dialog_numbers)]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.video | Filters.document | Filters.location, dialog_fallback)
        ]
    )

    dp.add_handler(dialog)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Вернуться в начало)$'),dialog_start))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()

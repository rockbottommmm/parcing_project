import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import greet_user, talk_to_me
from dialog import dialog_start, dialog_category, dialog_tags, filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')



def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher

    dialog = ConversationHandler(
        entry_points = [
            MessageHandler(Filters.regex('^(Выбрать категорию)$'), dialog_start)

        ],
        states = {
            "category": [MessageHandler(Filters.text, dialog_category)],
            "tag": [MessageHandler(Filters.text, dialog_tags)],
            "filters": [MessageHandler(Filters.text, filters)]


        },
        fallbacks = []


    )

    dp.add_handler(dialog)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()

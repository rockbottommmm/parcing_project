from telegram import ReplyKeyboardMarkup

def keyboard(reply_keyboard):
    keyboard = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True)
    return keyboard
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def keyboard(reply_keyboard):
    keyboard = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True)
    return keyboard

def inline_keyboard_category():
    keyboard = [
        [
            InlineKeyboardButton('Горячее', callback_data = 'hot'),
            InlineKeyboardButton('Свежее', callback_data= 'fresh')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
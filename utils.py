from telegram import ReplyKeyboardMarkup, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

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

def return_hot(elem,update,tag,reply_keyboard):
    return update.message.reply_text(f"""<b>Название поста:</b> {elem["item_title"]}\n<b>Теги поста:</b> \
{", ".join(elem["item_tags"])}\n<b>URL поста:</b> {elem["item_url"]}\n\
<b>Количество просмотров:</b> {elem["item_views"]}\n<b>Рейтинг поста:</b> {elem["item_rating"]}\n\
<b>Количество комментариев:</b> {elem["item_comments"]}\n<b>Дата и время публикации поста:</b> \
{datetime.fromtimestamp(elem["item_date_timestamp"]).strftime('%d-%m-%Y %H:%M:%S')}""",
parse_mode = ParseMode.HTML, reply_markup = keyboard(reply_keyboard))

def return_fresh(elem,update,tag,reply_keyboard):
    return update.message.reply_text(f"""<b>Название поста:</b> {elem["item_title"]}\n<b>Теги поста:</b> \
{", ".join(elem["item_tags"])}\n<b>URL поста:</b> {elem["item_url"]}\n<b>Количество комментариев:</b> {elem["item_comments"]}\n<b>Дата и время публикации поста:</b> \
{datetime.fromtimestamp(elem["item_date_timestamp"]).strftime('%d-%m-%Y %H:%M:%S')}""",
parse_mode = ParseMode.HTML, reply_markup = keyboard(reply_keyboard))

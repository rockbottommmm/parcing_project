from datetime import datetime
from telegram import ReplyKeyboardMarkup, ParseMode
from emoji import emojize
"""Здесь описаны все полезные функции, используемые на проекте"""

# Область эмоджи

USER_EMOJI = [':fire:', ':herb:', ':arrows_clockwise:', ':back:', ':100:', ':clock4:',
':pencil:', ':diamond_shape_with_a_dot_inside:', ':newspaper:',':fast_forward:',':dizzy:']
fire_emoji = emojize(USER_EMOJI[0], use_aliases=True)
fresh_emoji = emojize(USER_EMOJI[1], use_aliases=True)
restart_emoji= emojize(USER_EMOJI[2], use_aliases=True)
back_emoji = emojize(USER_EMOJI[3], use_aliases=True)
rating_emoji = emojize(USER_EMOJI[4], use_aliases=True)
time_emoji = emojize(USER_EMOJI[5], use_aliases=True)
comments_emoji = emojize(USER_EMOJI[6], use_aliases=True)
views_emoji = emojize(USER_EMOJI[7], use_aliases=True)
blanket_emoji = emojize(USER_EMOJI[8], use_aliases=True)
notags_emoji = emojize(USER_EMOJI[9], use_aliases=True)
begin_emoji = emojize(USER_EMOJI[10], use_aliases=True)


# Функция для создания клавиатуры в telegram


def keyboard(reply_keyboard):
    keyboard = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    return keyboard


# Функция для поддержания правильных работ падежей при выводе юзеру количества доступных
# тегов

def converter(lst):
    str_lst = str(lst)
    if 1 < int(str_lst[-1]) < 5 and lst < 10:
        return "а"
    elif 10 <= lst <= 20:
        return "ов"
    elif 5 <= int(str_lst[-1]) <= 9 and lst > 20:
        return "ов"
    elif lst > 20 and int(str_lst[-1]) == 0:
        return "ов"
    elif lst > 20 and 1 < int(str_lst[-1]) < 5:
        return "a"
    else:
        return ""

# Функция нужная для корректного возвращения пользователю тех или иных постов последовательно
# после того, как он прошел анкету (это для категории "горячих" постов)


def return_hot(elem, update, tag, reply_keyboard):
    return update.message.reply_text(f"""<b>Название поста:</b> {elem["item_title"]}\n<b>Теги поста:</b> \
{", ".join(elem["item_tags"])}\n<b>URL поста:</b> {elem["item_url"]}\n\
<b>Количество просмотров:</b> {elem["item_views"]}\n<b>Рейтинг поста:</b> {elem["item_rating"]}\n\
<b>Количество комментариев:</b> {elem["item_comments"]}\n<b>Дата и время публикации поста:</b> \
{datetime.fromtimestamp(elem["item_date_timestamp"]).strftime('%d-%m-%Y %H:%M:%S')}""",
parse_mode=ParseMode.HTML, reply_markup=keyboard(reply_keyboard))


# Функция нужная для корректного возвращения пользователю тех или иных постов последовательно
# после того, как он прошел анкету (это для категории "свежих" постов)


def return_fresh(elem, update, tag, reply_keyboard):
    return update.message.reply_text(f"""<b>Название поста:</b> {elem["item_title"]}\n<b>Теги поста:</b> \
{", ".join(elem["item_tags"])}\n<b>URL поста:</b> {elem["item_url"]}\n<b>Количество комментариев:</b> {elem["item_comments"]}\n<b>Дата и время публикации поста:</b> \
{datetime.fromtimestamp(elem["item_date_timestamp"]).strftime('%d-%m-%Y %H:%M:%S')}""",
parse_mode=ParseMode.HTML, reply_markup=keyboard(reply_keyboard))

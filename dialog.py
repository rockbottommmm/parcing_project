from mongo import (fresh_item_tags, hot_item_tags, collection_hot, collection_fresh)
from random import choice, sample
from telegram.parsemode import ParseMode
from telegram.ext import ConversationHandler
from utils import (keyboard, return_fresh, return_hot, converter)

"""Данный файл описывает диалог с пользователем"""

# Функция нужна, чтобы отреагировать на фразу юзера "Вернуться в начало


def restart(update, context):
    reply_keyboard = [["Выбрать категорию"]]
    update.message.reply_text(
        'Я тебя понял, выбирай категорию',
        reply_markup=keyboard(reply_keyboard))
    return ConversationHandler.END


# Функция инициирует диалог с юзером по фразе "Выбрать категорию"


def dialog_start(update, context):
    reply_keyboard = [["Горячее"], ['Свежее']]
    update.message.reply_text(
        "Ну же, выбирай!",
        reply_markup=keyboard(reply_keyboard)
    )
    return 'category'


# Функция предлагает пользователю выбрать горячее/свежее (рубрики Пикабу)


def dialog_category(update, context):
    category_lst = ['Горячее', 'Свежее']
    category = update.message.text
    if category not in category_lst:
        update.message.reply_text("Пожалуйста, выбери горячее/свежее")  # проверка на попадание в категорию
        return "category"
    else:
        context.user_data["dialog"] = {
            "category": category  # фиксирование в словаре "юзер_дата"
                    }
        reply_keyboard = [["Не хочу писать тег, хочу сразу все посты"],
        ["Вернуться в начало"]]
        if category == "Горячее":  # вывод пользователю ответа, что выбрано все правильно
            update.message.reply_text(f"Отлично! Ты выбрал '{category.strip()}', напиши желаемый тег, \
например <b>{choice(hot_item_tags)}</b>\n\
Всего тег{converter(len(hot_item_tags))}: {len(hot_item_tags)}\
\nПримеры тегов: {', '.join(sample(hot_item_tags,10))}",
            reply_markup=keyboard(reply_keyboard),
            parse_mode=ParseMode.HTML
            )
            return "tag"
        elif category == "Свежее":
            update.message.reply_text(f"Отлично! Ты выбрал '{category.strip()}', напиши желаемый тег, \
например <b>{choice(fresh_item_tags)}</b>\n\
Всего тег{converter(len(fresh_item_tags))}: {len(fresh_item_tags)}\
\nПримеры тегов: {', '.join(sample(fresh_item_tags,10))}",
            reply_markup=keyboard(reply_keyboard),
            parse_mode=ParseMode.HTML
            )
            return "tag"

# Функция помогает пользователю выбрать тег, а также проверяет на правильность написания тега


def dialog_tags(update, context):
    tag = update.message.text
    reply_keyboard=[["Фильтр по дате (сначала новое)"],
        ["Фильтр по просмотрам (сначала топ просмотров)"],
        ["Фильтр по рейтингу (сначала наибольший)"],
        ["Фильтр по комментариям (сначала много)"],
        ["Не надо сортировку, хочу простыню"],
        ["Вернуться в начало"]
        ]
    reply_fresh = [["Выдать простыню"],["Вернуться в начало"]]
    if (tag == "Не хочу писать тег, хочу сразу все посты") and (context.user_data['dialog']['category'] \
        == "Горячее"):
        context.user_data["dialog"]['tag'] = tag
        update.message.reply_text('Окей! Переходим сразу к фильтрации!',
        reply_markup=keyboard(reply_keyboard)
        )
        return "filters"
    elif (tag == "Не хочу писать тег, хочу сразу все посты") and (context.user_data['dialog']['category'] \
        == "Свежее"):
        context.user_data["dialog"]['tag'] = tag
        update.message.reply_text('Окей! Переходим сразу к постам!',
        reply_markup=keyboard(reply_fresh)
        )
        return "filters"
    elif tag == "Вернуться в начало":
        return restart(update, context)

    elif (tag not in hot_item_tags) and (context.user_data['dialog']['category'] == "Горячее"):
        update.message.reply_text('Извини, но такого тега у нас нет.. Попробуй еще раз! Пиши без кавычек')
        return "tag"
    elif (tag not in fresh_item_tags) and (context.user_data['dialog']['category'] == "Свежее"):
        update.message.reply_text('Извини, но такого тега у нас нет.. Попробуй еще раз!')
        return "tag"

    else:
        context.user_data["dialog"]['tag'] = tag.strip()
        if context.user_data["dialog"]["category"] == "Горячее":    

            update.message.reply_text(
                f'Отлично! Ты выбрал тег "{tag}". Давай отфильтруем посты!',
                reply_markup=keyboard(reply_keyboard)
            )
            return "filters"
        elif context.user_data["dialog"]["category"] == "Свежее":
            reply_keyboard = [["Выдать простыню"],
            ["Вернуться в начало"]]
            update.message.reply_text(
                f'Отлично! Ты выбрал тег "{tag}". Переходим к постам!',
                reply_markup=keyboard(reply_keyboard)
            )
            return "filters"

# Функция предлагает выбрать фильтр и проверяет правильность ввода фильтра


def dialog_filters(update, context):
    filters = ["Фильтр по дате (сначала новое)",
        "Фильтр по просмотрам (сначала топ просмотров)",
        "Фильтр по рейтингу (сначала наибольший)",
        "Фильтр по комментариям (сначала много)",
        "Не надо сортировку, хочу простыню",
        "Вернуться в начало"
        ]
    filter = update.message.text
    if filter == 'Вернуться в начало':
        return restart(update, context)
    elif (filter not in filters) and (filter != "Выдать простыню"):
        update.message.reply_text('Введи правильный фильтр')
        return "filters"
    else:
        reply_keyboard = [["Вернуться в начало"]]
        context.user_data["dialog"]['filter'] = filter
        update.message.reply_text("Отлично! Теперь напиши количество постов (цифра от 1 до 30)",
        reply_markup=keyboard(reply_keyboard))
        return "posts_number"

# Функция позволяет пользователю выбрать число постов для вывода + проверки на правильность 
# выбора количества постов


def dialog_numbers(update, context):
    tag = context.user_data['dialog']['tag']
    posts_amount = update.message.text
    reply_keyboard = [["Вернуться в начало "], ["Вернуться на шаг назад "]]
    filter = context.user_data['dialog']['filter']
    if posts_amount == "Вернуться в начало":
        return restart(update, context)
    elif posts_amount == "Вернуться на шаг назад":
        reply_keyboard = [["Вернуться в начало"]]
        update.message.reply_text(
            "Хорошо, выбирай количество постов (цифра от 1 до 30)",
            reply_markup=keyboard(reply_keyboard))
        return "posts_number"
    try:
        posts_amount = int(posts_amount)
        if posts_amount < 1 or posts_amount > 30:
            update.message.reply_text("Введи цифру от 1 до 30")
            return "posts_number"
    except:
        update.message.reply_text("Введи цифру от 1 до 30")
        return "posts_number"

    posts_amount = int(posts_amount)
    context.user_data['dialog']['posts_number'] = [posts_amount]


# Ниже происходит выдача постов прямиком из базы данных MongoDB,
# Где лежат посты. В зависимости от if-условия, можно отследить логику
# Выдачи
    if context.user_data["dialog"]["category"] == "Горячее":
        if filter == "Не надо сортировку, хочу простыню":
            if context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection_hot.find().limit(posts_amount):
                    return_hot(elem, update, tag, reply_keyboard)
            else:
                for elem in collection_hot.find({"item_tags": tag}).limit(posts_amount):
                    return_hot(elem, update, tag, reply_keyboard)

        elif filter == "Фильтр по дате (сначала новое)":
            if not context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection_hot.find({"item_tags": tag}).sort('item_date_timestamp',-1).limit(
                        posts_amount):
                    return_hot(elem, update, tag, reply_keyboard)
            else:
                for elem in collection_hot.find().sort('item_date_timestamp', -1).limit(posts_amount):
                    return_hot(elem, update, tag, reply_keyboard)

        elif filter == "Фильтр по рейтингу (сначала наибольший)":
            if not context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection_hot.find({"item_tags": tag}).sort('item_rating', -1).limit(
                        posts_amount):
                    return_hot(elem, update, tag, reply_keyboard)
            else:
                for elem in collection_hot.find().sort('item_rating', -1).limit(posts_amount):
                    return_hot(elem, update, tag, reply_keyboard)

        elif filter == "Фильтр по просмотрам (сначала топ просмотров)":
            if not context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection_hot.find({"item_tags":tag}).sort('item_views', -1).limit(
                        posts_amount):
                    return_hot(elem, update, tag, reply_keyboard)
            else:
                for elem in collection_hot.find().sort('item_views',-1).limit(posts_amount):
                    return_hot(elem, update, tag, reply_keyboard)

        elif filter == "Фильтр по комментариям (сначала много)":
            if not context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection_hot.find({"item_tags":tag}).sort('item_comments', -1).limit(
                        posts_amount):
                    return_hot(elem, update, tag, reply_keyboard)
            else:
                for elem in collection_hot.find().sort('item_comments', -1).limit(posts_amount):
                    return_hot(elem, update, tag, reply_keyboard)

        else:
            return ConversationHandler.END

    elif context.user_data["dialog"]["category"] == "Свежее":

        if filter == "Выдать простыню":
            if context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection_fresh.find().sort('item_date_timestamp', -1).limit(posts_amount):
                    return_fresh(elem, update, tag, reply_keyboard)
            else:
                for elem in collection_fresh.find({"item_tags": tag}).sort('item_date_timestamp', -1).limit(
                        posts_amount):
                    return_fresh(elem, update, tag, reply_keyboard)

        else:
            return ConversationHandler.END


def dialog_fallback(update, context):
    update.message.reply_text("Пожалуйста, не присылай мне документы, картинки или подобное, \
    я не отвечу")

from telegram import replykeyboardmarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from utils import keyboard, inline_keyboard_category
from telegram.ext import ConversationHandler
from mongo_settings import MyCluster
from pymongo import MongoClient

# cluster = MongoClient(MyCluster)
# db = cluster['Parcing_db']
# collection = db['Posts_info']

def restart (update,context):
    reply_keyboard = [["Выбрать категорию"]]
    update.message.reply_text('Я тебя понял, выбирай категорию',
    reply_markup = keyboard(reply_keyboard))
    return ConversationHandler.END

def dialog_start(update,context):
    reply_keyboard = [['Горячее'],['Свежее']]
    update.message.reply_text(
        "Ну же, выбирай!",
        reply_markup = keyboard(reply_keyboard)
    )
    return 'category'


def dialog_category(update,context):
    category_lst = ['Горячее','Свежее']
    category = update.message.text
    if category not in category_lst:
        update.message.reply_text("Пожалуйста, выбери горячее/свежее")
        return "category"
    else:
        context.user_data["dialog"] = {
            "category":category
        }
        reply_keyboard = [["Не хочу писать тег, хочу сразу все посты"],["Вернуться в начало"]]
        update.message.reply_text(f"Отлично! Ты выбрал '{category.strip()}', напиши желаемый тег",
        reply_markup = keyboard(reply_keyboard)
        )
        return "tag"

tags = ["Айти", "Еда"]
#здесь будет проверка на правильность тэга из монго


def dialog_tags(update,context):
    tag = update.message.text
    reply_keyboard = [["Фильтр по дате (сначала новое)"],
        ["Фильтр по просмотрам (сначала топ просмотров)"],
        ["Фильтр по рейтингу (сначала наибольший)"],
        ["Не надо сортировку, хочу простыню"],
        ["Вернуться в начало"]
        ]

    if tag == "Не хочу писать тег, хочу сразу все посты":
        context.user_data["dialog"]['tag'] = tag
        update.message.reply_text('Окей! Переходим сразу к фильтрации!',
        reply_markup = keyboard(reply_keyboard)
        )
        return "filters"

    elif tag == "Вернуться в начало":
        return restart(update,context)

    elif tag not in tags:
        update.message.reply_text('Извини, но такого тега у нас нет.. Попробуй еще раз!')
        return "tag"

    else:
        context.user_data["dialog"]['tag'] = tag
            

        update.message.reply_text(
            f'Отлично! Ты выбрал тег "{tag}". Давай отфильтруем посты!',
            reply_markup = keyboard(reply_keyboard)
        )
        return "filters"

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
        return restart(update,context)
    elif filter not in filters:
        update.message.reply_text('Введи правильный фильтр')
        return "filters"
    elif filter == "Не надо сортировку, хочу простыню":
        context.user_data["dialog"]['filter'] = filter
        reply_keyboard = [["Выбрать категорию"]]
        update.message.reply_text('Окей! Вот результат, 1 секунду...',
        reply_markup = keyboard(reply_keyboard))
        #Сюда вывод из монго
        return ConversationHandler.END
    
    
    else:

        context.user_data["dialog"]['filter'] = filter
        reply_keyboard = [["Выбрать категорию"]]
        update.message.reply_text(f'Отлично! Фильтруем по {filter.split()[2]}. 1 секунду...',
        reply_markup = keyboard(reply_keyboard))

        print(context.user_data)
        #Сюда вывод из монго
        return ConversationHandler.END

def dialog_fallback(update,context):
    update.message.reply_text("Не надо лишнего, плиз")



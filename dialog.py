from telegram import replykeyboardmarkup
from utils import keyboard


def dialog_start(update,context):
    reply_keyboard = [['Горячее'],['Свежее']]
    update.message.reply_text(
        "Привет! Выбери категорию",
        reply_markup = keyboard(reply_keyboard)
    )
    return "category"


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
        reply_keyboard = [["Не хочу писать тег, хочу сразу все посты"]]
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
        ["Не надо сортировку, хочу простыню"]
        ]

    if tag == "Не хочу писать тег, хочу сразу все посты":
        context.user_data["dialog"] = {
            "tag":tag
        }
        update.message.reply_text('Окей! Переходим сразу к фильтрации!',
        reply_markup = keyboard(reply_keyboard)
        )
        return "filters"

    elif tag not in tags:
        update.message.reply_text('Извини, но такого тега у нас нет.. Попробуй еще раз!')
        return "tag"

    else:
        context.user_data["dialog"] = {
            "tag":tag
        }

        update.message.reply_text(
            f'Отлично! Ты выбрал тег "{tag}". Давай отфильтруем посты!',
            reply_markup = keyboard(reply_keyboard)
        )
        return "filters"

def filters(update, context):
    filters = ["Фильтр по дате (сначала новое)",
        "Фильтр по просмотрам (сначала топ просмотров)",
        "Фильтр по рейтингу (сначала наибольший)",
        "Не надо сортировку, хочу простыню"
        ]
    filter = update.message.text
    if filter not in filters:
        update.message.reply_text('Введи правильный фильтр')
        return "filters"
    elif filter == "Не надо сортировку, хочу простыню":
        context.user_data["dialog"] = {
            "filter":filter
        }
        update.message.reply_text('Окей! Переходим сразу к фильтрации!')
        
        return "filters"
    else:

        context.user_data["dialog"] = {
            "filter": filter
        }

        update.message.reply_text(f'Отлично! Фильтруем по {filter.split()[2]}. 1 секунду...')

    

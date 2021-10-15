from utils import keyboard, return_result
from telegram.ext import ConversationHandler
from mongo import (item_tags, collection)

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

def dialog_tags(update,context):
    tag = update.message.text
    reply_keyboard = [["Фильтр по дате (сначала новое)"],
        ["Фильтр по просмотрам (сначала топ просмотров)"],
        ["Фильтр по рейтингу (сначала наибольший)"],
        ["Фильтр по комментариям (сначала много)"],
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

    elif tag not in item_tags:
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
    
    else:
        reply_keyboard = [["Выбрать категорию"]]
        tag = context.user_data['dialog']['tag']
        context.user_data["dialog"]['filter'] = filter
        
        if filter == "Не надо сортировку, хочу простыню":
            if context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection.find().limit(10):
                    return_result(elem,update,tag,reply_keyboard)
            else:
                for elem in collection.find({"item_tags":tag}).limit(10):
                    return_result(elem,update,tag,reply_keyboard)

        elif filter == "Фильтр по дате (сначала новое)":
            if not context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection.find({"item_tags":tag}).sort('item_date_timestamp',-1).limit(10):
                    return_result(elem,update,tag, reply_keyboard)
            else:
                for elem in collection.find().sort('item_date_timestamp',-1).limit(10):
                    return_result(elem,update,tag,reply_keyboard)

        elif filter == "Фильтр по рейтингу (сначала наибольший)":
            if not context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection.find({"item_tags":tag}).sort('item_rating',-1).limit(10):
                    return_result(elem,update, tag, reply_keyboard) 
            else:
                for elem in collection.find().sort('item_rating',-1).limit(10):
                    return_result(elem,update,tag,reply_keyboard)
        
        elif filter == "Фильтр по просмотрам (сначала топ просмотров)":
            if not context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection.find({"item_tags":tag}).sort('item_views',-1).limit(10):
                    return_result(elem,update,tag,reply_keyboard)
            else:
                for elem in collection.find().sort('item_views',-1).limit(10):
                    return_result(elem,update,tag,reply_keyboard)
        
        elif filter == "Фильтр по комментариям (сначала много)":            
            if not context.user_data['dialog']['tag'] == "Не хочу писать тег, хочу сразу все посты":
                for elem in collection.find({"item_tags":tag}).sort('item_comments',-1).limit(10):
                    return_result(elem,update,tag,reply_keyboard)
            else:
                for elem in collection.find().sort('item_comments',-1).limit(10):
                    return_result(elem,update,tag,reply_keyboard)
        

        print(context.user_data)
        return ConversationHandler.END

def dialog_fallback(update,context):
    update.message.reply_text("Не надо лишнего, плиз")



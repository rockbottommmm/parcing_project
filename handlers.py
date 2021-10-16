from utils import keyboard

def greet_user(update, context):
    reply_keyboard = [["Выбрать категорию"]]
    text = 'Привет! Выберем категорию?'
    print(text)
    
    update.message.reply_text(
        f'{text}',
        reply_markup = keyboard(reply_keyboard))

def talk_to_me(update,context):
    text = update.message.text
    if text != "Выдай еще" or text != "Вернуться на шаг назад":
        update.message.reply_text(f'Мы пока не можем обработать "{text}", но мы очень стараемся!')

# def dialog_start_inline(update,context):
#     update.callback_query.answer()
#     result = update.callback_query.data
#     update.callback_query.edit_message_caption(caption = f"Отлично! Ты выбрал {result}")
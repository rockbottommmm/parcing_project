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
    update.message.reply_text(f'Мы пока не можем обработать "{text}", но мы очень стараемся!')


def greet_user(update, context):
    text = 'Привет!'
    print(text)
    
    update.message.reply_text(
        f'{text}'
        )
def talk_to_me(update,context):
    text = update.message.text
    update.message.reply_text(f'Мы пока не можем обработать "{text}", но мы очень стараемся!')
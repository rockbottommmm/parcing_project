from utils import keyboard
"""Здесь лежат хэндлеры - обработчики тех или иных ситуаций"""

def greet_user(update, context):  # Приветствие пользователя
    reply_keyboard = [["Выбрать категорию"]]
    text = 'Привет! Ты попал в Пикабота :) Выберем категорию?'
    to_console = "Бот запущен"
    print(to_console)

    update.message.reply_text(
        f'{text}',
        reply_markup=keyboard(reply_keyboard))


def talk_to_me(update, context):  # Обработка всех текстов, за исключением ключевых из dialog.py
    text = update.message.text
    reply_keyboard = [["Выбрать категорию"]]
    if text != "Выдай еще" or text != "Вернуться на шаг назад":
        update.message.reply_text(
            f'Мы пока не можем обработать "{text}", но мы очень стараемся!',
            reply_markup=keyboard(reply_keyboard))

# Все, что не обработано в функции выше, обрабатывается в dialog.py в функции dialog_fallbacks
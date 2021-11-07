# Pikabot
Pikabot - это телеграм-бот для получения необходимых пользователю постов с сайта Pikabu.ru.  
Пользователь, попадая в бота, выбирает категорию постов: "Горячие" посты (с наибольшим рейтингом), либо "Свежие посты", написанные только что. Далее пользователю дана возможность выбрать тег поста (некое условное обозначение темы поста), либо не выбирать, а посмотреть все. Затем он может отфильтровать посты по разным критериям:
1. По дате (сначала новые)
2. По рейтингу (сначала самые рейтинговые)
3. По просмотрам (топ просмотров)
4. По комментариям (сначала топ комментариев)

Также пользователь может выбрать количество постов к выдаче: от 1 до 30 постов. И вернуться в начало по необходимости.

Попробовать: https://t.me/bot_pikabot  

Проект запущен на heroku, используется база данных MongoDB.

## Сборка репозитория и локальный запуск
Выполните в консоли:
```
git clone https://github.com/rockbottommmm/parcing_project.git
pip install -r requirments.txt
```
 
### Настройка
Создайте файл settings.py и добавьте туда следующие настройки:
```
API_KEY = "Апи ключ, который вы получили у BotFather"
MyClient = "Ссылка на клиент в вашей базе MongoDB Atlas
```
### Наполнение базы данных
Из корня проекта запустите парсер:
```
python parse_new.py
python parse_hot.py
```
Дождитесь, пока спарсятся данные по постам.

### Запуск
Чтобы запустить бота, выполните в консоли:
```
python bot.py
```
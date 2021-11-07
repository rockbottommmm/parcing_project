from pymongo import MongoClient
from settings import MyCluster

"""Здесь происходит подключение к базе данных MongoDB"""

cluster = MongoClient(MyCluster)
db = cluster['Parcing_db']
collection_hot = db['Hot_posts_info']  # Получена база данных "Горячих" постов
collection_fresh = db['Fresh_posts_info']  # Получена база данных "Свежих" постов

#Ниже подсчитывается количество тегов каждой категории постов

hot_item_tags = []
fresh_item_tags = []

result_hot = 0
result_fresh = 0
for elem in collection_hot.find():
    for tag in elem["item_tags"]:
        hot_item_tags.append(tag)

for elem in collection_fresh.find():
    for tag in elem['item_tags']:
        fresh_item_tags.append(tag)

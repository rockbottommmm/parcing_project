from pymongo import MongoClient
from pprint import PrettyPrinter
from settings import MyCluster

cluster = MongoClient(MyCluster)
db = cluster['Parcing_db']
collection = db['Posts_info']

db_for_work = []
for elem in collection.find():
    db_for_work.append(elem)

item_tags=[]

for elem in db_for_work:
    for tag in elem['item_tags']:
        item_tags.append(tag)

for elem in db_for_work:
    tag = 'Скриншот'
    if tag in elem['item_tags']:
        print(elem)

# for item in item_tags:
#     s = item_tags.count(item)
#     print(f'{item} | {s}')
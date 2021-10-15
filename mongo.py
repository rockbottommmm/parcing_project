from pymongo import MongoClient
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


# for elem in item_tags:
#     print(f'{elem} | {item_tags.count(elem)}')

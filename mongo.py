from pymongo import MongoClient
from settings import MyCluster
cluster = MongoClient(MyCluster)
db = cluster['Parcing_db']
collection_hot = db['Hot_posts_info']
collection_fresh = db['Fresh_posts_info']


hot_item_tags=[]
fresh_item_tags=[]

result_hot = 0
result_fresh = 0
for elem in collection_hot.find():
    for tag in elem["item_tags"]:
        hot_item_tags.append(tag)
        #result_hot +=1

for elem in collection_fresh.find():
    for tag in elem['item_tags']:
        fresh_item_tags.append(tag)
        #result_fresh +=1

# for elem in collection_hot.find():
#     print(elem)

# print(hot_item_tags)
# print(result_hot)
# print("--------------")
# print(fresh_item_tags)
# print(result_fresh)
# for elem in item_tags:
#     print(f'{elem} | {item_tags.count(elem)}')

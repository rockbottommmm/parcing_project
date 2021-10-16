# -*- coding: cp1251 -*-
import requests as rq
import xml
from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
import json
from pymongo import MongoClient
from settings import MyCluster
import certifi


cluster = MongoClient(MyCluster)
cert = certifi.where()

cluster = MongoClient(MyCluster, tlsCAFile=cert)
db = cluster["Parcing_db"]
collection_hot = db["Hot_posts_info"]
collection_fresh = db["Fresh_posts_info"]


def parse_new():
    #new_posts = []
    num_of_pages = 50
    for i in range(0,num_of_pages):
        url = "https://pikabu.ru/new?page=" + str(i + 1)

        headers = {
            'authority': 'pikabu.ru',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'
        }

        req = rq.get(url, headers=headers)
        soup = bs(req.content, 'html.parser')
        items = soup.findAll('div', class_='story__main')
        posts_dict = {}
        
        for item in items:
            with open('posts_dict.json') as file:
                new_dict = json.load(file)
            try:
                except_comments = item.find('span', class_= 'story__comments-link-count')
                if except_comments == None:
                    except_comments = 0
                else:
                    except_comments = item.find('span', class_= 'story__comments-link-count').get_text(strip=True)
                
                except_url_ad = item.find('a', class_='story__sponsor story__sponsor_bottom')
                if not except_url_ad:
                    except_url_ad = item.find('a', class_= 'story__title-link').get('href')
                else:
                    continue
            except:
                continue

            item_title =  item.find('a', class_='story__title-link').text.strip()
            item_url = except_url_ad
            item_comments = except_comments

            tags=[]
            item_tags = item.find('div', class_='story__tags tags')
            for i in item_tags.findAll('a', class_='tags__tag'):
                tags.append(i.text)

            item_date_time = item.find('time').get('datetime')
            date_from_iso = datetime.fromisoformat(item_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
            item_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

            item_id = item_url.split('_')[-1]


            posts_dict[item_id] = {
                'item_title': item_title,
                'item_url': item_url,
                'item_date_timestamp': item_date_timestamp,
                'item_comments': int(item_comments),
                'item_tags': tags
            }
            #new_posts.append(posts_dict)
            new_dict.update(posts_dict)

            collection_fresh.insert_one({
                'item_title': item_title,
                'item_url': item_url,
                'item_date_timestamp': item_date_timestamp,
                'item_comments': int(item_comments),
                'item_tags': tags
            })

            with open('posts_dict.json', 'w') as file:
                json.dump(new_dict, file, indent=4, ensure_ascii=False)




def check_new_posts():
    with open('posts_dict.json') as file:
        posts_dict = json.load(file)

    num_of_pages = 15
    fresh_posts = {}
    for i in range(0,num_of_pages):
        url = "https://pikabu.ru/new?page=" + str(i + 1)

        headers = {
            'authority': 'pikabu.ru',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'
        }

        req = rq.get(url, headers=headers)
        soup = bs(req.content, 'html.parser')
        items = soup.findAll('div', class_='story__main')

        for item in items:
            try:
                except_url_ad = item.find('a', class_='story__sponsor story__sponsor_bottom')
                if not except_url_ad:
                    except_url_ad = item.find('a', class_= 'story__title-link').get('href')
                else:
                    continue
            except:
                continue
            item_url = except_url_ad
            item_id = item_url.split('_')[-1]

            if item_id in posts_dict:
                continue
            else:
                try:
                    except_comments = item.find('span', class_= 'story__comments-link-count')
                    if except_comments == None:
                        except_comments = 0
                    else:
                        except_comments = item.find('span', class_= 'story__comments-link-count').get_text(strip=True)
                    
                    except_url_ad = item.find('a', class_='story__sponsor story__sponsor_bottom')
                    if not except_url_ad:
                        except_url_ad = item.find('a', class_= 'story__title-link').get('href')
                    else:
                        continue
                except:
                    continue

            item_title =  item.find('a', class_='story__title-link').text.strip()
            item_url = except_url_ad
            item_comments = except_comments

            tags=[]
            item_tags = item.find('div', class_='story__tags tags')
            for i in item_tags.findAll('a', class_='tags__tag'):
                tags.append(i.text)

            item_date_time = item.find('time').get('datetime')
            date_from_iso = datetime.fromisoformat(item_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
            item_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

            posts_dict[item_id] = {
                'item_title': item_title,
                'item_url': item_url,
                'item_date_timestamp': item_date_timestamp,
                'item_comments': int(item_comments),
                'item_tags': tags
            }

            fresh_posts[item_id] = {
                'item_title': item_title,
                'item_url': item_url,
                'item_date_timestamp': item_date_timestamp,
                'item_comments': item_comments,
                'item_tags': tags
            }

    posts_dict.update(fresh_posts)


    with open('posts_dict.json', 'w') as file:
        json.dump(posts_dict, file, indent=4, ensure_ascii=False)
    
    return fresh_posts

def parse_hot():
    num_of_pages = 5
    for i in range(0,num_of_pages):
        url = "https://pikabu.ru/?page=" + str(i + 1)

        headers = {
            'authority': 'pikabu.ru',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'
        }

        req = rq.get(url, headers=headers)
        soup = bs(req.content, 'html.parser')
        items = soup.findAll('article', class_='story')
        posts_dict = {}
        
        for item in items:
            story = item.find('div', class_='story__main')
            rating = item.find('div', class_='story__left')
            with open('hot_posts_dict.json') as file:
                new_dict = json.load(file)
            try:
                except_comments = story.find('span', class_= 'story__comments-link-count')
                if except_comments == None:
                    except_comments = 0
                else:
                    except_comments = story.find('span', class_= 'story__comments-link-count').get_text(strip=True)
                
                except_url_ad = story.find('a', class_='story__sponsor story__sponsor_bottom')
                if not except_url_ad:
                    except_url_ad = story.find('a', class_= 'story__title-link').get('href')
                else:
                    continue
            except:
                continue

            item_title =  story.find('a', class_='story__title-link').text.strip()
            item_url = except_url_ad
            item_comments = except_comments
            item_views = story.find('span', class_='story__views-count story__views-count_loaded hint').get('aria-label')
            item_views = item_views.split()[0]
            
            item_rating = rating.find('div', class_='story__rating-count').text.strip()
            


            tags=[]
            item_tags = story.find('div', class_='story__tags tags')
            for i in item_tags.findAll('a', class_='tags__tag'):
                tags.append(i.text)

            item_date_time = story.find('time').get('datetime')
            date_from_iso = datetime.fromisoformat(item_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
            item_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

            item_id = item_url.split('_')[-1]


            posts_dict[item_id] = {
                'item_title': item_title,
                'item_url': item_url,
                'item_date_timestamp': item_date_timestamp,
                'item_comments': int(item_comments),
                'item_tags': tags,
                'item_views': int(item_views),
                'item_rating': int(item_rating)
            }
            #new_posts.append(posts_dict)
            new_dict.update(posts_dict)
            
            collection_hot.insert_one({
                'item_title': item_title,
                'item_url': item_url,
                'item_date_timestamp': item_date_timestamp,
                'item_comments': int(item_comments),
                'item_tags': tags,
                'item_views': int(item_views),
                'item_rating': int(item_rating)
            }
            )

            with open('hot_posts_dict.json', 'w') as file:
                json.dump(new_dict, file, indent=4, ensure_ascii=False)

def check_hot_posts():
    with open('hot_posts_dict.json') as file:
        posts_dict = json.load(file)

    num_of_pages = 2
    fresh_posts = {}
    for i in range(0,num_of_pages):
        url = "https://pikabu.ru/?page=" + str(i + 1)

        headers = {
            'authority': 'pikabu.ru',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'
        }

        req = rq.get(url, headers=headers)
        soup = bs(req.content, 'html.parser')
        items = soup.findAll('article', class_='story')

        for item in items:
            story = item.find('div', class_='story__main')
            rating = item.find('div', class_='story__left')
            try:
                except_url_ad = story.find('a', class_='story__sponsor story__sponsor_bottom')
                if not except_url_ad:
                    except_url_ad = story.find('a', class_= 'story__title-link').get('href')
                else:
                    continue
            except:
                continue
            item_url = except_url_ad
            item_id = item_url.split('_')[-1]

            if item_id in posts_dict:
                continue
            else:
                try:
                    except_comments = story.find('span', class_= 'story__comments-link-count')
                    if except_comments == None:
                        except_comments = 0
                    else:
                        except_comments = story.find('span', class_= 'story__comments-link-count').get_text(strip=True)
                    
                    except_url_ad = story.find('a', class_='story__sponsor story__sponsor_bottom')
                    if not except_url_ad:
                        except_url_ad = story.find('a', class_= 'story__title-link').get('href')
                    else:
                        continue
                except:
                    continue

            item_title =  story.find('a', class_='story__title-link').text.strip()
            item_url = except_url_ad
            item_comments = except_comments

            tags=[]
            item_tags = story.find('div', class_='story__tags tags')
            for i in item_tags.findAll('a', class_='tags__tag'):
                tags.append(i.text)
            
            item_views = story.find('span', class_='story__views-count story__views-count_loaded hint').get('aria-label')
            item_views = item_views.split()[0]
            item_rating = rating.find('div', class_='story__rating-count').text.strip()

            item_date_time = story.find('time').get('datetime')
            date_from_iso = datetime.fromisoformat(item_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
            item_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

            posts_dict[item_id] = {
                'item_title': item_title,
                'item_url': item_url,
                'item_date_timestamp': item_date_timestamp,
                'item_comments': int(item_comments),
                'item_tags': tags,
                'item_views': int(item_views),
                'item_rating': int(item_rating)
            }

            fresh_posts[item_id] = {
                'item_title': item_title,
                'item_url': item_url,
                'item_date_timestamp': item_date_timestamp,
                'item_comments': int(item_comments),
                'item_tags': tags,
                'item_views': int(item_views),
                'item_rating': int(item_rating)
            }

    posts_dict.update(fresh_posts)


    with open('hot_posts_dict.json', 'w') as file:
        json.dump(posts_dict, file, indent=4, ensure_ascii=False)
    
    return fresh_posts

def main():
    parse_new()
    #check_new_posts()
    #parse_hot()
    #check_hot_posts()


if __name__ == '__main__':
    main()
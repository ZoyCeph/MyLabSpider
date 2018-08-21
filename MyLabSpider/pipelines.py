# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import pymongo
from scrapy.conf import settings
#from .spiders.CommentSpider import collection_name


class CommentMongoPipeline(object):
#    collection_name = 'Gsl6RoxfN'
#    global collection_name
#    global url
#    client = pymongo.MongoClient('localhost',27017)
#    db_name = 'Sina'
#    db = client[db_name]
#    collection_set01 = db['UrlsQueue']
#    datas=list(collection_set01.find({},{'_id':0,'url':1,'status':1}))
#    for data in datas:
#        if data.get('status') == 'proccessing':
#            url=data.get('url')
#            pattern='(?<=/)([0-9a-zA-Z]{9})(?=\?)'
#            if re.search(pattern,url):
#                collection_name=re.search(pattern,url).group(0)
#                break
#    client.close()
            

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.db['UrlsQueue'].update({'status':'proccessing'},{'$set':{'status':'finished'}})
        self.client.close()

    def process_item(self, item, spider):
        self.collection_name=item.pop('collection_name')
        self.db[self.collection_name].insert_one(dict(item))
        return item
    

class HomepageMongoPipeline(object):
    collection_name = ''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
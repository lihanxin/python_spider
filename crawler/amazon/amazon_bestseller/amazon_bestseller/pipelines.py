# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class AmazonBestsellerPipeline(object):
    def process_item(self, item, spider):
        return item



class MongodbPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient('120.78.67.236', 27017)
        self.auth = self.client.admin
        self.auth.authenticate("root", "Yibai1101")
        self.db = self.client['YB_others_spider']
        self.collections = self.db['Amazon_bestseller']


    def process_item(self, item, spider):
        self.collections.insert(dict(item))
        return item

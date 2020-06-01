# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class StockPipeline:
    def process_item(self, item, spider):
        client=pymongo.MongoClient()
        collection=client['stock']['stock_info']
        collection.insert(item)
        return item

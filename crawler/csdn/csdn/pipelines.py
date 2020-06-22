# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class CsdnPipeline:
    def process_item(self, item, spider):
        return item


class CsdnReviewPipeline:
    def process_item(self, item, spider):
        client=pymongo.MongoClient()
        collection=client['csdn']['review']
        collection.insert(item)
        return item

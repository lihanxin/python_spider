# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class MoviePipeline(object):
    client=MongoClient()
    collection=client["test"]["t2"]
    def process_item(self, item, spider):
        self.collection.insert(item)
        # with open("movie_list.txt","a",encoding="utf-8") as f:
        #     f.write(item+"\n")

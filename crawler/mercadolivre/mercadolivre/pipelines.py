# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class MercadolivrePipeline(object):
    # 爬虫开启时执行，只执行一次
    def open_spider(self, spider):
        #定义链接MongoDB客户端对象
        self.mongo_client=MongoClient()
        #MongoDB库
        self.db=self.mongo_client["mercadolivre"]
        #MongoDB表
        self.collections=self.db["top_search"]
        print("开启爬虫")

    # #处理提取的数据
    def process_item(self, item, spider):
        print("执行数据提取")
        self.collections.insert(item)
        return item
    #
    # #爬虫关闭时执行,只执行一次
    def close_spider(self, spider):
        print("关闭爬虫")
        pass

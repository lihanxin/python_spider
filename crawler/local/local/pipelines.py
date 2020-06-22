# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class LocalPipeline:
    def process_item(self, item, spider):
        return item


class ImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['img_url'],meta={'img_name':item['img_name']})

    def file_path(self, request, response=None, info=None):
        file_name=request.meta['img_name']
        return file_name
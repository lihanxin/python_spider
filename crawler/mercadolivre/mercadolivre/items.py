# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MercadolivreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id=scrapy.Field()
    site=scrapy.Field()
    onecate_name=scrapy.Field()
    twocate_name=scrapy.Field()
    threecate_name=scrapy.Field()
    url=scrapy.Field()
    hot_search=scrapy.Field()







# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CsdnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CsdnReviewItem(scrapy.Item):
    _id=scrapy.Field()
    review_username = scrapy.Field()
    review_content = scrapy.Field()
    review_zan = scrapy.Field()
    review_date = scrapy.Field()
    review_reply = scrapy.Field()

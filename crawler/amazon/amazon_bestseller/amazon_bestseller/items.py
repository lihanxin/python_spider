# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class AmazonBestsellerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name_one = scrapy.Field()
    product_name_one_url = scrapy.Field()
    product_name_two = scrapy.Field()
    product_name_two_url = scrapy.Field()
    product_name_three = scrapy.Field()
    product_name_three_url = scrapy.Field()
    price = scrapy.Field()
    image_url= scrapy.Field()
    reviews= scrapy.Field()
    title = scrapy.Field()
    product = scrapy.Field()
    product_url = scrapy.Field()
    product_location=scrapy.Field()
    scrore= scrapy.Field()
    level = scrapy.Field()
    higher_ups = scrapy.Field()
    end = scrapy.Field()
    crawling_time= scrapy.Field()
    pass

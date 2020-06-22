# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EbaybestsellerItem(scrapy.Item):
    product_name_one = scrapy.Field()
    product_name_one_url = scrapy.Field()
    product_name_two = scrapy.Field()
    product_name_two_url = scrapy.Field()
    product_name_three = scrapy.Field()
    product_name_three_url = scrapy.Field()
    price = scrapy.Field() #价格
    image_url = scrapy.Field() #图片地址
    watch = scrapy.Field() #多少人看
    title = scrapy.Field()
    product = scrapy.Field() #产品名称
    product_url = scrapy.Field() # 产品url
    product_location = scrapy.Field()
    sold = scrapy.Field() #销量
    level = scrapy.Field() #等 级
    higher_ups = scrapy.Field() #上级
    end = scrapy.Field()
    product_location = scrapy.Field() #位置
    surplus = scrapy.Field() # 剩余
    scrore= scrapy.Field() #星级
    reviews =scrapy.Field() #评论数
    crawling_time = scrapy.Field()
    pass

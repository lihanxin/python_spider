# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id=scrapy.Field()
    stock_name=scrapy.Field()
    stock_code=scrapy.Field()
    stock_today_open=scrapy.Field()
    stock_yesterday_closed=scrapy.Field()
    stock_trade_num=scrapy.Field()
    stock_trade_amount=scrapy.Field()
    stock_turnover_rate=scrapy.Field()
    stock_orpm=scrapy.Field()
    stock_highest=scrapy.Field()
    stock_lowest=scrapy.Field()
    stock_traded_market_value=scrapy.Field()

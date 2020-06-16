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
    stock_limit_up=scrapy.Field()
    stock_limit_down=scrapy.Field()
    stock_turnover_rate=scrapy.Field()
    stock_amplitude=scrapy.Field()
    stock_trade_volume=scrapy.Field()
    stock_trade_amount=scrapy.Field()
    stock_in_disc=scrapy.Field()
    stock_out_disc=scrapy.Field()
    stock_appoint_than=scrapy.Field()
    stock_price_limit=scrapy.Field()
    stock_pe=scrapy.Field()
    stock_pb=scrapy.Field()
    stock_trade_market_value=scrapy.Field()
    stock_total_market_value=scrapy.Field()
    stock_highest=scrapy.Field()
    stock_lowest=scrapy.Field()


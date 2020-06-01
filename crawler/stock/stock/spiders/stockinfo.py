# -*- coding: utf-8 -*-
import scrapy
import json
import re
from stock.items import StockItem


class StockinfoSpider(scrapy.Spider):
    name = 'stockinfo'
    allowed_domains = ['gucheng.com', '10jqka.com']
    start_urls = ['https://hq.gucheng.com/gpdmylb.html']

    def parse(self, response):
        stock_list = response.xpath('//*[@id="stock_index_right"]/div[3]/section/a/@href').extract()
        stocks = []
        for stock in stock_list:
            try:
                stocks.append(re.findall(r'\d{6}', stock)[0])
            except:
                print('--出现异常--')
                continue
        stocks=[item.lower() for item in stocks]
        for stock in stocks:
            yield scrapy.Request(
                'http://qd.10jqka.com.cn/quote.php?cate=real&type=stock&callback=showStockDate&return=json&code={0}'.format(
                    stock),
                callback=self.parse_stock_detail,
                meta={'stock_code': stock},
                dont_filter=True
            )

    def parse_stock_detail(self, response):
        stock_dict = json.loads(re.findall('showStockDate[(](.*?)[)]', response.text)[0])
        stock_code = str(response.meta['stock_code'])
        item = StockItem()
        item['stock_name'] = stock_dict['info'][stock_code]['name']
        item['stock_code'] = stock_code
        item['stock_today_open'] = stock_dict['data'][stock_code]['7']
        item['stock_yesterday_closed'] = stock_dict['data'][stock_code]['6']
        item['stock_trade_num'] = stock_dict['data'][stock_code]['13']
        item['stock_trade_amount'] = stock_dict['data'][stock_code]['19']
        item['stock_turnover_rate'] = stock_dict['data'][stock_code]['1968584']
        item['stock_orpm'] = stock_dict['data'][stock_code]['526792']
        item['stock_highest'] = stock_dict['data'][stock_code]['8']
        item['stock_lowest'] = stock_dict['data'][stock_code]['9']
        item['stock_traded_market_value'] = stock_dict['data'][stock_code]['3475914']
        yield item

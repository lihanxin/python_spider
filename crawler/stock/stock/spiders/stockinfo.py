# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import StockItem



class StockinfoSpider(scrapy.Spider):
    name = 'stockinfo'
    allowed_domains = ['gucheng.com']
    start_urls = ['https://hq.gucheng.com/gpdmylb.html']

    def parse(self, response):
        stock_list = response.xpath('//*[@id="stock_index_right"]/div[3]/section/a')
        for stock in stock_list:
            stock_info=stock.xpath('./text()').extract_first()
            stock_url=stock.xpath('./@href').extract_first()
            yield scrapy.Request(
                stock_url,
                callback=self.parse_stock_detail,
                dont_filter=True,
                meta={'stock_name':stock_info.split('(')[0],'stock_code':re.findall('[(](.*?)[)]',stock_info)[0]}
            )

    def parse_stock_detail(self, response):
        item=StockItem()
        item['stock_name']=response.meta['stock_name']
        item['stock_code']=response.meta['stock_code']
        item['stock_today_open']=response.xpath("//dt[text()='今开']/following-sibling::*[1]/text()").extract_first()
        item['stock_yesterday_closed']=response.xpath("//dt[text()='昨收']/following-sibling::*[1]/text()").extract_first()
        item['stock_limit_up']=response.xpath("//dt[text()='涨停']/following-sibling::*[1]/text()").extract_first()
        item['stock_limit_down']=response.xpath("//dt[text()='跌停']/following-sibling::*[1]/text()").extract_first()
        item['stock_turnover_rate']=response.xpath("//dt[text()='换手率']/following-sibling::*[1]/text()").extract_first()
        item['stock_amplitude']=response.xpath("//dt[text()='振幅']/following-sibling::*[1]/text()").extract_first()
        item['stock_trade_volume']=response.xpath("//dt[text()='成交量']/following-sibling::*[1]/text()").extract_first()
        item['stock_trade_amount']=response.xpath("//dt[text()='成交额']/following-sibling::*[1]/text()").extract_first()
        item['stock_in_disc']=response.xpath("//dt[text()='内盘']/following-sibling::*[1]/text()").extract_first()
        item['stock_out_disc']=response.xpath("//dt[text()='外盘']/following-sibling::*[1]/text()").extract_first()
        item['stock_appoint_than']=response.xpath("//dt[text()='委比']/following-sibling::*[1]/text()").extract_first()
        item['stock_price_limit']=response.xpath("//dt[text()='涨跌幅']/following-sibling::*[1]/text()").extract_first()
        item['stock_pe']=response.xpath("//dt[text()='市盈率']/following-sibling::*[1]/text()").extract_first()
        item['stock_pb']=response.xpath("//dt[text()='市净率']/following-sibling::*[1]/text()").extract_first()
        item['stock_trade_market_value']=response.xpath("//dt[text()='流通市值']/following-sibling::*[1]/text()").extract_first()
        item['stock_total_market_value']=response.xpath("//dt[text()='总市值']/following-sibling::*[1]/text()").extract_first()
        item['stock_highest']=response.xpath("//dt[text()='最高']/following-sibling::*[1]/text()").extract_first()
        item['stock_lowest']=response.xpath("//dt[text()='最低']/following-sibling::*[1]/text()").extract_first()
        yield item

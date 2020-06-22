# -*- coding: utf-8 -*-
import scrapy
from baidu.items import BaiduItem
import re


class ZhidaoSpider(scrapy.Spider):
    name = 'zhidao'
    allowed_domains = ['baidu.com']
    start_urls = ['https://zhidao.baidu.com/question/1952019122608079068.html']

    def parse(self, response):
        li_list = response.xpath("//div[@class='related-list line']/ul/li")
        for li in li_list:
            item=BaiduItem()
            item["text"] = li.xpath("./a/span/text()").extract_first()
            item["src"] = li.xpath("./a/@href").extract_first()
            zan = li.xpath("./a/em/span/text()").extract_first()
            item["zan"]=zan if zan else 0
            yield item

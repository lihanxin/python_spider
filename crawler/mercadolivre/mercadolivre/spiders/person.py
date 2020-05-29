# -*- coding: utf-8 -*-
import scrapy


class PersonSpider(scrapy.Spider):
    name = 'person'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net/']

    def parse(self, response):
        pass

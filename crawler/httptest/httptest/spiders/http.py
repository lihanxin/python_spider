# -*- coding: utf-8 -*-
import scrapy


class HttpSpider(scrapy.Spider):
    name = 'http'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/']

    def parse(self, response):
        self.logger.debug(response.text)
        print(self.settings['LOG_LEVEL'])

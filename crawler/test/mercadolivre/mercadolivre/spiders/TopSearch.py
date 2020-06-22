# -*- coding: utf-8 -*-
import scrapy


class TopsearchSpider(scrapy.Spider):
    name = 'TopSearch'
    allowed_domains = ['mercadolivre.com']
    start_urls = ['https://lista.mercadolivre.com.br/bebes/roupas/#menu=categories']

    def parse(self, response):
        category_list=response.xpath("//div/")

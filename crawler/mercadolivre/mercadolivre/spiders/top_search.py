# -*- coding: utf-8 -*-
import scrapy
import copy
from mercadolivre.items import MercadolivreItem
import time
import json
import re
import collections


class TopSearchSpider(scrapy.Spider):
    name = 'top_search'
    allowed_domains = ['mercadolivre.com']
    # start_urls = ['https://www.mercadolivre.com.br/menu/departments']
    start_urls = ['https://www.mercadolibre.com.ar/menu/departments',
                  'https://www.mercadolivre.com.br/menu/departments',
                  'https://www.mercadolibre.cl/menu/departments',
                  'https://www.mercadolibre.com.co/menu/departments',
                  'https://www.mercadolibre.com.mx/menu/departments',
                  'https://www.mercadolibre.com.pe/menu/departments',
                  'https://www.mercadolibre.com.uy/menu/departments']

    def parse(self, response):
        # 获取所有分类json
        result = json.loads(response.body.decode())
        category_list = result["departments"]
        site_temp = re.findall("https://www.(mercadolibre|mercadolivre).com.(.*?)/menu/departments", response.url)
        site = site_temp[0][1] if len(site_temp) > 0 else \
            re.findall("https://www.mercadolibre.(.*?)/menu/departments", response.url)[0]
        search_list = []
        for categorys in category_list:
            # 一级目录名
            onecate_name = categorys["name"]
            for cates in categorys["categories"]:
                if "name" in cates:
                    # 二级目录名
                    twocate_name = cates["name"]
                    if "children_categories" in cates:
                        # 三级目录如果第一个元素没有name键，则url默认用二级目录：
                        if "name" not in cates["children_categories"][0]:
                            search_list.append(
                                {"onecate_name": onecate_name, "twocate_name": twocate_name, "threecate_name": "",
                                 "url": cates["permalink"]})
                        else:
                            for cate in cates["children_categories"]:
                                if "name" in cate:
                                    search_list.append({"onecate_name": onecate_name, "twocate_name": twocate_name,
                                                        "threecate_name": cate["name"], "url": cate["permalink"]})

        for search in search_list:
            yield scrapy.Request(
                url=search["url"],
                callback=self.parse_detail,
                meta={"item": search, "site": site},
                dont_filter=True
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        site = response.meta["site"]
        data = MercadolivreItem()
        data["site"] = site
        data["onecate_name"] = item["onecate_name"]
        data["twocate_name"] = item["twocate_name"]
        data["threecate_name"] = item["threecate_name"]
        data["url"] = item["url"]
        hot_search = response.xpath("//ul[@class='related-searches__list']/li/a/text()").extract()
        # 热搜关联词
        data["hot_search"] = [i.strip() for i in hot_search]
        yield data

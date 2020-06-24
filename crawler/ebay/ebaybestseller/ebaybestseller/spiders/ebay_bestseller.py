# -*- coding: utf-8 -*-
import scrapy
from ..items import EbaybestsellerItem
import copy


class EbayBestsellerSpider(scrapy.Spider):
    name = 'ebay_bestseller'
    allowed_domains = ['ebay.com']
    # start_urls = ['https://www.ebay.com/b/Home-Garden/11700/bn_1853126']
    start_urls = ['https://www.ebay.com/b/Electronics/bn_7000259124',
                  'https://www.ebay.com/b/Collectibles-Art/bn_7000259855',
                  'https://www.ebay.com/b/Entertainment-Memorabilia/45100/bn_1859756',
                  'https://www.ebay.com/b/Fashion/bn_7000259856',
                  'https://www.ebay.com/b/Home-Garden/11700/bn_1853126',
                  'https://www.ebay.com/b/Auto-Parts-and-Vehicles/6000/bn_1865334?v=1',
                  'https://www.ebay.com/b/Sporting-Goods/888/bn_1865031',
                  'https://www.ebay.com/b/Toys-Hobbies/220/bn_1865497',
                  'https://www.ebay.com/b/Auto-Parts-and-Vehicles/6000/bn_1865334'
                  ]

    # headers={
    #     'accept-language': 'en',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    # }
    #
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, headers=self.headers)

    def parse(self, response):
        # print(response.url)
        trs_bestsell = response.xpath('//*[@class="b-module b-list b-categorynavigations b-display--landscape"]/ul/li')
        print("长度", len(trs_bestsell))
        for i in range(0, len(trs_bestsell)):
            try:
                if i + 1 < len(trs_bestsell):
                    item = EbaybestsellerItem()
                    category_one_url = trs_bestsell[i].xpath(
                        './a/@href| ./ul/li[{}+1]/a/@href'.format(i)).extract_first() + "?LH_BIN=1&rt=nc" if \
                        trs_bestsell[i].xpath('./a/@href| ./ul/li[{}+1]/a/@href'.format(i)).extract_first() else ""
                    category_one = trs_bestsell[i].xpath(
                        './a/text()| ./ul/li[{}+1]/a/text()'.format(i)).extract_first() if trs_bestsell[i].xpath(
                        './a/@text()| ./ul/li[{}+1]/a/text()'.format(i)).extract_first() else ''
                    print(category_one_url, category_one)
                    level = "1"
                    higher_ups = response.xpath('/html/body/div[3]/div[2]/h1/span/text()').extract_first()
                    meta = copy.copy(
                        {'category_one_url': category_one_url, 'category_one': category_one, "level": level,
                         "higher_ups": higher_ups})
                    yield scrapy.Request(url=category_one_url, callback=self.parse_item, meta=meta)
                else:
                    trs_bestsel2 = response.xpath('//ul[@id="listmore_1"]/li')
                    for t in trs_bestsel2:
                        category_one_url = t.xpath('./a/@href').extract_first() + "?LH_BIN=1&rt=nc" if t.xpath(
                            './a/@href').extract_first() else ""
                        category_one = t.xpath('./a/text()').extract_first() if t.xpath(
                            './a/text()').extract_first() else ''
                        print("更多", category_one_url, category_one)
                        level = "1"
                        higher_ups = response.xpath('/html/body/div[3]/div[2]/h1/span/text()').extract_first()
                        meta = copy.copy(
                            {'category_one_url': category_one_url, 'category_one': category_one, "level": level,
                             "higher_ups": higher_ups})
                        yield scrapy.Request(url=category_one_url, callback=self.parse_item, meta=meta)

            except TypeError as e:
                print(e)
                print("==")

    def parse_item(self, response):
        level = response.meta["level"];
        higher_ups = response.meta["higher_ups"];
        category_one_url = response.meta["category_one_url"];
        category_one = response.meta["category_one"]
        trtable = response.xpath('//ul[@class="b-list__items_nofooter"]/li')
        m = 0
        for i in trtable:
            m += 1;
            watch = '';
            sold = ''
            item = EbaybestsellerItem()
            product = i.xpath('./div/div[2]/a/h3/text()').extract_first()
            product_url = i.xpath('./div/div[2]/a/@href').extract_first()
            price = i.xpath('./div/div[2]/div/div[1]//text()').extract_first()
            image_url = i.xpath('./div/div[1]/div/a/div/img/@src').extract_first()
            watch_sold = i.xpath('./div/div[2]//span[@class="NEGATIVE"]/text()').extract_first()
            watch_sold = '' if watch_sold is None else watch_sold
            if str(watch_sold) != "":
                if "追踪" in str(watch_sold):
                    watch = watch_sold
                else:
                    watch = ""
                if "已售" in str(watch_sold):
                    sold = watch_sold
                else:
                    sold = ""
            surplus = i.xpath(
                './div/div[2]//span[@class="s-item__hotness s-item__authorized-seller"]/span/text()').extract_first()
            scrore = i.xpath('./div/div[2]/div[@class="s-item__reviews"]//span/text()').extract_first()
            reviews = i.xpath(
                './div/div[2]/div[@class="s-item__reviews"]/a/span[@class="s-item__reviews-count"]//text()').extract_first()
            product_location = m
            item["product_name_one"] = category_one
            item["product_name_one_url"] = category_one_url
            item["product"] = product
            item["product_url"] = product_url
            item["price"] = price
            item["image_url"] = image_url
            item["watch"] = watch
            item["sold"] = sold
            item["surplus"] = surplus
            item["scrore"] = scrore
            item["reviews"] = reviews
            item["higher_ups"] = higher_ups
            item["product_location"] = product_location
            yield item
            # print(product_location,product,product_url,price,image_url,watch,surplus,scrore,reviews)

        two_url = response.xpath('//ol[@class="ebayui-pagination__ol"]/li[2]/a/@href').extract_first()  # 第二页
        if two_url:
            if two_url != response.url:
                meta2 = copy.copy({'category_one_url': two_url, 'category_one': category_one, "level": level,
                                   "higher_ups": higher_ups})
                try:
                    yield scrapy.Request(url=two_url, callback=self.parse_item, meta=meta2)
                except:
                    pass
                # trtable2 = response.xpath('//ul[@class="b-module b-list b-categorynavigations b-display--landscape"]/li')

    # def parse_item2(self,response):
    #     level=response.meta["level"];higher_ups=response.meta["higher_ups"];category_one_url=response.meta["category_one_url"];category_one=response.meta["category_one"]
    #     trtable = response.xpath('//ul[@class="b-list__items_nofooter"]/li')
    #     m = 0
    #     for i in trtable:
    #         m += 1;watch='';sold=''
    #         item = EbaybestsellerItem()
    #         product = i.xpath('./div/div[2]/a/h3/text()').extract_first()
    #         product_url = i.xpath('./div/div[2]/a/@href').extract_first()
    #         price = i.xpath('./div/div[2]/div/div[1]//text()').extract_first()
    #         image_url = i.xpath('./div/div[1]/div/a/div/img/@src').extract_first()
    #         watch_sold = i.xpath('./div/div[2]//span[@class="NEGATIVE"]/text()').extract_first()
    #         watch_sold ='' if watch_sold is None else watch_sold
    #         if str(watch_sold) !="":
    #             if "追踪" in str(watch_sold) :
    #                 watch=watch_sold
    #             else:
    #                 watch=""
    #             if "已售" in str(watch_sold):
    #                 sold =watch_sold
    #             else :
    #                 sold =""
    #         surplus = i.xpath('./div/div[2]//span[@class="s-item__hotness s-item__authorized-seller"]/span/text()').extract_first()
    #         scrore= i.xpath('./div/div[2]/div[@class="s-item__reviews"]//span/text()').extract_first()
    #         reviews= i.xpath('./div/div[2]/div[@class="s-item__reviews"]/a/span[@class="s-item__reviews-count"]//text()').extract_first()
    #         product_location = m
    #         item["product_name_one"] = category_one
    #         item["product_name_one_url"] = category_one_url
    #         item["product"] = product
    #         item["product_url"] = product_url
    #         item["price"] = price
    #         item["image_url"] = image_url
    #         item["watch"] = watch
    #         item["sold"] = sold
    #         item["surplus"] = surplus
    #         item["scrore"] = scrore
    #         item["reviews"] = reviews
    #         item["higher_ups"] = higher_ups
    #         item["product_location"] =product_location
    #         yield item
    #         #print(product_location,product,product_url,price,image_url,watch,surplus,scrore,reviews)
    #
    #     two_url = response.xpath('//ol[@class="ebayui-pagination__ol"]/li[2]/a/@href').extract_first() # 第二页
    #     if two_url:
    #         if two_url !=response.url:
    #             meta3 = copy.copy({'category_one_url': two_url, 'category_one': category_one, "level": level,"higher_ups": higher_ups})
    #             yield scrapy.Request(url=two_url, callback=self.parse_item, meta = meta3)
